from django import forms
from .models import UserType, DonatorInfo


class DonatorInfoForm(forms.ModelForm):
    class Meta:
        model = DonatorInfo
        fields = ['information', 'donate_amount', 'blood_group']
