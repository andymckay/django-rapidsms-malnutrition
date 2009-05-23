from malnutrition.forms import Form
from malnutrition.forms import DateField, StringField, GenderField

from malnutrition.sms.resolve import models
from malnutrition.sms.command import Command, CommandError, authenticated

class NewForm(Form):
    child = StringField(valid="(\d+)")
    gmc = StringField(valid="(\d+)")
    sex = GenderField()
    dob = DateField(format="%m/%d/%Y")
    contact = StringField(valid="(\d+)", required=False)

class New(Command):
    @authenticated
    def post_init(self):
        self.form = NewForm
    
    def error_already_exists(self):
        return "That child already exists."
    
    def success(self):
        info = self.data.case.get_dictionary()
        info.update(self.data.provider.clinic.get_dictionary())
        return "Thank you for registering child #%(ref_id)s in %(name)s GMC,"\
            " %(gender_long)s, age %(raw_months)s months, born %(dob)s,"\
            " contact# %(mobile)s. If there is a mistake, please use EXIT to cancel"\
            " this registration and try again." % info

    def process(self):
        self.data.provider = provider = models.Provider.by_mobile(self.message.peer)
        lookup = {"ref_id": self.form.clean.child.data, "provider": provider}
        if "active" in [ f.name for f in models.Case._meta.fields ]:
            lookup["active"] = True
        try:
            models.Case.objects.get(**lookup)
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