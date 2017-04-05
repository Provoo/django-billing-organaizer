# from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User
from dashboard.models import Portafolio, documento, CredentialsModel
from dashboard.xmlReader import readDocumentXML

#google api imports
import logging
from oauth2client import tools
import pickle
import base64
import httplib2
from oauth2client import tools
from googleapiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render


# funcion para combrar la existencia de un portafolio o crear uno nuevo guardar
def modelDocumentoSave(document_object, portafolio_instance):
    p = documento(
        rucDocumento=portafolio_instance,
        numeroDeDocumento=document_object['NUMERO_DOCUMENTO'],
        RucEmisor=document_object['RUC_EMISOR'],
        NombreEmisor=document_object['NOMBRE_EMISOR'],
        DireccionEmisor=document_object['DIRECCION_EMISOR'],
        fecha=document_object['FECHA'],
        totalGastosf=document_object['TOTAL_GASTOS'],
        totalImpuestos=document_object['TOTAL_IMPUESTOS'],
        totalDocumento=document_object['TOTAL_DOCUMENTO'],
        deducible_vestimenta=document_object['DEDUCIBLE_VESTIMENTA'],
        deducible_educacion=document_object['DEDUCIBLE_EDUCACION'],
        deducible_comida=document_object['DEDUCIBLE_COMIDA'],
        deducible_salud=document_object['DEDUCIBLE_SALUD'],
        no_deducible=document_object['NO_DEDUCIBLE'],
        archivo=document_object['ARCHIVO'])
    p.save()


def saveDocumentPorfolio(document_object, user_id, portafolio_instance):
    try:
        p = Portafolio.objects.get(Ruc=document_object['RUC_XML'])
    except Portafolio.DoesNotExist:
        print("El ruc no exite, crearemos un nuevo portafolio para este Ruc")
        p = Portafolio(UserID=user_id, Ruc=document_object['RUC_XML'], Nombre=document_object['NOMBRE'])
        p.save()
        modelDocumentoSave(document_object, p)
    else:
        print("El ruc si existe")
        try:
            prueba_num_doc = documento.objects \
                                 .filter(numeroDeDocumento=document_object['NUMERO_DOCUMENTO'])[:1].get()
        except documento.DoesNotExist:
            modelDocumentoSave(document_object, portafolio_instance)
            print("Tu documento ya se guardo automaticamente")
        else:
            print("Tu factura ya existe")


class homeView(TemplateView):
    template_name = "homepage.html"


class dashboardView(ListView):
    context_object_name = 'portafolio'
    template_name = 'dashboard.html'
    pk_url_kwarg = 'pk'
    queryset = Portafolio.objects.all()

    # Se define el query para buscar el Portafolio que le corresponde al usuario

    def get_queryset(self):
        portafolio_user = super(dashboardView, self).get_queryset()
        return portafolio_user.filter(Ruc=self.kwargs['ruc'])[:1].get()

    def get_context_data(self, **kwargs):
        context = super(dashboardView, self).get_context_data(**kwargs)
        member = documento.objects.select_related('rucDocumento').filter(
            rucDocumento=self.kwargs['ruc']) \
            .annotate(mes=ExtractMonth('fecha'), anio=ExtractYear('fecha')) \
            .values('mes', 'anio').annotate(
            gastos_sin_impuestos=Sum('totalGastosf')) \
            .values('mes', 'anio', 'gastos_sin_impuestos')
        print(member)
        context['member'] = member
        return context

    def post(self, request, *args, **kwargs):
        portafolio_User = Portafolio.objects.get(
            UserID_id=self.request.user.id, Ruc=self.kwargs['ruc'])
        prueba = self.request.POST
        documentos = self.request.FILES.getlist('docfile')
        ajax = request.is_ajax()
        print(documentos)
        for documento_it in documentos:
            objetoNu = readDocumentXML(documento_it)
            print(objetoNu)
            saveDocumentPorfolio(objetoNu, self.request.user, portafolio_User)
        print(prueba)
        print(ajax)
        return HttpResponseRedirect(
            reverse('user_dashboard', kwargs={'pk': self.request.user, 'ruc': self.kwargs['ruc']}))


class portafolioView(ListView):
    template_name = 'portfolios.html'
    model = Portafolio

    def get_queryset(self):
        portafolio_User = super(portafolioView, self).get_queryset()
        print(portafolio_User)
        return portafolio_User.filter(UserID_id=self.request.user.id)


class documentoView(ListView):
    model = documento
    template_name = 'documento.html'

    def get_queryset(self):
        documentos = super(documentoView, self).get_queryset()
        get_object_or_404(Portafolio, UserID_id=self.request.user.id, Ruc=self.kwargs['ruc'])
        return documentos.filter(rucDocumento=self.kwargs['ruc'])


def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


@login_required
def googleImport(request):
    user = User.objects.get(username=request.user)
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']
    credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
    http = httplib2.Http()
    http = credentials.authorize(http)
    services = build("gmail", "v1", http=http)
    print(services)
    listemails = ListMessagesMatchingQuery(services, request.user, "factura has:attachment xml ")
    for nlist in listemails:
        print('numero de id: %s' % (nlist['id']))
    # activities = services.activities()
    # activitylist = activities.list(collection='public',
    #                                userId='me').execute()
    # print(activitylist)

    # credentials = flow_from_clientsecrets(settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON, settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE)
    # storage = Storage(CredentialsModel, 'id', request.user.id, 'credential')
    # credentials = storage.get()
    # storage.put(credentials)
    # credentials = tools.run_flow(credentials, storage)
    # print("Imprimiendo Credenciales en import %s" % (credentials))
    # print("Imprimiendo Cren2 en import %s" % (storage))
    #
    # if not credentials:
    #     credentials = flow_from_clientsecrets(settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON, settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE)
    #     storage = Storage(CredentialsModel, 'id', request.user.id, 'credential')
    #     storage.put(credentials)
    #     return HttpResponseRedirect(reverse('googleImport'))
    # else:
    #     print("entra!")
    #     http = httplib2.Http()
    #     http = credentials.authorize(http)
    #     print("Imprimiendo Credenciales en http %s" % (http))
    #
    #     service = build("gmail", "v1", http=http)
    #     activities = service.activities()
    #     activitylist = activities.list(collection='public',
    #                                    userId='me').execute()
    #     print(activitylist)
    return HttpResponseRedirect(
            reverse('portafolios', kwargs={'pk': request.user.id}))
