# this are
try:
    import django.dispatch

    form_not_validated = django.dispatch.Signal()
    form_validated = django.dispatch.Signal()
    command_success = django.dispatch.Signal()
    command_error = django.dispatch.Signal()
except ImportError:
    class dummysignal:
        def send(self, *args, **kw):
            pass
    form_not_validated = form_validated = command_success = command_error = dummysignal()