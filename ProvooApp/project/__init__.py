# -*- coding: utf-8 -*-

from .celery import app as celery_app

__about__ = """
In addition to what is provided by the "zero" project, this project
provides thorough integration with django-user-accounts, adding
comprehensive account management functionality. It is a foundation
suitable for most sites that have user accounts.
"""

default_app_config = "project.apps.AppConfig"

__all__ = ['celery_app']
