from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

from datetime import datetime

from malnutrition.utils.parse import stunting, weight_for_height
 
DEBUG = True

class Report(models.Model):
    class Meta:
        abstract = True
    
    case = models.ForeignKey("Case", db_index=True) 
    # this is essentially the reporter
    provider = models.ForeignKey("Provider", db_index=True)
    entered_at = models.DateTimeField(db_index=True)

    def save(self, *args):
        if not self.id:
            self.entered_at = datetime.now()
            
        super(Report, self).save(*args)
    
    def __unicode__ (self):
        return "#%d" % self.id
    
    def get_alert_recipients(self):
        """ Figuring out the appropriate recipients for this report, its still up to the view
        to determine a) if this should be sent and then c) how to send it... this does the missing
        bit, part b) who it should be sent to my looking up the following clinics etc """
        # this is the reporter, the provider or the CHW depending what you call it
        provider = self.provider
        facility = provider.clinic
        assert facility, "This provider does not have a clinic."

        recipients = []

        # find all the people assigned to alerts from this facility
        for user in facility.following_clinics.all():
            # only send if they want
            if user.alerts:
                if user not in recipients:
                    recipients.append(user)

        # find all the users monitoring this user
        for user in provider.following_users.all():
            if user.alerts:
                if user not in recipients:
                    recipients.append(user)

        return recipients

    def get_dictionary(self):
        return model_to_dict(self)

class Observation(models.Model):
    uid = models.CharField(max_length=15)
    name = models.CharField(max_length=255)
    letter = models.CharField(max_length=2, unique=True)

    class Meta:
        ordering = ("name",)
        abstract = True

    def get_dictionary(self):
        return model_to_dict(self)

    def __unicode__(self):
        return self.name
                
class ReportMalnutrition(Report):
    MODERATE_STATUS = 1
    SEVERE_STATUS = 2
    SEVERE_COMP_STATUS = 3
    HEALTHY_STATUS = 4
    STATUS_CHOICES = (
        (MODERATE_STATUS, _('MAM')),
        (SEVERE_STATUS, _('SAM')),
        (SEVERE_COMP_STATUS, _('SAM+')),
        (HEALTHY_STATUS, _("Healthy")),
    )
    
    muac = models.IntegerField(_("MUAC (mm)"), null=True, blank=True)
    height = models.FloatField(_("Height (cm)"), null=True, blank=True)
    weight = models.FloatField(_("Weight (kg)"), null=True, blank=True)
    stunted = models.BooleanField()
    weight_for_height = models.CharField(max_length="10")
    observed = models.ManyToManyField("Observation")
    status = models.IntegerField(choices=STATUS_CHOICES, db_index=True, blank=True, null=True)
    
    class Meta:
        get_latest_by = 'entered_at'
        ordering = ("-entered_at",)
        abstract = True

    def get_dictionary(self):
        dct = model_to_dict(self)
        dct.update({
            'muac': "%d mm" % self.muac,
            'height': "%s cm" % self.height,
            'weight': "%s kg" % self.weight,
            'stunted': self.stunted,
            'weight_for_height': self.weight_for_height,
            'observed': ", ".join([k.name for k in self.observed.all()]),
            'diagnosis': self.get_status_display(),
        })
        return dct
    
    def save(self, *args):
        # add in stunting and weight for height
        if not self.id:
            # stunting
            if self.height:
                number = stunting(self.case.dob, self.case.gender)
                if number:
                    self.stunted = float(number) < float(self.height)

            # weight for height            
            if self.height and self.weight:
                res = weight_for_height(self.height, self.weight)
                if res:
                    self.weight_for_height = res
                    if res in ["75%-70%", ]:
                        if self.status not in [self.SEVERE_STATUS, self.SEVERE_COMP_STATUS]:
                            if DEBUG: print "weight for height causing moderate status"
                            self.status = self.MODERATE_STATUS
                    if res in ["60%-", "70%-60%", ]:
                         if self.status not in [self.SEVERE_COMP_STATUS,]:
                             if DEBUG: print "weight for height causing severe status"
                             self.status = self.SEVERE_STATUS
            
            if self.muac < 125:
                if self.status not in [self.SEVERE_STATUS, self.SEVERE_COMP_STATUS]:
                    if DEBUG: print "muac causing moderate status"
                    self.status = self.MODERATE_STATUS
                    
            if self.muac < 110:
                if self.status not in [self.SEVERE_COMP_STATUS]:
                    if DEBUG: print "muac causing severe status"
                    self.status = self.SEVERE_STATUS
        
        super(ReportMalnutrition, self).save(*args)