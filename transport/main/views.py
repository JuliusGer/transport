import os
from xml import etree

from django.shortcuts import render, redirect
from .models import *
from .forms import *
import pandas as pd
from lxml import etree as et
import xml.etree.cElementTree as ET


def index(request):
    error = ''
    updating_id = request.GET.get('updating_id', '')
    updating_id_mes = ''
    if request.GET.get('updating_id', '')!='':
        updating_id_mes = 'Изменение записи с transport_id: ' + updating_id
    if request.method == 'POST':
        if updating_id != '':
            row_transport = transport_info.objects.get(id=updating_id)
            row_owner = transport_owners_info.objects.get(id=row_transport.owner_id)
        else:
            row_owner = transport_owners_info()
        row_owner.owner_name = request.POST.get('owner_name')
        row_owner.owner_gender = request.POST.get('owner_gender')
        row_owner.passport = request.POST.get('passport')
        row_owner.birth_date = request.POST.get('birth_date')
        row_owner.citizenship = request.POST.get('citizenship')
        if not transport_owners_info.objects.filter(owner_name=row_owner.owner_name, owner_gender=row_owner.owner_gender,
                                                passport=row_owner.passport, birth_date=row_owner.birth_date,
                                                citizenship=row_owner.citizenship).exists():
            row_owner.save()

        # owner_id = transport_owners_info.objects.latest('id').id
        owner_id = transport_owners_info.objects.only('id').get(owner_name=row_owner.owner_name,
                                                                owner_gender=row_owner.owner_gender,
                                                                passport=row_owner.passport,
                                                                birth_date=row_owner.birth_date,
                                                                citizenship=row_owner.citizenship).id
        if updating_id != '':
            row_transport = transport_info.objects.get(id=updating_id)
        else:
            row_transport = transport_info()
            # owner_id = transport_owners_info.objects.latest('id').id
            # owner_id = transport_owners_info.objects.only('id').get(owner_name=row_owner.owner_name,
            #                                                         owner_gender=row_owner.owner_gender,
            #                                                         passport=row_owner.passport,
            #                                                         birth_date=row_owner.birth_date,
            #                                                         citizenship=row_owner.citizenship).id
        row_transport.type_id = request.POST.get('type_id')
        row_transport.transport_number = request.POST.get('transport_number')
        row_transport.owner_id = owner_id
        # row_transport.prev_owner_id = request.POST.get('prev_owner_id')
        row_transport.manufacture_date = request.POST.get('manufacture_date')
        row_transport.cur_license_expires = request.POST.get('cur_license_expires')
        row_transport.made_in_country = request.POST.get('made_in_country')
        if not transport_info.objects.filter(type_id=row_transport.type_id, transport_number=row_transport.transport_number,
                                        owner_id=owner_id, manufacture_date=row_transport.manufacture_date,
                                        cur_license_expires=row_transport.cur_license_expires, made_in_country=row_transport.made_in_country).exists():
            row_transport.save()

        return redirect('/tables_data/tables_data')

    if updating_id != '':
        row_transport = transport_info.objects.get(id=updating_id)
        row_owner = transport_owners_info.objects.get(id=row_transport.owner_id)
        form_owner = transport_owners_form(initial={'owner_name': row_owner.owner_name, 'owner_gender': row_owner.owner_gender,
                                                    'passport': row_owner.passport, 'birth_date': row_owner.birth_date,
                                                    'citizenship': row_owner.citizenship})
        row_transport = transport_info.objects.get(id=updating_id)
        form_transport = transport_info_form(initial={'type_id': row_transport.type_id, 'transport_number': row_transport.transport_number,
                     # 'prev_owner_id': row_transport.prev_owner_id,
                     'manufacture_date': row_transport.manufacture_date,
                     'cur_license_expires': row_transport.cur_license_expires, 'made_in_country': row_transport.made_in_country})
    else:
        form_owner = transport_owners_form()
        form_transport = transport_info_form()
    data = {'form_owner': form_owner,
            'form_transport': form_transport,
            'error': error,
            'updating_id_mes': updating_id_mes}
    return render(request, 'main/index.html', data)


