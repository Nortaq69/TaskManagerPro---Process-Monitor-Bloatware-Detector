import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psutil
import threading
import time
import json
import os
from datetime import datetime
import win32gui
import win32process
import win32con
from collections import defaultdict

class ProcessMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TaskManagerPro - Process Monitor & Bloatware Detector")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Bloatware process definitions
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
            },
            "McAfeeSecurity.exe": {
                "name": "McAfee Security",
                "description": "McAfee antivirus",
                "severity": "medium",
                "category": "Security Software"
            },
            "NortonSecurity.exe": {
                "name": "Norton Security",
                "description": "Norton antivirus",
                "severity": "medium",
                "category": "Security Software"
            },
            "AdobeCreativeCloud.exe": {
                "name": "Adobe Creative Cloud",
                "description": "Adobe cloud services",
                "severity": "low",
                "category": "Creative Software"
            },
            "Spotify.exe": {
                "name": "Spotify",
                "description": "Music streaming service",
                "severity": "low",
                "category": "Media"
            },
            "Discord.exe": {
                "name": "Discord",
                "description": "Gaming chat application",
                "severity": "low",
                "category": "Communication"
            }
        }
        
        # User preferences
        self.whitelist = set()
        self.blacklist = set()
        self.auto_kill = False
        self.monitoring = False
        self.processes_data = {}
        self.log_file = "process_monitor.log"
        
        self.setup_ui()
        self.load_preferences()
        
    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background='#2d2d2d', foreground='white', fieldbackground='#2d2d2d')
        style.configure('Treeview.Heading', background='#404040', foreground='white')
        style.map('Treeview', background=[('selected', '#0078d4')])
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="TaskManagerPro - Process Monitor", 
                              font=('Segoe UI', 16, 'bold'), fg='#00ff00', bg='#1e1e1e')
        title_label.pack(pady=(0, 10))
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start/Stop button
        self.start_stop_btn = tk.Button(control_frame, text="Start Monitoring", 
                                       command=self.toggle_monitoring,
                                       bg='#0078d4', fg='white', font=('Segoe UI', 10, 'bold'))
        self.start_stop_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Auto-kill toggle
        self.auto_kill_var = tk.BooleanVar()
        auto_kill_cb = tk.Checkbutton(control_frame, text="Auto-kill bloatware", 
                                     variable=self.auto_kill_var, command=self.toggle_auto_kill,
                                     bg='#2d2d2d', fg='white', selectcolor='#404040')
        auto_kill_cb.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(control_frame, text="Refresh", 
                               command=self.refresh_processes,
                               bg='#404040', fg='white')
        refresh_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Settings button
        settings_btn = tk.Button(control_frame, text="Settings", 
                                command=self.open_settings,
                                bg='#404040', fg='white')
        settings_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Statistics labels
        self.total_processes_label = tk.Label(stats_frame, text="Total Processes: 0", 
                                             bg='#2d2d2d', fg='white', font=('Segoe UI', 10))
        self.total_processes_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.bloat_processes_label = tk.Label(stats_frame, text="Bloatware Detected: 0", 
                                             bg='#2d2d2d', fg='#ff6b6b', font=('Segoe UI', 10))
        self.bloat_processes_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.memory_usage_label = tk.Label(stats_frame, text="Total Memory: 0 MB", 
                                          bg='#2d2d2d', fg='white', font=('Segoe UI', 10))
        self.memory_usage_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Process list frame
        list_frame = tk.Frame(main_frame, bg='#1e1e1e')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for processes
        columns = ('PID', 'Name', 'Memory (MB)', 'CPU %', 'Status', 'Category')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Right-click menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Kill Process", command=self.kill_selected_process)
        self.context_menu.add_command(label="Add to Whitelist", command=self.add_to_whitelist)
        self.context_menu.add_command(label="Add to Blacklist", command=self.add_to_blacklist)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Properties", command=self.show_process_properties)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.show_process_properties)
        
        # Status bar
        self.status_bar = tk.Label(main_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def toggle_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.start_stop_btn.config(text="Stop Monitoring", bg='#d83b01')
            self.monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            self.monitor_thread.start()
            self.status_bar.config(text="Monitoring active...")
        else:
            self.monitoring = False
            self.start_stop_btn.config(text="Start Monitoring", bg='#0078d4')
            self.status_bar.config(text="Monitoring stopped")
    
    def toggle_auto_kill(self):
        self.auto_kill = self.auto_kill_var.get()
        self.log_event(f"Auto-kill {'enabled' if self.auto_kill else 'disabled'}")
    
    def monitor_processes(self):
        while self.monitoring:
            try:
                self.refresh_processes()
                time.sleep(2)  # Update every 2 seconds
            except Exception as e:
                self.log_event(f"Error in monitoring: {str(e)}")
                break
    
    def refresh_processes(self):
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            processes = []
            total_memory = 0
            bloat_count = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'status']):
                try:
                    info = proc.info
                    memory_mb = info['memory_info'].rss / 1024 / 1024
                    total_memory += memory_mb
                    
                    process_name = info['name']
                    is_bloat = process_name in self.BLOAT_PROCESSES
                    
                    if is_bloat and process_name not in self.whitelist:
                        bloat_count += 1
                        if self.auto_kill:
                            self.kill_process(proc.pid, process_name)
                    
                    category = self.get_process_category(process_name)
                    
                    processes.append({
                        'pid': info['pid'],
                        'name': process_name,
                        'memory': memory_mb,
                        'cpu': info['cpu_percent'],
                        'status': info['status'],
                        'category': category,
                        'is_bloat': is_bloat
                    })
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Sort processes by memory usage (descending)
            processes.sort(key=lambda x: x['memory'], reverse=True)
            
            # Add to treeview
            for proc in processes:
                values = (
                    proc['pid'],
                    proc['name'],
                    f"{proc['memory']:.1f}",
                    f"{proc['cpu']:.1f}",
                    proc['status'],
                    proc['category']
                )
                
                item = self.tree.insert('', 'end', values=values)
                
                # Color code bloatware processes
                if proc['is_bloat'] and proc['name'] not in self.whitelist:
                    self.tree.tag_configure('bloat', background='#ff6b6b', foreground='white')
                    self.tree.item(item, tags=('bloat',))
            
            # Update statistics
            self.total_processes_label.config(text=f"Total Processes: {len(processes)}")
            self.bloat_processes_label.config(text=f"Bloatware Detected: {bloat_count}")
            self.memory_usage_label.config(text=f"Total Memory: {total_memory:.0f} MB")
            
            self.processes_data = {proc['pid']: proc for proc in processes}
            
        except Exception as e:
            self.log_event(f"Error refreshing processes: {str(e)}")
    
    def get_process_category(self, process_name):
        if process_name in self.BLOAT_PROCESSES:
            return self.BLOAT_PROCESSES[process_name]['category']
        
        # Auto-categorize based on name patterns
        if 'chrome' in process_name.lower():
            return 'Browser'
        elif 'firefox' in process_name.lower():
            return 'Browser'
        elif 'edge' in process_name.lower():
            return 'Browser'
        elif 'svchost' in process_name.lower():
            return 'System Service'
        elif 'explorer' in process_name.lower():
            return 'Windows Shell'
        elif 'winlogon' in process_name.lower() or 'wininit' in process_name.lower():
            return 'System Service'
        else:
            return 'Application'
    
    def kill_selected_process(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process to kill.")
            return
        
        item = selection[0]
        pid = int(self.tree.item(item, 'values')[0])
        process_name = self.tree.item(item, 'values')[1]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to kill {process_name} (PID: {pid})?"):
            self.kill_process(pid, process_name)
    
    def kill_process(self, pid, process_name):
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            
            # Wait for process to terminate
            try:
                proc.wait(timeout=3)
            except psutil.TimeoutExpired:
                proc.kill()  # Force kill if it doesn't terminate
            
            self.log_event(f"Killed process: {process_name} (PID: {pid})")
            self.refresh_processes()
            
        except psutil.NoSuchProcess:
            self.log_event(f"Process {process_name} (PID: {pid}) already terminated")
        except psutil.AccessDenied:
            messagebox.showerror("Error", f"Access denied. Cannot kill {process_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to kill {process_name}: {str(e)}")
    
    def add_to_whitelist(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process to whitelist.")
            return
        
        item = selection[0]
        process_name = self.tree.item(item, 'values')[1]
        
        self.whitelist.add(process_name)
        self.save_preferences()
        self.log_event(f"Added {process_name} to whitelist")
        self.refresh_processes()
    
    def add_to_blacklist(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process to blacklist.")
            return
        
        item = selection[0]
        process_name = self.tree.item(item, 'values')[1]
        
        self.blacklist.add(process_name)
        self.save_preferences()
        self.log_event(f"Added {process_name} to blacklist")
        self.refresh_processes()
    
    def show_process_properties(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        pid = int(self.tree.item(item, 'values')[0])
        process_name = self.tree.item(item, 'values')[1]
        
        try:
            proc = psutil.Process(pid)
            info = proc.as_dict(attrs=[
                'pid', 'name', 'exe', 'cmdline', 'create_time', 'memory_info',
                'cpu_percent', 'num_threads', 'status', 'username'
            ])
            
            properties_window = tk.Toplevel(self.root)
            properties_window.title(f"Process Properties - {process_name}")
            properties_window.geometry("500x400")
            properties_window.configure(bg='#1e1e1e')
            
            # Create text widget for properties
            text_widget = tk.Text(properties_window, bg='#2d2d2d', fg='white', 
                                 font=('Consolas', 10))
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Format and display properties
            properties_text = f"""Process Properties:
{'='*50}

PID: {info['pid']}
Name: {info['name']}
Executable: {info['exe'] or 'N/A'}
Username: {info['username'] or 'N/A'}
Status: {info['status']}
Created: {datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')}

Memory Usage:
  RSS: {info['memory_info'].rss / 1024 / 1024:.1f} MB
  VMS: {info['memory_info'].vms / 1024 / 1024:.1f} MB

CPU Usage: {info['cpu_percent']:.1f}%
Threads: {info['num_threads']}

Command Line:
{' '.join(info['cmdline']) if info['cmdline'] else 'N/A'}

Bloatware Info:
"""
            
            if process_name in self.BLOAT_PROCESSES:
                bloat_info = self.BLOAT_PROCESSES[process_name]
                properties_text += f"""  Name: {bloat_info['name']}
  Description: {bloat_info['description']}
  Severity: {bloat_info['severity']}
  Category: {bloat_info['category']}
"""
            else:
                properties_text += "  Not classified as bloatware"
            
            text_widget.insert(tk.END, properties_text)
            text_widget.config(state=tk.DISABLED)
            
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "Process no longer exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get process properties: {str(e)}")
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def sort_treeview(self, col):
        """Sort treeview by column"""
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Sort items
        items.sort()
        
        # Rearrange items in sorted positions
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("600x500")
        settings_window.configure(bg='#1e1e1e')
        
        # Notebook for tabs
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Whitelist tab
        whitelist_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(whitelist_frame, text="Whitelist")
        
        tk.Label(whitelist_frame, text="Whitelisted Processes:", 
                bg='#1e1e1e', fg='white', font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        whitelist_listbox = tk.Listbox(whitelist_frame, bg='#2d2d2d', fg='white', height=15)
        whitelist_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for process in sorted(self.whitelist):
            whitelist_listbox.insert(tk.END, process)
        
        # Blacklist tab
        blacklist_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(blacklist_frame, text="Blacklist")
        
        tk.Label(blacklist_frame, text="Blacklisted Processes:", 
                bg='#1e1e1e', fg='white', font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        blacklist_listbox = tk.Listbox(blacklist_frame, bg='#2d2d2d', fg='white', height=15)
        blacklist_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for process in sorted(self.blacklist):
            blacklist_listbox.insert(tk.END, process)
        
        # Bloatware definitions tab
        bloat_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(bloat_frame, text="Bloatware Definitions")
        
        tk.Label(bloat_frame, text="Known Bloatware Processes:", 
                bg='#1e1e1e', fg='white', font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        bloat_text = tk.Text(bloat_frame, bg='#2d2d2d', fg='white', height=20)
        bloat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for process, info in self.BLOAT_PROCESSES.items():
            bloat_text.insert(tk.END, f"{process} - {info['name']} ({info['severity']})\n")
            bloat_text.insert(tk.END, f"  {info['description']}\n\n")
        
        bloat_text.config(state=tk.DISABLED)
    
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
        """Load user preferences from file"""
        try:
            if os.path.exists('preferences.json'):
                with open('preferences.json', 'r') as f:
                    data = json.load(f)
                    self.whitelist = set(data.get('whitelist', []))
                    self.blacklist = set(data.get('blacklist', []))
                    self.auto_kill = data.get('auto_kill', False)
                    self.auto_kill_var.set(self.auto_kill)
        except Exception as e:
            self.log_event(f"Failed to load preferences: {str(e)}")
    
    def save_preferences(self):
        """Save user preferences to file"""
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
        """Start the application"""
        self.refresh_processes()
        self.root.mainloop()

if __name__ == "__main__":
    app = ProcessMonitor()
    app.run()
