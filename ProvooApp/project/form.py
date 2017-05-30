import account.forms
from django import forms
from django.forms.extras.widgets import SelectDateWidget

# 
# class SignupForm(account.forms.SignupForm):
#     first_name = forms.CharField(max_length=20)
#     last_name = forms.CharField(max_length=20)
#     birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))