def tables_data(request):
    if request.method == 'POST':
        if 'delete' in request.POST:
            transport_owners_info.objects.filter(id=request.POST.get('change_data_id')).delete()
            transport_info.objects.filter(id=request.POST.get('change_data_id')).delete()
        elif 'update' in request.POST:
            updating_id = request.POST.get('change_data_id')
            return redirect('/?updating_id={0}'.format(updating_id))
        elif 'import' in request.POST:
            if request.POST.get('transport_owners_info_xml') != '':
                owners_xml = request.FILES['transport_owners_info_xml']
                tree = et.parse(owners_xml)
                root = tree.getroot()
                for appt in root.getchildren():
                    d = {}
                    for elem in appt.getchildren():
                        d[elem.tag] = elem.text
                    if transport_owners_info.objects.filter(id=d.get('id')).exists():
                        row_owner = transport_owners_info.objects.get(id=d.get('id'))
                    else:
                        row_owner = transport_owners_info()
                    row_owner.owner_name = d.get('owner_name')
                    row_owner.owner_gender = d.get('owner_gender')
                    row_owner.passport = d.get('passport')
                    row_owner.birth_date = d.get('birth_date')
                    row_owner.citizenship = d.get('citizenship')
                    if not transport_owners_info.objects.filter(owner_name=row_owner.owner_name,
                                                                owner_gender=row_owner.owner_gender,
                                                                passport=row_owner.passport,
                                                                birth_date=row_owner.birth_date,
                                                                citizenship=row_owner.citizenship).exists():
                        row_owner.save()

            if request.POST.get('transport_info_xml') != '':
                transport_xml = request.FILES['transport_info_xml']
                tree = et.parse(transport_xml)
                root = tree.getroot()
                for appt in root.getchildren():
                    d = {}
                    # row_transport = transport_info()
                    # for elem in appt.getchildren():
                    #     if elem.tag == 'id':
                    #         row_transport = transport_info.objects.get(id=elem.text)
                    #     row_transport.elem.tag = elem.text
                    for elem in appt.getchildren():
                        d[elem.tag] = elem.text
                    if transport_info.objects.filter(id=d.get('id')).exists():
                        row_transport = transport_info.objects.get(id=d.get('id'))
                    else:
                        row_transport = transport_info()
                    # owner_id = transport_owners_info.objects.only('id').get(owner_name=row_owner.owner_name,
                    #                                                         owner_gender=row_owner.owner_gender,
                    #                                                         passport=row_owner.passport,
                    #                                                         birth_date=row_owner.birth_date,
                    #                                                         citizenship=row_owner.citizenship).id
                    row_transport.type_id = d.get('type_id')
                    row_transport.transport_number = d.get('transport_number')
                    row_transport.owner_id = d.get('owner_id')
                    # row_transport.prev_owner_id = d.get('prev_owner_id')
                    row_transport.manufacture_date = d.get('manufacture_date')
                    row_transport.cur_license_expires = d.get('cur_license_expires')
                    row_transport.made_in_country = d.get('made_in_country')
                    if not transport_info.objects.filter(type_id=row_transport.type_id,
                                                        transport_number=row_transport.transport_number,
                                                        owner_id=row_transport.owner_id,
                                                        manufacture_date=row_transport.manufacture_date,
                                                        cur_license_expires=row_transport.cur_license_expires,
                                                        made_in_country=row_transport.made_in_country).exists():
                        row_transport.save()
            return redirect('/tables_data/tables_data')


    MODEL_HEADERS = [f.name for f in transport_types._meta.get_fields()]
    query_results = [list(i.values()) for i in list(transport_types.objects.all().values())]

    MODEL_HEADERS1 = [f.name for f in transport_owners_info._meta.get_fields()]
    query_results1 = [list(i.values()) for i in list(transport_owners_info.objects.all().values())]

    MODEL_HEADERS2 = [f.name for f in transport_info._meta.get_fields()]
    query_results2 = [list(i.values()) for i in list(transport_info.objects.all().values())]
    # return a response to your template and add query_results to the context

    return render(request, "main/tables_data.html", {
        "query_results": query_results,
        "model_headers": MODEL_HEADERS,

        "query_results1": query_results1,
        "model_headers1": MODEL_HEADERS1,

        "query_results2": query_results2,
        "model_headers2": MODEL_HEADERS2
    })


def xml_handler(request):
    dir = 'main/static/xmls/'
    df = pd.DataFrame(list(transport_types.objects.all().values()))
    root = et.Element('root')
    for row in df.iterrows():
        transport_type = et.SubElement(root, 'transport_type')
        type_id = et.SubElement(transport_type, 'id')
        type_name = et.SubElement(transport_type, 'type_name')

        type_id.text = str(row[1]['id'])
        type_name.text = str(row[1]['type_name'])
    tree = ET.ElementTree(root)
    tree.write(os.path.join(dir + "transport_types.xml"), encoding="utf-8")

    df = pd.DataFrame(list(transport_owners_info.objects.all().values()))
    root = et.Element('root')
    for row in df.iterrows():
        transport_owner = et.SubElement(root, 'transport_owners')
        owner_id = et.SubElement(transport_owner, 'id')
        name = et.SubElement(transport_owner, 'owner_name')
        gender = et.SubElement(transport_owner, 'owner_gender')
        passport = et.SubElement(transport_owner, 'passport')
        birth_date = et.SubElement(transport_owner, 'birth_date')
        citizenship = et.SubElement(transport_owner, 'citizenship')

        owner_id.text = str(row[1]['id'])
        name.text = str(row[1]['owner_name'])
        gender.text = str(row[1]['owner_gender'])
        passport.text = str(row[1]['passport'])
        birth_date.text = str(row[1]['birth_date'])
        citizenship.text = str(row[1]['citizenship'])
    tree = ET.ElementTree(root)
    tree.write(os.path.join(dir + "transport_owners_info.xml"), encoding="utf-8")

    df = pd.DataFrame(list(transport_info.objects.all().values()))
    root = et.Element('root')
    for row in df.iterrows():
        transport = et.SubElement(root, 'transport')
        id = et.SubElement(transport, 'id')
        type_id = et.SubElement(transport, 'type_id')
        number = et.SubElement(transport, 'transport_number')
        owner_id = et.SubElement(transport, 'owner_id')
        # prev_owner_id = et.SubElement(transport, 'prev_owner_id')
        manufacture_date = et.SubElement(transport, 'manufacture_date')
        license_expires = et.SubElement(transport, 'cur_license_expires')
        country = et.SubElement(transport, 'made_in_country')

        id.text = str(row[1]['id'])
        type_id.text = str(row[1]['type_id'])
        number.text = str(row[1]['transport_number'])
        owner_id.text = str(row[1]['owner_id'])
        # prev_owner_id.text = str(row[1]['prev_owner_id'])
        manufacture_date.text = str(row[1]['manufacture_date'])
        license_expires.text = str(row[1]['cur_license_expires'])
        country.text = str(row[1]['made_in_country'])
    tree = ET.ElementTree(root)
    tree.write(os.path.join(dir + "transport_info.xml"), encoding="utf-8")
    return render(request, 'main/xml_handler.html')
