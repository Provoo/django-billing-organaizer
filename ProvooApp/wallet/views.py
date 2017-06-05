# Views Important libraries
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Models Import
from .models import wallet



class walletsView(ListView):
    template_name = 'wallets.html'
    model = wallet

    def get_queryset(self):
        wallet_User = super(walletsView, self).get_queryset()
        print(wallet_User)
        return wallet_User.filter(UserID_id=self.request.user.id)
