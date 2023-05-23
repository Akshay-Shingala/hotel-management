from django import forms
from Rooms.models import *
from .models import ClientUser
import datetime
class RagistrationForm(forms.ModelForm):
    class Meta:
        model=ClientUser
        fields=['firstName', 'lastName', 'emailId', 'mobileNumber','password']
        try:
            widgets={
            'firstName':forms.TextInput(attrs={'class':'form-control ','name':'l_name','placeholder':'Enter Last name','required':True}),
            'lastName':forms.TextInput(attrs={'class':'form-control ','name':'f_name','placeholder':'Enter First name','required':True}),
            'emailId':forms.EmailInput(attrs={'class':'form-control ','name':'email','placeholder':'Enter Email','required':True}),
            'mobileNumber':forms.NumberInput(attrs={'class':'form-control ','name':'PhoneNumber','placeholder':'Enter Phone','required':True}),
            'password':forms.PasswordInput(attrs={'class':'form-control ','placeholder':'enter password','name=':'image','required':True})
        }
        except Exception as e:
            print(e)
            print("*******************************aaa")

class bookingForm(forms.Form):
    class Meta:
        model=Bookings
        fields=['userId', 'room','checkInTime', 'checkOutTime']
        widgets={
            'checkInTime':forms.DateInput(attrs={})
        }
class searchCityHotelForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
class checkInCheckOutForm(forms.Form):
    today=datetime.datetime.now() 
    print(today,"today")
    checkInDateVar=datetime.datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute)
    checkOutDateVar=datetime.datetime(year=today.year, month=today.month, day=today.day+1, hour=today.hour, minute=today.minute)
    checkInDate = forms.DateTimeField(widget=forms.DateTimeInput (attrs={'class':'form-control','type':'datetime-local','value':checkInDateVar.strftime("%Y-%m-%dT%H:%M")}),initial=checkInDateVar)
    checkOutDate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local','value':checkOutDateVar.strftime("%Y-%m-%dT%H:%M")}),initial=checkOutDateVar)
    
    def __init__(self, *args, **kwargs):
        super(checkInCheckOutForm, self).__init__(*args, **kwargs)
        today=datetime.datetime.now() 
        # checkInDate=datetime.datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute)
        # checkOutDate=datetime.datetime(year=today.year, month=today.month, day=today.day+1, hour=today.hour, minute=today.minute)
        # self.fields["checkInDate"].initial=checkInDate
        # self.fields["checkOutDate"].initial=checkOutDate

    