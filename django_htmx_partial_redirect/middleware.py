"""
Handle redirects for partial HTMX views in Django.

This middleware redirects direct accesses to partial views (e.g., HTMX modal content)
to a full page, passing the original URL as a 'partial_url' parameter.

Usage:
1. Add to MIDDLEWARE in settings.py
2. Set HTMX_PARTIAL_VIEWS = ['view1', 'view2']
3. Set HTMX_PARTIAL_VIEWS_REDIRECT_URL = '/'

Example:
    MIDDLEWARE = [
        'path.to.PartialViewRedirectMiddleware',
    ]
    HTMX_PARTIAL_VIEWS = ['login', 'signup']
    HTMX_PARTIAL_VIEWS_REDIRECT_URL = '/home/'

In your view or template:
    {% if request.GET.partial_url %}
        <div hx-get="{{ request.GET.partial_url }}"
             hx-target="body"
             hx-swap="beforeend"
             hx-trigger="load">
        </div>
    {% endif %}
"""

import logging
from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import Resolver404
from django.urls import resolve
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class HTMXPartialViewRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._check_configuration()

    def _check_configuration(self):
        if not hasattr(settings, 'HTMX_PARTIAL_VIEWS'):
            msg = "Set HTMX_PARTIAL_VIEWS in settings.py (e.g., ['login', 'signup'])"
            raise ImproperlyConfigured(msg)
        if not hasattr(settings, 'HTMX_PARTIAL_VIEWS_REDIRECT_URL'):
            msg = "Set HTMX_PARTIAL_VIEWS_REDIRECT_URL in settings.py (e.g., '/')"
            raise ImproperlyConfigured(msg)

    @cached_property
    def partial_views(self):
        return set(settings.HTMX_PARTIAL_VIEWS)

    @cached_property
    def redirect_url(self):
        return settings.HTMX_PARTIAL_VIEWS_REDIRECT_URL

    def __call__(self, request):
        if not request.headers.get('HX-Request'):
            try:
                resolved = resolve(request.path_info)
                if resolved.url_name in self.partial_views:
                    params = urlencode({'partial_url': request.path})
                    redirect_url = f'{self.redirect_url}?{params}'
                    logger.info(f'Redirecting partial view: {request.path} to {redirect_url}')
                    return redirect(redirect_url)
            except Resolver404:
                logger.warning(f'Unable to resolve path: {request.path_info}')

        return self.get_response(request)
