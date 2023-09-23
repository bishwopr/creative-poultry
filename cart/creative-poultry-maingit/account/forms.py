from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomerRegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('email',)
        help_texts = {
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(CustomerRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email
    
class BusinessRegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('email','business_info','address')
        help_texts = {
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(BusinessRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email