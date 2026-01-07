#!/usr/bin/env python3
"""
TodoMaster Pro - Installation Script
Author: Parvez Zamadar (@paruuvez)
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("TODO MASTER PRO - INSTALLATION")
    print("Developed by Parvez Zamadar (@paruuvez)")
    print("=" * 60)
    print()

def check_python_version():
    """Check Python version"""
    required = (3, 7)
    current = sys.version_info[:2]
    
    if current < required:
        print(f"❌ Python {required[0]}.{required[1]}+ required")
        print(f"   Current: Python {sys.version}")
        return False
    return True

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        return True
    except ImportError:
        print("❌ Tkinter is not installed")
        print("\nInstallation instructions:")
        system = platform.system()
        if system == "Linux":
            print("   Ubuntu/Debian: sudo apt-get install python3-tk")
            print("   Fedora/RHEL: sudo dnf install python3-tkinter")
            print("   Arch: sudo pacman -S tk")
        elif system == "Darwin":  # macOS
            print("   brew install python-tk")
        elif system == "Windows":
            print("   Tkinter should be included with Python on Windows")
            print("   If missing, reinstall Python with Tk/Tcl support")
        return False

def install_packages():
    """Install required packages"""
    packages = [
        "tkcalendar",
        "Pillow"
    ]
    
    print("📦 Installing packages...")
    print("-" * 40)
    
    for package in packages:
        print(f"Installing {package}...", end=" ", flush=True)
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅")
        except subprocess.CalledProcessError:
            print("❌")
            print(f"   Failed to install {package}")
            print(f"   Try: pip install {package}")
            return False
    
    return True

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        "assets",
        "exports",
        "backups",
        "screenshots"
    ]
    
    print("\n📁 Creating directory structure...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   Created: {directory}/")
    
    return True

def create_sample_data():
    """Create sample data files"""
    print("\n📝 Creating sample data...")
    
    # Create sample config
    config = """# TodoMaster Pro Configuration
# Generated during installation

[app]
name = TodoMaster Pro
version = 1.0.0
author = Parvez Zamadar
instagram = @paruuvez

[database]
path = todo_app.db
backup_interval = 7  # days

[ui]
theme = light
font_size = 10
auto_refresh = true
"""
    
    with open("config.ini", "w") as f:
        f.write(config)
    print("   Created: config.ini")
    
    return True

def setup_shortcuts():
    """Create desktop shortcuts"""
    print("\n⚡ Setting up shortcuts...")
    
    # Create batch file for Windows
    if platform.system() == "Windows":
        with open("run_todo.bat", "w") as f:
            f.write('''@echo off
echo Starting TodoMaster Pro...
python main.py
pause
''')
        print("   Created: run_todo.bat")
    
    # Create shell script for Linux/macOS
    else:
        with open("run_todo.sh", "w") as f:
            f.write('''#!/bin/bash
echo "Starting TodoMaster Pro..."
python3 main.py
''')
        os.chmod("run_todo.sh", 0o755)
        print("   Created: run_todo.sh")
    
    return True

def print_success():
    """Print success message"""
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📋 Quick Start Guide:")
    print("   1. Run the application:")
    print("      Windows: Double-click run_todo.bat")
    print("      Others: python main.py or ./run_todo.sh")
    print("\n   2. Add your first task using the '+' button")
    print("   3. Organize tasks by priority and category")
    print("   4. Use filters to view specific tasks")
    print("\n💡 Tips:")
    print("   • Press F5 to refresh")
    print("   • Ctrl+N to add new task")
    print("   • Double-click task to edit")
    print("   • Use search for quick filtering")
    print("\n📞 Support:")
    print("   Developer: Parvez Zamadar")
    print("   Instagram: @paruuvez")
    print("   GitHub: https://github.com/yourusername/todo-app")
    print("\n🌟 If you like this project, please star it on GitHub!")
    print("=" * 60)

def main():
    """Main installation function"""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        return 1
    
    if not check_tkinter():
        return 1
    
    # Install packages
    if not install_packages():
        return 1
    
    # Setup directories and files
    create_directory_structure()
    create_sample_data()
    setup_shortcuts()
    
    # Success
    print_success()
    
    # Launch application option
    response = input("\n🚀 Launch TodoMaster Pro now? (Y/n): ").strip().lower()
    if response in ['', 'y', 'yes']:
        print("\nStarting application...")
        try:
            subprocess.run([sys.executable, "main.py"])
        except Exception as e:
            print(f"Error: {e}")
            print("You can run manually: python main.py")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)