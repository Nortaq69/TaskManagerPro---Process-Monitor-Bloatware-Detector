import tkinter as tk
from tkinter import messagebox
import psutil
import threading
import time
import json
import os
from datetime import datetime
import win32gui
import win32con
import win32api
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item

class TrayProcessMonitor:
    def __init__(self):
        self.BLOAT_PROCESSES = {
            "YourPhone.exe": {
                "name": "Your Phone Companion",
                "description": "Microsoft's phone linking service",
                "severity": "medium",
                "category": "Microsoft Services"
            },
            "OneDrive.exe": {
                "name": "OneDrive",
                "description": "Microsoft cloud storage sync",
                "severity": "low",
                "category": "Microsoft Services"
            },
            "GameBar.exe": {
                "name": "Xbox Game Bar",
                "description": "Gaming overlay and recording",
                "severity": "medium",
                "category": "Gaming"
            },
            "MicrosoftEdgeUpdate.exe": {
                "name": "Microsoft Edge Update",
                "description": "Edge browser update service",
                "severity": "low",
                "category": "Microsoft Services"
            },
            "SearchApp.exe": {
                "name": "Windows Search",
                "description": "Windows search indexing",
                "severity": "medium",
                "category": "Windows Services"
            },
            "Cortana.exe": {
                "name": "Cortana",
                "description": "Windows virtual assistant",
                "severity": "high",
                "category": "Windows Services"
            },
            "Widgets.exe": {
                "name": "Windows Widgets",
                "description": "News and weather widgets",
                "severity": "medium",
                "category": "Windows Services"
            },
            "HPJumpStartBridge.exe": {
                "name": "HP JumpStart Bridge",
                "description": "HP bloatware service",
                "severity": "high",
                "category": "OEM Bloatware"
            },
            "DellDataVault.exe": {
                "name": "Dell Data Vault",
                "description": "Dell bloatware service",
                "severity": "high",
                "category": "OEM Bloatware"
            },
            "LenovoVantage.exe": {
                "name": "Lenovo Vantage",
                "description": "Lenovo system management",
                "severity": "medium",
                "category": "OEM Bloatware"
            }
        }
        
        self.whitelist = set()
        self.blacklist = set()
        self.auto_kill = False
        self.monitoring = False
        self.log_file = "tray_monitor.log"
        self.detected_bloatware = set()
        
        self.load_preferences()
        self.setup_tray()
        
    def create_icon(self):
        """Create a simple icon for the tray"""
        # Create a 64x64 image with a simple icon
        width = 64
        height = 64
        
        # Create a simple icon (red circle with 'P' for Process)
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Draw a red circle
        for x in range(width):
            for y in range(height):
                # Calculate distance from center
                center_x, center_y = width // 2, height // 2
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                
                if distance <= 25:  # Circle radius
                    image.putpixel((x, y), (255, 0, 0, 255))  # Red
                elif distance <= 30:  # Border
                    image.putpixel((x, y), (200, 0, 0, 255))  # Darker red
        
        return image
    
    def setup_tray(self):
        """Setup the system tray icon and menu"""
        self.icon_image = self.create_icon()
        
        menu = (
            item('Show Main Window', self.show_main_window),
            item('Start Monitoring', self.toggle_monitoring),
            item('Auto-kill Bloatware', self.toggle_auto_kill, checked=lambda item: self.auto_kill),
            pystray.Menu.SEPARATOR,
            item('Settings', self.show_settings),
            item('View Log', self.view_log),
            pystray.Menu.SEPARATOR,
            item('Quit', self.quit_app)
        )
        
        self.icon = pystray.Icon("TaskManagerPro", self.icon_image, "TaskManagerPro - Process Monitor", menu)
        
    def show_main_window(self, icon=None, item=None):
        """Show the main process monitor window"""
        # Import and run the main window
        try:
            from process_monitor import ProcessMonitor
            app = ProcessMonitor()
            app.run()
        except ImportError:
            messagebox.showerror("Error", "Main window module not found")
    
    def toggle_monitoring(self, icon=None, item=None):
        """Toggle monitoring on/off"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            self.monitor_thread.start()
            self.log_event("Background monitoring started")
        else:
            self.monitoring = False
            self.log_event("Background monitoring stopped")
    
    def toggle_auto_kill(self, icon=None, item=None):
        """Toggle auto-kill feature"""
        self.auto_kill = not self.auto_kill
        self.save_preferences()
        self.log_event(f"Auto-kill {'enabled' if self.auto_kill else 'disabled'}")
    
    def show_settings(self, icon=None, item=None):
        """Show settings window"""
        self.create_settings_window()
    
    def view_log(self, icon=None, item=None):
        """View the log file"""
        try:
            if os.path.exists(self.log_file):
                os.startfile(self.log_file)
            else:
                messagebox.showinfo("Info", "No log file found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log: {str(e)}")
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.monitoring = False
        self.icon.stop()
    
    def create_settings_window(self):
        """Create a settings window"""
        settings_window = tk.Toplevel()
        settings_window.title("TaskManagerPro Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg='#1e1e1e')
        
        # Title
        title_label = tk.Label(settings_window, text="Background Monitor Settings", 
                              font=('Segoe UI', 14, 'bold'), fg='#00ff00', bg='#1e1e1e')
        title_label.pack(pady=10)
        
        # Auto-kill setting
        auto_kill_var = tk.BooleanVar(value=self.auto_kill)
        auto_kill_cb = tk.Checkbutton(settings_window, text="Automatically kill detected bloatware", 
                                     variable=auto_kill_var, command=lambda: self.update_auto_kill(auto_kill_var),
                                     bg='#1e1e1e', fg='white', selectcolor='#404040')
        auto_kill_cb.pack(pady=10)
        
        # Whitelist section
        whitelist_frame = tk.Frame(settings_window, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        whitelist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(whitelist_frame, text="Whitelisted Processes (ignored by monitor):", 
                bg='#2d2d2d', fg='white', font=('Segoe UI', 10, 'bold')).pack(pady=5)
        
        whitelist_listbox = tk.Listbox(whitelist_frame, bg='#1e1e1e', fg='white', height=8)
        whitelist_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for process in sorted(self.whitelist):
            whitelist_listbox.insert(tk.END, process)
        
        # Add/Remove whitelist buttons
        whitelist_btn_frame = tk.Frame(whitelist_frame, bg='#2d2d2d')
        whitelist_btn_frame.pack(pady=5)
        
        add_whitelist_btn = tk.Button(whitelist_btn_frame, text="Add Process", 
                                     command=lambda: self.add_to_whitelist_dialog(whitelist_listbox),
                                     bg='#0078d4', fg='white')
        add_whitelist_btn.pack(side=tk.LEFT, padx=5)
        
        remove_whitelist_btn = tk.Button(whitelist_btn_frame, text="Remove Selected", 
                                        command=lambda: self.remove_from_whitelist(whitelist_listbox),
                                        bg='#d83b01', fg='white')
        remove_whitelist_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        status_label = tk.Label(settings_window, text=f"Monitoring: {'Active' if self.monitoring else 'Inactive'}", 
                               bg='#1e1e1e', fg='#00ff00' if self.monitoring else '#ff6b6b')
        status_label.pack(pady=10)
    
    def add_to_whitelist_dialog(self, listbox):
        """Add a process to whitelist via dialog"""
        dialog = tk.Toplevel()
        dialog.title("Add to Whitelist")
        dialog.geometry("300x150")
        dialog.configure(bg='#1e1e1e')
        
        tk.Label(dialog, text="Enter process name (e.g., chrome.exe):", 
                bg='#1e1e1e', fg='white').pack(pady=10)
        
        entry = tk.Entry(dialog, width=30)
        entry.pack(pady=10)
        
        def add_process():
            process_name = entry.get().strip()
            if process_name:
                self.whitelist.add(process_name)
                self.save_preferences()
                listbox.insert(tk.END, process_name)
                dialog.destroy()
        
        tk.Button(dialog, text="Add", command=add_process, 
                 bg='#0078d4', fg='white').pack(pady=10)
    
    def remove_from_whitelist(self, listbox):
        """Remove selected process from whitelist"""
        selection = listbox.curselection()
        if selection:
            process_name = listbox.get(selection[0])
            self.whitelist.discard(process_name)
            self.save_preferences()
            listbox.delete(selection[0])
    
    def update_auto_kill(self, var):
        """Update auto-kill setting"""
        self.auto_kill = var.get()
        self.save_preferences()
    
    def monitor_processes(self):
        """Monitor processes in background"""
        while self.monitoring:
            try:
                current_bloatware = set()
                
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        process_name = proc.info['name']
                        
                        if process_name in self.BLOAT_PROCESSES and process_name not in self.whitelist:
                            current_bloatware.add(process_name)
                            
                            # Auto-kill if enabled
                            if self.auto_kill:
                                self.kill_process(proc.pid, process_name)
                            
                            # Show notification for new detections
                            if process_name not in self.detected_bloatware:
                                self.show_notification(process_name)
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                
                # Update detected bloatware set
                self.detected_bloatware = current_bloatware
                
                # Log summary
                if current_bloatware:
                    self.log_event(f"Detected bloatware: {', '.join(current_bloatware)}")
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                self.log_event(f"Error in background monitoring: {str(e)}")
                time.sleep(10)  # Wait longer on error
    
    def kill_process(self, pid, process_name):
        """Kill a process"""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            
            try:
                proc.wait(timeout=3)
            except psutil.TimeoutExpired:
                proc.kill()
            
            self.log_event(f"Auto-killed: {process_name} (PID: {pid})")
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            self.log_event(f"Failed to kill {process_name}: {str(e)}")
    
    def show_notification(self, process_name):
        """Show Windows notification"""
        try:
            bloat_info = self.BLOAT_PROCESSES.get(process_name, {})
            title = "Bloatware Detected!"
            message = f"{bloat_info.get('name', process_name)} is running\n{bloat_info.get('description', 'Unknown process')}"
            
            # Use Windows notification
            self.icon.notify(title, message)
            
        except Exception as e:
            self.log_event(f"Failed to show notification: {str(e)}")
    
    def log_event(self, message):
        """Log events to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to write to log: {e}")
    
    def load_preferences(self):
        """Load user preferences"""
        try:
            if os.path.exists('preferences.json'):
                with open('preferences.json', 'r') as f:
                    data = json.load(f)
                    self.whitelist = set(data.get('whitelist', []))
                    self.blacklist = set(data.get('blacklist', []))
                    self.auto_kill = data.get('auto_kill', False)
        except Exception as e:
            self.log_event(f"Failed to load preferences: {str(e)}")
    
    def save_preferences(self):
        """Save user preferences"""
        try:
            data = {
                'whitelist': list(self.whitelist),
                'blacklist': list(self.blacklist),
                'auto_kill': self.auto_kill
            }
            with open('preferences.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.log_event(f"Failed to save preferences: {str(e)}")
    
    def run(self):
        """Start the tray application"""
        self.log_event("Tray monitor started")
        self.icon.run()

if __name__ == "__main__":
    app = TrayProcessMonitor()
    app.run()
