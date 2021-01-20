from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(label='First Name')
    first_name = forms.CharField(label='First Name',max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs={ }),)
    last_name = forms.CharField(label='Last Name',max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs={ }),)
    email = forms.EmailField(label='Email' , max_length=30, help_text='Required. Inform a valid email address.')
 
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name','password1', 'password2', )

 
 