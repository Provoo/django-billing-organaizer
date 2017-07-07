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
            print("Hay que recontruir xml")
            myxml = tree.getroot()
            parser = ET.XMLParser(encoding="utf-8")
            root = tree.iter('comprobante')
            imp = ""
            for elem in root:
                imp = elem.text

            imp = imp.replace('\n', '')
            imp = imp.replace('  ', '')
            imp = imp.replace('&', '&amp;')
            imp = imp.replace(u'\xe9', 'c3a9')
            imp = imp.replace(u'\xe1', 'c3a1')
            imp = imp.replace(u'\xed', 'c3ad')
            imp = imp.replace(u'\xf3', 'c3b3')
            imp = imp.replace(u'\xf9', 'c3ba')
            imp = imp.replace(u'\xd3', 'c393')
            imp = imp.replace(u'\xd1', 'c391')
            imp = imp.replace(u'\ufffd', 'c391')

            # print(imp)
            try:
                myxml = ET.fromstring(imp, parser=None)
            except Exception as e:
                print('error: {}'.format(e))
            else:
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
    try:
        Variables_Enterprise = MetaData.objects.get(IdDocument=search_ruc)
    except:
        Variables_Enterprise = MetaData.objects.get(IdDocument="default")


    print("imprimiendo Meta Empresa de la base: %s " % (Variables_Enterprise))
    # Seteamos Diccionario con los valores por defecto
    document_object['NUMERO_DOCUMENTO'] = ''
    document_object['DEDUCIBLE_COMIDA'] = Decimal(0.00)
    document_object['DEDUCIBLE_VESTIMENTA'] = Decimal(0.00)
    document_object['DEDUCIBLE_EDUCACION'] = Decimal(0.00)
    document_object['DEDUCIBLE_SALUD'] = Decimal(0.00)
    document_object['DEDUCIBLE_VIVIENDA'] = Decimal(0.00)
    document_object['TOTAL_DOCUMENTO'] = Decimal(0.00)
    document_object['ARCHIVO'] = xml_document

    for child in root.iter(Variables_Enterprise.EnterpriseTaxPercent):
        if child.text:
            document_object['NUMERO_DOCUMENTO'] = Decimal(child.text)

    for child in root.iter():
            if child.tag == Variables_Enterprise.Clienteid:
                document_object['RUC_XML'] = child.text

            if child.tag == Variables_Enterprise.ClientName:
                document_object['NOMBRE_DOCUMENTO'] = child.text

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

            if child.tag == Variables_Enterprise.EnterpriseNoTax:
                document_object['TOTAL_GASTOSF'] = Decimal(child.text)

            if child.tag == Variables_Enterprise.EnterpriseTotal:
                document_object['TOTAL_DOCUMENTO'] = Decimal(child.text)

    # End For

    # Busqueda de campos adicionales comida:
    if Variables_Enterprise.EnterpriseFood != 'null':
        additional = root.findall(Variables_Enterprise.EnterpriseFood)
        if additional:
            for a in additional:
                document_object['DEDUCIBLE_COMIDA'] = Decimal(a.text)
                print("probando busqueda de atributo: %s" % (a.text))

    if Variables_Enterprise.EnterpriseMed != 'null':
        additional = root.findall(Variables_Enterprise.EnterpriseMed)
        if additional:
            for a in additional:
                document_object['DEDUCIBLE_SALUD'] = Decimal(a.text)
                print("probando busqueda de atributo: %s" % (a.text))

    if Variables_Enterprise.EnterpriseClothes != 'null':
        additional = root.findall(Variables_Enterprise.EnterpriseClothes)
        if additional:
            for a in additional:
                document_object['DEDUCIBLE_VIVIENDA'] = Decimal(a.text)
                print("probando busqueda de atributo: %s" % (a.text))

    if Variables_Enterprise.EnterpriseEdu != 'null':
        additional = root.findall(Variables_Enterprise.EnterpriseEdu)
        if additional:
            for a in additional:
                document_object['DEDUCIBLE_EDUCACION'] = Decimal(a.text)
                print("probando busqueda de atributo: %s" % (a.text))

    if Variables_Enterprise.EnterpriseHome != 'null':
        additional = root.findall(Variables_Enterprise.EnterpriseHome)
        if additional:
            for a in additional:
                document_object['DEDUCIBLE_VIVIENDA'] = Decimal(a.text)
                print("probando busqueda de atributo: %s" % (a.text))

    # Taxes
    document_object['TOTAL_IMPUESTOS'] = document_object['TOTAL_DOCUMENTO'] -\
        document_object['TOTAL_GASTOSF']


    document_object['NO_DEDUCIBLE'] = document_object['TOTAL_DOCUMENTO'] -\
        document_object['DEDUCIBLE_COMIDA'] -\
        document_object['DEDUCIBLE_VESTIMENTA'] -\
        document_object['DEDUCIBLE_EDUCACION'] -\
        document_object['DEDUCIBLE_SALUD'] -\
        document_object['DEDUCIBLE_VIVIENDA'] -\
        document_object['TOTAL_IMPUESTOS']


    document_object['TAX'] = Decimal(14)

    print("Imprimiendo dentro del xml Reader %s" % (document_object))

    return document_object

# import os
# from DocumentReader.xmlReader import readDocumentXML
# path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'xml_de_prueba/favorita022017.xml')
# readDocumentXML(path)
