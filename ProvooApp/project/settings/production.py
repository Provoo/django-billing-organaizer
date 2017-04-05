from .base import *

#Important to be down in production
DEBUG = TEMPLATE_DEBUG = False

MANAGERS = (
    ('Errors', 'errors@provoo.com'),
)
