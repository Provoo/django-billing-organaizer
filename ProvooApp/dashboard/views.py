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
import json
from django.core.serializers.json import DjangoJSONEncoder

# Models Import
from dashboard.models import Portafolio, documento, documento_error
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Func
from datetime import datetime


#Xml Reader Api
from DocumentReader.xmlReader import readDocumentXML
from django.core.files.base import ContentFile
import re
import zipfile

# google api imports
from oauth2client.client import AccessTokenCredentials
from googleapiclient.discovery import build
import httplib2
from dashboard.GoogleApi import ListMessagesMatchingQuery, GetAttachments

#forms

from .forms import uploadManualForm, registerExpensesForm


# funcion para combrar la existencia de un portafolio o crear uno nuevo guardar
def modelDocumentoSave(document_object, portafolio_instance, tags):
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
        tags=tags,
        archivo=document_object['ARCHIVO'])
    p.save()


def saveDocumentPorfolio(document_object, user_id):
    # user_document = Portafolio.objects.get(UserID=user_id)
    errors_documents = []
    objeto_xml_paser = {}
    tags=[]
    try:
        objeto_xml_paser = readDocumentXML(document_object)
        print("documento parseado %s " % (objeto_xml_paser))
    except Exception as e:
        print("entro como error {}".format(e))
        errors_documents.append(str(document_object))
        documento_r = documento_error(
            user_documento_id=user_id, file_dcoumento=document_object)
        documento_r.save()
        return ("El documento , se ha guardado con error te comunicaremos por email cuando este listo")
    try:
        p = Portafolio.objects.get(Ruc=objeto_xml_paser['RUC_XML'], UserID_id=user_id)
    except Portafolio.DoesNotExist:
        p = Portafolio(
            UserID_id=user_id, Ruc=objeto_xml_paser['RUC_XML'],
            Nombre=objeto_xml_paser['NOMBRE_DOCUMENTO'])
        p.save()
        print(p)
        modelDocumentoSave(objeto_xml_paser, p, tags)
        return("No existe el ruc del documento %s, crearemos un nuevo portafolio para este Ruc %s" % (objeto_xml_paser['NUMERO_DOCUMENTO'], objeto_xml_paser['RUC_XML']))
    else:
        print("El ruc si existe")
        try:
            documento_exist = documento.objects.get(rucDocumento=p, numeroDeDocumento=objeto_xml_paser['NUMERO_DOCUMENTO'])
        except documento.DoesNotExist:
            modelDocumentoSave(objeto_xml_paser, p, tags)
            return("Tu %s ya se guardo automaticamente en el portafolio %s" % (objeto_xml_paser['NUMERO_DOCUMENTO'], objeto_xml_paser['RUC_XML']))
        else:
            return("Este %s ya existe, no necesitas duplicarlo" % (objeto_xml_paser['NUMERO_DOCUMENTO']))


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
                    return saveDocumentPorfolio(file_return, user_id)
            unzip_file.close()
    else:
        return saveDocumentPorfolio(document, user_id)


class homeView(TemplateView):
    template_name = "dashboard/homepage.html"


class portfoliosView(ListView):
    template_name = 'dashboard/portfolios.html'
    model = Portafolio

    def get_queryset(self):
        portafolio_User = super(portfoliosView, self).get_queryset()
        print(portafolio_User)
        return portafolio_User.filter(UserID_id=self.request.user.id)


