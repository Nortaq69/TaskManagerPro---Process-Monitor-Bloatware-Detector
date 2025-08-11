# TaskManagerPro - Process Monitor & Bloatware Detector

A powerful Windows 10 desktop application that monitors running processes, detects bloatware, and helps keep your PC clean and optimized.

## 🚀 Features

### Core Functionality
- **Real-time Process Monitoring**: Monitor all running processes with live updates
- **Bloatware Detection**: Built-in database of common Windows 10 bloatware processes
- **Process Management**: Kill unwanted processes with one click
- **Memory & CPU Tracking**: Monitor resource usage for each process
- **Auto-kill Mode**: Automatically terminate detected bloatware processes

### User Interface
- **Modern Dark Theme**: Clean, professional interface with dark mode
- **Sortable Process List**: Sort by PID, name, memory usage, CPU, status, or category
- **Context Menus**: Right-click for quick actions (kill, whitelist, properties)
- **Process Properties**: Detailed information about each process
- **Statistics Panel**: Real-time system statistics

### Advanced Features
- **Whitelist/Blacklist**: Customize which processes to ignore or target
- **System Tray Mode**: Background monitoring with notifications
- **Comprehensive Logging**: All actions logged to file for audit trail
- **Settings Management**: Persistent user preferences
- **Dual Mode Operation**: Run both GUI and tray monitor simultaneously

## 📋 Requirements

- **Operating System**: Windows 10 (64-bit)
- **Python**: 3.7 or higher
- **Administrator Rights**: Required for process termination

## 🛠 Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd TaskManagerProBloat
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python launcher.py
```

## 🎯 Usage

### Launch Options

1. **Launcher (Recommended)**: Run `launcher.py` to choose your preferred mode
2. **Main Window**: Run `process_monitor.py` for full GUI experience
3. **System Tray**: Run `tray_monitor.py` for background monitoring

### Main Window Features

#### Process List
- **PID**: Process ID
- **Name**: Process executable name
- **Memory (MB)**: Current memory usage
- **CPU %**: CPU usage percentage
- **Status**: Process status (running, sleeping, etc.)
- **Category**: Process category (System Service, Browser, etc.)

#### Actions
- **Start/Stop Monitoring**: Toggle real-time monitoring
- **Auto-kill Bloatware**: Automatically terminate detected bloatware
- **Refresh**: Manually refresh process list
- **Settings**: Configure whitelist, blacklist, and preferences

#### Right-click Menu
- **Kill Process**: Terminate selected process
- **Add to Whitelist**: Exclude process from bloatware detection
- **Add to Blacklist**: Mark process for special attention
- **Properties**: View detailed process information

### System Tray Features

#### Tray Menu
- **Show Main Window**: Open the full GUI
- **Start Monitoring**: Begin background monitoring
- **Auto-kill Bloatware**: Toggle automatic termination
- **Settings**: Configure preferences
- **View Log**: Open log file
- **Quit**: Exit application

#### Notifications
- **Bloatware Detection**: Popup notifications when bloatware is detected
- **Auto-kill Confirmations**: Notifications when processes are automatically terminated

## 🎨 Known Bloatware Processes

The application includes a comprehensive database of common Windows 10 bloatware:

### Microsoft Services
- `YourPhone.exe` - Your Phone Companion
- `OneDrive.exe` - OneDrive sync service
- `MicrosoftEdgeUpdate.exe` - Edge browser updates
- `Cortana.exe` - Windows virtual assistant
- `Widgets.exe` - Windows widgets

### Gaming
- `GameBar.exe` - Xbox Game Bar overlay

### Windows Services
- `SearchApp.exe` - Windows search indexing

### OEM Bloatware
- `HPJumpStartBridge.exe` - HP bloatware service
- `DellDataVault.exe` - Dell bloatware service
- `LenovoVantage.exe` - Lenovo system management

### Security Software
- `McAfeeSecurity.exe` - McAfee antivirus
- `NortonSecurity.exe` - Norton antivirus

### Creative Software
- `AdobeCreativeCloud.exe` - Adobe cloud services

### Media & Communication
- `Spotify.exe` - Music streaming service
- `Discord.exe` - Gaming chat application

## ⚙️ Configuration

### Preferences File
The application saves user preferences in `preferences.json`:
```json
{
  "whitelist": ["chrome.exe", "firefox.exe"],
  "blacklist": ["malware.exe"],
  "auto_kill": false
}
```

### Log Files
- `process_monitor.log` - Main application logs
- `tray_monitor.log` - System tray monitor logs

## 🔧 Customization

### Adding Custom Bloatware Definitions
Edit the `BLOAT_PROCESSES` dictionary in the source files:

```python
"CustomProcess.exe": {
    "name": "Custom Process Name",
    "description": "Description of what this process does",
    "severity": "high",  # low, medium, high
    "category": "Custom Category"
}
```

### Whitelist Management
- Add processes to whitelist to exclude them from bloatware detection
- Use the Settings dialog or right-click menu
- Whitelisted processes are ignored by auto-kill

### Blacklist Management
- Add processes to blacklist for special attention
- Blacklisted processes can be targeted for manual termination

## 🛡️ Security Considerations

### Administrator Rights
- Process termination requires administrator privileges
- Some system processes cannot be terminated for security reasons
- The application will show appropriate error messages

### Safe Mode
- Always test in a safe environment first
- Some processes may be critical for system operation
- Use whitelist to exclude important processes

## 🐛 Troubleshooting

### Common Issues

#### "Access Denied" Errors
- Run the application as Administrator
- Some system processes cannot be terminated
- Check if the process is critical for system operation

#### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

#### GUI Not Displaying
- Ensure tkinter is installed: `python -m tkinter`
- Check display settings and resolution
- Try running in compatibility mode

#### System Tray Not Working
- Check if pystray is properly installed
- Ensure system tray is enabled in Windows
- Try running as Administrator

### Performance Optimization
- Adjust monitoring frequency in the code
- Use whitelist to reduce false positives
- Close unnecessary applications before monitoring

## 📝 Logging

### Log Format
```
[2024-01-15 14:30:25] Background monitoring started
[2024-01-15 14:30:30] Detected bloatware: YourPhone.exe, OneDrive.exe
[2024-01-15 14:30:35] Auto-killed: YourPhone.exe (PID: 1234)
```

### Log Locations
- Main application: `process_monitor.log`
- System tray: `tray_monitor.log`
- Preferences: `preferences.json`

## 🤝 Contributing

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

### Reporting Issues
- Include Windows version and Python version
- Provide error messages and log files
- Describe steps to reproduce the issue

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is provided as-is for educational and personal use. Users are responsible for:
- Understanding the implications of terminating processes
- Testing in a safe environment before production use
- Ensuring compliance with their organization's IT policies
- Backing up important data before making system changes

The developers are not responsible for any system instability or data loss resulting from the use of this application.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the log files for error messages
- Ensure all dependencies are properly installed
- Test with administrator privileges

---

**TaskManagerPro** - Keep your Windows 10 system clean and optimized! 🚀
