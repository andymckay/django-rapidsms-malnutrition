urls
---------------------------

Malawi features a Django style URL resolver, it takes the incoming SMS as a peice of text, and then
lets the Django URL framework figure out where to send it. This has a few advantages: it's easy
to see all the messages and what they map to in one place, you turn on or off messages and you
can easily change the class that they point to.

To do this enable a URLResolver in your app eg::

    from django.core.urlresolvers import RegexURLResolver, Resolver404
    resolver = RegexURLResolver(r'', "apps.sms.sms")

In this cases apps.sms.sms contains our mapping of SMS to views. Then::

    callback, callback_args, callback_kwargs = resolver.resolve(message.text.lower())
    
Gives us our view (see http://github.com/andymckay/malawi/blob/bb133b9bb6a36e8097af2d3ca5af9e86720b1496/apps/sms/app.py)
for full code.

The SMS file looks like this::

    urlpatterns = patterns('',
        (r'^join (.*)', "apps.sms.views.joining.MalawiJoin"),
        (r'^exit (.*)', "apps.sms.views.exiting.MalawiExit"),
        ...

Exactly as you would normally expect.