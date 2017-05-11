from django import forms
from .models import vCard, vCard_names

class vCardMainForm(forms.ModelForm):
     class Meta:
        model = vCard
        fields = '__all__'
        prefix = 'vcard_main'
        
class vCardNamesForm(forms.ModelForm):
     class Meta:
        model = vCard_names
        fields = '__all__'
        prefix = 'vcard_name'
