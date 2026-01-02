#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XShot Premium - Installation & Setup Script
Version: 2.0
Author: Team AX
Website: https://team-ax.top/
"""

import os
import sys
import subprocess
import platform
import time
import shutil
import requests
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Colors
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE

class XShotInstaller:
    def __init__(self):
        self.system = platform.system()
        self.is_root = os.geteuid() == 0
        self.home = str(Path.home())
        self.install_dir = "/usr/local/share/xshot" if self.is_root else f"{self.home}/.xshot"
        self.bin_dir = "/usr/local/bin" if self.is_root else f"{self.home}/.local/bin"
        
    def print_banner(self):
        banner = f"""
{G}╔════════════════════════════════════════════════════════════╗
║                    {R}██╗  ██╗{Y}███████╗{C}██╗  ██╗ {M}█████╗  {B}███████╗{G}              ║
║                    {R}╚██╗██╔╝{Y}██╔════╝{C}██║  ██║{M}██╔══██╗{B}██╔════╝{G}              ║
║                    {R} ╚███╔╝ {Y}███████╗{C}███████║{M}███████║{B}███████╗{G}              ║
║                    {R} ██╔██╗ {Y}╚════██║{C}██╔══██║{M}██╔══██║{B}╚════██║{G}              ║
║                    {R}██╔╝ ██╗{Y}███████║{C}██║  ██║{M}██║  ██║{B}███████║{G}              ║
║                    {R}╚═╝  ╚═╝{Y}╚══════╝{C}╚═╝  ╚═╝{M}╚═╝  ╚═╝{B}╚══════╝{G}              ║
║{W}           Premium WPS Attack Suite - Installation           {G}║
╚════════════════════════════════════════════════════════════╝{W}
        """
        print(banner)
    
    def check_root(self):
        if not self.is_root and self.system != "Windows":
            print(f"{R}[!] Warning: Running without root privileges")
            print(f"{Y}[*] Some features may require sudo")
            time.sleep(2)
        return True
    
    def detect_os(self):
        print(f"{B}[*] Detecting system...")
        print(f"{C}    OS: {self.system}")
        print(f"{C}    Architecture: {platform.machine()}")
        print(f"{C}    Python: {platform.python_version()}")
        return self.system
    
    def check_dependencies(self):
        print(f"\n{B}[*] Checking dependencies...")
        
        deps = {
            "python3": "Python 3.6+",
            "git": "Git",
            "iw": "Wireless Tools",
            "wpa_supplicant": "WPA Supplicant",
        }
        
        missing = []
        for cmd, name in deps.items():
            try:
                subprocess.run(["which", cmd], check=True, capture_output=True)
                print(f"{G}    ✓ {name}")
            except:
                print(f"{R}    ✗ {name}")
                missing.append(cmd)
        
        if missing:
            print(f"\n{Y}[!] Missing dependencies: {', '.join(missing)}")
            return False
        return True
    
    def install_debian_deps(self):
        print(f"\n{B}[*] Installing dependencies for Debian/Ubuntu/Kali...")
        
        commands = [
            "apt-get update",
            "apt-get install -y python3 python3-pip git",
            "apt-get install -y wireless-tools iw wpasupplicant",
            "apt-get install -y hcxdumptool hcxtools",
            "pip3 install --upgrade pip"
        ]
        
        for cmd in commands:
            print(f"{C}    Running: {cmd}")
            try:
                subprocess.run(cmd.split(), check=True)
            except:
                print(f"{Y}    Note: Some packages might already be installed")
    
    def install_pixiewps(self):
        print(f"\n{B}[*] Installing Pixiewps...")
        
        pixie_path = "/usr/local/bin/pixiewps"
        if os.path.exists(pixie_path):
            print(f"{G}    ✓ Pixiewps already installed")
            return True
        
        # Try package manager first
        try:
            if self.system == "Linux":
                subprocess.run(["apt-get", "install", "-y", "pixiewps"], check=True)
                print(f"{G}    ✓ Pixiewps installed via apt")
                return True
        except:
            pass
        
        # Compile from source
        print(f"{C}    Compiling Pixiewps from source...")
        try:
            subprocess.run([
                "git", "clone", "https://github.com/wiire/pixiewps.git",
                "/tmp/pixiewps"
            ], check=True)
            
            os.chdir("/tmp/pixiewps")
            subprocess.run(["make"], check=True)
            subprocess.run(["sudo", "make", "install"], check=True)
            
            print(f"{G}    ✓ Pixiewps compiled and installed")
            return True
        except Exception as e:
            print(f"{R}    ✗ Failed to install Pixiewps: {e}")
            return False
    
    def install_termux_deps(self):
        print(f"\n{B}[*] Installing Termux dependencies...")
        
        commands = [
            "pkg update -y",
            "pkg upgrade -y",
            "pkg install -y python git root-repo",
            "pkg install -y wireless-tools tsu",
            "pkg install -y pixiewps",
            "pip install --upgrade pip"
        ]
        
        for cmd in commands:
            print(f"{C}    Running: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
            except:
                print(f"{Y}    Continuing...")
    
    def download_xshot(self):
        print(f"\n{B}[*] Downloading XShot Premium...")
        
        repo_url = "https://github.com/KhalidAX003/xshot.git"
        
        if os.path.exists("xshot"):
            print(f"{C}    Updating existing XShot...")
            os.chdir("xshot")
            subprocess.run(["git", "pull"], check=True)
        else:
            print(f"{C}    Cloning repository...")
            subprocess.run(["git", "clone", repo_url], check=True)
            os.chdir("xshot")
        
        print(f"{G}    ✓ XShot downloaded/updated")
        return os.getcwd()
    
    def install_python_deps(self):
        print(f"\n{B}[*] Installing Python dependencies...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            
            # Install requirements
            if os.path.exists("requirements.txt"):
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            else:
                # Basic dependencies
                deps = ["colorama", "requests", "scapy"]
                subprocess.run([sys.executable, "-m", "pip", "install"] + deps, check=True)
            
            print(f"{G}    ✓ Python dependencies installed")
            return True
        except Exception as e:
            print(f"{R}    ✗ Failed to install Python deps: {e}")
            return False
    
    def setup_symlink(self):
        print(f"\n{B}[*] Setting up system links...")
        
        current_dir = os.getcwd()
        main_script = os.path.join(current_dir, "xshot.py")
        
        # Make executable
        os.chmod(main_script, 0o755)
        
        # Create symlink
        link_path = os.path.join(self.bin_dir, "xshot")
        
        try:
            if os.path.exists(link_path):
                os.remove(link_path)
            
            os.makedirs(self.bin_dir, exist_ok=True)
            os.symlink(main_script, link_path)
            
            # Add to PATH if needed
            if self.bin_dir not in os.environ["PATH"]:
                print(f"{Y}[!] Add {self.bin_dir} to your PATH")
            
            print(f"{G}    ✓ Symlink created: {link_path}")
            return True
        except Exception as e:
            print(f"{Y}    Note: Could not create symlink: {e}")
            return False
    
    def create_config(self):
        print(f"\n{B}[*] Creating configuration...")
        
        config_dir = f"{self.home}/.xshot"
        os.makedirs(config_dir, exist_ok=True)
        
        # Create config file
        config_content = f"""[General]
