from datetime import datetime
from data import stunting_boys, stunting_girls
from data import weight_for_height as weight_for_height_data

def years_months(date):
    now = datetime.now().date()
    ymonths = (now.year - date.year) * 12
    months = ymonths + (now.month - date.month)
    return (now.year - date.year, months)
    
def stunting(date, gender):
    assert gender.lower() in ["m", "f"]
    years, months = years_months(date)
    # we have a month eg: 9, so we assume that is 8.5, since
    # it can't be 9.5... assuming the .5's are there to make sure that
    if int(months) > 73:
        raise ValueError, "Stunting charts only go as high as 72.5 months"
    elif int(months) >= 1:
        months = str(int(months) - 0.5)
    else:
        # lowest bound
        months = 0
        
    if gender.lower() == "m":
        stunts = stunting_boys.data
    else:
        stunts = stunting_girls.data
    return stunts[months]

def _dumb_round(number):
    # please improve
    assert isinstance(number, (float, int)), "Got a %s, which is a: %s" % (number, type(number)) # forget duck typing, this won't work on anything else
    remainder = number - int(number)
    if remainder >= 0.5:
        remainder = 0.5
    else:
        remainder = 0.0
    return int(number) + remainder

texts = ["60%-", "70%-60%","75%-70%", "80%-75%","85%-80%","100%-85%"]

def _get_text(value, targets):
    targets.reverse()
    result = "60%-"
    for text, target in zip(texts, targets):
        target = float(target)
        if value >= target:
            result = text
    return result
    
def weight_for_height(height, weight):
    weight = float(weight)
    number = _dumb_round(height)
    
    if number < 49.0:
        # raise ValueError, "Weight for height charts only go as low as 85.0, got height %s." % height
        return None
    elif number > 130.0:
        # raise ValueError, "Weight for height charts only go as high as 130.0, got height %s." % height
        return None
        
    targets = weight_for_height_data.data[str(number)][:]
    return _get_text(weight, targets)
