# Views Important libraries
from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# Models Import
from dashboard.models import Portafolio, documento, CredentialsModel
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum

#Xml Reader Api
from DocumentReader.xmlReader import readDocumentXML

# google api imports
from oauth2client.client import AccessTokenCredentials
from googleapiclient.discovery import build
import httplib2
from dashboard.GoogleApi import ListMessagesMatchingQuery, GetAttachments


# funcion para combrar la existencia de un portafolio o crear uno nuevo guardar
def modelDocumentoSave(document_object, portafolio_instance):
    p = documento(
        rucDocumento=portafolio_instance,
        nombreDocumento=document_object['NOMBRE_DOCUMENTO'],
        numeroDeDocumento=document_object['NUMERO_DOCUMENTO'],
        RucEmisor=document_object['RUC_EMISOR'],
        NombreEmisor=document_object['NOMBRE_EMISOR'],
        DireccionEmisor=document_object['DIRECCION_EMISOR'],
        fecha=document_object['FECHA'],
        Impuesto=document_object['TAX'],
        totalGastosf=document_object['TOTAL_GASTOSF'],
        totalImpuestos=document_object['TOTAL_IMPUESTOS'],
        totalDocumento=document_object['TOTAL_DOCUMENTO'],
        deducible_vestimenta=document_object['DEDUCIBLE_VESTIMENTA'],
        deducible_educacion=document_object['DEDUCIBLE_EDUCACION'],
        deducible_comida=document_object['DEDUCIBLE_COMIDA'],
        deducible_salud=document_object['DEDUCIBLE_SALUD'],
        deducible_vivienda=document_object['DEDUCIBLE_VIVIENDA'],
        no_deducible=document_object['NO_DEDUCIBLE'],
        archivo=document_object['ARCHIVO'])
    p.save()


def saveDocumentPorfolio(document_object, user_id):
    try:
        p = Portafolio.objects.get(Ruc=document_object['RUC_XML'])
    except Portafolio.DoesNotExist:
        print("El ruc no exite, crearemos un nuevo portafolio para este Ruc")
        p = Portafolio(
            UserID=user_id, Ruc=document_object['RUC_XML'],
            Nombre=document_object['NOMBRE_DOCUMENTO'])
        p.save()
        ps = Portafolio.objects.get(Ruc=document_object['RUC_XML'])
        print(p)
        modelDocumentoSave(document_object, ps)
    else:
        print("El ruc si existe")
        modelDocumentoSave(document_object, p)
        print("Tu documento ya se guardo automaticamente")
        # try:
        #     prueba_num_doc = documento.objects.filter(
        #             numeroDeDocumento=document_object['NUMERO_DOCUMENTO']
        #             )[:1].get()
        # except documento.DoesNotExist:

        # else:
        #     print("Tu factura ya existe")


class homeView(TemplateView):
    template_name = "homepage.html"


class dashboardView(ListView):
    context_object_name = 'portafolio'
    template_name = 'dashboard.html'
    pk_url_kwarg = 'pk'
    queryset = Portafolio.objects.all()

    # Query para buscar el Portafolio que le corresponde al usuario
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
        get_object_or_404(
            Portafolio, UserID_id=self.request.user.id, Ruc=self.kwargs['ruc'])
        return documentos.filter(rucDocumento=self.kwargs['ruc'])


@login_required
@require_http_methods(["POST"])
def upLoad(request, *args, **kwargs):
    # portafolio_User = Portafolio.objects.get(
    #     UserID_id=self.request.user.id, Ruc=self.kwargs['ruc'])
    prueba = request.POST
    usuario = request.user.id
    documentos = request.FILES.getlist('docfile')
    ajax = request.is_ajax()
    print(documentos)
    for documento_it in documentos:
        objetoNu = readDocumentXML(documento_it)
        print(objetoNu)
        saveDocumentPorfolio(objetoNu, request.user)
    print(usuario)
    print(documentos)
    print(prueba)
    print(ajax)
    mensaje = "Tu factura se guardo en el siguiente usuario: %s"\
        % (usuario)
    data = {
        'mensaje': mensaje}
    return JsonResponse(data)


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
    listemails = ListMessagesMatchingQuery(
        services, request.user, "factura has:attachment xml ")
    for nlist in listemails:
        print('numero de id: %s' % (nlist['id']))
        f_buffer = GetAttachments(services, request.user, nlist['id'])
        if f_buffer:
            print("El buffer antes guardar es: %s" % (f_buffer['name']))
        else:
            print("este archivo esta vacio")
        f_buffer = None
        # Aqui hacer con GetAttachments un buffer para escribir el archivo

    return HttpResponseRedirect(
            reverse('portafolios', kwargs={'pk': request.user.id}))



# def upLoad(self, request, *args, **kwargs):
#     portafolio_User = Portafolio.objects.get(
#         UserID_id=self.request.user.id, Ruc=self.kwargs['ruc'])
#     prueba = self.request.POST
#     documentos = self.request.FILES.getlist('docfile')
#     ajax = request.is_ajax()
#     print(documentos)
#     for documento_it in documentos:
#         objetoNu = readDocumentXML(documento_it)
#         print(objetoNu)
#         saveDocumentPorfolio(objetoNu, self.request.user, portafolio_User)
#     print(prueba)
#     print(ajax)
#     mensaje = "Tu factura se guardo en el siguiente portafolio: %s"\
#         % (self.kwargs['ruc'])
#     data = {
#         'mensaje': mensaje}
#     return JsonResponse(data)
