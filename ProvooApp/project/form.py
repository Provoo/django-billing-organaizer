# from django.contrib.auth.models import User
# from django.forms.extras.widgets import SelectDateWidget

import account.forms
from django import forms
from account.utils import get_user_lookup_kwargs
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    # phone = forms.CharField(max_length=30, label='Phone')
    # UserIDu = forms.CharField(max_length=30, label='Country Id')

    def clean_username(self):
        clean_username = super(SignupForm, self).clean()
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))
        return clean_username

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["email"]
