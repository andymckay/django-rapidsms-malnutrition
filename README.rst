This is a series of re-usable modules for the Kenyan and Malawi Malnutrition projects.

forms
---------------------

Contains a simple SMS form handler. Based on Django's forms, but doesn't have the same API, it specifies how the form will
look, then takes the text and validates the input. The format is similar to Django forms::

    class ReportForm(Form):
        sick = BooleanField()
        id = StringField(required=True, valid="(\d+)")
        
This means we expect a y or n followed by a number.

To process it pass in data eg::

    rf = ReportForm("y 19122008")

Was it valid?::

    rf.is_valid()
    
If not, there's a list of errors in the .errors attribute::

    rf.errors

You can also find the error on the field::

    rf.sick.error
    
And finally the parsed (eg: dates into datetime fields) value is there in data::

    rf.sick.data
    
You can make fields required, by passing through required=True in the Field construction.

models
---------------------

Models are some standard models, we've been reusing. These aren't included in your project, you have
to include them, however that is pretty easy since they are all abstract. For example::

    from malnutrition.models import case
    
    class Case(case.Case):
        pass
        
A few notes on this:

- Since the models are related to each other, you will likely get errors unless you pull all of them in and name them: Case, Provider, Facility, Zone

- Report requires patient and provider

- Log is standalone and requires nothing

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