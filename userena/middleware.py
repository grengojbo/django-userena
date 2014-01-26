# -*- mode: python; coding: utf-8; -*-
from django.utils import translation
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
from django.conf import settings
from userena import settings as userena_settings
from django.contrib.sites.models import Site
import logging

logger = logging.getLogger(__name__)


class UserenaLocaleMiddleware(object):
    """
    Set the language by looking at the language setting in the profile.

    It doesn't override the cookie that is set by Django so a user can still
    switch languages depending if the cookie is set.

    """

    def process_request(self, request):
        host = request.META["HTTP_HOST"]
        logger.debug("HTTP_HOST: %s", host)
        try:
            site = Site.objects.get(domain=host)
            #site = qsite.id
        except Site.DoesNotExist:
            logger.error('Site.DoesNotExist')
        site = Site.objects.get_current()
        #lang_cookie = request.session.get(settings.LANGUAGE_COOKIE_NAME)
        #if not lang_cookie:
        if request.user.is_authenticated():
            try:
                profile = request.user.get_profile()
            except (ObjectDoesNotExist, SiteProfileNotAvailable):
                profile = False

            if profile:
                try:
                    lang = getattr(profile, userena_settings.USERENA_LANGUAGE_FIELD)
                    translation.activate(lang)
                    logger.info("SET LANGUAGE: {0}".format(translation.get_language()))
                    request.LANGUAGE_CODE = translation.get_language()
                except AttributeError:
                    pass
        else:
            try:
                if userena_settings.USERENA_LANG.has_key(host):
                    lang = userena_settings.USERENA_LANG[host]
                else:
                    lang = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', 'uk')
                translation.activate(lang)
                logger.info("SET LANGUAGE: {0}, host: {1}, site: {2}".format(translation.get_language(), host, site.id))
                request.site = site
                request.LANGUAGE_CODE = translation.get_language()
            except AttributeError:
                pass


class CsrfFixMiddleware:
    def process_view(self, request, view_func, callback_args, callback_kwargs):
        request.META["CSRF_COOKIE_USED"] = True
        return None
