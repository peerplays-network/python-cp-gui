from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(label='Last Name',max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(label='Email' , max_length=30, help_text='Required. Inform a valid email address.')
    # about = forms.EmailField(label='About' , max_length=254, required=False , help_text="Optional. ")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )