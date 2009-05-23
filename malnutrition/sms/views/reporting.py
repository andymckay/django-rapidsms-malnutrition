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
        self.data.provider = provider = models.Provider.by_mobile(self.message.peer)
        lookup = {"ref_id": self.form.clean.child.data, "provider": provider}
        if "active" in [ f.name for f in models.Case._meta.fields ]:
            lookup["active"] = True
        try:
            case = models.Case.objects.get(**lookup)
        except models.Case.DoesNotExist:
            raise CommandError, self.error_not_registered()

        self.data.case = case

        # if there is more than one case entered on one day, remove the last
        try:
            last_report = case.reportmalnutrition_set.latest("entered_at")
            if (datetime.now() - last_report.entered_at).days == 0:
                # last report was today. so delete it before filing another.
                last_report.delete()
        except ObjectDoesNotExist:
            pass

        report = models.ReportMalnutrition(case=case, provider=provider, muac=self.form.clean.muac.data, 
            weight=self.form.clean.weight.data, height=self.form.clean.height.data)
        report.save()
        log(report, "report_taken")
        self.data.report = report


