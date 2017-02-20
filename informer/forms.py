from django import forms
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class RegistrationFormTOSAndEmail(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    pass

class DjangoProfileForm(forms.ModelForm):
    email = forms.EmailField(help_text=_(u'Email address'), required=True)    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        prefix = 'person_main'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'photo', 'website', 'bio', 'phone', 'city', 'country', 'language']
        prefix = 'person_adds'
        