from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                'The user is awating admin approval',
                code='inactive',
            )
        elif self.user_cache is None:
             raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
            )
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is None or username is '':
            raise forms.ValidationError(
                        'Username cannot be left blank',
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
        elif username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            print(self.user_cache)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(username=username)
                except:
                    user_temp = None

                if user_temp is not None:
                        self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
          
        return self.cleaned_data

class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(label='First Name')
    first_name = forms.CharField(label='First Name',max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs={ }),)
    last_name = forms.CharField(label='Last Name',max_length=30, required=False, help_text='Optional.',widget=forms.TextInput(attrs={ }),)
    email = forms.EmailField(label='Email' , max_length=30, help_text='Required. Inform a valid email address.')
 
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name','password1', 'password2', )

 
 