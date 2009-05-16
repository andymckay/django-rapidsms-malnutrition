from django.http import HttpResponseRedirect
from django.contrib import auth

from rapidsms_baseui.forms.login import LoginForm
from shortcuts import as_html, login_required

from django.utils.translation import ugettext_lazy as _

messages = {
    "login_failed": _("Username or password did not match"),
    "logged_out": _("You have been logged out"),
}

def login(request):
    context = {}
    if request.GET.has_key("msg"):
        msg = messages.get(request.GET["msg"], "")
        if msg:
            context["msg"] = msg
    
    if request.method == "POST" and not request.user.is_authenticated():
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data["username"], 
                password=form.cleaned_data["password"])
            if user:
                if user.is_active and user.is_staff:
                    auth.login(request, user)
                    return HttpResponseRedirect("/")
            return HttpResponseRedirect("/accounts/login/?msg=login_failed")
    else:
        form = LoginForm(request.POST)
    context["form"] = form
    return as_html(request, "login.html", context)

    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/?msg=logged_out")
