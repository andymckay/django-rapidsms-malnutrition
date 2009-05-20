from datetime import datetime, date
import re

class FieldError(Exception):
    pass

class Field:
    creation_counter = 0
    
    def __init__(self, required=True):
        assert required is not None
        self.name = None
        self.required = required
        self.data = None
        self.valid = False
        self.error = None
        
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

class Data:
    pass

class IterData:
    def __init__(self):
        self._counter = 0
        
    def __iter__(self):
        while self._counter < len(self._fields):
            yield self._fields[self._counter]
            self._counter += 1
    
class Form:
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
        self.clean = IterData()
        self.clean._fields = []
        fields = []
        for f in self.fields:
            fields.append(f[1])
            cleaned = Data()
            cleaned.name = f[1].name
            setattr(self.clean, cleaned.name, cleaned)
            self.clean._fields.append(cleaned)
        self.fields = fields

        self.__call__(text)
    
    def __call__(self, text):
        text = text.strip().split(self.sep)
        
        for bit, field in map(None, text, self.fields):
            clean = getattr(self.clean, field.name)
            clean.data = None
            clean.error = None
            clean.raw = None
            
            if field is None:
                self.errors.append("The text was longer than the form.")
                continue 
            if not bit:
                if field.required:
                    msg = "The field %s is required" % field.name
                    clean.error = msg
                    self.errors.append(msg)
                continue
                
            try:
                clean.raw = bit
                if hasattr(field, "parser"):
                    bit = field.parser(bit)
                data = field.validate(bit)
                clean.data = data
            except FieldError, e: 
                clean.error = str(e)
                self.errors.append(str(e))
    
    def is_valid(self):
        return not bool(self.errors)


