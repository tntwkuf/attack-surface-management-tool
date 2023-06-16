from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Modules, Progress, Exceptions, Total, Ports, Domains, Keywords, KnownIPs, Vulns, Relations, IPs

admin.site.site_header = 'Периметр'
admin.site.site_title = 'Периметр'


def ip_founded_by(obj):
    try:
        result = ''
        temp = (IPs.objects.filter(ip=obj.ip).get().founded_by).split(', ')
        l = len(temp)
        for i in temp:
            m = Modules.objects.get(name=i)
            link = reverse("admin:app_modules_change", args=[m.id])
            if l == 1:
                result += f'<a href="{link}">{i}</a>\n'
            else:
                result += f'<a href="{link}">{i}, </a>\n'
        return format_html(result)
    except:
        return None


ip_founded_by.short_description = 'Обнаружен модулем'


@admin.register(IPs)
class IPsAdmin(admin.ModelAdmin):
    list_display = ('ip', ip_founded_by)
    list_filter = ()
    search_fields = ['ip']


def parent__name(obj):
    try:
        return obj.parent.name
    except:
        return None


parent__name.short_description = 'Родительский домен'


@admin.register(Vulns)
class VulnsAdmin(admin.ModelAdmin):
    list_display = ('cve', 'cvss', 'description')
    list_filter = ()
    search_fields = ['cve', 'cvss', 'description']


@admin.register(Domains)
class DomainsAdmin(admin.ModelAdmin):
    list_display = ('name', 'descr')
    list_filter = ()
    search_fields = ['name']


@admin.register(Modules)
class ModulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'descr')
    list_filter = ()
    search_fields = ['name', 'level']


def open_ports(obj):
    try:
        return format_html(', '.join([f'<a href="{reverse("admin:app_ports_change", args=[x])}">{x} </a>\n' for x in
                                      (Total.objects.filter(object_id=obj.object_id).get().open_ports).split(', ')]))
    except:
        return None


open_ports.short_description = 'Открытые порты'


def vulns(obj):
    try:
        return format_html(', '.join([f'<a href="{reverse("admin:app_vulns_change", args=[x])}">{x} </a>\n' for x in
                                      (Total.objects.filter(object_id=obj.object_id).get().vulns).split(', ')]))
    except:
        return None


vulns.short_description = 'Уязвимости'


def total_founded_by(obj):
    try:
        return format_html(', '.join(
            [f'<a href="{reverse("admin:app_modules_change", args=[Modules.objects.get(name=x).id])}">{x} </a>\n' for x
             in
             (Total.objects.filter(object=obj.object).get().founded_by).split(', ')]))
    except:
        return None


total_founded_by.short_description = 'Обнаружен модулем'


def is_available(obj):
    if obj.online_by_hostname or obj.online_by_ip:
        return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
    else:
        return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')


is_available.short_description = 'Объект доступен'


@admin.register(Total)
class TotalAdmin(admin.ModelAdmin):
    list_display = (
        'object_id', 'object', 'ip', 'a_record', parent__name, total_founded_by, open_ports, 'date_add', is_available,
        'isnew',
        'known')
    list_filter = ()
    search_fields = ['object', 'ip', 'parent__name']
    actions = ['add_to_exception']

    def add_to_exception(self, request, queryset):
        for i in request.POST.getlist('_selected_action'):
            try:
                obj = Total.objects.get(object_id=i)
                domain = obj.parent.name
            except:
                pass
            try:
                Exceptions.objects.update_or_create({'name': domain}, name=domain)
            except:
                pass
            try:
                Total.objects.filter(parent=domain).delete()
            except:
                pass
            try:
                Domains.objects.filter(name=domain).delete()
            except:
                pass
            try:
                Progress.objects.filter(object=obj).delete()
            except:
                pass
            try:
                Relations.objects.filter(query=domain).delete()
            except:
                pass

    add_to_exception.short_description = "Добавить домены в исключение"


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'object', 'module')
    list_filter = ()
    search_fields = ['object', 'module']


def module_descr(obj):
    try:
        return obj.module.descr
    except:
        return ''


module_descr.short_description = 'Описание модуля'


@admin.register(Relations)
class RelationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'object', 'query', 'module', module_descr)
    list_filter = ()
    search_fields = ['object', 'query', 'module__name']


@admin.register(Exceptions)
class ExceptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ()
    search_fields = ['name']


@admin.register(Ports)
class PortsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ()
    search_fields = ['name']


@admin.register(Keywords)
class KeywordsAdmin(admin.ModelAdmin):
    list_display = (
        'keyword', )
    list_filter = ()
    search_fields = ['keyword']


@admin.register(KnownIPs)
class KnownIPsAdmin(admin.ModelAdmin):
    list_display = ('ip',)
    list_filter = ()
    search_fields = ['ip']

    class Media:
        js = ('jquery-3.5.1.js', 'knownips.js',)
        css = {
            'all': ('knownips.css',)
        }
