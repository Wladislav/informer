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
                     vCard_category,
                     vCard_email,
                     vCard_expertise,
                     vCard_hobby,
                     vCard_impp,
                     vCard_interest,
                     vCard_names,
                     vCard_organization,
                     vCard_phone,
                     vCard_related)
from .forms import vCardMainForm, vCardNamesForm
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
    
# def convert_record(iter_dict):
#     if len(iter_dict)==0:
#         return None
#     i_arr = []
#     for item in iter_dict:
#         i_dict = {}
#         for field_key in item.keys():
#             i_dict[field_key]=item[field_key]
#         i_arr.append(i_dict)
#     return i_arr

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
    i = 0;
    for vc in qs:
        i = i+1;
        # qs_adress           = vCard_adress.objects.filter(owner = vc['uid']).values()
        # qs_category         = vCard_category.objects.filter(owner = vc['uid']).values()
        # qs_email            = vCard_email.objects.filter(owner = vc['uid']).values()
        # qs_expertise        = vCard_expertise.objects.filter(owner = vc['uid']).values()
        # qs_hobby            = vCard_hobby.objects.filter(owner = vc['uid']).values()
        # qs_impp             = vCard_impp.objects.filter(owner = vc['uid']).values()
        # qs_interest         = vCard_interest.objects.filter(owner = vc['uid']).values()
        # qs_names            = vCard_names.objects.filter(owner = vc['uid']).values()
        # qs_organization     = vCard_organization.objects.filter(owner = vc['uid']).values()
        # qs_phone            = vCard_phone.objects.filter(owner = vc['uid']).values()
        # qs_related          = vCard_related.objects.filter(owner = vc['uid']).values()
        # 
        # info = {
        #     'adress':       convert_record(qs_adress),
        #     'category':     convert_record(qs_category),
        #     'email':        convert_record(qs_email),
        #     'expertise':    convert_record(qs_expertise),
        #     'hobby':        convert_record(qs_hobby),
        #     'social':       convert_record(qs_impp),
        #     'interest':     convert_record(qs_interest),
        #     'names':        convert_record(qs_names),
        #     'organization': convert_record(qs_organization),
        #     'phone':        convert_record(qs_phone),
        #     'related':      convert_record(qs_related),
        #     }
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
        
        #vcard_dict['info'] = info
        item_result.append(vcard_dict)
    
    result = {'items':item_result}
    
    return result
    
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
                    # with open("static/vcard_list.json", "w") as out:
                    #      out.write(json_vcards)
                    return HttpResponse(json_vcards, content_type='application/json')
                
        return TemplateResponse(request, template_name, context)
    else:
        raise PermissionDenied
    

class InformerClearableFileInput(widgets.ClearableFileInput):
    
    initial_text = ugettext('Currently')
    input_text = ugettext('Change')
    clear_checkbox_label = ugettext('Clear')
    
    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a>'
        '%(clear_template)s%(input_text)s: %(input)s'
    )
    template_with_initial_sound = (
        '<audio controls>'
            '<source src="%(initial_url)s" type="audio/ogg; codecs=vorbis">'
            '<source src="%(initial_url)s" type="audio/mpeg; codecs="mp3">'
            'Your browser does not support HTML5 audio. Here is a <a href="%(initial_url)s">link to the audio</a> instead.'
        '</audio></br>'
        '%(clear_template)s%(input_text)s: %(input)s'
        )
    template_with_initial_video = (
        '<video controls>'
            '<source src="%(initial_url)s" type="video/mp4">'
            '<source src="%(initial_url)s" type="video/webm">'
            'Your browser does not support HTML5 video. Here is a <a href="%(initial_url)s">link to the video</a> instead.'
        '</video>'
        )

    #template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s%(clear)s</label>'
    
    template_with_clear = (
        '<div class="skin-minimal">'
           '<ul class="list">'
              '<li>'
                '<label for="%(clear_checkbox_id)s">%(clear)s%(clear_checkbox_label)s</label>'
              '</li>'
           '</ul>'
        '</div>'
    )
    
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if self.is_initial(value):
            extention = str(value)[-3:]
            if extention == 'mp3' or extention == 'ogg':
                self.template_with_initial = self.template_with_initial_sound 
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)    

