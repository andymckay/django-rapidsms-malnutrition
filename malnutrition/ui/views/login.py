from django.http import HttpResponseRedirect
from django.contrib import auth

from malnutrition.ui.forms.login import LoginForm
from shortcuts import as_html, login_required

from django.utils.translation import ugettext_lazy as _

messages = {
    "login_failed": _("Username or password did not match"),
    "logged_out": _("You have been logged out"),
}

def login(request):
    context = {}
    context["msg"] = messages.get(request.GET.get("msg", None))
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not request.user.is_authenticated():
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
        form = LoginForm()
        
    context["form"] = form
    return as_html(request, "login.html", context)

    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/?msg=logged_out")
