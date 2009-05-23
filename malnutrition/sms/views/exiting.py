from malnutrition.forms import Form
from malnutrition.forms import StringField
from malnutrition.sms.resolve import models

from malnutrition.utils.log import log
from malnutrition.sms.command import authenticated, CommandError, Command, FormFailed

class ExitForm(Form):
    child = StringField(valid="(\d+)")
    gmc = StringField(valid="(\d+)")
    reason = StringField(valid="(\w+)")
class Exit(Command):
    @authenticated
    def post_init(self):
        self.form = ExitForm
    
    def error_not_exists(self):
        return "Cannot find a child to cancel"
    
    def success(self):
        info = self.data.case.get_dictionary()
        info.update(self.data.case.provider.clinic.get_dictionary())
        return "Case %(ref_id)s cancelled for %(codename)s" % info
    
    def pre_process(self):
        if not self.form.clean.reason.data or self.form.clean.reason.data.lower() not in ["d", "dm", "do", "m"]:
            raise FormFailed("No reason given must be one of: D (death), DM (death malnutrition), DO (dropout), M (mistake).")
    
    def process(self):
        self.data.provider = provider = models.Provider.by_mobile(self.message.peer)
        lookup = {"ref_id": self.form.clean.child.data, "provider": provider}
        if "active" in [ f.name for f in models.Case._meta.fields ]:
            lookup["active"] = True
        try:
            case = models.Case.objects.get(**lookup)
        except models.Case.DoesNotExist:
            raise CommandError, self.error_not_exists()
        
        case.active = False
        case.save()
    
        reason = self.form.clean.reason.data.lower()
        if reason == "d":
            log(case, "case_cancelled_death")
            self.data.reason = "death"
        elif reason == "dm":
            log(case, "case_cancelled_death_malnutrition")
            self.data.reason = "death of causes related to malnutrition"
        elif reason == "do":
            log(case, "dropout")
            self.data.reason = "dropout of program"
        elif reason == "m":
            log(case, "case_cancelled_mistake")
            self.data.reason = "mistake"
            
        self.data.case = case