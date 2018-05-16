from django import forms
from django.contrib.auth.forms import AuthenticationForm

from . import models


class LoginForm(AuthenticationForm):
    pass


class SignUpForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', strip=False, widget=forms.PasswordInput)
    
    class Meta:
        model = models.User
        fields = ('login', 'display_name', 'password1', 'password2')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2