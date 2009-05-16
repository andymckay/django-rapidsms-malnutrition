from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

def as_html(request, template, context):
    """ A useful wrapper, because writing render_to_response gets boring quickly """
    rcontext = RequestContext(request)
    return render_to_response(template, context, context_instance=rcontext)
    
def login_required(fn):
    """ Front end is limited to staff only """
    def new(*args, **kw):
        request = args[0]
        if request.user.is_authenticated:
            if request.user.is_staff and request.user.is_active:
                return fn(*args, **kw)
        
        return HttpResponseRedirect("/accounts/login/")
    return new
