#!/usr/bin/env python
from django.conf.settings import INSTALLED_APPS
from django.utils.importlib import import_module
import os

app_names = (x for x in INSTALLED_APPS if not x.startswith('django'))
print(app_names)
app_paths = (os.path.dirname(os.path.abspath(import_module(x).__file__)) for x in app_names)
print("\n".join(x for x in app_paths if not x.startswith(os.getcwd())))
