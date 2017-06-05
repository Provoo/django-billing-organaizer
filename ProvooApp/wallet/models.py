from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify


class wallet(models.Model):
    UserID = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    description = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    def slug(self):
        return slugify(self.Ruc)

    def get_absolute_url(self):
        return reverse("user_dashboard", (), kwargs={
            'pk': self.UserID,
            'slug': self.slug
        })

    def __str__(self):
        return '%s %s' % (self.UserID, self.name)
