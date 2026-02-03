from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class AddTeacherForm(forms.Form):
    full_name = forms.CharField(label="Teacher Name", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Username of Teacher", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password for Teacher", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

class ChangeTeacherPasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
