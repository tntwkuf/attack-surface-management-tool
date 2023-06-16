from netaddr import IPAddress

#
def check_name_is_not_private_ip(name):
    '''
    Проверка, является ли аргумент хостнеймом, локальным или публичным IP
    Вернет False, если аргумент - локальный IP или localhost,
    Вернет True, если аргумент - хостнейм или публичный IP

    example.com -> True
    113.241.61.227 -> True
    10.50.10.20 -> False
    127.0.0.1 - > False
    localhost -> False
    '''
    result = True
    try:
        if name == 'localhost' or IPAddress(name).is_private() or IPAddress(name).is_loopback():
            result = False
    except:
        pass
    return result


def check_ip_is_public(ip):
    '''
    Проверка, является ли аргумент хостнеймом, локальным или публичным IP
    Вернет False, если аргумент - хостнейм, локальный IP или localhost,
    Вернет True, если аргумент - публичный IP

    example.com -> True
    113.241.61.227 -> True
    10.50.10.20 -> False
    127.0.0.1 - > False
    localhost -> False
    '''
    result = False
    try:
        if not IPAddress(ip).is_private() and not IPAddress(ip).is_loopback():
            result = True
    except:
        pass
    return result