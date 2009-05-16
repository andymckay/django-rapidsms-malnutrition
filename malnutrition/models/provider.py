from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

import md5

class Provider(models.Model):
    def __unicode__ (self): 
        return self.mobile
    
    class Meta:
        abstract = True
    
    CHW_ROLE    = 1
    NURSE_ROLE  = 2
    DOCTOR_ROLE = 3
    SENIOR_CHW_ROLE = 4
    CLINICAL_OFFICER_ROLE = 5
    NUTRITIONIST_ROLE = 6
    HEALTH_FAC_ROLE = 7
    HEALTH_COR_ROLE = 8
    
    ROLE_CHOICES = (
        (CHW_ROLE,    _('CHW')),
        (NURSE_ROLE,  _('Nurse')),
        (DOCTOR_ROLE, _('Doctor')),
        (SENIOR_CHW_ROLE, _("Senior CHW")),
        (CLINICAL_OFFICER_ROLE, _("Clinical Officer")),
        (NUTRITIONIST_ROLE, _("Nutritionist")),
        (HEALTH_FAC_ROLE, _("Health Facilitator")),
        (HEALTH_COR_ROLE, _("Health Co-ordinator")),        
    )
    
    user    = models.OneToOneField(User)
    mobile  = models.CharField(max_length=16, null=True, db_index=True)
    role    = models.IntegerField(choices=ROLE_CHOICES, default=CHW_ROLE)
    active  = models.BooleanField(default=True)
    alerts  = models.BooleanField(default=False, db_index=True)
    clinic  = models.ForeignKey("Facility", null=True, db_index=True)
    manager = models.ForeignKey("Provider", blank=True, null=True)
    
    # i have a feeling that these may be unique to Kenya and should be overridden in
    # the Kenya MCTC project, but I'm not sure at this point
    following_users = models.ManyToManyField("Provider", related_name="following_users", blank=True, null=True)
    following_clinics = models.ManyToManyField("Facility", related_name="following_clinics", blank=True, null=True)

    def get_name_display(self):
        """ Work through some logic to figure out a nice name to show in areas """
        if self.user.first_name or self.user.last_name:
            return "%s %s" % (self.user.first_name, self.user.last_name)
        if self.mobile:
            return str(self.mobile)
        else:
            return str(self.id)

    def get_dictionary(self):
        """ Return the data as a generic dictionary with some useful convenience methods done """
        return {
                "user_first_name": self.user.first_name,
                "user_last_name": self.user.last_name.upper(),
                "id": self.id,
                "mobile": self.mobile,
                "provider_mobile": self.mobile,
                "provider_user": self.user,
                "provider_name": self.user.first_name[0] + ' ' + self.user.last_name.upper(),
                "provider_name_inverted": self.user.last_name + ' ' + self.user.first_name,
                "clinic": self.clinic.name,
                "username": self.user.username
            }

    @classmethod
    def by_mobile (cls, mobile):
        try:
            return cls.objects.get(mobile=mobile, active=True)
        except models.ObjectDoesNotExist:
            return None