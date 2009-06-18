from malnutrition.sms.signals import form_not_validated, form_validated, command_success, command_error
        
class CommandError(Exception):
    pass

class HandlerFailed(Exception):
    pass
    
class FormFailed(Exception):
    pass
    
def _(txt): return txt

class Data: pass

def authenticated(func):
    def wrapper(self, *args, **kw):
        if self.message.sender:
            return func(self, *args, **kw)
        else:
            raise CommandError(self.not_allowed())
            
    return wrapper
    
class Command:
    """ After doing a few of these, there's a clear process to a command
        - get the form, validate it, message if that's wrong
        - process the data
        - if there's a problem tell the user 
        - if it works do that
        This can be abstract
    """
    def __init__(self, message, *args, **kw):
        self.form = kw.get("form", None)
        self.text = args[0]
        self.message = message
        # this is just a general namespace you can stuff things into in
        # process to allow other methods to pull the informationno  
        self.data = Data()
        
        self.can_process = True
        try:
            self.post_init()
        except CommandError, e:
            self.can_process = False
            raise HandlerFailed(e)
    
    def not_allowed(self):
        return "%s is not a registered number." % self.message.peer
    
    def post_init(self):
        pass
        
    def not_valid(self, form):
        return "There was an error processing that: %s" % ". ".join(form.errors)
        
    def success(self):
        raise NotImplementedError
        
    def error(self):
        pass

    def process(self):
        raise NotImplementedError
        
    def pre_process(self):
        pass
            
    def post_process(self):
        pass

    def __call__(self):
        """ This actually processes a request """
        # if something failed in post_init, ignore
        if not self.can_process:
            return
            
        assert self.form, "There needs to be a form to process and there is none when calling the command %s" % self
            
        # 1. test the form is good
        self.form = self.form(self.text)
        if not self.form.is_valid():
            form_not_validated.send(sender=self)
            raise FormFailed(self.not_valid(self.form))
            
        form_validated.send(sender=self)
        # 2. yay its good process it
        for method in [self.pre_process, self.process, self.post_process]:
            try:
                method()
            except CommandError, e:
                raise HandlerFailed(e.message)
            except:
                raise
                
        # 3. if something good happens, do that
        command_success.send(sender=self)
        msg = self.success()
        return msg