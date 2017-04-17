#!/usr/bin/env python

import xml.etree.ElementTree as ET
from DocumentReader.models import EnterprisesMetadataEcuador as MetaData
from datetime import datetime
from decimal import Decimal

'''
Codigo lector de facturas, es importante tomar en cuenta que algunas facturas
tienen mal definido el xml, es por esto que se lo transforma a texto nuevamente
y se lo convierte en xml para que coincida con las tags definidas.

'''


def get_xml_tree(xml_file):
    try:
        tree = ET.parse(xml_file)
    except Exception as e:
        print('error: {}'.format(e))
    else:
        flag = False
        for child in tree.iter('ruc'):
            if child.text:
                flag = True
        print('good')
        if not flag:
            print(tree.findall('ruc'))
            print("no existe el ruc")
            myxml = tree.getroot()
            parser = ET.XMLParser(encoding="utf-8")
            root = tree.iter('comprobante')
            imp = ""
            for elem in root:
                imp = elem.text

            imp = imp.replace('&', '&amp;')
            myxml = ET.fromstring(imp, parser=parser)
            return myxml
        else:
            return tree.getroot()


def readDocumentXML(xml_document):
    root = get_xml_tree(xml_document)
    document_object = {}
    search_ruc = ""
    for child in root.iter('ruc'):
        if child.text:
            search_ruc = child.text

    Variables_Enterprise = MetaData.objects.get(IdDocument=search_ruc)
    print("imprimiendo objeto de la base: %s " % (Variables_Enterprise))
    # Seteamos Diccionario con los valores por defecto
    document_object['NUMERO_DOCUMENTO'] = ''
    document_object['DEDUCIBLE_COMIDA'] = 0.00
    document_object['DEDUCIBLE_VESTIMENTA'] = 0.00
    document_object['DEDUCIBLE_EDUCACION'] = 0.00
    document_object['DEDUCIBLE_SALUD'] = 0.00
    document_object['NO_DEDUCIBLE'] = 0.00
    document_object['ARCHIVO'] = xml_document

    for child in root.iter():
            if child.tag == Variables_Enterprise.Clienteid:
                document_object['RUC_XML'] = child.text

            if child.tag == Variables_Enterprise.EnterpriseId:
                document_object['RUC_EMISOR'] = child.text

            if child.tag == Variables_Enterprise.EnterpriseComercialName:
                document_object['NOMBRE_EMISOR'] = child.text

            if child.tag == Variables_Enterprise.EnterpriseAddress:
                document_object['DIRECCION_EMISOR'] = child.text

            if child.tag == Variables_Enterprise.EnterpriseDateAuth:
                document_object['FECHA'] = datetime.strptime(
                    child.text, "%d/%m/%Y")

            if child.tag == "estab":
                document_object['NUMERO_DOCUMENTO'] = child.text

            if child.tag == "ptoEmi":
                document_object['NUMERO_DOCUMENTO'] += '-%s' % (child.text)

            if child.tag == "secuencial":
                document_object['NUMERO_DOCUMENTO'] += '-%s' % (child.text)

            if child.tag == Variables_Enterprise.EnterpriseBaseTax:
                document_object['TOTAL_GASTOS'] = Decimal(child.text) * Variables_Enterprise.EnterpriseTaxPercent / 100

            if child.tag == Variables_Enterprise.EnterpriseTotal:
                document_object['TOTAL_DOCUMENTO'] = float(child.text)

    # End For

    # Busqueda de campos adicionales comida:
    if Variables_Enterprise.EnterpriseFood != 'null':
        additional = root.findall(Variables_Enterprise.EnterpriseFood)
        if additional:
            for a in additional:
                document_object['DEDUCIBLE_COMIDA'] = float(a.text)
                print("probando busqueda de atributo: %s" % (a.text))

    document_object['NO_DEDUCIBLE'] = document_object['TOTAL_DOCUMENTO'] -\
        document_object['DEDUCIBLE_COMIDA'] -\
        document_object['DEDUCIBLE_VESTIMENTA'] -\
        document_object['DEDUCIBLE_EDUCACION'] -\
        document_object['DEDUCIBLE_SALUD']

    return document_object

# import os
# from DocumentReader.xmlReader import readDocumentXML
# path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'xml_de_prueba/JuanValdez.xml')
# readDocumentXML(path)
