from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

from datetime import datetime
from malnutrition import utils

class Case(models.Model):
    GENDER_CHOICES = (
        ('M', _('Male')), 
        ('F', _('Female')), 
    )

    ref_id      = models.IntegerField(_('Case ID #'), null=True, db_index=True)
    first_name  = models.CharField(max_length=255, db_index=True)
    last_name   = models.CharField(max_length=255, db_index=True)
    gender      = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob         = models.DateField(_('Date of Birth'))
    guardian    = models.CharField(max_length=255, null=True, blank=True)
    mobile      = models.CharField(max_length=16, null=True, blank=True)
    provider    = models.ForeignKey("Provider", db_index=True)
    zone        = models.ForeignKey("Zone", null=True, db_index=True)
    village     = models.CharField(max_length=255, null=True, blank=True)
    district    = models.CharField(max_length=255, null=True, blank=True)
    created_at  = models.DateTimeField()
    updated_at  = models.DateTimeField()

    def __unicode__ (self):
        return "#%d" % self.ref_id

    def _luhn(self, x):
        parity = True
        sum = 0
        for c in reversed(str(x)):
            n = int(c)
            if parity:
                n *= 2
                if n > 9: n -= 9
            sum += n
        return x * 10 + 10 - sum % 10

    def save(self, *args):
        if not self.id:
            self.created_at = self.updated_at = datetime.now()
        else:
            self.updated_at = datetime.now()
        super(Case, self).save(*args)
        if not self.ref_id:
            self.ref_id = self._luhn(self.id)
            super(Case, self).save(*args)

    def get_dictionary(self):
        """ Return the data as a generic dictionary with some useful convenience methods done """
        dct = {
            'ref_id': self.ref_id,
            'last_name': self.last_name.upper(),
            'first_name': self.first_name,
            'first_name_short': self.first_name.upper()[0],
            'gender': self.gender.upper()[0],
            'months': self.age(),
            'guardian': self.guardian,
            'village': self.village,
        }
        data = model_to_dict(self)
        data.update(dct)
        return data
    
    def years_months(self):
        return utils.years_months(self.dob)

    def age(self):
        years, months = self.years_months()
        if years >= 3:
            return str(years)
        else:
            return "%sm" % months

    class Meta:
        abstract = True
