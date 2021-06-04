from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=gettext('First Name'), max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(label=gettext('Last Name'), max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(label=gettext('Email'), max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
