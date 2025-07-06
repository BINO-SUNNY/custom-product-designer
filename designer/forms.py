from django import forms
from django.core.exceptions import ValidationError
from adminapp.models import Designers
from customproductdesignerapp.models import logins
import re

class DesignerProfileForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter new email'}),
        required=True
    )
    phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        required=True
    )
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter current password'}),
        required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        required=False
    )

    class Meta:
        model = Designers
        fields = ['name', 'phonenumber', 'qualification', 'description', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.login:
            self.login_instance = self.instance.login  # Store login reference
            self.fields['email'].initial = self.login_instance.email  # Set initial email value

    def clean_email(self):
        new_email = self.cleaned_data.get('email')

        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, new_email):
            raise ValidationError("Enter a valid email address.")

        # Check uniqueness of email
        if logins.objects.filter(email=new_email).exclude(id=self.instance.login.id).exists():
            raise ValidationError("This email is already in use.")

        return new_email

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')

        # Ensure phone number is exactly 10 digits
        if not re.fullmatch(r'\d{10}', phonenumber):
            raise ValidationError("Phone number must be exactly 10 digits.")

        return phonenumber

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if not self.login_instance or self.login_instance.password != current_password:
            raise ValidationError("Current password is incorrect.")

        return current_password

    def save(self, commit=True):
        designer = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        new_email = self.cleaned_data.get('email')

        # Update email in the linked login instance
        if new_email and self.instance.login:
            self.instance.login.email = new_email
            self.instance.login.save()

        # Update password only if a new one is provided
        if new_password:
            self.instance.login.password = new_password  # You should hash this password
            self.instance.login.save()

        if commit:
            designer.save()

        return designer
