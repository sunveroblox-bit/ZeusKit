#!/usr/bin/env python3
import sys, os, subprocess
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except ImportError:
    print("[!] Error: colorama not installed. Run: pip install colorama")
    sys.exit(1)

from modules import TOOLS, VERSION, AUTHOR, execute_tool

def banner():
    print(Fore.CYAN + f"""
███████╗███████╗██╗   ██╗███████╗██╗  ██╗██╗████████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝██║ ██╔╝██║╚══██╔══╝
  ███╔╝ █████╗  ██║   ██║███████╗█████╔╝ ██║   ██║   
 ███╔╝  ██╔══╝  ██║   ██║╚════██║██╔-██╗ ██║   ██║   
███████╗███████╗╚█████╔╝███████║██║  ██║██║   ██║   
╚══════╝╚══════╝ ╚════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
    [ ZeusKit Mobile Cybersecurity Suite {VERSION} ]
    [ Architecture: Modular Open-Source Wrapper Framework ]
""")

def global_tool_finder():
    print(Fore.CYAN + "\n=== 🔎 GLOBAL TOOL FINDER ===")
    q = input(Fore.YELLOW + "Search keyword: ").strip().lower()
    if not q: return
    matches = {tid: data for tid, data in TOOLS.items() if q in data[0].lower()}
    if matches:
        print(Fore.GREEN + f"\n[+] Found {len(matches)} match(es):")
        for tid, (name, cat) in matches.items(): print(f"  [{tid}] {name} (Suite #{cat})")
        choice = input(Fore.YELLOW + "\nEnter Tool ID to run (Enter to back): ").strip()
        if choice.isdigit() and int(choice) in matches: execute_tool(int(choice))
    else:
        print(Fore.RED + f"[-] No matches for '{q}'.")
    input(Fore.YELLOW + "\nPress Enter...")

def run_menu(title, start_id, end_id):
    while True:
        print(Fore.CYAN + f"\n=== {title} ===")
        for tid in range(start_id, end_id + 1):
            print(f" [{tid}] {TOOLS[tid][0]}")
        print(" [0] Back to Main Menu")
        c = input(Fore.YELLOW + "Selection > ").strip()
        if c.isdigit():
            val = int(c)
            if val == 0: break
            elif start_id <= val <= end_id: execute_tool(val)
            else: print(Fore.RED + "[!] Invalid ID.")

def main():
    while True:
        banner()
        print(Fore.CYAN + f"=== ZEUSKIT {VERSION} - MAIN MENU (OPEN-SOURCE WRAPPERS) ===")
        print(" [1] 🌐 Recon & Network Tools         (15 Tools)")
        print(" [2] 🔐 Code, Decode & Crypto         (15 Tools)")
        print(" [3] 🔍 Web Analysis & OSINT          (15 Tools)")
        print(" [4] ⚡ Attacking, DoS & Brute-Force  (15 Tools)")
        print(" [5] 🛠️ System Diagnostics            (15 Tools)")
        print(" [6] 🧪 Vulnerability & Injection     (10 Tools)")
        print(" [7] ☁️ Cloud, API & Mobile           ( 7 Tools)")
        print(" [8] 📡 Wireless & Custom Plugins     ( 8 Tools)")
        print(" [99] 🔎 Global Tool Finder / Search")
        print("[67] Check for GitHub Updates")
        print(" [0] Exit ZeusKit")
        print("--------------------------------------------------")
        
        choice = input(Fore.YELLOW + "ZeusKit > Main Menu: ").strip()
        if choice == "1": run_menu("[1] RECON & NETWORK", 1, 15)
        elif choice == "2": run_menu("[2] CODE & CRYPTO", 16, 30)
        elif choice == "3": run_menu("[3] WEB & OSINT", 31, 45)
        elif choice == "4": run_menu("[4] ATTACKING & DOS", 46, 60)
        elif choice == "5": run_menu("[5] SYSTEM DIAGNOSTICS", 61, 75)
        elif choice == "6": run_menu("[6] VULN & INJECTION", 76, 85)
        elif choice == "7": run_menu("[7] CLOUD & API", 86, 92)
        elif choice == "8": run_menu("[8] WIRELESS & PLUGINS", 93, 100)
        elif choice == "99": global_tool_finder()
        elif choice == "67":
            print(Fore.YELLOW + "[*] Checking updates...")
            subprocess.run(["git", "pull", "origin", "main"])
        elif choice == "0":
            print(Fore.CYAN + "[+] Exiting ZeusKit. Stay secure!")
            break

if __name__ == "__main__":
    main()
