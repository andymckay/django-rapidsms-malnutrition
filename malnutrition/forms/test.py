import unittest

from datetime import datetime, date
import re

from forms import Form
from fields import BooleanField, StringField, DateField, CatchallField

def parser(text):
    return date(year=int(text[4:8]),day=int(text[0:2]),month=int(text[2:4]))

class test(unittest.TestCase):
    # These need to be expanded 

    def testSimple(self):
        class ReportForm(Form):
            male = BooleanField()
            date = DateField(format="%m%d%Y")
            date.parser = parser
            id = StringField(required=True, valid="(\d+)")

        rf = ReportForm("y 19122008 123")
        assert not rf.clean.id.error #== "The field id is required"

    def testCatchAll(self):
        class OtherForm(Form):
            male = BooleanField()
            text = CatchallField()
            
        of = OtherForm("n sdklfj sd fjsldf sdlfjs dfsdf sdf")
        assert of.clean.text.data == "sdklfj sd fjsldf sdlfjs dfsdf sdf"

        class OtherForm(Form):
            male = BooleanField()
            text = CatchallField()
            # this will never work
            id = StringField(required=True, valid="(\d+)")
            
        of = OtherForm("n sdklfj sd fjsldf sdlfjs dfsdf sdf")
        assert of.clean.text.data == "sdklfj sd fjsldf sdlfjs dfsdf sdf"
        assert of.errors

if __name__=="__main__":
    unittest.main()