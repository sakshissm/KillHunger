from django import forms
from .models import SignUp,Applicant,AreaReport,Donate,Contact
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(),label="Choose password\n")
    class Meta:
        model=User
        fields=('first_name','last_name','username','password','email')

class ApplicantForm(forms.ModelForm):
    profile_pic=forms.ImageField(required=False)
    class Meta:
        model=Applicant
        fields="__all__"
    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        if len(mobile)==10 and mobile.isdigit():
            return mobile
        else:
            raise forms.ValidationError("Please enter a valid contact number")
    def clean_pincode1(self):
        pincode1=self.cleaned_data['pincode1']
        if len(pincode1)==6 and pincode1.isdigit():
            return pincode1
        else:
            raise forms.ValidationError("Please enter a valid pincode")
    def clean_pincode2(self):
        pincode2=self.cleaned_data['pincode2']
        if len(pincode2)==6 and pincode2.isdigit():
            return pincode2
        else:
            raise forms.ValidationError("Please enter a valid pincode")

    def clean_pincode3(self):
        pincode3=self.cleaned_data['pincode3']
        if len(pincode3)==6 and pincode3.isdigit():
            return pincode3
        else:
            raise forms.ValidationError("Please enter a valid pincode")

class AreaForm(forms.ModelForm):
    name=forms.CharField(label="Name of the area:")
    source=forms.CharField(label="How you come to know about this area?")
    class Meta:
        model=AreaReport
        fields="__all__"

    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        if len(mobile)==10 and mobile.isdigit():
            return mobile
        else:
            raise forms.ValidationError("Please enter a valid contact number")

    def clean_pincode(self):
        pincode=self.cleaned_data['pincode']
        if len(pincode)==6 and pincode.isdigit():
            return pincode
        else:
            raise forms.ValidationError("Please enter a valid pincode")

class DonateForm(forms.ModelForm):
    food_description=forms.CharField(widget=forms.Textarea,label="Please provide detailed description of food like name,quantity,etc:")
    purpose=forms.CharField(label="Why you have leftover food(like because of birthday party,marriage)?")
    location=forms.URLField(label="Provide a google map link of your location:")
    class Meta:
        model=Donate
        exclude=['donor','start_time','driver','end_time','flag']

def clean_pincode(self):
    pincode=self.cleaned_data['pincode']
    if len(pincode)==6 and pincode.isdigit():
        return pincode
    else:
        raise forms.ValidationError("Please enter a valid pincode")

def clean_mobile(self):
    mobile=self.cleaned_data['mobile']
    if len(mobile)==10 and mobile.isdigit():
        return mobile
    else:
        raise forms.ValidationError("Please enter a valid contact number")


class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        exclude=['user']
