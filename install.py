#!/usr/bin/env python3
# One-line install script for XShot
import os, sys, subprocess, tempfile, urllib.request

def install_xshot():
    print("🚀 Installing XShot Premium...")
    
    # Create temp file for setup.py
    setup_url = "https://raw.githubusercontent.com/KhalidAX003/xshot/main/setup.py"
    
    try:
        # Download setup.py
        print("📥 Downloading setup script...")
        response = urllib.request.urlopen(setup_url)
        setup_content = response.read().decode()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(setup_content)
            setup_file = f.name
        
        # Execute setup.py
        print("⚙️ Running installation...")
        subprocess.run([sys.executable, setup_file], check=True)
        
        # Cleanup
        os.unlink(setup_file)
        
        print("\n✅ Installation complete!")
        print("Usage: sudo xshot -i wlan0 --scan")
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_xshot()
