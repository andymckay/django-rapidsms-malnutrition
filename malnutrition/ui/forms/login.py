from django import forms
from django.utils.translation import ugettext_lazy as _
from base import BaseForm

class LoginForm(BaseForm):
    username = forms.CharField(
        label = _("Username"),
        required = True
    )
    
    password = forms.CharField(
        label = _("Password"),
        required = True,
        widget = forms.PasswordInput()
    )
