ui
------------------------

A base reusable user interface allows you to start with a base login, logout and search etc without having to specify this in the project.

For example:: 

    # add in rapidsms_baseui
    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.append('malnutrition.ui')
    
Add in the URLs to your urls.py::

    urlpatterns = patterns('',
        (r'^', include('malnutrition.ui.urls')),
    )

And that should be it.

To install custom apps, you will have to use a custom manage.py to avoid the settings lockdown in a standard RapidSMS site. eg:

http://github.com/andymckay/malawi/blob/bb133b9bb6a36e8097af2d3ca5af9e86720b1496/manage.py