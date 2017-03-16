from django.shortcuts import render_to_response, get_object_or_404
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.http import *
from django.conf import settings
from django.template.loader import render_to_string
from django.apps import apps
from django.views.decorators.csrf import csrf_protect
from newsletter.models import Subscription
from newsletter.forms import SubscriptionForm
from newsletter.core import csv

import datetime
import re

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def generate_csv(request, model_str="newsletter.subscription", data=None):
    '''
    TODO:
    
    '''

    if not data:
        model = apps.get_model(*model_str.split('.'))
        data = model._default_manager.filter(subscribed=True)
    
    if len(data) == 0:
        data = [["no subscriptions"],]
    return csv.ExcelResponse(data)

@csrf_protect
def subscribe_detail(request, form_class=SubscriptionForm, 
        template_name='newsletter/subscribe.html',  
        success_template='newsletter/success.html',
        extra_context=None,
        model_str="newsletter.subscription"):

    if request.POST:   
        try:
            model = apps.get_model(*model_str.split('.')) 
            instance = model._default_manager.get(email=request.POST['email'])
        except model.DoesNotExist: 
            instance = None
        form = form_class(request.POST, instance = instance)
        if form.is_valid():
            subscribed = form.cleaned_data["subscribed"]
            
            form.save()
            if subscribed:
                message = getattr(settings,
                    "NEWSLETTER_OPTIN_MESSAGE", "Success! You've been added.")
            else:
                message = getattr(settings,
                     "NEWSLETTER_OPTOUT_MESSAGE", 
                     "You've been removed. Sorry to see ya go.")          

            context = {
                'success': True,
                'message': message,
                'form': form_class(),
            }
            return TemplateResponse(request, success_template, context)
    else:
        form = form_class()
    
    context = {
        'form': form,
    }    
    return TemplateResponse(request, template_name, context)

