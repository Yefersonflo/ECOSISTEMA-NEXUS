"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import copy

# Patch Python 3.14 incompatibility with Django Template Context __copy__
try:
    from django.template import context
    def _safe_context_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        if hasattr(self, '__dict__'):
            duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = [d.copy() for d in getattr(self, 'dicts', [])]
        if hasattr(self, 'render_context'):
            duplicate.render_context = copy.copy(self.render_context)
        return duplicate

    context.BaseContext.__copy__ = _safe_context_copy
    context.Context.__copy__ = _safe_context_copy
    context.RequestContext.__copy__ = _safe_context_copy
except Exception:
    pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
