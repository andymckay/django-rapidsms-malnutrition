forms
---------------------

This is something I added to malnutrition for Malawi. Essentially there was a requirement for Malawi to have slightly
different syntax on the sms message. A form is an easy way to do things like change the order of the fields, without
having to update the method.

Further since the first job of almost every sms message is essentially "validate the message is well formed", you often end 
up with a lot of this kind of code at the top of each method.

Based on Django's forms, but doesn't have the same API, it specifies how the form will
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

    rf.clean.sick.error
    
And finally the parsed (eg: dates into datetime fields) value is there in data::

    rf.clean.sick.data
    
You can make fields required, by passing through required=True in the Field construction. But you can't have anything optional after being required (that just gets confusing).