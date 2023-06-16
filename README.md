# Attack-surface-management-tool
Tool for recursive gathering sensitive information (IPs, domain, subdomains, open ports, CVEs etc) using OSINT and keywords. Have module structure for easy add-in new modules/sources.

Uses next sources/modules/scripts:
- Border gateway Protocol (BGP)
- Top Level Domains (TLD)
- Reverse DNS Lookup
- Reverse Whois
- SSL-certs search
- Urlscan
- Google Dorks
- Crobat API
- DNSDumpster
- Sublister
- Threatcrowd
- DNSRepo
- Shodan
- ViewDNS
- RapidDNS
- Virustotal
- CVECircl
- Web-crawler (recursively discovers all links on current web-site)
- Web-techs (language, libs, styles) detect with Wappalyzer

Interface: Django + pyvis for visualization:
![image](https://github.com/tntwkuf/attack-surface-management-tool/assets/49122588/65ac9f55-daec-4b4a-95b7-e26dfddea78d)

![image](https://github.com/tntwkuf/attack-surface-management-tool/assets/49122588/f5ee7354-159f-4009-9aa8-c207bb42dbc4)

![image](https://github.com/tntwkuf/attack-surface-management-tool/assets/49122588/e7f58cb8-d8d1-44b2-9144-f7a4339fabd3)

![image](https://github.com/tntwkuf/attack-surface-management-tool/assets/49122588/cc8a2733-77ef-4c00-a127-c47c70d8ec36)

![image](https://github.com/tntwkuf/attack-surface-management-tool/assets/49122588/ad262186-2e46-4fc7-a01b-a2b94b676e66)

TODO List:
- Add CMS scan (wpscan etc);
- Add Censys module
- Add Atlas.io module
- Add vuln scan
- Add fuzzing
- Add multiprocessing
