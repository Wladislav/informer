from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from informer_core.utils import INFORMER_STATUS as info_status

from .models import (vCard,
                     vCard_adress,
                     vCard_email,
                     vCard_expertise,
                     vCard_hobby,
                     vCard_social,
                     vCard_messengers,
                     vCard_interest,
                     vCard_names,
                     vCard_organization,
                     vCard_phone,
                     vCard_related)
from .forms import vCardMainForm, vCardNamesForm, vCardPhoneForm
import json, uuid, datetime
from django import forms
from django.forms import modelform_factory
from django.forms.models import inlineformset_factory
from django.conf import settings
from informer.models import UserProfile
from geoposition.fields import GeopositionField
from django.http import HttpResponseBadRequest
from django.forms import widgets
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.translation import ugettext

def lang_context_processor(request):
    return {'LANG': request.LANGUAGE_CODE}

def default(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()
    elif isinstance(o, uuid.UUID):
        return str(o)
    
def convert_record(classHandler, iter_dict):
     if len(iter_dict)==0:
        return None
     i_arr = []
     for item in iter_dict:
         i_dict = {}
         for field_key in item.keys():
            fl = classHandler._meta.get_field(field_key)
            if len(fl.flatchoices)>0: # это choice
                i_dict[field_key] = str(fl.choices.__getitem__(item[field_key]))
            else:
                i_dict[field_key] = str(item[field_key])
         i_arr.append(i_dict)

     return i_arr

def get_verbose_and_help_fields(className, class_dict):
    vcard_fields = className._meta.get_fields()
    fields_verbose_name = {}
    fields_help_text = {}
    for field in vcard_fields:
        if hasattr(field, 'verbose_name'):
            fields_verbose_name[field.name] = str(field.verbose_name)
        if hasattr(field, 'help_text'):
            fields_help_text[field.name] = str(field.help_text)
    class_dict['fields_verbose_name'] = fields_verbose_name
    class_dict['fields_help_text'] = fields_help_text

def convert_fields(iter_record):
    i_dict = {}
    for field_key in iter_record.keys():
        if field_key == 'status':
            i_dict[field_key] = str(info_status[iter_record[field_key]])
        elif field_key == 'secure':
            i_dict[field_key] = str(vCard.CLASS[iter_record[field_key]])
        else:
            i_dict[field_key] = iter_record[field_key]
            
    return i_dict
  
def get_vcards_dict_format(user_id):
    qs = vCard.objects.filter(user_id=user_id).values()
    item_result = []
    for vc in qs:
        vcard_dict = convert_fields(vc)
        vcard_fields = vCard._meta.get_fields()
        fields_verbose_name = {}
        fields_help_text = {}
        for field in vcard_fields:
            if hasattr(field, 'verbose_name'):
                fields_verbose_name[field.name] = str(field.verbose_name)
            if hasattr(field, 'help_text'):
                fields_help_text[field.name] = str(field.help_text)
        vcard_dict['fields_verbose_name'] = fields_verbose_name
        vcard_dict['fields_help_text'] = fields_help_text
        item_result.append(vcard_dict)
    
    result = {'items':item_result}
    
    return result

def json_model(django_model, uid_vcard):
    qs_model  = django_model.objects.filter(owner = uid_vcard)
    model = convert_record(django_model, qs_model.values())
    result = {'items':model}
    get_verbose_and_help_fields(django_model, result)
    json_model_data = json.dumps(result, default=default)
    print(django_model.__name__)
    #to file for test
    with open("static/"+django_model.__name__+".json", "w") as out:
        out.write(json_model_data)    
    return json_model_data
    
@login_required
def vcard_list(request, template_name='informer_vcard/vcard_index.html',):
    context = {}
    user = User.objects.get_by_natural_key(request.user.username)
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == 'GET':
            if request.is_ajax():
                what_get = request.get_full_path()
                if what_get.find('vcard_list.json')>0:
                    user = request.user
                    dict_vcards = get_vcards_dict_format(user.id)
                    json_vcards = json.dumps(dict_vcards, default=default)
                    with open("static/vcard_list.json", "w") as out:
                         out.write(json_vcards)
                    return HttpResponse(json_vcards, content_type='application/json')
                
        return TemplateResponse(request, template_name, context)
    else:
        raise PermissionDenied
    

class InformerClearableFileInput(widgets.ClearableFileInput):
    
    template_name = 'forms/widgets/clearable_file_input.html'

    # template_with_initial_sound = (
    #     '<audio controls>'
    #         '<source src="%(initial_url)s" type="audio/ogg; codecs=vorbis">'
    #         '<source src="%(initial_url)s" type="audio/mpeg; codecs="mp3">'
    #         'Your browser does not support HTML5 audio. Here is a <a href="%(initial_url)s">link to the audio</a> instead.'
    #     '</audio></br>'
    #     '%(clear_template)s%(input_text)s: %(input)s'
    #     )
    # template_with_initial_video = (
    #     '<video controls>'
    #         '<source src="%(initial_url)s" type="video/mp4">'
    #         '<source src="%(initial_url)s" type="video/webm">'
    #         'Your browser does not support HTML5 video. Here is a <a href="%(initial_url)s">link to the video</a> instead.'
    #     '</video>'
    #     )
    # 
    # #template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s%(clear)s</label>'

class InformerCheckboxInput(widgets.CheckboxInput):
    template_name = 'forms/widgets/checkbox.html'

@login_required
def vcard_change(request, template_name='informer_vcard/vcard_change.html',):
    context = {}
    allowed_action = ['add','copy','change']
    user = User.objects.get_by_natural_key(request.user.username)
    vcard_to_change = None
    vcard_names_to_change = None
    pie_of_path = request.path_info.split('/')[:-1]
    action = pie_of_path[len(pie_of_path)-1]
    prefix = lang_context_processor(request)['LANG']
    if request.user.id != user.id:
        raise PermissionDenied
    # if request.method == "POST":
    #     if action not in pie_of_path:
    #         return HttpResponseBadRequest('Bad action...', status = 400)
    #     if action == 'change':
    #         uid_vcard = pie_of_path[len(pie_of_path)-2]
    #         try:
    #             vcard_to_change = vCard.objects.get(pk=uid_vcard)
    #         except ObjectDoesNotExist:
    #             return HttpResponseBadRequest('Object vCard does not exist...', status = 400)
    #         if vcard_to_change:
    #             try:
    #                 vcard_names_to_change = vCard_names.objects.get(pk=vcard_to_change)
    #             except ObjectDoesNotExist:
    #                 return HttpResponseBadRequest('Object vCard_names does not exist...', status = 400)
    #         
    #         vcard_main = vCardMainForm(request.POST, request.FILES, instance = vcard_to_change)
    #         vcard_name = vCardNamesForm(request.POST, instance = vcard_names_to_change)
    #         vcard_phone = vCardPhoneForm(request.POST, instance = vcard_names_to_change)
    #         form_vcard_main = vcard_main.is_valid()
    #         form_vcard_name = vcard_name.is_valid()
    #         print(request.POST)                
    #         print('1-'+str(form_vcard_main))
    #         print('2-'+str(form_vcard_name))
    #         if form_vcard_main:
    #             vcard_main.save()
    #         if form_vcard_name: 
    #             vcard_name.save()
    # 
    #     if action == 'add':
    #         print("add")
    # 
    #     return HttpResponseRedirect('/'+prefix+'/vcards/')
    
    if request.method == "GET":
        if action not in pie_of_path:
            return HttpResponseBadRequest('Bad action...', status = 400)
        if action == 'change':
            uid_vcard = pie_of_path[len(pie_of_path)-2]
            try:
                vcard_to_change = vCard.objects.get(pk=uid_vcard)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Object vCard does not exist...', status = 400)
            
            if vcard_to_change.user!=user:
                return HttpResponseBadRequest('Wrong owner...', status = 400)
            
            if vcard_to_change:
                try:
                    vcard_names_to_change = vCard_names.objects.get(pk=vcard_to_change)
                except ObjectDoesNotExist:
                    return HttpResponseBadRequest('Object vCard_names does not exist...', status = 400)
                
            if request.is_ajax():
                what_get = request.get_full_path()
                if what_get.find('vcard_adress.json')>0:
                    return HttpResponse(json_model(vCard_adress, uid_vcard), content_type='application/json')
                if what_get.find('vcard_phones.json')>0:
                    return HttpResponse(json_model(vCard_phone, uid_vcard), content_type='application/json')
                if what_get.find('vcard_emails.json')>0:
                    return HttpResponse(json_model(vCard_email, uid_vcard), content_type='application/json')
                if what_get.find('vcard_social.json')>0:
                    return HttpResponse(json_model(vCard_social, uid_vcard), content_type='application/json')
                if what_get.find('vcard_messeng.json')>0:
                    return HttpResponse(json_model(vCard_messengers, uid_vcard), content_type='application/json')
                if what_get.find('vcard_hobby.json')>0:
                    return HttpResponse(json_model(vCard_hobby, uid_vcard), content_type='application/json')
                if what_get.find('vcard_interest.json')>0:
                    return HttpResponse(json_model(vCard_interest, uid_vcard), content_type='application/json')
                if what_get.find('vcard_expertise.json')>0:
                    return HttpResponse(json_model(vCard_expertise, uid_vcard), content_type='application/json')                 
                
                    
        media_dict = {}
        # if vcard_to_change:
        #     if vcard_to_change.photo:
        #         media_dict[1] = {'path':vcard_to_change.photo.url, 'name':vCard._meta.get_field('photo').verbose_name.title()}
        #     else:
        #         media_dict[1] = {'path':'/media/avatars/avatar.png', 'name':_('Фотография')}
        # else:
        #     media_dict[1] = {'path':'/media/avatars/avatar.png', 'name':_('Фотография')}
        # if vcard_to_change:
        #     if vcard_to_change.logo:
        #         media_dict[2] = {'path':vcard_to_change.logo.url, 'name':vCard._meta.get_field('logo').verbose_name.title()}
        
        #vCard
        user_profile = UserProfile.objects.get(pk=user)
        vcard_main_formfactory = modelform_factory(
            vCard,
            fields = '__all__',
            widgets = {
                'user':      forms.TextInput(attrs={'type':'hidden'}),
                'objectname':forms.TextInput(attrs={'type':'hidden'}),
                # 'photo':     InformerClearableFileInput(attrs={'class':'input-photo'},),
                # 'logo':      InformerClearableFileInput(attrs={'class':'input-photo'},),
                # 'sound':     InformerClearableFileInput(attrs={'class':'input-photo'},),
                'label':     forms.TextInput(attrs={'type':'hidden'}),
                'status':    forms.Select(attrs={'class':'form-control'}),
                'category':  forms.TextInput(attrs={'class':'form-control'}),
                'note':      forms.TextInput(attrs={'class':'form-control'}),
                'language':  forms.Select(attrs={'class':'form-control'}),
                'tz':        forms.Select(attrs={'class':'form-control'}),
                'url':       forms.TextInput(attrs={'class':'form-control'}),
                'secure':    forms.Select(attrs={'class':'form-control'}),
                'start':     forms.DateTimeInput(attrs={
                    'required':'false',
                    'type':'text',
                    'data-dojo-type':'dijit/form/DateTextBox',
                    }),
                'end':       forms.DateTimeInput(attrs={
                    'required':'false',
                    'type':'text',
                    'data-dojo-type':'dijit/form/DateTextBox',
                    }),                     
                },
            )
        initial_vcard_main={
                'tz': user_profile.timezone,
                'language': user_profile.language,
                'user': user,
                }
        #vCard_names
        vcard_name_formfactory = modelform_factory(
            vCard_names,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'full_name':    forms.TextInput(attrs={'class':'form-control'}),
                'first_name':   forms.TextInput(attrs={'class':'form-control'}),
                'second_name':  forms.TextInput(attrs={'class':'form-control'}),
                'middle_name':  forms.TextInput(attrs={'class':'form-control'}),
                'bday':         forms.DateTimeInput(attrs={
                    'required':'false',
                    'type':'text',
                    'data-dojo-type':'dijit/form/DateTextBox',
                    }),                
                'prefix':       forms.TextInput(attrs={'class':'form-control'}),
                'suffix':       forms.TextInput(attrs={'class':'form-control'}),
                'nickname':     forms.TextInput(attrs={'class':'form-control'}),
                'title':        forms.TextInput(attrs={'class':'form-control'}),
                'role':         forms.TextInput(attrs={'class':'form-control'}),
                'sort_as':      forms.TextInput(attrs={'class':'form-control','type':'hidden'}),
            },
        )
        #vCard_phone
        vcard_phone_formfactory = modelform_factory(
            vCard_phone,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'tel':          forms.TextInput(attrs={'class':'form-control'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_phone'}),
                'function':     forms.Select(attrs={'class':'form-control'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_phone'}),
                },
        )
        #vCard_adress
        vcard_adress_formfactory = modelform_factory(
            vCard_adress,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'adress':       forms.TextInput(attrs={'class':'form-control'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_adress'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_adress'}),
                },            
        )
        #vCard_email
        vсard_email_formfactory = modelform_factory(
            vCard_email,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'email':        forms.TextInput(attrs={'class':'form-control'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_email'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_email'}),
                },
        )
        #vCard_social
        vcard_social_formfactory = modelform_factory(
            vCard_social,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'url':          forms.TextInput(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_social'}),
                },
        )
        #vCard_messengers
        vcard_messengers_formfactory = modelform_factory(
            vCard_messengers,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_messenger'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'identifier':   forms.TextInput(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_messengers'}),
                },
        )        
        #vCard_organization
        vcard_organization_formfactory = modelform_factory(
            vCard_organization,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_organization'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'org':          forms.TextInput(attrs={'class':'form-control'}),
                'form':         forms.TextInput(attrs={'class':'form-control'}),
                'title':         forms.TextInput(attrs={'class':'form-control'}),
                'role':         forms.TextInput(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_organization'}),
                },
        )
        #vCard_expertise
        vcard_expertise_formfactory = modelform_factory(
            vCard_expertise,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_expertise'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'expertise':    forms.TextInput(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_expertise'}),
                },
        )
        #vCard_hobby
        vcard_hobby_formfactory = modelform_factory(
            vCard_hobby,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_hobby'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'hobby':        forms.TextInput(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_hobby'}),
                },
        )
        #vCard_related
        vcard_related_formfactory = modelform_factory(
            vCard_related,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_related'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'relate':       forms.Select(attrs={'class':'form-control'}),
                'king':         forms.Select(attrs={'class':'form-control'}),
                },
        )
        #vCard_interest
        vcard_interest_formfactory = modelform_factory(
            vCard_interest,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'type':         forms.Select(attrs={'class':'form-control','id':'id_type_interest'}),
                'description':  forms.Textarea(attrs={'class':'form-control'}),
                'interest':     forms.TextInput(attrs={'class':'form-control'}),
                'prefer':       InformerCheckboxInput(attrs={'class':'form-control','id':'id_prefer_interest'}),
                },
        )        
        if vcard_to_change:
            vcard_main   = vcard_main_formfactory(instance=vcard_to_change)
            vcard_name   = vcard_name_formfactory(instance=vcard_names_to_change)
            vcard_phone  = vcard_phone_formfactory(instance=vcard_names_to_change)
            vcard_adress = vcard_adress_formfactory(instance=vcard_names_to_change)
            vсard_email  = vсard_email_formfactory(instance=vcard_names_to_change)
            vсard_social = vcard_social_formfactory(instance=vcard_names_to_change)
            vсard_messengers = vcard_messengers_formfactory(instance=vcard_names_to_change)
            vсard_organization = vcard_organization_formfactory(instance=vcard_names_to_change)
            vсard_expertise = vcard_expertise_formfactory(instance=vcard_names_to_change)
            vсard_hobby = vcard_hobby_formfactory(instance=vcard_names_to_change)
            vсard_interest = vcard_interest_formfactory(instance=vcard_names_to_change)
            vсard_related = vcard_related_formfactory(instance=vcard_names_to_change)
        else:
            vcard_main   = vcard_main_formfactory(initial_vcard_main)
            vcard_name   = vcard_name_formfactory()
            vcard_phone  = vcard_phone_formfactory()
            vcard_adress = vcard_adress_formfactory()
            vсard_email  = vсard_email_formfactory()
            vсard_social = vcard_social_formfactory()
            vсard_messengers = vcard_messengers_formfactory()
            vсard_organization = vcard_organization_formfactory()
            vсard_expertise = vcard_expertise_formfactory()
            vсard_hobby = vcard_hobby_formfactory()
            vсard_interest = vcard_interest_formfactory()
            vсard_related = vcard_related_formfactory()
               
        return render(request, "informer_vcard/vcard_change.html", {
            "user": user,
            "vcard_main":        vcard_main,
            "vcard_name":        vcard_name,
            "vcard_phone":       vcard_phone,
            "vcard_adress":      vcard_adress,
            "vсard_email":       vсard_email,
            "vсard_social":      vсard_social,
            "vсard_messengers":  vсard_messengers,
            "vсard_organization":vсard_organization,
            "vсard_expertise":   vсard_expertise,
            "vсard_hobby":       vсard_hobby,
            "vсard_interest":    vсard_interest,
            "vсard_related":     vсard_related,
            "media_dict":        media_dict,
            "MEDIA_URL":         settings.MEDIA_URL,
            "STATIC_URL":        settings.STATIC_URL,
        })        

    
    
    