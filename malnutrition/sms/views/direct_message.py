from django.db.models import ObjectDoesNotExist

from malnutrition.forms import Form
from malnutrition.forms import BooleanField, StringField, FloatField

from malnutrition.sms.resolve import models
from malnutrition.sms.command import Command, CommandError, authenticated, _

from datetime import datetime
from malnutrition.utils.log import log

class ReportForm(Form):
    child = StringField(valid="(\d+)")
    weight = FloatField()
    height = FloatField()
    muac = FloatField()
    oedema = BooleanField()
    diarrhea = BooleanField()

class Report(Command):
    @authenticated
    def post_init(self):
        self.form = ReportForm

    def error_not_registered(self):
        return "That child is not registered."

    def success(self):
        pass
        
    def process(self):
        try:
            if re.match(r'^\d+$', target):
                provider = Provider.objects.get(id=target)
                user = provider.user
            else:
                user = User.objects.get(username__iexact=target)
        except models.ObjectDoesNotExist:
            # FIXME: try looking up a group
            self.respond_not_registered(message, target)
        try:
            mobile = user.provider.mobile
        except:
            self.respond_not_registered(message, target)
        sender = message.sender.username
        return message.forward(mobile, "@%s> %s" % (sender, text))