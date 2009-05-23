from malnutrition.forms import Form
from malnutrition.forms import StringField
from malnutrition.sms.resolve import models
from malnutrition.sms.command import Command, CommandError
from malnutrition.utils.log import log

class JoinForm(Form):
    facility = StringField(valid="(\d+)")
    last = StringField(valid="(.+)")
    first = StringField(valid="(.+)")
    username = StringField(valid="(.+)", required=False)

class Join(Command):
    def post_init(self):
        if self.form is None:
            self.form = JoinForm
        self.data.username = None
    
    def success(self):
        info = self.data.provider.get_dictionary()
        info.update(self.data.facility.get_dictionary())
        return "%(mobile)s registered to @%(username)s (%(user_last_name)s, %(user_first_name)s) at %(clinic)s." % info
    
    def error_facility_exists(self):
        return "The facility given does not exist."
    
    def error_in_use(self, in_use, facility):
        # so it's in use, don't save anything
        info = in_use.get_dictionary()
        info.update(facility.get_dictionary())
        info["username"] = self.data.username
        return "Phone %(mobile)s is already registered to %(user_last_name)s, %(user_first_name)s. Reply with 'CONFIRM %(username)s'." % info
    
    def error_username_used(self):
        return "Username %s is already in user. Reply with: JOIN <last> <first> <username>" % self.data.username
    
    def process(self):
        try:
            facility = models.Facility.objects.get(codename=self.form.clean.facility.data)
        except models.Facility.DoesNotExist:
            raise CommandError, self.error_facility_exists()
        
        # by default if we haven't got a username mangled already, then make one automatically
        if not self.data.username:
            tmp = self.data.username = (self.form.clean.first.data[0] + self.form.clean.last.data).lower()
            # if we are going to calculate usernames, we need to prevent clashes
            for x in range(1, 100):
                try:
                    models.User.objects.get(username=tmp)
                    tmp = "%s-%03d" % (self.data.username, x)
                except models.User.DoesNotExist:
                    break
                
            self.data.username = tmp
        
        # if we have got a username, double check it's ok
        if models.User.objects.filter(username__iexact=self.data.username).count():
            raise CommandError, self.error_username_used()
        
        mobile = self.message.peer
        in_use = models.Provider.by_mobile(mobile)
        
        user = models.User(username=self.data.username, first_name=self.form.clean.first.data.title(), last_name=self.form.clean.last.data.title())
        user.save()
        
        # ok its not in use, save it all and respond
        provider = models.Provider(mobile=mobile, user=user, clinic=facility, active=not bool(in_use))
        provider.save()
        
        log(provider, "provider_registered")
        if not in_use:
            # all goood!
            self.data.provider = provider
            self.data.facility = facility
            return True
        else:
            # send them back a confirm message
            raise CommandError, self.error_in_use(in_use, facility)