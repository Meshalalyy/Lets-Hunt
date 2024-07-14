import socket
import dns.resolver
import requests
import whois
import subprocess
from datetime import datetime
import re

def get_ip_address(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "Unable to retrieve IP address"

def print_heading(heading):
    print("\n" + "\033[31m" + "\033[1m" + heading + "\033[0m" + "\n")

def print_separator():
    print("=" * 40)

def get_dns_records(domain):
    dns_records = {}
    for qtype in ["A", "AAAA", "MX", "NS", "SOA", "TXT", "CNAME"]:
        try:
            answers = dns.resolver.resolve(domain, qtype)
            dns_records[qtype] = [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
            dns_records[qtype] = []
    return dns_records

def get_server_details(domain):
    try:
        response = requests.get(f"http://{domain}")
        server_details = {
            "web_server": response.headers.get("Server"),
            "operating_system": response.headers.get("X-Powered-By"),
            "http_headers": dict(response.headers)
        }
        return server_details
    except requests.exceptions.RequestException:
        return {"web_server": None, "operating_system": None, "http_headers": {}}

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        whois_info = {
            "domain_name": w.get("domain_name"),
            "registrar": w.get("registrar"),
            "whois_server": w.get("whois_server"),
            "referral_url": w.get("referral_url"),
            "updated_date": _convert_date(w.get("updated_date")),
            "creation_date": _convert_date(w.get("creation_date")),
            "expiration_date": _convert_date(w.get("expiration_date")),
            "name_servers": w.get("name_servers"),
            "status": w.get("status"),
            "emails": w.get("emails"),
            "dnssec": w.get("dnssec")
        }
        return whois_info
    except Exception as e:
        print(f"Error fetching WHOIS using whois library: {e}")
        return fetch_whois_direct(domain)

def _convert_date(date):
    if isinstance(date, datetime):
        return date.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(date, list) and all(isinstance(d, datetime) for d in date):
        return [d.strftime('%Y-%m-%d %H:%M:%S') for d in date]
    else:
        return date

def fetch_whois_direct(domain):
    try:
        command = f"whois {domain}"
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        whois_info = parse_whois_output(output)
        return whois_info
    except subprocess.CalledProcessError as e:
        return str(e)

def parse_whois_output(output):
    whois_info = {
        "domain_name": None,
        "registrar": None,
        "whois_server": None,
        "referral_url": None,
        "updated_date": None,
        "creation_date": None,
        "expiration_date": None,
        "name_servers": None,
        "status": None,
        "emails": None,
        "dnssec": None
    }
    patterns = {
        "domain_name": r"Domain Name:\s*(.+)",
        "registrar": r"Registrar:\s*(.+)",
        "whois_server": r"Registrar WHOIS Server:\s*(.+)",
        "referral_url": r"Registrar URL:\s*(.+)",
        "updated_date": r"Updated Date:\s*(.+)",
        "creation_date": r"Creation Date:\s*(.+)",
        "expiration_date": r"Registry Expiry Date:\s*(.+)",
        "name_servers": r"Name Server:\s*(.+)",
        "status": r"Domain Status:\s*(.+)",
        "emails": r"Registrar Abuse Contact Email:\s*(.+)",
        "dnssec": r"DNSSEC:\s*(.+)"
    }
    for key, pattern in patterns.items():
        match = re.findall(pattern, output, re.IGNORECASE)
        if match:
            whois_info[key] = match if len(match) > 1 else match[0]
    return whois_info

def enumerate_subdomains(domain):
    subdomains = []
    try:
        with open("subdomains.txt", "r") as f:
            for line in f:
                subdomain = line.strip() + "." + domain
                try:
                    answers = dns.resolver.resolve(subdomain, "A")
                    for rdata in answers:
                        subdomains.append((subdomain, rdata.to_text()))
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
                    pass
    except FileNotFoundError:
        print("\033[31m\033[1m subdomains.txt file not found.\033[0m ")
    return subdomains

def port_scan(domain, ip_address):
    open_ports = []
    command = f"nmap -p 1-1024 {ip_address}"
    try:
        output = subprocess.check_output(command, shell=True)
        for line in output.decode("utf-8").splitlines():
            if "open" in line:
                port = line.split()[0]
                open_ports.append(port)
    except subprocess.CalledProcessError:
        pass
    return open_ports

def main(domain):
    print("\n\n\033[31m\033[1m Domain Information Gathering Tool\033[0m")
    print("=================================\n\n")
    
    print_heading(f"Domain: {domain}")

    print_heading("IP Address")
    ip_address = get_ip_address(domain)
    print(f"IP Address: {ip_address}\n\n")

    print_heading("DNS Records")
    dns_records = get_dns_records(domain)
    for qtype, records in dns_records.items():
        print(f" {qtype}: {', '.join(records)}\n")

    print_heading("Server Details")
    server_details = get_server_details(domain)
    print(f"\033[1m  Web Server\033[0m : {server_details.get('web_server')}\n")
    print(f"\033[1m Operating System\033[0m : {server_details.get('operating_system')}\n")
    print("\033[1m  HTTP Headers\033[0m :\n")
    for key, value in server_details.get("http_headers", {}).items():
        print(f"  {key}: {value}\n")

    whois_info = get_whois_info(domain)
    if isinstance(whois_info, dict):
        for key, value in whois_info.items():
            if isinstance(value, list):
                value = ', '.join(value)
            print(f" {key}: {value}\n")
    else:
        print(f" {whois_info}\n")

    print_heading("Subdomains")
    subdomains = enumerate_subdomains(domain)
    for subdomain, ip_address in subdomains:
        print(f"\033[1m  {subdomain}\033[0m : {ip_address}\n")

    print_heading("Open Ports")
    open_ports = port_scan(domain, ip_address)
    for port in open_ports:
        print(f" {port}\n")

if __name__ == "__main__":
    domain = input("\033[1m Enter target domain:\033[0m ")
    main(domain)
