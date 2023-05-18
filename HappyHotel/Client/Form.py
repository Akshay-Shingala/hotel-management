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
    today=datetime.date.today() 
    checkInDate = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date','value':datetime.date.today()}))
    checkOutDate = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date','value':today + datetime.timedelta(days=1)}))