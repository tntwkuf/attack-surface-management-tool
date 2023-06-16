import os

from django.http import HttpResponse
from . import conf
from .modules import base_module_class, bgp_api, reverse_whois_api, crt_api, resolve_host_api, port_scan_api, \
    reverse_dns_crobat_api, reverse_dns_threatcrowd_api, crobat_api, dns_dumpster_api, google_search, sublister_api, \
    threatcrowd_api, shodan_api, cve_circl_api, urlscan_api, virustotal_api, rapiddns_api, dnsrepo_api, reverse_ip_api
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from .models import Modules, Progress, Exceptions, Total, Domains, Ports, Keywords, KnownIPs, Vulns, Relations, IPs
from .work_with_excel import export_search_result, ips_import
from .forms import UploadFileForm
import datetime, time
from django.shortcuts import redirect, render
from colorama import init
from netaddr import IPNetwork, IPAddress
from .check_service import complex_check
from django.db.models import Q
from .graph_builder import base_graph, relations_graph


# Удаление дубликатов в поле
def remove_duplicates(row: str, t: str) -> str:
    result = []
    try:
        for i in row.split(', '):
            if str(t) != str(i):
                result.append(i)
        result.append(str(t))
        return ', '.join(result)
    except:
        return str(t)


def module_clear(request) -> None:
    cursor = connection.cursor()
    Modules.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_modules'")
    return redirect('/admin/app/modules/')


def domains_clear(request) -> None:
    cursor = connection.cursor()
    Domains.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_domains'")
    return redirect('/admin/app/domains/')


def known_ips_clear(request) -> None:
    cursor = connection.cursor()
    KnownIPs.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_knownips'")
    return redirect('/admin/app/knownips/')


def keywords_clear(request) -> None:
    cursor = connection.cursor()
    Keywords.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_keywords'")
    return redirect('/admin/app/keywords/')


def ips_clear(request) -> None:
    cursor = connection.cursor()
    IPs.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_ips'")
    return redirect('/admin/app/ips/')


def relations_clear(request) -> None:
    cursor = connection.cursor()
    Relations.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_relations'")
    return redirect('/admin/app/relations/')


# Запись модулей в БД
def module_add(request) -> None:
    for m in list(conf.MODULES_ENUM.values()):
        module = m()
        Modules.objects.update_or_create(
            {'id': module.id, 'name': module.name, 'level': module.level, 'descr': module.descr},
            name=module.name)
    return redirect('/admin/app/modules/')


def progress_clear(request) -> None:
    cursor = connection.cursor()
    Progress.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_progress'")
    return redirect('/admin/app/progress/')


def total_clear(request) -> None:
    cursor = connection.cursor()
    Total.objects.all().delete()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_total'")
    return redirect('/admin/app/total/')


def renew_isnew(request) -> None:
    for i in Total.objects.all():
        try:
            i.isnew = False
            i.save()
        except:
            pass


def check_known_ips() -> None:
    for row in Total.objects.all():
        if row.ip:
            for ip in str(row.ip).split(', '):
                for range in list(KnownIPs.objects.values_list('ip', flat=True)):
                    if IPAddress(ip) in IPNetwork(range):
                        row.known = True
                        row.save()
                        break


def run_module(module, outp_name, target):
    module.print_start(outp_name)
    pool = []
    f, res_list = module.search(target)
    if f:
        module.print_succes(outp_name)
        for r in res_list:
            try:
                record, domain = module.get_domain_from_record(r['object'])
                if not module.is_exception(domain,
                                           list(Exceptions.objects.values_list('name', flat=True))):
                    cur_domain, _ = Domains.objects.get_or_create(name=domain)
                    obj, isNew = Total.objects.get_or_create(object=record)
                    pool.append((cur_domain, _))
                    ip = r.get('ip', None)
                    ports = r.get('ports', None)
                    banner = r.get('banner', None)
                    cve = r.get('vulns', None)
                    if ip and ip not in ['-', '127.0.0.1', '8.8.8.8'] and not IPAddress(ip).is_private():
                        obj.ip = remove_duplicates(obj.ip, ip)
                    if ports:
                        obj.open_ports = remove_duplicates(obj.open_ports, ports)
                    if banner:
                        obj.banner = remove_duplicates(obj.banner, banner)
                    if cve:
                        vuln, _ = Vulns.objects.get_or_create(cve=cve[0],
                                                              defaults={'cvss': cve[1],
                                                                        'description': cve[2]})
                        obj.vulns = remove_duplicates(obj.vulns, vuln)
                    obj.founded_by = remove_duplicates(obj.founded_by, module.name)
                    obj.parent = cur_domain
                    obj.isnew = True
                    obj.date_add = datetime.datetime.today()
                    obj.save()
                    if isinstance(target, str):
                        query = target
                    else:
                        query = target.object
                    if query != obj.object:
                        Relations.objects.get_or_create(query=query, object=obj.object,
                                                        module=Modules.objects.filter(id=module.id).get())

            except Exception as e:
                print(res_list)
                module.print_fail(outp_name, e)
        Progress.objects.create(object=outp_name, status='OK',
                                module=Modules.objects.filter(id=module.id).get())

    else:
        module.print_fail(outp_name, res_list)
        Progress.objects.create(object=outp_name, status='BAD',
                                module=Modules.objects.filter(id=module.id).get())
    return pool