language = en
theme = dark
auto_update = true

[Attack]
default_mode = pixie
stealth_mode = false
threads = 4

[Database]
update_frequency = daily
"""
        
        config_file = os.path.join(config_dir, "config.ini")
        with open(config_file, "w") as f:
            f.write(config_content)
        
        # Create directories
        dirs = ["sessions", "logs", "reports", "database"]
        for d in dirs:
            os.makedirs(os.path.join(config_dir, d), exist_ok=True)
        
        print(f"{G}    ✓ Configuration created at {config_dir}")
    
    def download_database(self):
        print(f"\n{B}[*] Downloading vulnerability database...")
        
        vuln_url = "https://raw.githubusercontent.com/KhalidAX003/xshot/main/database/vulnwsc.txt"
        db_path = f"{self.home}/.xshot/database/vulnwsc.txt"
        
        try:
            response = requests.get(vuln_url)
            with open(db_path, "w") as f:
                f.write(response.text)
            print(f"{G}    ✓ Database downloaded")
        except:
            print(f"{Y}    Note: Could not download database")
    
    def setup_completion(self):
        print(f"\n{B}[*] Setting up shell completion...")
        
        completion_script = """# XShot bash completion
_xshot_complete() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    opts="-i --interface -b --bssid -p --pin -K --pixie-dust -B --bruteforce --pbc -d --delay -w --write -v --verbose --scan --auto --stealth --ai --update --help --version"
    
    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _xshot_complete xshot
