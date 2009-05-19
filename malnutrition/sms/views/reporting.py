from django.db.models import ObjectDoesNotExist

from malnutrition.forms import Form
from malnutrition.forms import BooleanField, DateField, StringField, GenderField, FloatField

from malnutrition.sms.resolve import models
from malnutrition.sms.command import Command, CommandError, authenticated, _

from datetime import datetime

class NewForm(Form):
    child = StringField(valid="(\d+)")
    gmc = StringField(valid="(\d+)")
    sex = GenderField()
    dob = DateField(format="%m/%d/%Y")
    contact = StringField(valid="(\d+)", required=False)

class New(Command):
    @authenticated
    def post_init(self):
        self.form = ReportForm
    
    def error_already_exists(self):
        return "That child already exists."
    
    def success(self):
        info = self.data.case.get_dictionary()
        info.update(self.data.provider.clinic.get_dictionary())
        return "Thank you for registering child #%(ref_id)s in %(name)s GMC,"\
            " %(gender_long)s, age %(raw_months)s months, born %(dob)s,"\
            " contact# %(mobile)s. If there is a mistake, please cancel"\
            " this registration and try again." % info

    def process(self):
        self.data.provider = provider = models.Provider.by_mobile(self.message.peer)
        try:
            models.Case.objects.get(ref_id=self.form.clean.child.data, provider=provider)
            raise CommandError, self.error_already_exists()
        except models.Case.DoesNotExist:
            case = models.Case(
                ref_id=self.form.clean.child.data,
                provider=provider,
                mobile=self.form.clean.contact.data,
                gender=self.form.clean.sex.data,
                dob=self.form.clean.dob.data
            )
            case.save()
            self.data.case = case


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
        return _("That child is not registered.")

    def success(self):
        pass
        
    def process(self):
        self.data.provider = provider = models.Provider.by_mobile(self.message.peer)
                
        try:
            case = models.Case.objects.get(ref_id=self.form.clean.child.data, provider=provider)
        except models.Case.DoesNotExist:
            raise CommandError, self.error_not_registered()

        self.data.case = case

        # if there is more than one case entered on one day, remove the last
        try:
            last_report = models.ReportMalnutrition.objects.latest("entered_at")
            if (datetime.now() - last_report.entered_at).days == 0:
                # last report was today. so delete it before filing another.
                last_report.delete()
        except ObjectDoesNotExist:
            pass

        report = models.ReportMalnutrition(case=case, provider=provider, muac=self.form.clean.muac.data, 
            weight=self.form.clean.weight.data, height=self.form.clean.height.data)
        report.save()

        self.data.report = report


