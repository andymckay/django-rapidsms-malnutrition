from django.utils.translation import ugettext_lazy as _
from malnutrition.sms.resolve import models
from datetime import datetime

messages = {
    "provider_registered": _("Provider registered, waiting confirmation"),
    "patient_created": _("Patient created"),
    "muac_taken": _("MUAC taken for the patient"),
    "mrdt_taken": _("MRDT taken for the patient"),
    "diagnosis_taken": _("Diagnosis taken for the patient"), 
    "report_taken": _("Report taken for the patient"),     
    "user_logged_in": _("User logged into the user interface"),
    "confirmed_join": _("Provider confirmed"),
    "case_cancelled_death": _("Case was cancelled by the provider due to death"),
    "case_cancelled_dropout": _("Case was cancelled by the provider due to dropout"),
    "case_cancelled_death_malnutrition": _("Case was cancelled by the provider due to death related to malnutrition"),
    "case_cancelled": _("Case was cancelled by the provider"),
    "case_cancelled_mistake": _("Case was cancelled by the provider due to mistake"),
    "note_added": _("Note added to the case by the provider"),
    "report_cancelled": _("Report cancelled")
}

def log(source, message):
    if not messages.has_key(message):
        raise ValueError, "No message: %s exists, please add to logs.py"
    try:
        ev = models.EventLog()
    except AttributeError:
        return
    ev.content_object = source
    ev.message = message
    ev.created_at = datetime.now()
    ev.save()