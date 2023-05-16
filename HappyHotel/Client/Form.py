from django import forms
from .models import ClientUser
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