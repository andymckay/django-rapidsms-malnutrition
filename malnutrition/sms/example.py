import sys
from os.path import dirname

parent = dirname(dirname(dirname(__file__)))
sys.path.append(parent)

from malnutrition.forms import Form
from malnutrition.forms import FloatField
from malnutrition.sms.command import Command, FormFailed, CommandError, HandlerFailed

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

class SillyNumberForm(Form):
    second = FloatField()
    first = FloatField()
    
class SillyDivide(Divide):
    def post_init(self):
        self.form = SillyNumberForm
        
    def not_valid(self, form):
        return "You sir, are a muppet."

if __name__=="__main__":
    print Divide(None, "1 2",)()
    try:
        print Divide(None, "a 2",)()
    except FormFailed, e:
        print "a 2 failed with: %s" % e
    try:
        print Divide(None, "6.0 0",)()        
    except HandlerFailed, e:
        print "6.0 0 failed with: %s" % e
    print SillyDivide(None, "2 1")()
    try:
        print SillyDivide(None, "0 1")()    
    except HandlerFailed, e:
        print "0 1 failed with: %s" % e
    try:
        print SillyDivide(None, "a 2",)()
    except FormFailed, e:
        print "a 2 failed with: %s" % e
    