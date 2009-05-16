from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

class MessageLog(models.Model):
    """ This is the raw dirt message log, useful for some things """
    mobile      = models.CharField(max_length=255, db_index=True)
    sent_by     = models.ForeignKey(User, null=True)
    text        = models.TextField(max_length=255)
    was_handled = models.BooleanField(default=False, db_index=True)
    created_at  = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ("-created_at",)
        abstract = True  

    def save(self, *args):
        if not self.id:
            self.created_at = datetime.now()
        super(MessageLog, self).save(*args)