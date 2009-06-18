views
------------------------------------

So your have a URL pointing to view, how do you avoid having each view be a bit of python code its hard to 
alter for different projects? Try using the Command class in malnutrition.sms.

After doing a few of these it became clear there is a workflow. And that goes something like this:

1. get the SMS and text and try and validate it. If it's wrong send back an error to the sender.

2. process the data

3. if processing the data caused a problem, send back a message to the sender

4. if processing the data worked, complete it

So how can we abstract this a little more? Use the Command class to inherit your views from. The command class is created
with a message passed in from the SMS message (see urls.rst). It then calls the following:

- post_init: in this method you usually assign a Form (thats a Form as defined in forms.rst). You could pass this through in urls.py if you wanted. If there's something else like security or any other sort of init here, this is your chance. 

- not_valid: the form is validated and if it fails the form will be sent to this method. If it validated correctly this step is not called.

- pre_process, process and post_process: each of these is called in order. The form is in self.form and you can do as you see fit in each of these methods. 

- success: if its all gone well, this method will be called and the result sent back to the user.

The url mapping job will usually pass these errors back to the user. I tried to keep the Command parser free of that (see urls.rst).

See example.py in malnutrition.sms example::

    class NumberForm(Form):
        first = FloatField()
        second = FloatField()

    class Divide(Command):
        def post_init(self):
            self.form = NumberForm

        def success(self):
            return self.form.clean.first.data/self.form.clean.second.data
    
        def process(self):
            pass
    
        def pre_process(self):
            if not int(self.form.clean.second.data):
                raise CommandError("Cannot divide by zero")
    
Here we have method called divide, that takes two numbers and divides one by the other. As a pre_process I check that the second number 
is not zero. And that's about it. In your site, you'd probably want something a bit more complicated in the process. Now supposing you 
get asked for a different error message or a different form? Sub class the above and link it up in your SMS urls. Here's an example of 
a silly form that swaps the numbers around and returns a different error::

    class SillyNumberForm(Form):
        second = FloatField()
        first = FloatField()
    
    class SillyDivide(Divide):
        def post_init(self):
            self.form = SillyNumberForm
        
        def not_valid(self, form):
            return "You sir, are a muppet."

The meat of the method, pre_process, success and process are untouched.

You can see this in action in Malawi.

