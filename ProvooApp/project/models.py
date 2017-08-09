from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    phone = models.CharField(max_length=30, blank=False)
    UserIDu = models.CharField(max_length=30, blank=False, verbose_name=_('Unique ID'))

    class Meta:
        verbose_name = _('User Profile')
