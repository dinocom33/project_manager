from django import forms
from django.contrib.auth import get_user_model

from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'bio', 'avatar']
        exclude = ['password']
