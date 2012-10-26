#import simplejson
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from userena.forms import SignupForm, SignupFormOnlyEmail, AuthenticationForm, ChangeEmailForm, EditProfileForm
from userena.utils import signin_redirect, get_profile_model
from userena import signals as userena_signals
from django.core.urlresolvers import reverse
from userena import settings as userena_settings
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from userena.decorators import secure_required
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
#@secure_required
#@csrf_exempt

#@dajaxice_register(method='GET')
#@ensure_csrf_cookie
@dajaxice_register(method='POST', name='sigup_form')
def sigup_form_test(request, form, success_url=None):
    dajax = Dajax()
    #dajax.alert("Hello World!")
    #dajax.add_css_class('div .alert', 'red')
    #return render_to_response('json.html', {'json': dajax.json()}, mimetype="application/json", context_instance = RequestContext(request))
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
        for error in form.errors:
            dajax.add_css_class('#sigup_form #gr_id_%s' % error, 'error')
            #dajax.remove_css_class('#sigup_form #e_id_%s' % error, 'hide')
            dajax.assign('#sigup_form #e_id_%s' % error, 'innerHTML', form.errors[error][0])

    return HttpResponse(dajax.json(), mimetype="application/json")

@dajaxice_register(method='POST', name='signin_form')
def signin_form_test(request, form, success_url=None):
    dajax = Dajax()
    return HttpResponse(dajax.json(), mimetype="application/json")

