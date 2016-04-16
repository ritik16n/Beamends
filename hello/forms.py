from django import forms
from .models import Link
import datetime
from django.contrib.auth.models import User

class Linkform(forms.ModelForm):
    class Meta:
        model = Link
        exclude=('user','total','sites','permonth',)

class RegistrationForm(forms.Form):
    username=forms.CharField(label='User Name',max_length=15)
    password = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    password1=forms.CharField(label='Verify Password',widget=forms.PasswordInput(render_value=False))
    email=forms.EmailField(label='Email')

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken, please select another.")
        return username

    def clean(self):
        password=self.cleaned_data['password']
        password1=self.cleaned_data['password1']
        if password != password1:
            raise forms.ValidationError("Password Mismatch")
        else:
            return self.cleaned_data


class InpurDateForDisplay(forms.Form):
    dt=forms.DateField(label='Enter Date',widget=forms.DateInput(format='%Y-%m-%d'))

class DateRangeForm(forms.Form):
    dt_from=forms.DateField(label='From',widget=forms.DateInput(format='%Y-%m-%d'))
    dt_to=forms.DateField(label='To', widget=forms.DateInput(format='%y-%m-%d'))


class ChangeUsername(forms.Form):
    curruser=forms.CharField(label='Current username')
    newuser=forms.CharField(label='New username')

    def clean_curruser(self):
        curruser=self.cleaned_data['curruser']
        if User.objects.filter(username=curruser).exists():
            return self.cleaned_data
        else:
            raise forms.ValidationError("Wrong user name")

class ChangeEmail(forms.Form):
    oldemail=forms.EmailField(label='Current Email address:')
    newmail=forms.EmailField(label='New Email address:')

class Dadsmail(forms.Form):
    dadsmail=forms.EmailField(label="What's your dad's Email address? :")

class LoginForm(forms.Form):
    username=forms.CharField(label='Username')
    password=forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
