import unittest
from datetime import datetime, timedelta
from parse import years_months, stunting, weight_for_height

def date_boundaries():
    now = datetime.now()
    mapping = {
        "under 2 months": 45,
        "over 2 months": 72,
        "over 1 year": 380,
        "over 2 years": 770,
        "over 3 years": 1110,
        "over 3.5 years": 1300,
        "over 6 years": 2300,
        "over 9 years": 3300,
        "over 15 years": 5500
    }
    for age, diff in mapping.items():
        mapping[age] = (now - timedelta(days=diff))

    return mapping
    
class test(unittest.TestCase):
    def test_stunting(self):
        dates = date_boundaries()
        # this is actually 1 and a bit months, not 1.5
        assert stunting(dates["under 2 months"], "m") == "47.98"
        assert stunting(dates["over 1 year"], "m") == "69.83"
        assert stunting(dates["over 3 years"], "m") == "88.13"
        assert stunting(dates["over 3.5 years"], "m") == "91.59"
        
    def test_weight_for_height(self):
        assert weight_for_height(85.3, 12.50) == "100%-85%"
        assert weight_for_height(85.3, 8.7) == "70%-60%"
        assert weight_for_height(107.4, 14.0) == "80%-75%" # rounding down
        assert weight_for_height(107.5, 14.0) == "75%-70%" # leaving same
        assert weight_for_height(107.6, 12.0) == "60%-" # rounding down to 56.5
      
if __name__=="__main__":
    unittest.main()