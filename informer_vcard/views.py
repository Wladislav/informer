from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.core import serializers
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
import json, uuid, datetime
from django.core.serializers.json import DjangoJSONEncoder

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
def vcard(request, template_name='informer_vcard/vcard_index.html',):
    context = {}
    if request.method == 'GET':
        if request.is_ajax():
            what_get = request.get_full_path()
            if what_get.find('vcard-list.json')>0:
                user = request.user
                dict_vcards = get_vcards_dict_format(user.id)
                json_vcards = json.dumps(dict_vcards, default=default)
                with open("static/file.json", "w") as out:
                    out.write(json_vcards)
                return HttpResponse(json_vcards)
            
    return TemplateResponse(request, template_name, context)
