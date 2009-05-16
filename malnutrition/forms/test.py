import unittest

from datetime import datetime, date
import re

from forms import Form
from fields import BooleanField, StringField, DateField

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
        assert rf.is_valid()
        assert rf.male.data
        assert rf.date.data.month == 12
        assert not rf.errors

if __name__=="__main__":
    unittest.main()