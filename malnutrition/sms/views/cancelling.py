from malnutrition.forms import Form
from malnutrition.forms import StringField
from malnutrition.sms.resolve import models

from malnutrition.utils.log import log
from malnutrition.sms.command import authenticated, CommandError, Command, FormFailed

from django.db.models import ObjectDoesNotExist

class CancelForm(Form):
    child = StringField(valid="(\d+)")

class Cancel(Command):
    @authenticated
    def post_init(self):
        self.form = CancelForm
    
    def error_not_exists(self):
        return "Cannot find a child to cancel"
    
    def success(self):
        info = self.data.case.get_dictionary()
        return "Last report for %(ref_id)s cancelled" % info
    
    def error_no_report(self, ref_id):
        return "No report for %s to cancel" % ref_id
    
    def process(self):
        # to do, refactor this out
        self.data.provider = provider = models.Provider.by_mobile(self.message.peer)
        lookup = {"ref_id": self.form.clean.child.data, "provider": provider}
        if "active" in [ f.name for f in models.Case._meta.fields ]:
            lookup["active"] = True
            
        try:
            case = models.Case.objects.get(**lookup)
        except models.Case.DoesNotExist:
            raise CommandError, self.error_not_exists()
        
        try:
            report = case.reportmalnutrition_set.latest()
            report.delete()
        except ObjectDoesNotExist:
            raise CommandError, self.error_no_report(case.ref_id)
            
        log(case, "report_cancelled")
        self.data.case = case