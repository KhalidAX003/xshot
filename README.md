XShot - Advanced WPS Attack Tool 🚀


📌 Overview

XShot is a comprehensive WPS (Wi-Fi Protected Setup) security assessment tool that combines Pixie Dust attack and Bruteforce techniques to test the security of WPS-enabled wireless networks. This tool is designed for educational purposes and authorized penetration testing only.

⚠️ DISCLAIMER: This tool is for educational and authorized security testing purposes only. Unauthorized use against networks you don't own or have explicit permission to test is illegal. Team AX is not responsible for any misuse.

✨ Features

🔥 Core Capabilities

· Pixie Dust Attack - Exploits weak random number generation in WPS implementations
· Smart Bruteforce - Intelligent PIN generation and validation
· WPS Push Button Connect - Support for PBC mode
· Vendor-Specific PIN Algorithms - 20+ algorithms for different manufacturers
· Session Management - Save/resume bruteforce sessions
· Credential Storage - Auto-save successful results

📊 Advanced Features

· Real-time Statistics - Progress tracking with time estimates
· Network Scanner - Automatic WPS-enabled AP detection
· Vulnerable Device Detection - Pre-loaded vulnerability database
· Verbose Debugging - Detailed attack process logging
· Cross-platform - Works on Linux/Android (Termux)

📋 Prerequisites

System Requirements

· Operating System: Linux (Kali, Parrot, Ubuntu, etc.) or Android (Termux)
· Python: Version 3.6 or higher
· Root Privileges: Required for network interface operations
· Wireless Adapter: Must support monitor mode and packet injection

Dependencies

```bash
# Essential tools
sudo apt-get update
sudo apt-get install -y:
    wireless-tools    # iw, iwconfig
    wpasupplicant     # WPS implementation
    pixiewps          # Pixie Dust attack tool
    python3-pip       # Python package manager

# Python packages
pip3 install:
    No additional packages required (all included)
```

🚀 Installation

Method 1: Direct Download

```bash
# Clone or download the script
wget https://raw.githubusercontent.com/your-repo/xshot/main/xshot.py
chmod +x xshot.py

# Make executable
sudo mv xshot.py /usr/local/bin/xshot
```

Method 2: Git Clone

```bash
git clone https://github.com/your-repo/xshot.git
cd xshot
sudo chmod +x xshot.py
sudo cp xshot.py /usr/local/bin/xshot
```

Android (Termux) Installation

```bash
pkg update && pkg upgrade
pkg install python wireless-tools root-repo
pkg install pixiewps wpasupplicant
git clone https://github.com/your-repo/xshot.git
cd xshot
python3 xshot.py --help
```

🎯 Usage

Basic Syntax

```bash
sudo xshot -i <interface> [options]
```

Common Examples

1. Network Discovery

```bash
# Scan for WPS-enabled networks
sudo xshot -i wlan0
```

2. Pixie Dust Attack

```bash
# Target specific AP with Pixie Dust
sudo xshot -i wlan0 -b AA:BB:CC:DD:EE:FF -K

# With force mode (bruteforce full range)
sudo xshot -i wlan0 -b AA:BB:CC:DD:EE:FF -K -F
```

3. Smart Bruteforce

```bash
# Online bruteforce attack
sudo xshot -i wlan0 -b AA:BB:CC:DD:EE:FF -B

# With delay between attempts
sudo xshot -i wlan0 -b AA:BB:CC:DD:EE:FF -B -d 2.5
```

4. Push Button Connect

```bash
# WPS PBC attack
sudo xshot -i wlan0 --pbc
```

5. Advanced Attacks

```bash
# Verbose mode with credential saving
sudo xshot -i wlan0 -b AA:BB:CC:DD:EE:FF -K -v -w

# Loop mode for multiple targets
sudo xshot -i wlan0 -l
```

⚙️ Command Line Options

Required Arguments

Option Description
-i, --interface Wireless interface name (e.g., wlan0)

Attack Modes

Option Description
-K, --pixie-dust Execute Pixie Dust attack
-B, --bruteforce Execute online bruteforce attack
--pbc WPS Push Button Connect mode
-b, --bssid Target AP MAC address
-p, --pin Specific WPS PIN to test

Advanced Options

Option Description
-d, --delay Delay between PIN attempts (seconds)
-F, --pixie-force Force Pixiewps full range bruteforce
-X, --show-pixie-cmd Display Pixiewps command
-w, --write Save credentials to file
-l, --loop Run in continuous loop
-v, --verbose Verbose output
-r, --reverse-scan Reverse network list order
--iface-down Disable interface after operation
--mtk-wifi MediaTek Wi-Fi chipset support
--vuln-list Custom vulnerable devices list

🔧 Configuration

File Locations

File/Directory Purpose Default Location
Session Files Save bruteforce progress ~/.XShot/sessions/
Pixiewps Data Store calculated PINs ~/.XShot/pixiewps/
Reports Successful credentials ./reports/
Vulnerable List Known vulnerable devices /usr/share/xshot/vulnwsc.txt

