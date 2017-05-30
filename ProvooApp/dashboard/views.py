import os
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
from dashboard.models import Portafolio, documento, documento_error
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum

#Xml Reader Api
from DocumentReader.xmlReader import readDocumentXML
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import re
import zipfile

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
    # user_document = Portafolio.objects.get(UserID=user_id)
    errors_documents = []
    objeto_xml_paser = {}
    try:
        objeto_xml_paser = readDocumentXML(document_object)
        print("documento parseado %s " % (objeto_xml_paser))
    except Exception as e:
        print("entro como error {}".format(e))
        errors_documents.append(str(document_object))
        documento_r = documento_error(
            user_documento_id=user_id, file_dcoumento=document_object)
        documento_r.save()
        return "se gurado un archivo con error"

    try:
        p = Portafolio.objects.get(Ruc=objeto_xml_paser['RUC_XML'], UserID_id=user_id)
    except Portafolio.DoesNotExist:
        print("El ruc no exite, crearemos un nuevo portafolio para este Ruc")
        p = Portafolio(
            UserID_id=user_id, Ruc=objeto_xml_paser['RUC_XML'],
            Nombre=objeto_xml_paser['NOMBRE_DOCUMENTO'])
        p.save()
        print(p)
        modelDocumentoSave(objeto_xml_paser, p)
    else:
        print("El ruc si existe")
        try:
            documento_exist = documento.objects.get(rucDocumento=p, numeroDeDocumento=objeto_xml_paser['NUMERO_DOCUMENTO'])
        except documento.DoesNotExist:
            modelDocumentoSave(objeto_xml_paser, p)
            print("Tu documento ya se guardo automaticamente")
        else:
            print("Este documento ya existe, no necesitas duplicarlo")


def xml_handler(document, user_id):
    if re.search(r"zip", str(document.name)):
        print("nombre documento en xml_handler %s" % (str(document.name)))
        try:
            unzip_file = zipfile.ZipFile(document, "r")
        except Exception as e:
            print('error: {}'.format(e))
        else:
            extrac_zip = unzip_file.filelist
            for ds in extrac_zip:
                if re.search(r"xml", str(ds.filename)):
                    file_data = unzip_file.read(ds.filename)
                    file_return = ContentFile(str(file_data), name=str(ds.filename))
                    saveDocumentPorfolio(file_return, user_id)
            unzip_file.close()
    else:
        saveDocumentPorfolio(document, user_id)


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
            rucDocumento=self.request.user.id) \
            .annotate(mes=ExtractMonth('fecha'), anio=ExtractYear('fecha')) \
            .values('mes', 'anio').annotate(
            gastos_sin_impuestos=Sum('totalGastosf')) \
            .values('mes', 'anio', 'gastos_sin_impuestos')
        print(member)
        context['member'] = member
        return context


class portafolioView(ListView):
    template_name = 'portafolios.html'
    model = Portafolio

    def get_queryset(self):
        portafolio_User = super(portafolioView, self).get_queryset()
        print(portafolio_User)
        return portafolio_User.filter(UserID_id=self.request.user.id)


class documentoView(ListView):
    model = documento
    template_name = 'documents.html'

    def get_queryset(self):
        documentos = super(documentoView, self).get_queryset()
        porta = get_object_or_404(
            Portafolio, UserID_id=self.request.user.id, Ruc=self.kwargs['ruc'])
        print(porta)
        return documentos.filter(rucDocumento=porta)


class notificationsView(ListView):
    model = User
    template_name = 'notifications.html'

    def get_queryset(self):
        notifica = super(
            notificationsView, self).get_queryset().get(
            pk=self.request.user.id).notifications.unread()
        print("noticaciones son: %s" % (notifica))
        return notifica


@login_required
@require_http_methods(["POST"])
def upLoad(request, *args, **kwargs):
    # ajax = request.is_ajax()
    prueba = request.POST
    usuario = request.user.id
    documentos = request.FILES.getlist('docfile')
    print("los documentos del upload %s" % (documentos))
    print("es usuario es  %s" % (usuario))
    for documento_it in documentos:
        xml_handler(documento_it, request.user.id)
    mensaje = "Tu factura se guardo se ha guardado exitosamente"
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
    # Aqui hacer con GetAttachments un buffer para escribir el archivo
    listemails = ListMessagesMatchingQuery(
        services, request.user, "factura has:attachment xml ")
    for nlist in listemails:
        print('numero de id: %s' % (nlist['id']))
        f_buffer = GetAttachments(services, request.user, nlist['id'])
        if f_buffer:
            xml_handler(f_buffer, request.user.id)
        f_buffer = None
    return HttpResponseRedirect(
            reverse('portafolios', kwargs={'pk': request.user.id}))
