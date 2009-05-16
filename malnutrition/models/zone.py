from django.db import models
from django.utils.translation import ugettext_lazy as _

class Zone(models.Model):
    """ A generic zone for the project """
    def __unicode__ (self): 
        return self.name
    
    class Meta:
        verbose_name_plural = "Facilities"
        abstract = True
    
    CLUSTER_ZONE = 1
    VILLAGE_ZONE = 2
    SUBVILLAGE_ZONE = 3
    ZONE_TYPES = (
        (CLUSTER_ZONE, _('Cluster')),
        (VILLAGE_ZONE, _('Village')),
        (SUBVILLAGE_ZONE, _('Sub village'))
    )
    
    number = models.PositiveIntegerField(unique=True,db_index=True)
    name = models.CharField(max_length=255)
    head = models.ForeignKey("self", null=True,blank=True)
    category = models.IntegerField(choices=ZONE_TYPES, default=VILLAGE_ZONE)
    lon = models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
