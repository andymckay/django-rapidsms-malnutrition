from django.db import models
from django.contrib.auth.models import User

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
