# ZeusKit ⚡
A professional mobile cybersecurity suite designed for Termux and Linux.

## 🚀 Features
- **DNS Resolution Suite**: Fast lookups using native Python and `dnspython`.
- **Auto-Update System**: Check and pull updates directly from GitHub using option `[67]`.
- **Anti-Skid Protection**: Built-in integrity checks and author verification (`sunveroblox-bit`).

## 📥 Installation & Setup

### For Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install git python python-pip -y
git clone [https://github.com/sunveroblox-bit/ZeusKit.git](https://github.com/sunveroblox-bit/ZeusKit.git)
cd ZeusKit
pip install -r requirements.txt
python3 zeuskit.py
```

### For Linux (Debian / Ubuntu / Kali)
```bash
sudo apt update && sudo apt install git python3 python3-pip -y
git clone [https://github.com/sunveroblox-bit/ZeusKit.git](https://github.com/sunveroblox-bit/ZeusKit.git)
cd ZeusKit
pip install -r requirements.txt
python3 zeuskit.py
```
