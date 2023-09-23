
from .models import BusinessInfo
from django import forms

class BusinessInfoForm(forms.ModelForm):

	class Meta:
		model = BusinessInfo
		exclude = ['user']

