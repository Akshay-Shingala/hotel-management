from django.db import models
from datetime import datetime
# importing validationerror
from django.core.exceptions import ValidationError
import re
def validate_mobile(value):
    """ Raise a ValidationError if the value looks like a mobile telephone number.
    """
    r=re.fullmatch('[6-9][0-9]{9}',value) # calling fullmatch function by passing pattern and n
    if r==None: # checking whether it is none or not 
        msg = u"Invalid mobile number."
        raise ValidationError(msg)
    else:
        return value
def numberValidation(value):
    try:
        int(value)
        return value
    except:
        return ValidationError("enter valid number")

def checkIndateValidation(value):
    if value < datetime.now():
        return ValidationError("not proper check in datetime")
    