"""
        
        # Try to add to bashrc
        bashrc = f"{self.home}/.bashrc"
        if os.path.exists(bashrc):
            with open(bashrc, "a") as f:
                f.write(f"\n# XShot Completion\n{completion_script}")
            print(f"{G}    ✓ Bash completion added")
    
    def check_wireless(self):
        print(f"\n{B}[*] Checking wireless capabilities...")
        
        try:
            result = subprocess.run(["iw", "list"], capture_output=True, text=True)
            if "monitor" in result.stdout.lower():
                print(f"{G}    ✓ Monitor mode supported")
            else:
                print(f"{Y}    ⚠ Monitor mode may not be supported")
            
            # Check interfaces
            result = subprocess.run(["iwconfig"], capture_output=True, text=True)
            if "IEEE 802.11" in result.stdout:
                print(f"{G}    ✓ Wireless interfaces detected")
            else:
                print(f"{R}    ✗ No wireless interfaces found")
        except:
            print(f"{Y}    ⚠ Could not check wireless capabilities")
    
    def run_tests(self):
        print(f"\n{B}[*] Running basic tests...")
        
        current_dir = os.getcwd()
        
        # Test 1: Check main script
        if os.path.exists("xshot.py"):
            print(f"{G}    ✓ Main script found")
            
            # Test 2: Check Python version
            version = sys.version_info
            if version.major == 3 and version.minor >= 6:
                print(f"{G}    ✓ Python {version.major}.{version.minor}.{version.micro} OK")
            else:
                print(f"{R}    ✗ Python 3.6+ required")
                return False
            
            # Test 3: Check dependencies
            try:
                import colorama
                print(f"{G}    ✓ Colorama imported")
            except:
                print(f"{Y}    ⚠ Colorama not installed")
            
            return True
        else:
            print(f"{R}    ✗ Main script not found!")
            return False
    
    def show_usage(self):
        print(f"\n{G}╔════════════════════════════════════════════════════════════╗")
        print(f"║                    {W}QUICK START GUIDE                        {G}║")
        print(f"╚════════════════════════════════════════════════════════════╝{W}")
        
        print(f"\n{Y}🚀 Basic Usage:{W}")
        print(f"  sudo xshot -i wlan0 --scan                {C}# Scan networks")
        print(f"  sudo xshot -i wlan0 -K                    {C}# Pixie Dust attack")
        print(f"  sudo xshot -i wlan0 -b BSSID -K           {C}# Target specific AP")
        
        print(f"\n{Y}🎯 Premium Features:{W}")
        print(f"  sudo xshot -i wlan0 --auto                {C}# Auto attack")
        print(f"  sudo xshot -i wlan0 --stealth             {C}# Stealth mode")
        print(f"  sudo xshot -i wlan0 --ai                  {C}# AI-powered attack")
        
        print(f"\n{Y}📱 Termux (Android):{W}")
        print(f"  sudo python xshot.py -i wlan0 -K")
        print(f"  {M}Note: Turn OFF Hotspot, Turn ON Location")
        
        print(f"\n{Y}❓ Help:{W}")
        print(f"  xshot --help                              {C}# Show all options")
        print(f"  xshot --update                            {C}# Update XShot")
        
        print(f"\n{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
        print(f"{B}💡 Tip: Run '{C}xshot --scan{W}' first to find targets!")
        print(f"{B}🔗 Website: {W}https://team-ax.top/")
        print(f"{B}📚 Docs: {W}https://github.com/KhalidAX003/xshot")
        print(f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
    
    def install(self):
        self.print_banner()
        
        print(f"{M}[*] XShot Premium Installation")
        print(f"{M}    Version: 2.0 | Platform: {self.system}")
        print(f"{M}    Author: Team AX | Website: https://team-ax.top/")
        print(f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
        
        # Step 1: Check root
        self.check_root()
        
        # Step 2: Detect OS
        os_type = self.detect_os()
        
        # Step 3: Install based on OS
        if os_type == "Linux":
            # Check if Termux
            if "ANDROID_ROOT" in os.environ:
                print(f"\n{B}[*] Detected Termux (Android)")
                self.install_termux_deps()
            else:
                # Regular Linux
                if not self.check_dependencies():
                    self.install_debian_deps()
            
            # Install Pixiewps
            self.install_pixiewps()
            
        elif os_type == "Darwin":  # macOS
            print(f"\n{Y}[!] macOS detected - manual steps may be needed")
            print(f"{C}    Run: brew install python3 git pixiewps")
            
        elif os_type == "Windows":
            print(f"\n{R}[!] Windows requires WSL2 for full functionality")
            print(f"{C}    Install WSL2: wsl --install -d Ubuntu")
            return False
        
        # Step 4: Download XShot
        try:
            xshot_dir = self.download_xshot()
        except Exception as e:
            print(f"{R}    ✗ Failed to download XShot: {e}")
            return False
        
        # Step 5: Install Python dependencies
        if not self.install_python_deps():
            print(f"{Y}[!] Some Python dependencies failed")
        
        # Step 6: Setup symlink
        self.setup_symlink()
        
        # Step 7: Create config
        self.create_config()
        
        # Step 8: Download database
        self.download_database()
        
        # Step 9: Setup completion
        self.setup_completion()
        
        # Step 10: Check wireless
        self.check_wireless()
        
        # Step 11: Run tests
        if not self.run_tests():
            print(f"{Y}[!] Some tests failed")
        
        print(f"\n{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
        print(f"{G}[✓] XShot Premium Installation Complete!")
        print(f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{W}")
        
        # Show usage
        self.show_usage()
        
        return True
    
    def update(self):
        self.print_banner()
        print(f"{M}[*] Updating XShot Premium...")
        
        try:
            # Update git repo
            if os.path.exists("xshot"):
                os.chdir("xshot")
                subprocess.run(["git", "pull"], check=True)
            else:
                print(f"{R}[!] XShot not found. Run installation first.")
                return False
            
            # Update dependencies
            if os.path.exists("requirements.txt"):
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"], check=True)
            
            # Update database
            self.download_database()
            
            print(f"\n{G}[✓] XShot updated successfully!")
            print(f"{C}    Run '{W}xshot --version{C}' to check new version")
            
        except Exception as e:
            print(f"{R}[!] Update failed: {e}")
            return False
        
        return True
    
    def uninstall(self):
        self.print_banner()
        print(f"{R}[!] Uninstalling XShot...")
        
        confirm = input(f"{Y}[?] Are you sure? (y/N): ").lower()
        if confirm != 'y':
            print(f"{C}[*] Uninstall cancelled")
            return
        
        # Remove symlink
        link_path = os.path.join(self.bin_dir, "xshot")
        if os.path.exists(link_path):
            os.remove(link_path)
            print(f"{G}    Removed symlink")
        
        # Remove config
        config_dir = f"{self.home}/.xshot"
        if os.path.exists(config_dir):
            shutil.rmtree(config_dir)
            print(f"{G}    Removed config directory")
        
        # Remove installation
        if os.path.exists("xshot"):
            shutil.rmtree("xshot")
            print(f"{G}    Removed XShot directory")
        
        print(f"\n{G}[✓] XShot uninstalled successfully")
        print(f"{C}    Thanks for using XShot!")

def main():
    installer = XShotInstaller()
    
    # Parse arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--update":
            installer.update()
        elif sys.argv[1] == "--uninstall":
            installer.uninstall()
        elif sys.argv[1] == "--help":
            print(f"""
{C}XShot Setup Script - Usage:{W}

  python setup.py                    {G}# Install XShot
  python setup.py --update           {G}# Update XShot
  python setup.py --uninstall        {G}# Remove XShot
  python setup.py --help             {G}# Show this help

{Y}Examples:{W}
  sudo python setup.py               {C}# Complete installation
  python setup.py --update           {C}# Update existing installation
            """)
        else:
            print(f"{R}[!] Unknown option: {sys.argv[1]}")
            print(f"{C}Use 'python setup.py --help' for usage")
    else:
        # Default: install
        installer.install()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{R}[!] Installation failed: {e}")
        sys.exit(1)
