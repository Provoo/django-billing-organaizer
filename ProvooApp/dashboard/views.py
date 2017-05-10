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
    errors_documents = []
    objetoNu = {}
    p = {}
    try:
        objetoNu = readDocumentXML(document_object)
    except Exception as e:
        print("entro como error {}".format(e))
        errors_documents.append(str(document_object))
        documento_r = documento_error(
            user_documento_id=user_id, file_dcoumento=document_object)
        documento_r.save()
        return "se gurado un archivo con error"

    obj, created = Portafolio.objects.get_or_create(
        Ruc=objetoNu['RUC_XML'], UserID_id=user_id,
        Nombre=objetoNu['NOMBRE_DOCUMENTO'])
    print("portafolio primero obj %s" % (obj))
    print("portafolio primero created %s" % (created))

    try:
        documento_exist = documento.objects.filter(
            rucDocumento_id=user_id, numeroDeDocumento=objetoNu['NUMERO_DOCUMENTO'])
        print("portafolio despues dle si exsites %s" % (documento_exist))
    except documento.DoesNotExist:
        modelDocumentoSave(objetoNu, obj)
        print("Tu documento ya se guardo automaticamente")
        return "Tu documento ya se guardo automaticamente"
    else:
        print("El documento ya existe")

    # try:
    #
    #
    #
    # except Exception as e:
    #     print("entro como error {}".format(e))
    #     print("El ruc no exite, crearemos un nuevo portafolio para este Ruc")
        # ps = Portafolio(
        #     UserID_id=user_id, Ruc=objetoNu['RUC_XML'],
        #     Nombre=objetoNu['NOMBRE_DOCUMENTO'])
        # ps.save()
        # print("portafolio del segundo try %s" % (ps))
        # modelDocumentoSave(objetoNu, ps)
        # return "listo se guardo tu portafolio"

    # try:
    #     print("El ruc si existe")
    #     print("portafolio despues dle si exsites %s" % (p))
    #     documento_exist = documento.objects.get(
    #         rucDocumento_id=p, numeroDeDocumento=objetoNu['NUMERO_DOCUMENTO'])
    #     print("portafolio despues dle si exsites %s" % (documento_exist))
    # except documento.DoesNotExist:
    #     modelDocumentoSave(objetoNu, p)
    #     print("Tu documento ya se guardo automaticamente")
    #     return "Tu documento ya se guardo automaticamente"
    # else:
    #     print("Este documento ya existe, no necesitas duplicarlo")
    #     return "Este documento ya existe, no necesitas duplicarlo"


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
                    print(file_data)
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
        print(notifica)
        return notifica


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
        xml_handler(documento_it, request.user.id)
    print(usuario)
    print(documentos)
    print(prueba)
    print(ajax)
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
