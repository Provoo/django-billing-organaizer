
from dashboard.models import Portafolio, documento, documento_error
# Xml Reader Api
from DocumentReader.xmlReader import readDocumentXML
from django.core.files.base import ContentFile
import re
import zipfile


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
    errors_documents = []
    objeto_xml_paser = {}
    tags = []
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
