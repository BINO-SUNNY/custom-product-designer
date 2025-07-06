from django import forms
from .models import *
import re

from django.core.exceptions import ValidationError
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)
class RegistrationForm(forms.Form):
    # Fields for the form
    name = forms.CharField(max_length=254, required=True)
    phno = forms.CharField(max_length=10, required=True)  # Limited to 10 digits
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=50, required=True)

    # Validate Name (only alphabets and spaces)
    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Name can only contain alphabets and spaces.")
        return name

    # Validate Email (check uniqueness)
    def clean_email(self):
        email = self.cleaned_data['email']
        if logins.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
           
        return email

    # Validate Phone Number (must be exactly 10 digits)
    def clean_phno(self):
        phno = self.cleaned_data['phno']
        if not re.match(r'^\d{10}$', phno):  # Ensures exactly 10 digits
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phno

    # Validate Passwords Match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    # Save data to both Login and User models
    def save(self, user_type='user'):  # Allow setting user_type dynamically
        # Create a Login instance with hashed password
        login_instance = logins.objects.create(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'], # Hash password
            user_type=user_type
        )

        # Create a User instance, linking to the login instance
        user_instance = users.objects.create(
            name=self.cleaned_data['name'],
            phno=self.cleaned_data['phno'],
            login=login_instance
        )

        return user_instance