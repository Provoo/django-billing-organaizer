from .base import *

#Important to be down in production
DEBUG = TEMPLATE_DEBUG = True

MANAGERS = (
    ('Errors', 'errors@provoo.com'),
)