@login_required
def vcard_add_copy_change(request, template_name='informer_vcard/vcard_add_copy_change.html',):
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
    if request.method == "POST":
        if action not in pie_of_path:
            return HttpResponseBadRequest('Bad action...', status = 400)
        if action == 'change':
            uid_vcard = pie_of_path[len(pie_of_path)-2]
            try:
                vcard_to_change = vCard.objects.get(pk=uid_vcard)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Object vCard does not exist...', status = 400)
            if vcard_to_change:
                try:
                    vcard_names_to_change = vCard_names.objects.get(pk=vcard_to_change)
                except ObjectDoesNotExist:
                    return HttpResponseBadRequest('Object vCard_names does not exist...', status = 400)
            
            vcard_main = vCardMainForm(request.POST, request.FILES, instance = vcard_to_change)
            vcard_name = vCardNamesForm(request.POST, instance = vcard_names_to_change)
            form_vcard_main = vcard_main.is_valid()
            form_vcard_name = vcard_name.is_valid()
            print(request.POST)                
            print('1-'+str(form_vcard_main))
            print('2-'+str(form_vcard_name))
            if form_vcard_main:
                vcard_main.save()
            if form_vcard_name: 
                vcard_name.save()
            # if form_vcard_main and form_vcard_name:
            #     messages.success(request, _('Данные успешно сохранены!'))
        if action == 'add':
            print("add")

        return HttpResponseRedirect('/'+prefix+'/vcards/')
    
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
                    
        css_class = {'class':'form-control'}
        media_dict = {}
        if vcard_to_change:
            if vcard_to_change.photo:
                media_dict[1] = {'path':vcard_to_change.photo.url, 'name':vCard._meta.get_field('photo').verbose_name.title()}
            else:
                media_dict[1] = {'path':'/media/avatars/avatar.png', 'name':_('Здесь будет фотография')}
        else:
            media_dict[1] = {'path':'/media/avatars/avatar.png', 'name':_('Здесь будет фотография')}
        if vcard_to_change:
            if vcard_to_change.logo:
                media_dict[2] = {'path':vcard_to_change.logo.url, 'name':vCard._meta.get_field('logo').verbose_name.title()}
        user_profile = UserProfile.objects.get(pk=user)
        vcard_main_formfactory = modelform_factory(
            vCard,
            fields = '__all__',
            widgets = {
                'user':      forms.TextInput(attrs={'type':'hidden'}),
                'objectname':forms.TextInput(attrs={'type':'hidden'}),
                'photo':     InformerClearableFileInput(attrs={'class':'input-photo'},),
                'logo':      InformerClearableFileInput(attrs={'class':'input-photo'},),
                'sound':     InformerClearableFileInput(attrs={'class':'input-photo'},),                    
                'label':     forms.TextInput(attrs=css_class),
                'status':    forms.Select(attrs=css_class),
                'note':      forms.TextInput(attrs=css_class),
                'language':  forms.Select(attrs=css_class),
                'tz':        forms.Select(attrs=css_class),
                'url':       forms.TextInput(attrs=css_class),
                'secure':    forms.Select(attrs=css_class),
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
        initial_vcard_name={}            
        vcard_name_formfactory = modelform_factory(
            vCard_names,
            fields = '__all__',
            widgets = {
                'owner':        forms.TextInput(attrs={'type':'hidden'}),
                'full_name':    forms.TextInput(attrs=css_class),
                'first_name':   forms.TextInput(attrs=css_class),
                'second_name':  forms.TextInput(attrs=css_class),
                'middle_name':  forms.TextInput(attrs=css_class),
                'bday':         forms.DateTimeInput(attrs={
                    'required':'false',
                    'type':'text',
                    'data-dojo-type':'dijit/form/DateTextBox',
                    }),                
                'prefix':       forms.TextInput(attrs=css_class),
                'suffix':       forms.TextInput(attrs=css_class),
                'nickname':     forms.TextInput(attrs=css_class),
                'title':        forms.TextInput(attrs=css_class),
                'role':         forms.TextInput(attrs=css_class),
                'sort_as':      forms.TextInput(attrs={'class':'form-control','type':'hidden'}),
            },
        )            
        if vcard_to_change:
            vcard_main = vcard_main_formfactory(instance=vcard_to_change)
            vcarf_name = vcard_name_formfactory(instance=vcard_names_to_change)
        else:
            vcard_main = vcard_main_formfactory(initial_vcard_main)
            vcarf_name = vcard_name_formfactory(initial_vcard_name)
               
        return render(request, "informer_vcard/vcard_add_copy_change.html", {
            "user": user,
            "vcard_main": vcard_main,
            "vcarf_name": vcarf_name,
            "media_dict": media_dict,
            "MEDIA_URL": settings.MEDIA_URL,
            "STATIC_URL": settings.STATIC_URL,
        })        

    
    
    