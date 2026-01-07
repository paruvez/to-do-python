#!/usr/bin/env python3
"""
TodoMaster Pro - Main Launcher
Author: Parvez Zamadar (@paruuvez)
Description: Launcher script for Todo App
"""

import sys
import os
from tkinter import messagebox
import tkinter as tk

def check_dependencies():
    """Check if all dependencies are installed"""
    missing = []
    
    try:
        import sqlite3
    except ImportError:
        missing.append("sqlite3")
    
    try:
        from tkcalendar import DateEntry
    except ImportError:
        missing.append("tkcalendar")
    
    try:
        from PIL import Image, ImageTk, ImageDraw
    except ImportError:
        missing.append("Pillow")
    
    return missing

def install_dependencies(missing):
    """Offer to install missing dependencies"""
    if not missing:
        return True
    
    root = tk.Tk()
    root.withdraw()
    
    packages = " ".join(missing)
    response = messagebox.askyesno(
        "Missing Dependencies",
        f"The following packages are missing:\n\n{', '.join(missing)}\n\n"
        f"Would you like to install them now?\n\n"
        f"Command: pip install {packages}"
    )
    
    if response:
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            messagebox.showinfo("Success", "Dependencies installed successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install dependencies:\n\n{e}")
            return False
    else:
        messagebox.showinfo("Information", 
                           "Please install the missing packages manually:\n"
                           f"pip install {packages}")
        return False

def create_assets():
    """Create default assets if they don't exist"""
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Create default icon if not exists
    icon_path = os.path.join(assets_dir, "icon.ico")
    if not os.path.exists(icon_path):
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse([5, 5, 59, 59], outline='#4361ee', width=4)
            draw.line([(20, 35), (32, 47), (48, 25)], fill='#4361ee', width=6)
            img.save(icon_path, format='ICO')
        except:
            pass

def main():
    """Main function"""
    print("=" * 60)
    print("TodoMaster Pro - Task Management System")
    print("Developed by Parvez Zamadar (@paruuvez)")
    print("=" * 60)
    
    # Check dependencies
    missing = check_dependencies()
    if missing and not install_dependencies(missing):
        print("\n❌ Please install missing dependencies and try again.")
        input("\nPress Enter to exit...")
        return
    
    # Create assets
    create_assets()
    
    # Launch application
    try:
        from todo_gui import TodoApp
        
        root = tk.Tk()
        app = TodoApp(root)
        app.run()
        
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()