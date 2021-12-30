from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class ASCIIUsernameField(UsernameField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(ASCIIUsernameValidator())


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        field_classes = {'username': ASCIIUsernameField}
