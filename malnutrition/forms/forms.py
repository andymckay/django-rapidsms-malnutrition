from datetime import datetime, date
import re

class FieldError(Exception):
    pass

class Field:
    creation_counter = 0
    
    def __init__(self, required=None):
        assert required is not None
        self.name = None
        self.required = required
        self.data = None
        self.valid = False
        self.error = None
        
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1
    
class Form(object):
    def __init__(self, text):
        self.fields = []
        self.errors = []
        self.sep = " "
        
        for item in dir(self):
            obj = getattr(self, item)
            if issubclass(obj.__class__, Field):
                obj.name = item
                self.fields.append([obj.creation_counter, obj])
        
        self.fields.sort()
        self.fields = [ f[1] for f in self.fields ]
    
        self.__call__(text)
    
    def __call__(self, text):
        text = text.strip().split(self.sep)
        
        for bit, field in map(None, text, self.fields):
            if field is None:
                self.errors.append("The text was longer than the form.")
                continue 
            if not bit:
                if field.required:
                    msg = "The field %s is required" % field.name
                    field.error = msg
                    self.errors.append(msg)
                continue
                
            try:
                if hasattr(field, "parser"):
                    bit = field.parser(bit)
                field.validate(bit)
            except FieldError, e: 
                field.error = str(e)
                self.errors.append(str(e))
    
        if not self.errors:
            self.valid = True
    
    def is_valid(self):
        return not bool(self.errors)