class dashboardView(ListView):
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'portafolio'
    queryset = Portafolio.objects.all()

    # Query para buscar el Portafolio que le corresponde al usuario
    def get_queryset(self):
        portafolio_user = super(dashboardView, self).get_queryset()
        return Portafolio.objects.get(Ruc=self.kwargs['ruc'], UserID_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        port = Portafolio.objects.get(UserID=self.request.user.id, Ruc=self.kwargs["ruc"])
        print(port)
        context = super(dashboardView, self).get_context_data(**kwargs)
        query = documento.objects.select_related('rucDocumento').filter(
                rucDocumento=port)\
            .annotate(mes=ExtractMonth('fecha'), anio=ExtractYear('fecha')) \
            .values('mes', 'anio').annotate(
            gastos_sin_impuestos=Sum('totalGastosf')) \
            .values('mes', 'anio', 'gastos_sin_impuestos')

        query_expenses = documento.objects.select_related('rucDocumento').filter(
                rucDocumento=port).annotate(codes_len=Func(F('tags'), function='unnest')).values('codes_len').annotate(sum=Sum('totalGastosf'))
        print(" la lista de query expense %s =" % query_expenses)
        monthly_expenses = json.dumps(list(query), cls=DjangoJSONEncoder)
        print(" la lista de query monthly expenses %s =" % monthly_expenses)

        context['monthly_expenses'] = monthly_expenses
        context['query_expenses'] = query_expenses

        return context


class documentoView(ListView):
    model = documento
    template_name = 'dashboard/documents.html'

    def get_queryset(self):
        documentos = super(documentoView, self).get_queryset()
        porta = get_object_or_404(
            Portafolio, UserID_id=self.request.user.id, Ruc=self.kwargs['ruc'])
        print(porta)
        return documentos.filter(rucDocumento=porta)


class notificationsView(ListView):
    model = User
    template_name = 'dashboard/notifications.html'

    def get_queryset(self):
        notifica = super(
            notificationsView, self).get_queryset().get(
            pk=self.request.user.id).notifications.unread()
        print("noticaciones son: %s" % (notifica))
        return notifica


@login_required
@require_http_methods(["POST"])
def upLoad(request, *args, **kwargs):
    list_message = []
    documentos = request.FILES.getlist('docfile')
    for documento_it in documentos:
        list_message.append(xml_handler(documento_it, request.user.id))
    print(list_message)
    mensaje = ', '.join(list_message)

    print(mensaje)
    data = {
        'mensaje': mensaje}
    return JsonResponse(data)


@login_required
def upLoadManual(request, *args, **kwargs):
    document_object = {}
    form = uploadManualForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            document_object['NOMBRE_EMISOR'] = form.cleaned_data['numeroDeDocumento']
            document_object['RUC_EMISOR'] = form.cleaned_data['RucEmisor']
            document_object['NOMBRE_DOCUMENTO'] = form.cleaned_data['nombreDocumento']
            document_object['RUC_XML'] = form.cleaned_data['rucDocumento']
            document_object['NUMERO_DOCUMENTO'] = form.cleaned_data['numeroDeDocumento']
            document_object['DIRECCION_EMISOR'] = ""
            document_object['FECHA'] = datetime.strptime(
                            form.cleaned_data['fecha'], "%d/%m/%Y")
            document_object['TAX'] = form.cleaned_data['Impuesto']
            document_object['TOTAL_GASTOSF'] = form.cleaned_data['totalGastosf']
            document_object['TOTAL_IMPUESTOS'] = form.cleaned_data['totalImpuestos']
            document_object['TOTAL_DOCUMENTO'] = form.cleaned_data['totalDocumento']
            document_object['DEDUCIBLE_COMIDA'] = form.cleaned_data['deducible_comida']
            document_object['DEDUCIBLE_SALUD'] = form.cleaned_data['deducible_salud']
            document_object['DEDUCIBLE_VESTIMENTA'] = form.cleaned_data['deducible_vestimenta']
            document_object['DEDUCIBLE_EDUCACION'] = form.cleaned_data['deducible_educacion']
            document_object['DEDUCIBLE_VIVIENDA'] = form.cleaned_data['deducible_vivienda']
            document_object['NO_DEDUCIBLE'] = form.cleaned_data['no_deducible']
            document_object['TAGS'] = form.cleaned_data['tags'].split(",")
            document_object['TAGS'].append('Factura Manual')
            document_object['ARCHIVO'] = None

            try:
                p = Portafolio.objects.get(Ruc=document_object['RUC_XML'], UserID_id=request.user.id)
            except Portafolio.DoesNotExist:
                p = Portafolio(
                    UserID_id=request.user.id, Ruc=document_object['RUC_XML'],
                    Nombre=document_object['NOMBRE_DOCUMENTO'])
                p.save()
                print(p)
                modelDocumentoSave(document_object, p, document_object['TAGS'])
                # return("No existe el ruc del documento %s, crearemos un nuevo portafolio para este Ruc %s" % (objeto_xml_paser['NUMERO_DOCUMENTO'], objeto_xml_paser['RUC_XML']))
            else:
                print("El ruc si existe")
                try:
                    documento_exist = documento.objects.get(rucDocumento=p, numeroDeDocumento=document_object['NUMERO_DOCUMENTO'])
                except documento.DoesNotExist:
                    modelDocumentoSave(document_object, p, document_object['TAGS'])
                    # return("Tu %s ya se guardo automaticamente en el portafolio %s" % (objeto_xml_paser['NUMERO_DOCUMENTO'], objeto_xml_paser['RUC_XML']))
                else:
                     print("Este %s ya existe, no necesitas duplicarlo" % (document_object['NUMERO_DOCUMENTO']))
            print("esta es la variable post %s" % document_object)
            return HttpResponseRedirect(reverse('user_portfolios'))
    return render(request, 'dashboard/uploadmanual.html', {'form': form})


@login_required
def registerExpenses(request, *args, **kwargs):
    portafolio = Portafolio.objects.get(UserID=request.user.id, Ruc=kwargs["ruc"])
    query = documento.objects.select_related('rucDocumento').filter(
            rucDocumento=portafolio).values('NombreEmisor').annotate(count=Count('NombreEmisor')).order_by()
    form = registerExpensesForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            a = form.cleaned_data['tags']
            uPdocumento = documento.objects.select_related().filter(rucDocumento=portafolio, NombreEmisor=form.cleaned_data['Empresas'])
            for o in uPdocumento:
                o.tags.append(a)
                o.save()
            return HttpResponseRedirect(reverse('user_portfolios'))
    return render(request, 'dashboard/create_expenses.html', {'form': form, 'supliers': query})



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
            reverse('user_portfolios'))
