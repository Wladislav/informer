from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from newsletter.models import Subscription

class SubscriptionForm(forms.ModelForm):
    '''
    TODO:
    
    '''
    email = forms.EmailField(help_text=_(u'Email address'), required=True)
    class Meta:
        model = Subscription
        fields = ('email','subscribed')
        prefix = 'subscription'


        
        
        
