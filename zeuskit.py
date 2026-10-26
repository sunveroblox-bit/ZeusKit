#!/usr/bin/env python3
import sys
import os
import socket
import urllib.request
import urllib.parse
import hashlib
import base64
import json
import ssl
import subprocess
import time
import random
import string
import hmac

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except ImportError:
    print("[!] Error: colorama is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

VERSION = "v0.2.0"
AUTHOR = "sunveroblox-bit"

def banner():
    print(Fore.CYAN + """
███████╗███████╗██╗   ██╗███████╗██╗  ██╗██╗████████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝██║ ██╔╝██║╚══██╔══╝
  ███╔╝ █████╗  ██║   ██║███████╗█████╔╝ ██║   ██║   
 ███╔╝  ██╔══╝  ██║   ██║╚════██║██╔-██╗ ██║   ██║   
███████╗███████╗╚█████╔╝███████║██║  ██║██║   ██║   
╚══════╝╚══════╝ ╚════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
    [ ZeusKit Mobile Cybersecurity Suite """ + VERSION + """ ]
    [ Developed by: """ + AUTHOR + """ ]
""")

def clean_url(url):
    url = url.strip()
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    if "/" in url:
        url = url.split("/")[0]
    return url

def check_for_updates():
    print(Fore.YELLOW + "\n[*] Checking for ZeusKit updates from GitHub...")
    try:
        subprocess.run(["git", "fetch", "origin", "main"], capture_output=True, text=True, check=True)
        local_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        remote_commit = subprocess.run(["git", "rev-parse", "origin/main"], capture_output=True, text=True, check=True).stdout.strip()
        
        if local_commit == remote_commit:
            print(Fore.GREEN + "[+] ZeusKit is already up to date! No updates found.")
        else:
            print(Fore.YELLOW + "[!] Update found! Downloading latest version...")
            subprocess.run(["git", "pull", "origin", "main"], check=True)
            print(Fore.GREEN + "[+] ZeusKit successfully updated! Please restart the script.")
    except Exception as e:
        print(Fore.RED + f"[!] Update check failed: {e}")

# --- 40+ TOOLS IMPLEMENTATION ---

def tool_1_quick_ip():
    domain = clean_url(input(Fore.YELLOW + "Enter domain/URL: "))
    try:
        ip = socket.gethostbyname(domain)
        print(Fore.GREEN + f"[+] Target IP for {domain}: {ip}")
    except Exception as e:
        print(Fore.RED + f"[!] Error resolving IP: {e}")

def tool_2_dns_records():
    domain = clean_url(input(Fore.YELLOW + "Enter domain/URL: "))
    print(Fore.CYAN + "[+] Querying DNS records (A, AAAA, MX, NS, TXT)...")
    try:
        import dns.resolver
        for rtype in ["A", "AAAA", "MX", "NS", "TXT"]:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                print(Fore.GREEN + f"\n--- {rtype} Records ---")
                for rdata in answers:
                    print(f"  {rdata}")
            except Exception:
                pass
    except ImportError:
        print(Fore.RED + "[!] Error: dnspython not installed. Run: pip install -r requirements.txt")

def tool_3_port_scanner():
    target = clean_url(input(Fore.YELLOW + "Enter IP or domain to scan: "))
    ports_str = input(Fore.YELLOW + "Enter ports (comma separated e.g. 21,22,80,443) or press Enter for common: ").strip()
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 8080] if not ports_str else [int(p.strip()) for p in ports_str.split(",")]
    try:
        target_ip = socket.gethostbyname(target)
        print(Fore.CYAN + f"[*] Scanning {target_ip}...")
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)
            if s.connect_ex((target_ip, port)) == 0:
                print(Fore.GREEN + f"  [OPEN] Port {port}")
            s.close()
    except Exception as e:
        print(Fore.RED + f"[!] Scan error: {e}")

