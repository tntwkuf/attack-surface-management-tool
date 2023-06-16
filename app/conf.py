from .modules import base_module_class, bgp_api, reverse_whois_api, tld_api, crt_api, urlscan_api, \
    reverse_dns_crobat_api, resolve_host_api, port_scan_api, crobat_api, dns_dumpster_api, google_search, sublister_api, \
    threatcrowd_api, reverse_dns_threatcrowd_api, shodan_api, virustotal_api, rapiddns_api, dnsrepo_api, reverse_ip_api

PROXY_NEEDED = True
# Удален resolve_host_api из-за размещения в ЛВС
MODULES_ENUM = {'bgp_api': bgp_api, 'reverse_whois_api': reverse_whois_api, 'tld_api': tld_api, 'crt_api': crt_api,
                'urlscan_api': urlscan_api, 'port_scan_api': port_scan_api,
                'crobat_api': crobat_api, 'dns_dumpster_api': dns_dumpster_api, 'google_search': google_search,
                'sublister_api': sublister_api, 'threatcrowd_api': threatcrowd_api, 'shodan_api': shodan_api,
                'virustotal_api': virustotal_api, 'rapiddns_api': rapiddns_api, 'dnsrepo_api': dnsrepo_api,
                'reverse_dns_crobat_api': reverse_dns_crobat_api,
                'reverse_dns_threatcrowd_api': reverse_dns_threatcrowd_api,
                'reverse_ip_api': reverse_ip_api}  # , 'crawler_api': crawler_api}

LEVELS = 5
PROXIES = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
    'referer': 'https://www.google.co.in/'}