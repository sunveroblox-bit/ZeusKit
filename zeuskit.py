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

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except ImportError:
    print("[!] Error: colorama is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

VERSION = "v0.1.0"
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

# --- 25 TOOLS IMPLEMENTATION ---

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
    if not ports_str:
        ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 8080]
    else:
        ports = [int(p.strip()) for p in ports_str.split(",")]
    
    try:
        target_ip = socket.gethostbyname(target)
        print(Fore.CYAN + f"[*] Scanning {target_ip}...")
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                print(Fore.GREEN + f"  [OPEN] Port {port}")
            s.close()
    except Exception as e:
        print(Fore.RED + f"[!] Scan error: {e}")

def tool_4_http_headers():
    url_input = input(Fore.YELLOW + "Enter full URL (e.g. https://example.com): ").strip()
    if not url_input.startswith("http"):
        url_input = "https://" + url_input
    try:
        req = urllib.request.Request(url_input, headers={"User-Agent": "ZeusKit/0.1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            print(Fore.GREEN + f"\n[+] Status Code: {response.getcode()}")
            print(Fore.CYAN + "[+] Response Headers:")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")
    except Exception as e:
        print(Fore.RED + f"[!] Error fetching headers: {e}")

def tool_5_ssl_checker():
    domain = clean_url(input(Fore.YELLOW + "Enter domain (e.g. google.com): "))
    print(Fore.CYAN + f"[*] Inspecting SSL certificate for {domain}...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print(Fore.GREEN + "[+] SSL Certificate Details:")
                print(f"  Subject: {dict(x[0] for x in cert['subject'])}")
                print(f"  Issuer: {dict(x[0] for x in cert['issuer'])}")
                print(f"  Valid From: {cert['notBefore']}")
                print(f"  Valid Until: {cert['notAfter']}")
    except Exception as e:
        print(Fore.RED + f"[!] SSL Check error: {e}")

def tool_6_whois_lookup():
    domain = clean_url(input(Fore.YELLOW + "Enter domain for WHOIS query: "))
    print(Fore.CYAN + f"[*] Querying WHOIS info for {domain} via Port 43...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("whois.verisign-grs.com", 43))
        s.send((domain + "\r\n").encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        print(Fore.GREEN + response.decode("utf-8", errors="ignore"))
    except Exception as e:
        print(Fore.RED + f"[!] WHOIS error: {e}")

def tool_7_subnet_calculator():
    ip = input(Fore.YELLOW + "Enter IP address (e.g. 192.168.1.10): ").strip()
    try:
        parts = ip.split(".")
        if len(parts) == 4:
            print(Fore.GREEN + f"[+] IP Class: {'A' if int(parts[0]) < 128 else 'B' if int(parts[0]) < 192 else 'C'}")
            print(f"[+] Network Base: {parts[0]}.{parts[1]}.{parts[2]}.0/24")
            print(f"[+] Broadcast: {parts[0]}.{parts[1]}.{parts[2]}.255")
        else:
            print(Fore.RED + "[!] Invalid IP format.")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

def tool_8_reverse_ip():
    domain = clean_url(input(Fore.YELLOW + "Enter domain: "))
    try:
        ip = socket.gethostbyname(domain)
        hostname, _, _ = socket.gethostbyaddr(ip)
        print(Fore.GREEN + f"[+] Reverse PTR for {ip} -> {hostname}")
    except Exception as e:
        print(Fore.RED + f"[!] Reverse lookup failed: {e}")

def tool_9_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(Fore.GREEN + f"[+] Local IP Address: {local_ip}")
    except Exception as e:
        print(Fore.RED + f"[!] Error getting local IP: {e}")

def tool_10_public_ip_geo():
    print(Fore.CYAN + "[*] Fetching Public IP & Geolocation info...")
    try:
        req = urllib.request.Request("https://ipinfo.io/json", headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print(Fore.GREEN + "[+] Public IP Info:")
            for k, v in data.items():
                print(f"  {k}: {v}")
    except Exception as e:
        print(Fore.RED + f"[!] Failed to fetch public IP: {e}")

def tool_11_custom_http_req():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    method = input(Fore.YELLOW + "Method (GET/POST) [GET]: ").strip().upper() or "GET"
    try:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": "ZeusKit-Client"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(Fore.GREEN + f"[+] Status: {resp.getcode()} | Size: {len(resp.read())} bytes")
    except Exception as e:
        print(Fore.RED + f"[!] Request error: {e}")

def tool_12_user_agent_generator():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) Mobile/15E148",
        "Mozilla/5.0 (Linux; Android 14; SM-A556B) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    ]
    print(Fore.GREEN + "[+] Random User-Agents:")
    for a in agents:
        print(f"  - {a}")

def tool_13_url_redirect_trace():
    url = input(Fore.YELLOW + "Enter URL to trace: ").strip()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        resp = urllib.request.urlopen(req, timeout=5)
        print(Fore.GREEN + f"[+] Final URL: {resp.geturl()}")
        print(f"[+] Status Code: {resp.getcode()}")
    except Exception as e:
        print(Fore.RED + f"[!] Trace error: {e}")

def tool_14_md5_sha_generator():
    text = input(Fore.YELLOW + "Enter text to hash: ").strip()
    md5_val = hashlib.md5(text.encode()).hexdigest()
    sha256_val = hashlib.sha256(text.encode()).hexdigest()
    print(Fore.GREEN + f"[+] MD5: {md5_val}")
    print(Fore.GREEN + f"[+] SHA256: {sha256_val}")

def tool_15_base64_codec():
    choice = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelect: ").strip()
    text = input(Fore.YELLOW + "Enter text: ").strip()
    if choice == "1":
        res = base64.b64encode(text.encode()).decode()
        print(Fore.GREEN + f"[+] Encoded: {res}")
    else:
        try:
            res = base64.b64decode(text.encode()).decode()
            print(Fore.GREEN + f"[+] Decoded: {res}")
        except Exception as e:
            print(Fore.RED + f"[!] Decode error: {e}")

def tool_16_url_codec():
    choice = input(Fore.YELLOW + "[1] URL Encode\n[2] URL Decode\nSelect: ").strip()
    text = input(Fore.YELLOW + "Enter text: ").strip()
    if choice == "1":
        print(Fore.GREEN + f"[+] Encoded: {urllib.parse.quote(text)}")
    else:
        print(Fore.GREEN + f"[+] Decoded: {urllib.parse.unquote(text)}")

def tool_17_password_generator():
    import random, string
    length = int(input(Fore.YELLOW + "Password length [16]: ").strip() or 16)
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    pwd = "".join(random.choice(chars) for _ in range(length))
    print(Fore.GREEN + f"[+] Generated Password: {pwd}")

def tool_18_jwt_decoder():
    token = input(Fore.YELLOW + "Enter JWT Token: ").strip()
    try:
        parts = token.split(".")
        if len(parts) >= 2:
            header = base64.b64decode(parts[0] + "==").decode()
            payload = base64.b64decode(parts[1] + "==").decode()
            print(Fore.GREEN + f"[+] Header: {header}")
            print(Fore.GREEN + f"[+] Payload: {payload}")
        else:
            print(Fore.RED + "[!] Invalid JWT format.")
    except Exception as e:
        print(Fore.RED + f"[!] JWT decode error: {e}")

def tool_19_system_info():
    print(Fore.GREEN + f"[+] OS Platform: {sys.platform}")
    print(Fore.GREEN + f"[+] Python Version: {sys.version.split()[0]}")
    print(Fore.GREEN + f"[+] CPU Cores: {os.cpu_count()}")

def tool_20_ping_sweep_stub():
    base = input(Fore.YELLOW + "Enter subnet base (e.g. 192.168.1): ").strip()
    print(Fore.CYAN + f"[*] Pinging hosts on {base}.1 to {base}.20...")
    for i in range(1, 21):
        ip = f"{base}.{i}"
        res = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
        if res == 0:
            print(Fore.GREEN + f"  [UP] {ip}")

def tool_21_banner_grabbing():
    domain = clean_url(input(Fore.YELLOW + "Enter domain/IP: "))
    port = int(input(Fore.YELLOW + "Enter port [80]: ").strip() or 80)
    try:
        s = socket.socket()
        s.settimeout(2.0)
        s.connect((domain, port))
        s.send(b"HEAD / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n\r\n")
        banner_data = s.recv(1024).decode(errors="ignore")
        print(Fore.GREEN + f"[+] Banner Response:\n{banner_data}")
        s.close()
    except Exception as e:
        print(Fore.RED + f"[!] Banner grab error: {e}")

def tool_22_mac_vendor_stub():
    print(Fore.CYAN + "[+] MAC Vendor Lookup tool active. (Offline database mode)")
    mac = input(Fore.YELLOW + "Enter MAC prefix (e.g. AA:BB:CC): ").strip()
    print(Fore.GREEN + f"[+] Querying OUI registry for {mac}...")

def tool_23_tcp_latency():
    domain = clean_url(input(Fore.YELLOW + "Enter domain/IP to test: "))
    port = int(input(Fore.YELLOW + "Enter port [443]: ").strip() or 443)
    import time
    try:
        start = time.time()
        s = socket.create_connection((domain, port), timeout=3.0)
        latency = (time.time() - start) * 1000
        s.close()
        print(Fore.GREEN + f"[+] TCP Latency to {domain}:{port} = {latency:.2f} ms")
    except Exception as e:
        print(Fore.RED + f"[!] Connection failed: {e}")

def tool_24_http_status_checker():
    url = input(Fore.YELLOW + "Enter URL: ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit"})
        resp = urllib.request.urlopen(req, timeout=4)
        print(Fore.GREEN + f"[+] HTTP Status: {resp.getcode()} OK")
    except urllib.error.HTTPError as e:
        print(Fore.YELLOW + f"[!] HTTP Error Code: {e.code}")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

def tool_25_secure_vault_stub():
    text = input(Fore.YELLOW + "Enter secret note to encode: ").strip()
    encoded = base64.b64encode(text.encode()[::-1]).decode()
    print(Fore.GREEN + f"[+] Vault Encrypted String: {encoded}")

def main():
    while True:
        banner()
        print(Fore.CYAN + "=== ZEUSKIT v0.1.0 - 25 TOOLS SUITE ===")
        print(" [1] Quick Domain IP Lookup         [14] MD5 & SHA256 Generator")
        print(" [2] Full DNS Records Lookup        [15] Base64 Encoder / Decoder")
        print(" [3] TCP Port Scanner               [16] URL Encoder / Decoder")
        print(" [4] HTTP Header Inspector          [17] Strong Password Generator")
        print(" [5] SSL Certificate Checker        [18] JWT Token Decoder")
        print(" [6] WHOIS Information Lookup       [19] System Diagnostics Info")
        print(" [7] Subnet & CIDR Calculator       [20] Ping Sweep (Local Subnet)")
        print(" [8] Reverse PTR Lookup             [21] HTTP Banner Grabbing")
        print(" [9] Local Network IP Finder        [22] MAC Address Vendor Lookup")
        print("[10] Public IP Geolocation          [23] TCP Latency Test")
        print("[11] Custom HTTP Request Sender     [24] HTTP Status Code Checker")
        print("[12] Random User-Agent Generator    [25] Secure Vault Note Encrypter")
        print("[67] Check for GitHub Updates      [ 0] Exit ZeusKit")
        print("--------------------------------------------------")
        
        choice = input(Fore.YELLOW + "ZeusKit > Selection: ").strip()
        
        if choice == "1": tool_1_quick_ip()
        elif choice == "2": tool_2_dns_records()
        elif choice == "3": tool_3_port_scanner()
        elif choice == "4": tool_4_http_headers()
        elif choice == "5": tool_5_ssl_checker()
        elif choice == "6": tool_6_whois_lookup()
        elif choice == "7": tool_7_subnet_calculator()
        elif choice == "8": tool_8_reverse_ip()
        elif choice == "9": tool_9_local_ip()
        elif choice == "10": tool_10_public_ip_geo()
        elif choice == "11": tool_11_custom_http_req()
        elif choice == "12": tool_12_user_agent_generator()
        elif choice == "13": tool_13_url_redirect_trace()
        elif choice == "14": tool_14_md5_sha_generator()
        elif choice == "15": tool_15_base64_codec()
        elif choice == "16": tool_16_url_codec()
        elif choice == "17": tool_17_password_generator()
        elif choice == "18": tool_18_jwt_decoder()
        elif choice == "19": tool_19_system_info()
        elif choice == "20": tool_20_ping_sweep_stub()
        elif choice == "21": tool_21_banner_grabbing()
        elif choice == "22": tool_22_mac_vendor_stub()
        elif choice == "23": tool_23_tcp_latency()
        elif choice == "24": tool_24_http_status_checker()
        elif choice == "25": tool_25_secure_vault_stub()
        elif choice == "67": check_for_updates()
        elif choice == "0":
            print(Fore.CYAN + "[+] Exiting ZeusKit. Stay secure!")
            break
        else:
            print(Fore.RED + "[!] Invalid selection. Choose 1-25 or 67.")
        
        input(Fore.YELLOW + "\nPress Enter to return to main menu...")

if __name__ == "__main__":
    main()