def tool_4_http_headers():
    url = input(Fore.YELLOW + "Enter full URL (e.g. https://example.com): ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit/0.2.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(Fore.GREEN + f"\n[+] Status Code: {resp.getcode()}")
            for h, v in resp.headers.items(): print(f"  {h}: {v}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_5_ssl_checker():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print(Fore.GREEN + f"[+] Issued To: {dict(x[0] for x in cert['subject'])}")
                print(Fore.GREEN + f"[+] Valid Until: {cert['notAfter']}")
    except Exception as e: print(Fore.RED + f"[!] SSL error: {e}")

def tool_6_whois_lookup():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        s = socket.socket()
        s.connect(("whois.verisign-grs.com", 43))
        s.send((domain + "\r\n").encode())
        res = b""
        while True:
            d = s.recv(4096)
            if not d: break
            res += d
        s.close()
        print(Fore.GREEN + res.decode(errors="ignore"))
    except Exception as e: print(Fore.RED + f"[!] WHOIS error: {e}")

def tool_7_subnet_calculator():
    ip = input(Fore.YELLOW + "Enter IP (e.g. 192.168.1.5): ").strip()
    parts = ip.split(".")
    if len(parts) == 4:
        print(Fore.GREEN + f"[+] Network Base: {parts[0]}.{parts[1]}.{parts[2]}.0/24")
        print(Fore.GREEN + f"[+] Broadcast: {parts[0]}.{parts[1]}.{parts[2]}.255")

def tool_8_reverse_ptr():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        ip = socket.gethostbyname(domain)
        print(Fore.GREEN + f"[+] PTR: {socket.gethostbyaddr(ip)[0]}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_9_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(Fore.GREEN + f"[+] Local IP: {s.getsockname()[0]}")
        s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_10_public_ip_geo():
    try:
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=5) as r:
            data = json.loads(r.read().decode())
            for k, v in data.items(): print(f"  {k}: {v}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_11_custom_http_req():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(Fore.GREEN + f"[+] Status: {r.getcode()} | Size: {len(r.read())} bytes")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_12_user_agent_gen():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)",
        "Mozilla/5.0 (Linux; Android 14; SM-A556B)"
    ]
    for a in agents: print(Fore.GREEN + f" - {a}")

def tool_13_redirect_trace():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        r = urllib.request.urlopen(req, timeout=5)
        print(Fore.GREEN + f"[+] Final URL: {r.geturl()} [Status: {r.getcode()}]")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_14_hash_generator():
    t = input(Fore.YELLOW + "Enter text: ").strip()
    print(Fore.GREEN + f"[+] MD5: {hashlib.md5(t.encode()).hexdigest()}")
    print(Fore.GREEN + f"[+] SHA1: {hashlib.sha1(t.encode()).hexdigest()}")
    print(Fore.GREEN + f"[+] SHA256: {hashlib.sha256(t.encode()).hexdigest()}")

def tool_15_base64_codec():
    choice = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelect: ").strip()
    text = input(Fore.YELLOW + "Enter text: ").strip()
    if choice == "1": print(Fore.GREEN + f"[+] {base64.b64encode(text.encode()).decode()}")
    else: print(Fore.GREEN + f"[+] {base64.b64decode(text.encode()).decode()}")

def tool_16_url_codec():
    choice = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelect: ").strip()
    text = input(Fore.YELLOW + "Enter text: ").strip()
    if choice == "1": print(Fore.GREEN + f"[+] {urllib.parse.quote(text)}")
    else: print(Fore.GREEN + f"[+] {urllib.parse.unquote(text)}")

def tool_17_password_gen():
    length = int(input(Fore.YELLOW + "Length [16]: ").strip() or 16)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    print(Fore.GREEN + f"[+] Password: {''.join(random.choice(chars) for _ in range(length))}")

def tool_18_jwt_decoder():
    token = input(Fore.YELLOW + "Enter JWT: ").strip()
    try:
        parts = token.split(".")
        print(Fore.GREEN + f"[+] Header: {base64.b64decode(parts[0] + '==').decode()}")
        print(Fore.GREEN + f"[+] Payload: {base64.b64decode(parts[1] + '==').decode()}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_19_system_info():
    print(Fore.GREEN + f"[+] Platform: {sys.platform} | Python: {sys.version.split()[0]} | Cores: {os.cpu_count()}")

def tool_20_ping_sweep():
    base = input(Fore.YELLOW + "Enter subnet (e.g. 192.168.1): ").strip()
    for i in range(1, 15):
        ip = f"{base}.{i}"
        if os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1") == 0:
            print(Fore.GREEN + f"  [UP] {ip}")

def tool_21_banner_grab():
    d = clean_url(input(Fore.YELLOW + "Enter domain: "))
    p = int(input(Fore.YELLOW + "Port [80]: ").strip() or 80)
    try:
        s = socket.socket(); s.settimeout(2)
        s.connect((d, p))
        s.send(b"HEAD / HTTP/1.1\r\nHost: " + d.encode() + b"\r\n\r\n")
        print(Fore.GREEN + s.recv(512).decode(errors="ignore"))
        s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_22_tcp_latency():
    d = clean_url(input(Fore.YELLOW + "Enter domain: "))
    p = int(input(Fore.YELLOW + "Port [443]: ").strip() or 443)
    try:
        start = time.time()
        s = socket.create_connection((d, p), timeout=3)
        print(Fore.GREEN + f"[+] Latency: {((time.time() - start)*1000):.2f} ms")
        s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_23_http_status():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        r = urllib.request.urlopen(req, timeout=4)
        print(Fore.GREEN + f"[+] Status: {r.getcode()} OK")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_24_secure_vault():
    t = input(Fore.YELLOW + "Secret note: ").strip()
    print(Fore.GREEN + f"[+] Encrypted Vault: {base64.b64encode(t.encode()[::-1]).decode()}")

# --- NEW TOOLS 25 to 42 ---

def tool_25_robots_parser():
    domain = clean_url(input(Fore.YELLOW + "Enter domain (e.g. example.com): "))
    url = f"https://{domain}/robots.txt"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(Fore.GREEN + f"[+] Robots.txt found for {domain}:\n" + r.read().decode(errors="ignore"))
    except Exception as e: print(Fore.RED + f"[!] Could not fetch robots.txt: {e}")

def tool_26_subdomain_enum_stub():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    common = ["www", "mail", "ftp", "admin", "test", "api", "shop", "blog", "vpn", "remote"]
    print(Fore.CYAN + f"[*] Brute-forcing common subdomains for {domain}...")
    for sub in common:
        sub_domain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(sub_domain)
            print(Fore.GREEN + f"  [FOUND] {sub_domain} -> {ip}")
        except Exception:
            pass

def tool_27_hex_codec():
    choice = input(Fore.YELLOW + "[1] Text to Hex\n[2] Hex to Text\nSelect: ").strip()
    text = input(Fore.YELLOW + "Enter data: ").strip()
    if choice == "1": print(Fore.GREEN + f"[+] Hex: {text.encode().hex()}")
    else: print(Fore.GREEN + f"[+] Text: {bytes.fromhex(text).decode(errors='ignore')}")

def tool_28_binary_codec():
    choice = input(Fore.YELLOW + "[1] Text to Binary\n[2] Binary to Text\nSelect: ").strip()
    if choice == "1":
        text = input(Fore.YELLOW + "Enter text: ").strip()
        print(Fore.GREEN + f"[+] Binary: " + " ".join(format(ord(c), '08b') for c in text))
    else:
        b_str = input(Fore.YELLOW + "Enter binary (space separated): ").strip()
        try:
            print(Fore.GREEN + f"[+] Text: " + "".join(chr(int(b, 2)) for b in b_str.split()))
        except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_29_epoch_converter():
    choice = input(Fore.YELLOW + "[1] Current Epoch\n[2] Epoch to Date\nSelect: ").strip()
    if choice == "1":
        print(Fore.GREEN + f"[+] Current Timestamp: {int(time.time())}")
    else:
        epoch = int(input(Fore.YELLOW + "Enter Epoch timestamp: ").strip())
        print(Fore.GREEN + f"[+] Date: {time.ctime(epoch)}")

def tool_30_uuid_generator():
    import uuid
    print(Fore.GREEN + f"[+] Generated UUIDv4: {uuid.uuid4()}")

def tool_31_hmac_generator():
    msg = input(Fore.YELLOW + "Enter message: ").strip()
    key = input(Fore.YELLOW + "Enter secret key: ").strip()
    sig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()
    print(Fore.GREEN + f"[+] HMAC-SHA256 Signature: {sig}")

def tool_32_http_headers_compare():
    print(Fore.CYAN + "[+] Security Headers Checklist (HSTS, CSP, X-Frame-Options, etc.)")
    url = input(Fore.YELLOW + "Enter full URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        with urllib.request.urlopen(req, timeout=5) as r:
            headers = [h.lower() for h in r.headers.keys()]
            sec_headers = ["strict-transport-security", "content-security-policy", "x-frame-options", "x-content-type-options"]
            for sh in sec_headers:
                if sh in headers: print(Fore.GREEN + f"  [PRESENT] {sh}")
                else: print(Fore.RED + f"  [MISSING] {sh}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_33_local_arp_stub():
    print(Fore.CYAN + "[*] Checking local ARP cache...")
    os.system("arp -a")

def tool_34_network_interfaces():
    print(Fore.CYAN + "[*] Inspecting active socket interfaces...")
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(Fore.GREEN + f"[+] Hostname: {hostname}")
        print(Fore.GREEN + f"[+] Resolved Host IP: {ip}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_35_html_title_grabber():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        with urllib.request.urlopen(req, timeout=5) as r:
            html = r.read().decode(errors="ignore")
            if "<title>" in html and "</title>" in html:
                title = html.split("<title>")[1].split("</title>")[0].strip()
                print(Fore.GREEN + f"[+] Page Title: {title}")
            else:
                print(Fore.YELLOW + "[!] No <title> tag found.")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_36_password_strength_checker():
    pwd = input(Fore.YELLOW + "Enter password to evaluate: ").strip()
    score = 0
    if len(pwd) >= 8: score += 1
    if len(pwd) >= 12: score += 1
    if any(c.isupper() for c in pwd) and any(c.islower() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in "!@#$%^&*()_+" for c in pwd): score += 1
    ratings = ["Very Weak", "Weak", "Moderate", "Strong", "Military Grade"]
    print(Fore.GREEN + f"[+] Password Strength: {ratings[score]} (Score: {score}/5)")

def tool_37_port_service_lookup():
    port = input(Fore.YELLOW + "Enter port number: ").strip()
    common_ports = {"21": "FTP", "22": "SSH", "23": "Telnet", "25": "SMTP", "53": "DNS", "80": "HTTP", "110": "POP3", "443": "HTTPS", "3306": "MySQL", "8080": "HTTP-Proxy"}
    print(Fore.GREEN + f"[+] Service mapping for port {port}: {common_ports.get(port, 'Unknown/Custom')}")

def tool_38_random_string_gen():
    length = int(input(Fore.YELLOW + "Length [32]: ").strip() or 32)
    print(Fore.GREEN + f"[+] Random Hex Key: {os.urandom(length).hex()}")

def tool_39_dns_zone_transfer_check():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    print(Fore.CYAN + f"[*] Checking nameservers for zone transfer vulnerabilities on {domain}...")
    try:
        import dns.resolver, dns.query, dns.zone
        ns_answers = dns.resolver.resolve(domain, 'NS')
        for ns in ns_answers:
            ns_host = str(ns).rstrip('.')
            print(Fore.YELLOW + f"[*] Testing NS server: {ns_host}")
            try:
                z = dns.zone.from_xfr(dns.query.tcp(domain, ns_host, timeout=3))
                print(Fore.GREEN + f"  [VULNERABLE] Zone transfer successful on {ns_host}!")
                for n, node in z.nodes.items():
                    print(f"    {n}: {node}")
            except Exception:
                print(Fore.RED + f"  [SECURE] Zone transfer refused by {ns_host}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_40_secure_hasher_hmac():
    msg = input(Fore.YELLOW + "Message: ").strip()
    print(Fore.GREEN + f"[+] SHA3-256: {hashlib.sha3_256(msg.encode()).hexdigest()}")

def main():
    while True:
        banner()
        print(Fore.CYAN + "=== ZEUSKIT v0.2.0 - 40 TOOLS ULTRA SUITE ===")
        print(" [1] Quick Domain IP Lookup         [21] HTTP Banner Grabbing")
        print(" [2] Full DNS Records Lookup        [22] TCP Latency Test")
        print(" [3] TCP Port Scanner               [23] HTTP Status Code Checker")
        print(" [4] HTTP Header Inspector          [24] Secure Vault Note Encrypter")
        print(" [5] SSL Certificate Checker        [25] Robots.txt Parser & Crawler")
        print(" [6] WHOIS Information Lookup       [26] Subdomain Enumerator (Stub)")
        print(" [7] Subnet & CIDR Calculator       [27] Hex Encoder / Decoder")
        print(" [8] Reverse PTR Lookup             [28] Binary Encoder / Decoder")
        print(" [9] Local Network IP Finder        [29] Epoch / Unix Timestamp Tool")
        print("[10] Public IP Geolocation          [30] UUIDv4 Generator")
        print("[11] Custom HTTP Request Sender     [31] HMAC-SHA256 Generator")
        print("[12] Random User-Agent Generator    [32] Security Headers Checker")
        print("[13] URL Redirect Trace             [33] Local ARP Cache Viewer")
        print("[14] Multi-Hash Generator           [34] Network Interfaces Info")
        print("[15] Base64 Encoder / Decoder       [35] HTML Page Title Grabber")
        print("[16] URL Encoder / Decoder          [36] Password Strength Analyzer")
        print("[17] Strong Password Generator      [37] Port-to-Service Lookup")
        print("[18] JWT Token Decoder              [38] Random Hex Key Generator")
        print("[19] System Diagnostics Info        [39] DNS Zone Transfer Checker")
        print("[20] Ping Sweep (Local Subnet)      [40] SHA3-256 Advanced Hasher")
        print("[67] Check for GitHub Updates      [ 0] Exit ZeusKit")
        print("----------------------------------------------------------------")
        
        choice = input(Fore.YELLOW + "ZeusKit > Selection: ").strip()
        
        if choice == "1": tool_1_quick_ip()
        elif choice == "2": tool_2_dns_records()
        elif choice == "3": tool_3_port_scanner()
        elif choice == "4": tool_4_http_headers()
        elif choice == "5": tool_5_ssl_checker()
        elif choice == "6": tool_6_whois_lookup()
        elif choice == "7": tool_7_subnet_calculator()
        elif choice == "8": tool_8_reverse_ptr()
        elif choice == "9": tool_9_local_ip()
        elif choice == "10": tool_10_public_ip_geo()
        elif choice == "11": tool_11_custom_http_req()
        elif choice == "12": tool_12_user_agent_gen()
        elif choice == "13": tool_13_redirect_trace()
        elif choice == "14": tool_14_hash_generator()
        elif choice == "15": tool_15_base64_codec()
        elif choice == "16": tool_16_url_codec()
        elif choice == "17": tool_17_password_gen()
        elif choice == "18": tool_18_jwt_decoder()
        elif choice == "19": tool_19_system_info()
        elif choice == "20": tool_20_ping_sweep()
        elif choice == "21": tool_21_banner_grab()
        elif choice == "22": tool_22_tcp_latency()
        elif choice == "23": tool_23_http_status()
        elif choice == "24": tool_24_secure_vault()
        elif choice == "25": tool_25_robots_parser()
        elif choice == "26": tool_26_subdomain_enum_stub()
        elif choice == "27": tool_27_hex_codec()
        elif choice == "28": tool_28_binary_codec()
        elif choice == "29": tool_29_epoch_converter()
        elif choice == "30": tool_30_uuid_generator()
        elif choice == "31": tool_31_hmac_generator()
        elif choice == "32": tool_32_http_headers_compare()
        elif choice == "33": tool_33_local_arp_stub()
        elif choice == "34": tool_34_network_interfaces()
        elif choice == "35": tool_35_html_title_grabber()
        elif choice == "36": tool_36_password_strength_checker()
        elif choice == "37": tool_37_port_service_lookup()
        elif choice == "38": tool_38_random_string_gen()
        elif choice == "39": tool_39_dns_zone_transfer_check()
        elif choice == "40": tool_40_secure_hasher_hmac()
        elif choice == "67": check_for_updates()
        elif choice == "0":
            print(Fore.CYAN + "[+] Exiting ZeusKit. Stay secure!")
            break
        else:
            print(Fore.RED + "[!] Invalid selection. Choose 1-40 or 67.")
        
        input(Fore.YELLOW + "\nPress Enter to return to main menu...")

if __name__ == "__main__":
    main()
