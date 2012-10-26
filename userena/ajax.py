# -*- mode: python; coding: utf-8; -*-
#import simplejson
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from userena.forms import SignupForm, SignupFormOnlyEmail, AuthenticationForm, ChangeEmailForm, EditProfileForm
from userena.utils import signin_redirect, get_profile_model
from userena import signals as userena_signals
from django.core.urlresolvers import reverse
from userena import settings as userena_settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from userena.decorators import secure_required
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
#@secure_required
#@csrf_exempt

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class ErrorList(list):
    """
    A collection of errors that knows how to display itself in various formats.
    """
    def __unicode__(self):
        return self.as_ul()

    def as_ul(self):
        if not self: return u''

#@dajaxice_register(method='GET')
#@ensure_csrf_cookie
@dajaxice_register(method='POST', name='sigup_form')
def signup_form(request, form, success_url=None):
    logger.debug("signup_form")
    dajax = Dajax()
    signup_form = SignupForm
    if userena_settings.USERENA_WITHOUT_USERNAMES:
        signup_form = SignupFormOnlyEmail

    form = signup_form(deserialize_form(form))

    if form.is_valid():
        user = form.save()

        # Send the signup complete signal
        userena_signals.signup_complete.send(sender=None,
            user=user)

        if success_url: redirect_to = success_url
        else: redirect_to = reverse('userena_signup_complete',
            kwargs={'username': user.username})

        # A new signed user should logout the old one.
        if request.user.is_authenticated():
            logout(request)
        dajax.remove_css_class('#sigup_form div', 'error')
        dajax.clear('#sigup_form .help-inline', 'innerHTML')
        dajax.redirect(redirect_to, delay=10)
        #dajax.alert("Form is_valid(), your username is: %s" % form.cleaned_data.get('username'))
    else:
        dajax.remove_css_class('#sigup_form div', 'error')
        dajax.clear('#sigup_form .help-inline', 'innerHTML')
        dajax.clear('#sigup_form .alert-error', 'innerHTML')
        dajax.add_css_class('#sigup_form div.alert-error', 'hide')
        try:
            if form.errors['__all__'] is not None:
                dajax.remove_css_class('#sigup_form div.alert-error', 'hide')
                logger.debug(">>>>>>>>>>>> %s" % form.errors['__all__'])
                dajax.assign('#sigup_form .alert-error', 'innerHTML',
                "<button type='button' class='close' data-dismiss='alert'>×</button>{0}".format(form.errors['__all__']))
        except Exception, e:
            pass
        for error in form.errors:
            dajax.add_css_class('#sigup_form #gr_id_%s' % error, 'error')
            #dajax.remove_css_class('#sigup_form #e_id_%s' % error, 'hide')
            dajax.assign('#sigup_form #e_id_%s' % error, 'innerHTML', form.errors[error][0])

    return HttpResponse(dajax.json(), mimetype="application/json")


@dajaxice_register(method='POST', name='signin_form')
def signin_form_test(request, form, success_url=None):
    logger.debug("signin_form")
    dajax = Dajax()
    form = AuthenticationForm(deserialize_form(form))
    if form.is_valid():
        identification, password, remember_me = (form.cleaned_data['identification'],
                                                 form.cleaned_data['password'],
                                                 form.cleaned_data['remember_me'])
        user = authenticate(identification=identification, password=password)
        if user.is_active:
            login(request, user)
            if remember_me:
                request.session.set_expiry(userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
            else: request.session.set_expiry(0)

            # TODO: добавить сообщения
            if userena_settings.USERENA_USE_MESSAGES:
                messages.success(request, _('You have been signed in.'), fail_silently=True)

            # TODO: изменить переадресацию после регистрации
            redirect_to = signin_redirect(REDIRECT_FIELD_NAME, user)
        else:
            redirect_to = reverse('userena_disabled', kwargs={'username': user.username})

        dajax.remove_css_class('#signin_form div', 'error')
        dajax.clear('#signin_form .help-inline', 'innerHTML')
        dajax.redirect(redirect_to, delay=10)
    else:
        dajax.remove_css_class('#signin_form div', 'error')
        dajax.clear('#signin_form .help-inline', 'innerHTML')
        dajax.add_css_class('#signin_form div.alert-error', 'hide')
        try:
            if form.errors['__all__'] is not None:
                dajax.remove_css_class('#signin_form div.alert-error', 'hide')
                dajax.assign('#signin_form .alert-error', 'innerHTML',
                "<button type='button' class='close' data-dismiss='alert'>×</button>{0}".format(form.errors['__all__']))
        except Exception, e:
            pass
        for error in form.errors:
            dajax.add_css_class('#signin_form #gr_id_%s' % error, 'error')
            #dajax.remove_css_class('#signin_form #e_id_%s' % error, 'hide')
            dajax.assign('#signin_form #e_id_%s' % error, 'innerHTML', form.errors[error][0])

    return HttpResponse(dajax.json(), mimetype="application/json")

