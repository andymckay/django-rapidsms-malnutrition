# this are
import django.dispatch

form_not_validated = django.dispatch.Signal()
form_validated = django.dispatch.Signal()
command_success = django.dispatch.Signal()
command_error = django.dispatch.Signal()