Custom Vulnerable Device List

Create a text file with vulnerable device models (one per line):

```bash
# Example vulnwsc.txt
D-Link DIR-300
TP-Link TL-WR841N
ASUS RT-N12
Netgear WNR1000
```

📊 Output Examples

Network Scan Results

```
# Networks list:
#    BSSID              ESSID                    Sec.    PWR  WSC device name        WSC model
1)  AA:BB:CC:DD:EE:FF  HomeNetwork              WPA2    -45  D-Link Router          DIR-615
2)  11:22:33:44:55:66  OfficeWiFi               WPA     -62  TP-Link AP             TL-WR740N
```

Successful Attack

```
[+] WPS PIN: '12345670'
[+] WPA PSK: 'MySecretPassword123'
[+] AP SSID: 'HomeNetwork'
[i] Credentials saved to ./reports/xshot_stored.txt
[✓] Done! Visit https://team-ax.top/ for more tools 🔥
```

🔐 Supported Vendors & Algorithms

XShot includes specialized PIN generation algorithms for:

Vendor Algorithms Notes
D-Link pin24, pin28, pinDLink, pinDLink1 Multiple models supported
ASUS pinASUS, pin32 Various router series
Broadcom pinBrcm1-6 Chipset-based calculation
Realtek pinRealtek1-3, pinAirocon Common in many devices
Cisco pinCisco Static PIN
TP-Link pin24, pin28 Depends on model
Other 15+ static PINs Various manufacturers

🛡️ Security Notes

Legal Requirements

1. Authorization Required: Only test networks you own or have written permission to test
2. Compliance: Follow local laws and regulations
3. Disclosure: Report vulnerabilities to vendors responsibly

Safety Precautions

· Always use in controlled environments
· Disable attacks immediately if unintended network is affected
· Keep logs for authorized testing evidence
· Use VPN/Tor for anonymity (where legal)

🚨 Troubleshooting

Common Issues & Solutions

1. Interface Not Found

```bash
# Check available interfaces
iwconfig
ip link show

# Set interface to monitor mode
sudo airmon-ng start wlan0
```

2. Pixiewps Not Found

```bash
# Install Pixiewps
sudo apt-get install pixiewps

# Or compile from source
git clone https://github.com/wiire/pixiewps.git
cd pixiewps
make
sudo make install
```

3. Permission Denied

```bash
# Run as root
sudo xshot -i wlan0

# Check SELinux/AppArmor
sudo setenforce 0
```

4. WPS Not Supported

```bash
# Check if AP supports WPS
sudo wash -i wlan0

# Ensure wpasupplicant has WPS support
wpa_supplicant -v | grep WPS
```

📈 Performance Tips

Optimizing Attack Speed

1. Use wired connection for stability
2. Reduce delay (-d 0.5) for faster attacks
3. Prioritize nearby APs (stronger signal)
4. Use --pixie-force only when necessary
5. Close unnecessary applications to free CPU

Signal Strength Guidelines

Signal Quality Success Rate
-50 dBm Excellent High
-50 to -70 dBm Good Medium-High
-70 to -80 dBm Fair Medium
< -80 dBm Poor Low

🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Follow the code style guide
5. Update documentation as needed

Code Standards

· Use Python 3.6+ syntax
· Follow PEP 8 guidelines
· Document new functions
· Add tests for new features

📚 Documentation

Additional Resources

· WPS Security White Paper
· Pixie Dust Attack Details
· Wi-Fi Security Best Practices

Related Tools

· Aircrack-ng - Wireless security suite
· Reaver - WPS attack tool
· Bully - WPS bruteforce implementation
· Wifite - Automated wireless auditor

⭐ Support

Need Help?

· Documentation: https://team-ax.top/docs/xshot
· Issues: GitHub Issues page
· Community: Team AX Discord/Telegram
· Email: support@team-ax.top

Donate

Support development via:

· BTC: 1AXTeamYourAddressHere
· ETH: 0xAXTeamYourAddressHere
· PayPal: donate@team-ax.top

📄 License

```
Copyright (c) 2024 Team AX

This tool is for educational purposes only. Users are responsible for
complying with all applicable laws. The developers assume no liability
for any misuse of this software.

Redistribution and use with attribution is permitted.
Commercial use requires explicit permission.
```

🔗 Connect With Us

· Website: https://team-ax.top/
· GitHub: https://github.com/team-ax
· Twitter: @TeamAXSecurity
· Blog: https://blog.team-ax.top/

---

⚠️ Important Note for Mobile Users:
For Android/Termux usage, ensure Hotspot is disabled and Location Services are enabled as some devices require location permissions for Wi-Fi scanning functionality.

Remember: With great power comes great responsibility. Use this tool ethically and legally. Happy testing! 🎯
