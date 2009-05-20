from forms import Field, FieldError
import re
from datetime import datetime

class StringField(Field):
    def __init__(self, valid=None, required=False):
        self.rx = None
        if valid:
            self.rx = re.compile("^%s$" % valid)
        Field.__init__(self, required=required)
                    
    def validate(self, text):
        if self.rx.match(text):
            return text
        else:
            raise FieldError, "The field %s did not match the required format." % (self.name)


class FloatField(Field):
    def validate(self, text):
        try:
            data = float(text)
        except (TypeError, ValueError):
            raise FieldError, "The field %s was not formatted as a float, got %s" % (self.name, text)
        return data
        
class GenderField(Field):
    def validate(self, text):
        if text.lower() not in ["m", "f"]:
            raise FieldError, "The field %s was not formatted correctly, got %s" % (self.name, text)
        return text.lower()

class BooleanField(Field):
    def validate(self, text):
        if text.lower() not in ["y", "n"]:
            raise FieldError, "The field %s was not formatted correctly, got %s" % (self.name, text)
        return text.lower() == "y"
    
class DateField(Field):
    def __init__(self, format="%d/%m/%Y", required=False):
        self.format = format
        Field.__init__(self, required=required)
    
    def validate(self, text):
        try:
            if isinstance(text, str):
                return datetime.strptime(text, self.format).date()
            else:
                return text
        except ValueError, e:
            raise FieldError, "The field %s was not formatted correctly, got %s, expecting in format %s" % (self.name, text, self.format)

