from django import forms 
from .models import *
import re
from adminapp.models import *


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = Design_request
        fields = ['category', 'product', 'size', 'color', 'requestdescription', 'image', 'add_to_template']

class TemplateSelectionForm(forms.Form):
    template = forms.ModelChoiceField(queryset=Template.objects.all(), empty_label="Select a template")


class UserColorForm(forms.ModelForm):
     class Meta:
        model = usercolor
        fields = ['Color_image']


class FreeTemplateSelectionForm(forms.Form):
    template = forms.ModelChoiceField(queryset=FreeTemplate.objects.all(), empty_label="Select a freetemplate")    
import datetime

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'hname', 'district', 'landmark', 'pin', 'phonenumber']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'hname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter House Name'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter District'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Landmark'}),
            'pin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 6-digit PIN', 'maxlength': '6'}),
            'phonenumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit Phone Number', 'maxlength': '10'}),
        }

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if not pin.isdigit() or len(pin) != 6:
            raise forms.ValidationError("PIN must be exactly 6 digits.")
        return pin

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if not phonenumber.isdigit() or len(phonenumber) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phonenumber

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['date', 'description', 'gift_note']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter gift description', 'rows': 3}),
            'gift_note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter gift note', 'rows': 2}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'id': 'giftDatePicker'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set fields to be required or not based on the context
        # If the 'is_gift' field is checked (true), make these fields required
        if kwargs.get('initial', {}).get('is_gift', False):
            self.fields['date'].required = True
            self.fields['description'].required = True
        else:
            self.fields['date'].required = False
            self.fields['description'].required = False

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']
