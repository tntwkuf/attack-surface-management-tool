from django.db import models


class IPs(models.Model):
    ip = models.CharField(max_length=50, null=True, blank=True, verbose_name='IP-адрес')

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['ip']
        verbose_name = 'IP-адрес'
        verbose_name_plural = 'IP-адреса'


# Уязвимости
class Vulns(models.Model):
    cve = models.CharField(primary_key=True, max_length=500, null=False, blank=True,
                           verbose_name='CVE')
    cvss = models.CharField(max_length=500, null=False, blank=True,
                            verbose_name='CVSS')
    description = models.TextField(null=False, blank=True,
                                   verbose_name='Описание')

    def __str__(self):
        return self.cve

    class Meta:
        ordering = ['cve']
        verbose_name = 'CVE'
        verbose_name_plural = 'CVE'


# Домены
class Domains(models.Model):
    name = models.CharField(primary_key=True, max_length=500, null=False, blank=True,
                            verbose_name='Имя домена')
    descr = models.CharField(max_length=500, null=False, blank=True,
                            verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Родителський домен'
        verbose_name_plural = 'Родительские домены'


# Ключевые слова
class Keywords(models.Model):
    keyword = models.CharField(primary_key=True, max_length=500, null=False, blank=True,
                               verbose_name='Ключевое слово')
    visibility = models.TextField(null=True, blank=True, default='all', verbose_name='Видимость модулям')

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ['keyword']
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'


# Модули
class Modules(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=500, null=True, blank=True, verbose_name='Наименование модуля')
    level = models.IntegerField(verbose_name='Номер этапа', null=True, blank=True)
    descr = models.TextField(null=True, blank=True, verbose_name='Описание модуля')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id', 'level']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


# Домены/поддомены
class Total(models.Model):
    object_id = models.AutoField(primary_key=True, verbose_name='ID')
    object = models.CharField(max_length=500, null=True, blank=True, verbose_name='Имя домена/поддомена')
    ip = models.CharField(max_length=500, default=None, null=True, blank=True, verbose_name='IP адрес')
    a_record = models.TextField('Содержимое A-записи', null=True, blank=True)
    parent = models.ForeignKey(Domains, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Родительский домен')
    founded_by = models.CharField(max_length=500, null=True, blank=True,
                                  verbose_name='Модуль')
    open_ports = models.CharField(max_length=500, default=None, null=True, blank=True,
                                  verbose_name='Открытые порты')
    banner = models.TextField(default=None, null=True, blank=True, verbose_name='Баннер')
    isnew = models.BooleanField(default=True, verbose_name='Объект изменился')
    date_add = models.DateField(null=True, blank=True, verbose_name='Дата обнаружения')
    vulns = models.CharField(max_length=500, default=None, null=True, blank=True,
                             verbose_name='Уязвимости')
    known = models.BooleanField(default=False, verbose_name='Есть в БД Периметра')
    online_by_hostname = models.BooleanField('Доступен по hostname', default=False)
    online_by_ip = models.BooleanField('Доступен по IP', default=False)
    response_code_hostname = models.CharField('Код ответа по доменному имени', max_length=10, null=True, blank=True)
    response_code_ip = models.CharField('Код ответа по IP', max_length=100, null=True, blank=True)
    techs = models.TextField('Технологии', null=True, blank=True)
    cert = models.CharField('Сертификат', max_length=100, null=True, blank=True)
    redirect = models.CharField('Переадресация', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.object

    class Meta:
        ordering = ['object_id']
        verbose_name = 'Домен/Поддомен'
        verbose_name_plural = 'Домены/Поддомены'


# Прогресс
class Progress(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    object = models.CharField(max_length=500, null=True, blank=True, verbose_name='Объект')
    module = models.ForeignKey(Modules, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Модуль')
    status = models.CharField(max_length=500, null=True, blank=True, verbose_name='Статус')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс'


# Исключения
class Exceptions(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=500, null=True, blank=True,
                            verbose_name='Домен/поддомен-исключение')
    descr = models.TextField(null=True, blank=True,
                             verbose_name='Комментарий')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Исключение'
        verbose_name_plural = 'Исключения'


# Порты
class Ports(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Порт')
    name = models.CharField(max_length=500, null=True, blank=True,
                            verbose_name='Имя сервиса')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Порт'
        verbose_name_plural = 'Порты'


# Известные IP
class KnownIPs(models.Model):
    ip = models.CharField(primary_key=True, max_length=500, null=False, blank=True,
                          verbose_name='IP')

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['ip']
        verbose_name = 'Известный IP диапазон'
        verbose_name_plural = 'Известные IP диапазоны'


# Связи
class Relations(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    query = models.CharField(max_length=500, null=True, blank=True,
                             verbose_name='Поисковый запрос')
    object = models.CharField(max_length=500, null=True, blank=True,
                              verbose_name='Домен/поддомен')
    module = models.ForeignKey(Modules, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Модуль')

    def __str__(self):
        return self.query

    class Meta:
        ordering = ['id']
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
