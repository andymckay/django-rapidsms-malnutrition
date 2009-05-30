from urllib import quote, urlopen

from django.contrib.auth.models import Group
from django.db.models import ObjectDoesNotExist

from malnutrition.sms.resolve import models
# # This sends out a direct message to some users or groups

def message_users(mobile, message=None, groups=None, users=None, domain="localhost", port="8080"):
    # problems that might still exist here
    # timeouts in the browser because we have to post all the messages
    # timeouts in the url request filtering up to the above
    recipients = []
    # get all the user
    provider_objects = [ models.Provider.objects.get(id=user) for user in users ]
    for provider in provider_objects:
        try:
            if provider not in recipients:
                recipients.append(provider)
        except models.ObjectDoesNotExist:
            pass
     # get all the users for the groups
    if groups:
        group_objects = [ Group.objects.get(id=group) for group in groups ]
        for group in group_objects:
            for user in group.user_set.all():
                try:
                    if user.provider not in recipients:
                        recipients.append(user.provider)
                except ObjectDoesNotExist:
                    pass
    
    passed = []
    failed = []
    for recipient in recipients:
        msg = quote("@%s %s" % (recipient.id, message))
        cmd = "http://%s:%s/spomc/%s/%s" % (domain, port, mobile, msg)
        try:
            print cmd
            urlopen(cmd).read()
            passed.append(recipient)
        except IOError:
            # if the mobile number is badly formed and the number regex fails
            # this is the error that is raised
            failed.append(recipient)
    
    results_text = ""
    if not passed and not failed:
        results_text = "No recipients were sent that message."
    elif not failed and passed:
        results_text = "The message was sent to %s recipients" % (len(passed))
    elif failed and passed:
        results_text = "The message was sent to %s recipients, but failed for the following: %s" % (len(passed), ", ".join([ str(f) for f in failed]))
    elif not passed and failed:
        results_text = "No-one was sent that message. Failed for the following: %s" % ", ".join([ str(f) for f in failed])
    return results_text