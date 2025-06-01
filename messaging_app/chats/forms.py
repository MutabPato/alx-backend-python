from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class UserCreationForm(UserCreationForm):

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number')


class UserChangeForm(UserChangeForm):

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model =User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number')