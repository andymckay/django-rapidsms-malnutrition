models
---------------------

Models are some standard models, we've been reusing. These aren't included in your project, you have
to include them, however that is pretty easy since they are all abstract. For example::

    from malnutrition.models import case
    
    class Case(case.Case):
        class Meta:
            app_label = "yoursmsapp"
        
A few notes on this:

- Since the models are related to each other, you will likely get errors unless you pull all of them in and name them: Case, Provider, Facility, Zone

- Report requires patient and provider

- Log is standalone and requires nothing

See: http://github.com/andymckay/malawi/blob/bb133b9bb6a36e8097af2d3ca5af9e86720b1496/apps/sms/models/base.py
