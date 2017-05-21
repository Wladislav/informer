from django import forms
from .models import vCard, vCard_names, vCard_phone

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
        
class vCardPhoneForm(forms.ModelForm):
     class Meta:
        model = vCard_phone
        fields = '__all__'
        prefix = 'vcard_phone'
     
