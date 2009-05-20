from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

class Facility(models.Model):
    """ A generic model for a facility """
    class Meta:
        abstract = True
        verbose_name_plural = "Facilities"
        
    def __unicode__ (self): 
        return self.name

    CLINIC_ROLE  = 1
    DISTRIB_ROLE = 2
    ROLE_CHOICES = (
        (CLINIC_ROLE,  _('Clinic')),
        (DISTRIB_ROLE, _('Distribution Point')),
    )

    name        = models.CharField(max_length=255)
    role        = models.IntegerField(choices=ROLE_CHOICES, default=CLINIC_ROLE)
    zone        = models.ForeignKey("Zone", db_index=True)
    codename    = models.CharField(max_length=255,unique=True,db_index=True)
    lon         = models.FloatField(null=True,blank=True)
    lat         = models.FloatField(null=True,blank=True)
    
    def get_dictionary(self):
        dct = {
            "name": self.name, 
            "codename": self.codename
        }
        data = model_to_dict(self)
        data.update(dct)
        return data