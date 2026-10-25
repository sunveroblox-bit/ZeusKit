import os
import subprocess
import sys
import time
import socket
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import defaultdict
import threading

request_history = defaultdict(list)
history_lock = threading.Lock()
RATE_LIMIT_WINDOW = 5
MAX_REQUESTS_PER_WINDOW = 3

SERVER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white p-8 rounded-xl shadow-md max-w-sm w-full border border-gray-200">
        <div class="text-center mb-6">
            <h1 class="text-2xl font-bold text-gray-800">Local Portal</h1>
            <p class="text-xs text-gray-500 mt-1">Protected by Rate-Limiting Defense</p>
        </div>
        <form onsubmit="handleLogin(event)" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                <input type="text" id="username" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input type="password" id="password" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg transition duration-200">Log In</button>
        </form>
        <div id="status-msg" class="mt-4 text-center text-sm hidden p-2 rounded-lg"></div>
    </div>
    <script>
        function handleLogin(event) {
            event.preventDefault();
            const statusDiv = document.getElementById('status-msg');
            statusDiv.classList.remove('hidden', 'bg-red-100', 'text-red-700', 'bg-green-100', 'text-green-700');
            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${encodeURIComponent(document.getElementById('username').value)}`
            })
            .then(res => {
                if (res.status === 429) {
                    statusDiv.innerText = "Error 429: Too Many Requests (Rate Limited)";
                    statusDiv.classList.add('bg-red-100', 'text-red-700');
                } else {
                    statusDiv.innerText = "Request Processed Successfully";
                    statusDiv.classList.add('bg-green-100', 'text-green-700');
                }
            })
            .catch(() => {
                statusDiv.innerText = "Connection Error";
                statusDiv.classList.add('bg-red-100', 'text-red-700');
            });
        }
    </script>
</body>
</html>
"""

class RateLimitedHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} - {args[0]}")
    def is_rate_limited(self):
        client_ip = self.client_address[0]
        now = time.time()
        with history_lock:
            timestamps = [t for t in request_history[client_ip] if now - t < RATE_LIMIT_WINDOW]
            request_history[client_ip] = timestamps
            if len(timestamps) >= MAX_REQUESTS_PER_WINDOW:
                return True
            request_history[client_ip].append(now)
            return False
    def do_GET(self):
        if self.is_rate_limited():
            self.send_response(429)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"429 Too Many Requests: Rate limit exceeded.")
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(SERVER_HTML.encode('utf-8'))
    def do_POST(self):
        if self.is_rate_limited():
            self.send_response(429)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"429 Too Many Requests")
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Success")

def run_server(port=6700):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RateLimitedHandler)
    print(f"[+] Defensive Web Server running on port {port}...")
    print(f"[+] Rate Limit Rule: Max {MAX_REQUESTS_PER_WINDOW} requests every {RATE_LIMIT_WINDOW} seconds per IP.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Shutting down server.")
        httpd.server_close()

def banner():
    print(r"""
    ███████╗███████╗H   ██╗███████╗██╗  ██╗██╗████████╗
    ╚══███╔╝██╔════╝██╗  ██║██╔════╝██║ ██╔╝██║╚══██╔══╝
      ███╔╝ █████╗  ██║  ██║███████╗█████╔╝ ██║   ██║   
     ███╔╝  ██╔══╝  ██║  ██║╚════██║██╔-██╗ ██║   ██║   
    ███████╗███████╗╚█████╔╝███████║██║  ██╗██║   ██║   
    ╚══════╝╚══════╝ ╚════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   
        [ ZeusKit Mobile Cybersecurity Suite v0.0.7 ]
    """)

def nmap_menu():
    while True:
        os.system('clear')
        banner()
        print("    === NMAP RECONNAISSANCE & INSTRUCTION SUITE ===")
        print("    [1] Basic Port Scan        -> nmap <target>")
        print("    [2] Service Version Scan   -> nmap -sV <target>")
        print("    [3] Aggressive Scan        -> nmap -A <target>")
        print("    [4] Custom Port Scan       -> nmap -p <port> <target>")
        print("    [0] Back to Main Menu")
        print("-" * 55)
        choice = input("ZeusKit/Nmap > Selection: ").strip()
        
        if choice == '1':
            target = input("Enter target IP (default 127.0.0.1): ").strip() or "127.0.0.1"
            cmd = f"nmap {target}"
            print(f"\n[MANUAL INSTRUCTION] Command: {cmd}")
            print("[INFO] Runs a default TCP port scan against the target IP.\n")
            subprocess.run(cmd.split())
            input("\nPress Enter to continue...")
        elif choice == '2':
            target = input("Enter target IP (default 127.0.0.1): ").strip() or "127.0.0.1"
            cmd = f"nmap -sV {target}"
            print(f"\n[MANUAL INSTRUCTION] Command: {cmd}")
            print("[INFO] The -sV flag probes open ports to determine service and version info.\n")
            subprocess.run(cmd.split())
            input("\nPress Enter to continue...")
        elif choice == '3':
            target = input("Enter target IP (default 127.0.0.1): ").strip() or "127.0.0.1"
            cmd = f"nmap -A {target}"
            print(f"\n[MANUAL INSTRUCTION] Command: {cmd}")
            print("[INFO] The -A flag enables OS detection, version detection, script scanning, and traceroute.\n")
            subprocess.run(cmd.split())
            input("\nPress Enter to continue...")
        elif choice == '4':
            target = input("Enter target IP (default 127.0.0.1): ").strip() or "127.0.0.1"
            port = input("Enter port number (e.g. 6700): ").strip() or "6700"
            cmd = f"nmap -p {port} {target}"
            print(f"\n[MANUAL INSTRUCTION] Command: {cmd}")
            print("[INFO] The -p flag restricts the scan to a specific port instead of scanning all common ports.\n")
            subprocess.run(cmd.split())
            input("\nPress Enter to continue...")
        elif choice == '0':
            break

def server_menu():
    while True:
        os.system('clear')
        banner()
        print("    === WEB SERVER & DEFENSE SUITE ===")
        print("    [1] Start Rate-Limited Server (Port 6700)")
        print("    [2] Start Rate-Limited Server (Custom Port)")
        print("    [0] Back to Main Menu")
        print("-" * 50)
        choice = input("ZeusKit/Server > Selection: ").strip()
        
        if choice == '1':
            run_server(6700)
            input("\nServer stopped. Press Enter to continue...")
        elif choice == '2':
            port_input = input("Enter custom port: ").strip()
            if port_input.isdigit():
                run_server(int(port_input))
            input("\nServer stopped. Press Enter to continue...")
        elif choice == '0':
            break

def network_menu():
    while True:
        os.system('clear')
        banner()
        print("    === NETWORK & RECON TOOLS ===")
        print("    [1] View Network Interfaces (ifconfig)")
        print("    [2] View Active Sockets (netstat)")
        print("    [0] Back to Main Menu")
        print("-" * 50)
        choice = input("ZeusKit/Network > Selection: ").strip()
        
        if choice == '1':
            print("\n[MANUAL INSTRUCTION] Command: ifconfig\n")
            subprocess.run(["ifconfig"])
            input("\nPress Enter to continue...")
        elif choice == '2':
            print("\n[MANUAL INSTRUCTION] Command: netstat -tuln\n")
            subprocess.run(["netstat", "-tuln"])
            input("\nPress Enter to continue...")
        elif choice == '0':
            break

def clean_domain(raw_input):
    domain = raw_input.strip()
    if "://" in domain:
        domain = domain.split("://")[1]
    domain = domain.split("/")[0]
    return domain

def dns_menu():
    while True:
        os.system('clear')
        banner()
        print("    === DNS FINDER & RESOLUTION SUITE ===")
        print("    [1] Quick Domain to IP Lookup (socket)")
        print("    [2] Full DNS Records Lookup (nslookup)")
        print("    [0] Back to Main Menu")
        print("-" * 50)
        choice = input("ZeusKit/DNS > Selection: ").strip()
        
        if choice == '1':
            raw_input = input("Enter domain or URL (e.g. swis.montfort.ac.th): ").strip()
            if raw_input:
                domain = clean_domain(raw_input)
                print(f"\n[INFO] Cleaned target: {domain}")
                print(f"[INFO] Resolving IP address via Python socket...\n")
                try:
                    ip = socket.gethostbyname(domain)
                    print(f"[+] Resolved IP Address: {ip}")
                except socket.gaierror:
                    print(f"[-] Could not resolve domain '{domain}' via socket.")
            input("\nPress Enter to continue...")
        elif choice == '2':
            raw_input = input("Enter domain or URL (e.g. swis.montfort.ac.th): ").strip()
            if raw_input:
                domain = clean_domain(raw_input)
                cmd = f"nslookup {domain}"
                print(f"\n[INFO] Cleaned target: {domain}")
                print(f"[MANUAL INSTRUCTION] Command: {cmd}\n")
                subprocess.run(["nslookup", domain])
            input("\nPress Enter to continue...")
        elif choice == '0':
            break

def send_stress_request(url):
    try:
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0

def stress_test_menu():
    while True:
        os.system('clear')
        banner()
        print("    === DOS & STRESS TEST SUITE ===")
        print("    [1] Local Rate-Limit Flood Test (Port 6700)")
        print("    [2] Custom URL Stress Test")
        print("    [3] External Tools Manager & Runner (ZX-DDoS / Dos)")
        print("    [0] Back to Main Menu")
        print("-" * 50)
        choice = input("ZeusKit/StressTest > Selection: ").strip()
        
        if choice == '1':
            target_port = input("Enter target port (default 6700): ").strip() or "6700"
            num_reqs = input("Enter number of requests to flood (default 10): ").strip()
            num_reqs = int(num_reqs) if num_reqs.isdigit() else 10
            
            url = f"http://127.0.0.1:{target_port}/"
            print(f"\n[MANUAL INSTRUCTION] Target: {url} | Requests: {num_reqs}")
            print("[INFO] Launching concurrent threads to test rate limiting defense (HTTP 429)...\n")
            
            success = 0
            rate_limited = 0
            other = 0
            
            def worker():
                nonlocal success, rate_limited, other
                status = send_stress_request(url)
                if status == 200:
                    success += 1
                elif status == 429:
                    rate_limited += 1
                else:
                    other += 1

            start_time = time.time()
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(lambda _: worker(), range(num_reqs))
            duration = time.time() - start_time
            
            print(f"\n[+] Stress Test Finished in {duration:.2f}s")
            print(f"    - Successful (200 OK): {success}")
            print(f"    - Rate Limited (429 Too Many Requests): {rate_limited}")
            print(f"    - Errors / Connection Fails: {other}")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            url = input("Enter target URL (e.g., http://127.0.0.1:6700): ").strip()
            if not url.startswith("http"):
                url = "http://" + url
            num_reqs = input("Enter number of requests to flood (default 10): ").strip()
            num_reqs = int(num_reqs) if num_reqs.isdigit() else 10
            
            print(f"\n[MANUAL INSTRUCTION] Target: {url} | Requests: {num_reqs}")
            success = 0
            rate_limited = 0
            other = 0
            
            def worker():
                nonlocal success, rate_limited, other
                status = send_stress_request(url)
                if status == 200:
                    success += 1
                elif status == 429:
                    rate_limited += 1
                else:
                    other += 1

            start_time = time.time()
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(lambda _: worker(), range(num_reqs))
            duration = time.time() - start_time
            
            print(f"\n[+] Stress Test Finished in {duration:.2f}s")
            print(f"    - Successful (200 OK): {success}")
            print(f"    - Rate Limited (429): {rate_limited}")
            print(f"    - Errors / Connection Fails: {other}")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            os.system('clear')
            banner()
            print("    === EXTERNAL TOOLS MANAGER & RUNNER ===")
            print("    [1] Clone & Run ZX-DDoS (MrGoofyDev)")
            print("    [2] Clone & Run BayuStore Dos (bayustore22)")
            print("    [0] Back")
            print("-" * 45)
            sub = input("ZeusKit/External > Selection: ").strip()
            
            if sub == '1':
                repo_dir = "ZX-DDoS"
                if not os.path.exists(repo_dir):
                    print(f"\n[+] Cloning {repo_dir} from GitHub...")
                    subprocess.run(["git", "clone", "https://github.com/MrGoofyDev/ZX-DDoS"])
                else:
                    print(f"\n[+] Directory '{repo_dir}' already exists.")
                
                if os.path.exists(repo_dir):
                    os.chdir(repo_dir)
                    if os.path.exists("requirements.txt"):
                        print("[+] Installing dependencies (pip install)...")
                        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                    print("[+] Launching ZX-DDoS (python3 start.py)...")
                    subprocess.run([sys.executable, "start.py"])
                    os.chdir("..")
                input("\nExecution finished. Press Enter to return to ZeusKit...")
                
            elif sub == '2':
                repo_dir = "Dos"
                if not os.path.exists(repo_dir):
                    print(f"\n[+] Cloning {repo_dir} from GitHub...")
                    subprocess.run(["git", "clone", "https://github.com/bayustore22/Dos"])
                else:
                    print(f"\n[+] Directory '{repo_dir}' already exists.")
                
                if os.path.exists(repo_dir):
                    os.chdir(repo_dir)
                    if os.path.exists("requirements.txt"):
                        print("[+] Installing dependencies (pip install)...")
                        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                    print("[+] Launching Dos framework (python3 main.py)...")
                    subprocess.run([sys.executable, "main.py"])
                    os.chdir("..")
                input("\nExecution finished. Press Enter to return to ZeusKit...")
        elif choice == '0':
            break

def main():
    while True:
        os.system('clear')
        banner()
        print("    === ZEUSKIT MAIN MENU (v0.0.7) ===")
        print("    [1] Nmap Reconnaissance Suite")
        print("    [2] Web Server & Defense Suite")
        print("    [3] Network & Recon Tools")
        print("    [4] DoS & Stress Test Suite")
        print("    [5] DNS Finder Suite")
        print("    [10] Update Details")
        print("    [0] Exit ZeusKit")
        print("-" * 50)
        choice = input("ZeusKit > Selection: ").strip()
        if choice == '1':
            nmap_menu()
        elif choice == '2':
            server_menu()
        elif choice == '3':
            network_menu()
        elif choice == '4':
            stress_test_menu()
        elif choice == '5':
            dns_menu()
        elif choice == '10':
            os.system('clear')
            banner()
            print("    === ZEUSKIT UPDATE DETAILS ===")
            print("    * Version Name: ZeusKit v0.0.7")
            print("    * Release Track: Mobile Cybersecurity Suite")
            print("    * Changelog:")
            print("      - Bumped version to v0.0.7 following update conventions.")
            print("      - Added intelligent URL parser/cleaner for DNS Finder Suite (supports https:// and paths).")
            print("      - Maintained external tool runner and rate-limit defenses.")
            print("-" * 50)
            input("\nPress Enter to return to Main Menu...")
        elif choice == '0':
            sys.exit(0)

if __name__ == '__main__':
    main()
