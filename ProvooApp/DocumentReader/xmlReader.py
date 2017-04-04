import xml.etree.ElementTree as ET
from DocumentReader.models import EnterprisesMetadataEcuador as MetaData
from datetime import datetime


def get_xml_tree(xml_file):
    try:
        tree = ET.parse(xml_file)
    except Exception as e:
        print('error: {}'.format(e))
    else:
        print('good')
        root = tree.getroot()

    return root


def readDocumentXML(xml_document):
    root = get_xml_tree(xml_document)
    iterat = root.getiterator()
    document_object = {}
    # Seteamos Diccionario con los valores por defecto
    document_object['NUMERO_DOCUMENTO'] = ''
    document_object['DEDUCIBLE_COMIDA'] = 0.00
    document_object['DEDUCIBLE_VESTIMENTA'] = 0.00
    document_object['DEDUCIBLE_EDUCACION'] = 0.00
    document_object['DEDUCIBLE_SALUD'] = 0.00
    document_object['NO_DEDUCIBLE'] = 0.00
    document_object['ARCHIVO'] = xml_document

    for child in iterat:
            if child.tag == "identificacionComprador":
                document_object['RUC_XML'] = child.text

            if child.tag == "ruc":
                document_object['RUC_EMISOR'] = child.text

            if child.tag == "nombreComercial":
                document_object['NOMBRE_EMISOR'] = child.text

            if child.tag == "dirEstablecimiento":
                document_object['DIRECCION_EMISOR'] = child.text

            if child.tag == "fechaAutorizacion":
                document_object['FECHA'] = datetime.strptime(child.text, "%d/%m/%Y %H:%M:%S")

            if child.tag == "estab":
                document_object['NUMERO_DOCUMENTO'] = child.text

            if child.tag == "ptoEmi":
                document_object['NUMERO_DOCUMENTO'] += '-%s' % (child.text)

            if child.tag == "secuencial":
                document_object['NUMERO_DOCUMENTO'] += '-%s' % (child.text)

            if child.tag == "totalSinImpuestos":
                document_object['TOTAL_GASTOS'] = float(child.text)

            if child.tag == "totalConImpuestos":
                imp = child.getiterator()
                for nchild in imp:
                    if nchild.tag == "valor":
                        document_object['TOTAL_IMPUESTOS'] = float(nchild.text)
                        print("{} =  {}".format(nchild.tag, nchild.text))
                        break

            if child.tag == "importeTotal":
                document_object['TOTAL_DOCUMENTO'] = float(child.text)

            if child.tag == "campoAdicional" and \
                    child.attrib.get('nombre') == "DEDUCIBLE ALIMENTACION":
                document_object['DEDUCIBLE_COMIDA'] = float(child.text)

    # End For
    document_object['NO_DEDUCIBLE'] = document_object['TOTAL_DOCUMENTO'] -\
        document_object['DEDUCIBLE_COMIDA'] -\
        document_object['DEDUCIBLE_VESTIMENTA'] -\
        document_object['DEDUCIBLE_EDUCACION'] -\
        document_object['DEDUCIBLE_SALUD']

    return document_object
