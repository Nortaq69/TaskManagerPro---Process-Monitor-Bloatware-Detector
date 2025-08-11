# TaskManagerPro Configuration File
# Modify these settings to customize the application behavior

# Monitoring Settings
MONITORING_INTERVAL = 2  # Seconds between process list updates (main window)
TRAY_MONITORING_INTERVAL = 5  # Seconds between checks (system tray)
AUTO_KILL_TIMEOUT = 3  # Seconds to wait before force killing a process

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
LAUNCHER_WIDTH = 400
LAUNCHER_HEIGHT = 300

# Colors (Dark Theme)
COLORS = {
    'background': '#1e1e1e',
    'secondary_bg': '#2d2d2d',
    'accent': '#404040',
    'primary': '#0078d4',
    'success': '#00ff00',
    'warning': '#ff6b6b',
    'error': '#d83b01',
    'text': '#ffffff',
    'text_secondary': '#cccccc'
}

# Logging Settings
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = '[{timestamp}] {message}'
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Process Categories for Auto-categorization
PROCESS_CATEGORIES = {
    'browser': ['chrome', 'firefox', 'edge', 'opera', 'safari'],
    'system_service': ['svchost', 'winlogon', 'wininit', 'lsass', 'csrss'],
    'windows_shell': ['explorer', 'dwm', 'taskmgr'],
    'antivirus': ['avast', 'avg', 'norton', 'mcafee', 'kaspersky', 'malwarebytes'],
    'gaming': ['steam', 'origin', 'uplay', 'battle.net', 'epicgames'],
    'development': ['code', 'pycharm', 'intellij', 'visualstudio', 'notepad++'],
    'media': ['spotify', 'vlc', 'windowsmediaplayer', 'itunes'],
    'communication': ['discord', 'teams', 'skype', 'zoom', 'slack']
}

# Custom Bloatware Definitions (add your own here)
CUSTOM_BLOATWARE = {
    # Example:
    # "MyCustomProcess.exe": {
    #     "name": "My Custom Process",
    #     "description": "Description of what this process does",
    #     "severity": "medium",  # low, medium, high
    #     "category": "Custom Category"
    # }
}

# Performance Settings
MAX_PROCESSES_DISPLAY = 1000  # Maximum processes to show in GUI
MEMORY_THRESHOLD = 100  # MB - Processes using more memory than this will be highlighted
CPU_THRESHOLD = 10  # % - Processes using more CPU than this will be highlighted

# Notification Settings
ENABLE_NOTIFICATIONS = True
NOTIFICATION_DURATION = 5000  # milliseconds
SHOW_NOTIFICATIONS_ON_STARTUP = False

# Security Settings
REQUIRE_ADMIN_FOR_KILL = True
CONFIRM_PROCESS_KILL = True
SAFE_MODE = False  # If True, prevents killing system-critical processes

# System Critical Processes (never kill these)
CRITICAL_PROCESSES = [
    'System',
    'Registry',
    'smss.exe',
    'csrss.exe',
    'wininit.exe',
    'services.exe',
    'lsass.exe',
    'winlogon.exe',
    'explorer.exe',
    'dwm.exe'
]

# File Paths
DEFAULT_LOG_DIR = '.'  # Current directory
PREFERENCES_FILE = 'preferences.json'
MAIN_LOG_FILE = 'process_monitor.log'
TRAY_LOG_FILE = 'tray_monitor.log'

# Advanced Settings
ENABLE_PROCESS_TREE = False  # Show process parent-child relationships
ENABLE_NETWORK_MONITORING = False  # Monitor network connections
ENABLE_FILE_MONITORING = False  # Monitor file system activity
ENABLE_REGISTRY_MONITORING = False  # Monitor registry changes

# Export Settings
EXPORT_FORMATS = ['txt', 'csv', 'json']
DEFAULT_EXPORT_FORMAT = 'txt'

# Update Settings
CHECK_FOR_UPDATES = False
UPDATE_URL = 'https://api.github.com/repos/your-repo/releases/latest'

# Debug Settings
DEBUG_MODE = False
VERBOSE_LOGGING = False
SHOW_PROCESS_DETAILS = True
