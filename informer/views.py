from django import forms
from .forms import RegistrationFormTOSAndEmail
from .forms import (DjangoProfileForm, UserProfileForm)
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout 
from django.contrib.auth.views import login
from registration.backends.model_activation.views import RegistrationView
from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.forms.models import inlineformset_factory
from django.forms import modelform_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import (REDIRECT_FIELD_NAME, get_user_model, login as auth_login,logout as auth_logout, update_session_auth_hash)
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm)
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url
from django.core.exceptions import ObjectDoesNotExist

def login_handler(sender, request, **kwargs):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(pk=user.id)
    except (ObjectDoesNotExist, UserProfile.DoesNotExist):
        pass
    return 
user_logged_in.connect(login_handler)

@csrf_protect
@never_cache
def login_user(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
            try:
                user_profile = UserProfile.objects.get(pk=user.id)
                LOGIN_REDIRECT_URL = "/%s" % user_profile.language
                request.session[LANGUAGE_SESSION_KEY] = user_profile.language                
            except (ObjectDoesNotExist, UserProfile.DoesNotExist):
                LOGIN_REDIRECT_URL = '/accounts/profile'
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(LOGIN_REDIRECT_URL)
            # Okay, security check complete. Log the user in.
            auth_login(request, user)

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

def logout_user(request):
    logout(request)
    #return render(request, 'registration/logout.html', {})
    prefix = lang_context_processor(request)
    return redirect('/'+prefix['LANG'], {})

def index(request):
    return render(request, 'informer/index.html', {})

class newRegistratonView(RegistrationView):
    form_class = RegistrationFormTOSAndEmail

def lang_context_processor(request):
    return {'LANG': request.LANGUAGE_CODE}

@login_required
def user_profile(request):
    user = User.objects.get_by_natural_key(request.user.username)
    user_form = UserProfileForm(instance=user)
    DjangoProfileInlineFormset = modelform_factory(User, DjangoProfileForm, fields=('first_name', 'last_name', 'email'))
    formusr_main = DjangoProfileInlineFormset(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, can_delete=False,
                                                 fields=('user', 'photo', 'website', 'bio', 'phone', 'city', 'country', 'language'),)
                                                 #widgets = {'language':forms.Select(choices=settings.LANGUAGES)})
    formset_adds = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            formusr_main = DjangoProfileInlineFormset(request.POST, instance=user)
            formset_adds = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            fsv = formset_adds.is_valid()
            fuv = formusr_main.is_valid()
            if fsv:
                formset_adds.save()
            if fuv: 
                formusr_main.save()
            if fsv and fuv:
                messages.success(request, _('Профиль успешно обновлен.')) #Profile details updated.
            return HttpResponseRedirect('/accounts/profile/')

        return render(request, "informer/userprofile.html", {
            "user": {'first_name':user.first_name,
                     'last_name':user.last_name,
                     'email':user.email,
                     'is_authenticated': user.is_authenticated,
                     'username':user.username,
                     'id':user.id,
                     'is_superuser':user.is_superuser},
            "formusr_main": formusr_main,
            "formset_adds": formset_adds,
            "MEDIA_URL": settings.MEDIA_URL,
            "STATIC_URL": settings.STATIC_URL,
        })
    else:
        raise PermissionDenied