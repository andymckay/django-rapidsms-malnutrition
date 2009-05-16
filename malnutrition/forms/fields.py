from forms import Field, FieldError
import re

class StringField(Field):
    def __init__(self, valid=None, required=False):
        self.rx = None
        if valid:
            self.rx = re.compile("^%s$" % valid)
        Field.__init__(self, required=required)
                    
    def validate(self, text):
        if not self.rx:
            self.valid = True
        else:
            if self.rx.match(text):
                self.valid = True
                self.data = text
            else:
                raise FieldError, "The field %s did not match the required format." % (self.name)

class GenderField(Field):
    def __init__(self, required=False):
        Field.__init__(self, required=required)

    def validate(self, text):
        if text.lower() not in ["m", "f"]:
            raise FieldError, "The field %s was not formatted correctly, got %s" % (self.name, text)
        self.valid = True
        self.data = text.lower()

class BooleanField(Field):
    def __init__(self, required=False):
        Field.__init__(self, required=required)
        
    def validate(self, text):
        if text.lower() not in ["y", "n"]:
            raise FieldError, "The field %s was not formatted correctly, got %s" % (self.name, text)
        self.valid = True
        self.data = text.lower() == "y"
    
class DateField(Field):
    def __init__(self, format="%d/%m/%Y", required=False):
        self.format = format
        Field.__init__(self, required=required)
    
    def validate(self, text):
        try:
            if isinstance(text, str):
                self.data = datetime.strptime(text, self.format).date()
            else:
                self.data = text
        except ValueError, e:
            raise FieldError, "The field %s was not formatted correctly, got %s, expecting in format %s" % (self.name, text, self.format)
        self.valid = True
