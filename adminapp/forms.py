from django import forms
from .models import *
from django.core.exceptions import ValidationError
from customproductdesignerapp.models import logins

import re

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        },

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['colorname']
        widgets = {
            'colorname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter color name'}),
        }
class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['sizename']
        widgets = {
            'sizename': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter size name'}),
        }
class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['category', 'image','description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
class DesignerForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=50, required=True)

    class Meta:
        model = Designers
        fields = ['name', 'phonenumber', 'qualification', 'description', 'photo']

    # Name validation: Only alphabet and space
    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Name can only contain alphabets and spaces.")
        return name

    # Phone number validation: Must be exactly 10 digits
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']
        if len(phonenumber) != 10 or not phonenumber.isdigit():
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phonenumber

    # Password match validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    # Save user and designer
    def save(self, commit=True):
        login = logins.objects.create(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            user_type='Designer'
        )
        designer = super().save(commit=False)
        designer.login = login
        if commit:
            designer.save()
        return designer
class FreetemplateForm(forms.ModelForm):
    class Meta:
        model = FreeTemplate
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter template name'}),
        },

        
        
