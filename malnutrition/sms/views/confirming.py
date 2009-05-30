from malnutrition.forms import Form
from malnutrition.forms import StringField
from malnutrition.sms.resolve import models
from malnutrition.sms.command import Command, CommandError
from django.contrib.auth.models import User
from malnutrition.utils.log import log

class ConfirmForm(Form):
    username = StringField(valid="(.+)", required=True)

class Confirm(Command):
    def post_init(self):
        self.form = ConfirmForm
    
    def success(self):
        info = self.data.provider.get_dictionary()
        info.update(self.data.facility.get_dictionary())
        return "%(mobile)s registered to @%(username)s (%(user_last_name)s, %(user_first_name)s) at %(clinic)s." % info
    
    def error_facility_exists(self):
        return "The facility given does not exist."
    
    def error_not_registered(self):
        return "That username does not exist."
    
    def process(self):
        username = self.form.clean.username.data
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise CommandError, self.error_not_registered()
            self.respond_not_registered(username)
        
        # deactivate all the old ones and activate the new ones
        for provider in models.Provider.objects.filter(mobile=self.message.peer):
            if provider.user.id == user.id:
                provider.active = True
                self.data.provider = provider
                self.data.facility = self.data.provider.clinic
                provider.save()
        
        if not self.data.provider:
            raise HandlerError, "Something went wrong with that confirmation: %s" % self.text
        
        # check the above works before disabling a bunch of people
        for provider in models.Provider.objects.filter(mobile=self.message.peer):
            if provider.user.id != user.id:
                provider.active = False
            provider.save()
            log(provider, "confirmed_join")