def ip_search(module, outp_name, target):
    module.print_start(outp_name)
    f, res_list = module.search(target)
    if f:
        module.print_succes(outp_name)
        for r in res_list:
            try:
                ip = r.get('ip', None)
                if ip:
                    new_ip, _ = IPs.objects.get_or_create(ip=ip)
                    # new_ip.founded_by = remove_duplicates(new_ip.founded_by, module.name)
                    Relations.objects.create(query=outp_name, object=ip,
                                             module=Modules.objects.filter(id=module.id).get())
            except Exception as e:
                module.print_fail(outp_name, e)
        Progress.objects.create(object=outp_name, status='OK',
                                module=Modules.objects.filter(id=module.id).get())

    else:
        module.print_fail(outp_name, res_list)
        Progress.objects.create(object=outp_name, status='BAD',
                                module=Modules.objects.filter(id=module.id).get())


def search(pool: list, level: int, timeout: int, to_if_exist: int) -> None:
    while pool:
        if level == 0 or level == 1:
            target = pool[0]['keyword']
            allow_module = pool[0]['module']
            outp_name = target
        elif level == 2:
            target = pool[0]
            allow_module = 'all'
            outp_name = target.ip
        else:
            target = pool[0]
            allow_module = 'all'
            outp_name = target.object
        for q in list(Modules.objects.values_list('name', flat=True).filter(level=level)):
            module = conf.MODULES_ENUM[q]()
            if module.id == 17:
                continue
            if (allow_module == 'all' or module.name in allow_module) and not module.is_exception(outp_name,
                                                                                                  list(
                                                                                                      Exceptions.objects.values_list(
                                                                                                          'name',
                                                                                                          flat=True))):
                if not module.is_checked(target, Progress.objects.filter(module__name=module.name)):
                    if level != 0:
                        if level == 2:
                            time.sleep(timeout / 10)
                        else:
                            time.sleep(timeout)
                        new_domains = run_module(module, outp_name, target)
                        for d, c in new_domains:
                            if c and level == 3:
                                nd, dc = Total.objects.get_or_create(object=d.name)
                                nd.founded_by = remove_duplicates(nd.founded_by, module.name)
                                nd.parent = Domains.objects.get_or_create(name=nd)[0]
                                nd.isnew = True
                                nd.date_add = datetime.datetime.today()
                                nd.save()
                                pool.append(nd)
                    else:
                        time.sleep(timeout / 10)
                        ip_search(module, outp_name, target)
                else:
                    timeout = to_if_exist
                    module.print_exists(outp_name)
            module = None
        pool.pop(0)


# запуск поиска
def start_search(request) -> None:
    init()
    start = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    keywords = [{'keyword': i.keyword, 'module': i.visibility} for i in Keywords.objects.all()]
    for level in range(0, conf.LEVELS + 1):
        if level == 0 or level == 1:
            pool = keywords.copy()
        elif level == 2:
            pool = list(IPs.objects.all())
        else:
            pool = list(Total.objects.all())
        search(pool, level, 30, 1)

    check_known_ips()
    end = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f'[#] Начало: {start}\n[#] Конец: {end}')
    return HttpResponse("Сканирование завершено")


def export_search_to_excel(request) -> None:
    if request.user.is_authenticated:
        res = list(
            Total.objects.values_list('object_id', 'object', 'ip', 'parent__name', 'founded_by', 'open_ports',
                                      'banner', 'vulns', 'known', 'isnew', 'date_add'))
        ports = list(
            Ports.objects.values_list('id', 'name'))
        modules = list(
            Modules.objects.values_list('id', 'name', 'level', 'descr'))
        domains = list(
            Domains.objects.values_list('name', flat=True))
        vulns = list(Vulns.objects.values_list('cve', 'cvss', 'description'))
        relations = list(Relations.objects.values_list('id', 'object', 'query', 'module__name'))
        return export_search_result(res, ports, modules, domains, vulns, relations)
    else:
        return HttpResponse('403 Forbidden')


# функция для импорта известных диапазонов
def import_from_perimetr(request) -> None:
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                files_list = request.FILES.getlist('file')
                result = ips_import(files_list[0])
                for i in result:
                    KnownIPs.objects.create(ip=i)
                return redirect('/admin/app/knownips/')
            else:
                return HttpResponse('Invalid form')
        else:
            return HttpResponse('Invalid request')
    else:
        return HttpResponse('403 Forbidden')


# функция проверки отдельных модулей
def test(request):
    return HttpResponse('@@@')


def vis_base_graph(request):
    if request.user.is_authenticated:
        b_graph = base_graph(Total.objects.all(), Domains.objects.all())
        if not b_graph:
            return render(request, './base_graph.html')
        else:
            return HttpResponse(f'Error: {b_graph}')
    else:
        return HttpResponse('403 Forbidden')


def vis_relations_graph(request):
    if request.user.is_authenticated:
        r_graph = relations_graph(Relations.objects.all(), Keywords.objects.all())
        if not r_graph:
            return render(request, './relations_graph.html')
        else:
            return HttpResponse(f'Error: {r_graph}')
    else:
        return HttpResponse('403 Forbidden')
