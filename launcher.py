import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class TaskManagerProLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TaskManagerPro - Launcher")
        self.root.geometry("400x300")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="TaskManagerPro", 
                              font=('Segoe UI', 24, 'bold'), fg='#00ff00', bg='#1e1e1e')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame, text="Process Monitor & Bloatware Detector", 
                                 font=('Segoe UI', 12), fg='#cccccc', bg='#1e1e1e')
        subtitle_label.pack(pady=(0, 30))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#1e1e1e')
        buttons_frame.pack(expand=True)
        
        # Main Window button
        main_window_btn = tk.Button(buttons_frame, text="Launch Main Window", 
                                   command=self.launch_main_window,
                                   bg='#0078d4', fg='white', font=('Segoe UI', 12, 'bold'),
                                   width=20, height=2)
        main_window_btn.pack(pady=10)
        
        # Tray Monitor button
        tray_btn = tk.Button(buttons_frame, text="Launch System Tray Monitor", 
                            command=self.launch_tray_monitor,
                            bg='#404040', fg='white', font=('Segoe UI', 12, 'bold'),
                            width=20, height=2)
        tray_btn.pack(pady=10)
        
        # Both button
        both_btn = tk.Button(buttons_frame, text="Launch Both", 
                            command=self.launch_both,
                            bg='#d83b01', fg='white', font=('Segoe UI', 12, 'bold'),
                            width=20, height=2)
        both_btn.pack(pady=10)
        
        # Info frame
        info_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_text = """Main Window: Full process monitoring with GUI
Tray Monitor: Background monitoring with notifications
Both: Run both versions simultaneously"""
        
        info_label = tk.Label(info_frame, text=info_text, 
                             bg='#2d2d2d', fg='#cccccc', font=('Segoe UI', 10),
                             justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # Exit button
        exit_btn = tk.Button(main_frame, text="Exit", 
                            command=self.root.quit,
                            bg='#666666', fg='white', font=('Segoe UI', 10),
                            width=10)
        exit_btn.pack(pady=(10, 0))
    
    def launch_main_window(self):
        """Launch the main process monitor window"""
        try:
            subprocess.Popen([sys.executable, 'process_monitor.py'])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch main window: {str(e)}")
    
    def launch_tray_monitor(self):
        """Launch the system tray monitor"""
        try:
            subprocess.Popen([sys.executable, 'tray_monitor.py'])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch tray monitor: {str(e)}")
    
    def launch_both(self):
        """Launch both the main window and tray monitor"""
        try:
            subprocess.Popen([sys.executable, 'process_monitor.py'])
            subprocess.Popen([sys.executable, 'tray_monitor.py'])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch applications: {str(e)}")
    
    def run(self):
        """Start the launcher"""
        self.root.mainloop()

if __name__ == "__main__":
    launcher = TaskManagerProLauncher()
    launcher.run()
