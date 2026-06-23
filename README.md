# JagaraBrowser

A modern, feature-rich web browser built with PyQt5 and Qt WebEngine, designed with anti-detection capabilities and enhanced user experience features.

## Features

### Core Browser Features
- **Tabbed Browsing** - Multiple tabs with efficient management
- **Address Bar** - Smart address bar with autocomplete and search
- **Bookmarks** - Full bookmark management system
- **History** - Comprehensive browsing history tracking
- **Downloads** - Built-in download manager
- **Settings** - Customizable browser settings

### Anti-Detection & Privacy
- **User Agent Spoofing** - Mimics Chrome 125 on Windows 10
- **WebDriver Removal** - Hides automation fingerprints
- **Privacy Controls** - Hyperlink auditing disabled
- **Secure Settings** - Insecure content blocked by default

### Performance Optimizations
- **Disk Cache** - Persistent caching for faster loading
- **DNS Prefetching** - Faster domain resolution
- **Hardware Acceleration** - WebGL and 2D canvas acceleration
- **Lazy Loading** - Optimized resource loading

### Built-in Tools & Features
- **Ad Blocker** - Built-in advertisement blocking
- **Night Mode** - Dark theme for comfortable browsing
- **Reading Mode** - Distraction-free reading experience
- **Calculator** - Quick access calculator
- **Pomodoro Timer** - Productivity timer
- **RSS Reader** - Built-in RSS feed reader
- **Weather Widget** - Quick weather information
- **Translator** - Text translation support
- **Voice Search** - Voice-activated search
- **Screenshot Tools** - Full page and area screenshots
- **Password Manager** - Secure password storage
- **Proxy Manager** - Proxy configuration support
- **Session Manager** - Save and restore browsing sessions
- **Mouse Gestures** - Gesture-based navigation

### Developer Features
- **CSS Injector** - Custom CSS injection
- **User Scripts** - JavaScript injection support
- **PIP Mode** - Picture-in-Picture video playback

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd JagaraBrowser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the browser:
```bash
python main.py
```

## Project Structure

```
JagaraBrowser/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── LICENSE                 # License file
├── README.md               # This file
├── browser/                # Core browser components
│   ├── window.py           # Main browser window
│   ├── tab.py              # Tab implementation
│   ├── tabwidget.py        # Tab widget manager
│   ├── addressbar.py       # Address bar component
│   ├── bookmark_manager.py # Bookmark management
│   ├── history_manager.py  # History tracking
│   ├── download_manager.py # Download handling
│   ├── sidebar.py          # Side panel
│   ├── newtab.py           # New tab page
│   └── settings_dialog.py  # Settings interface
├── core/                   # Core functionality
│   ├── adblocker.py        # Ad blocking logic
│   ├── password_manager.py # Password storage
│   ├── proxy_manager.py    # Proxy configuration
│   ├── session_manager.py  # Session handling
│   ├── gestures.py         # Mouse gestures
│   ├── optimizer.py        # Performance optimization
│   ├── download_manager.py # Core download logic
│   └── user_scripts.py     # User script injection
├── database/               # Database layer
│   └── db_manager.py       # SQLite database manager
├── features/               # Additional features
│   ├── calculator.py       # Calculator tool
│   ├── night_mode.py       # Dark mode toggle
│   ├── reading_mode.py     # Reading view
│   ├── pomodoro.py         # Pomodoro timer
│   ├── rss_reader.py       # RSS feed reader
│   ├── weather.py          # Weather widget
│   ├── translator.py       # Translation service
│   ├── voice_search.py     # Voice input
│   ├── screenshot.py       # Screenshot capture
│   ├── fullpage_screenshot.py # Full page capture
│   ├── css_injector.py     # CSS injection
│   └── pip.py              # Picture-in-Picture
└── ui/                     # UI components
    ├── resources.py        # UI resources
    └── shortcut_dialog.py  # Keyboard shortcuts
```

## Configuration

The browser stores user data in:
- **Linux/macOS**: `~/.local/share/JagaraBrowser/`
- **Windows**: `%APPDATA%/JagaraBrowser/`

Database location: `~/.jagarabrowser/data.db`

## Requirements

- PyQt5 >= 5.15.0
- PyQtWebEngine >= 5.15.0
- requests
- beautifulsoup4
- Pillow
- pyperclip
- psutil

## Usage Tips

1. **Keyboard Shortcuts**: Use standard browser shortcuts (Ctrl+T for new tab, Ctrl+W to close, etc.)
2. **Bookmarks**: Access bookmark manager from the menu or use Ctrl+Shift+B
3. **History**: View browsing history with Ctrl+H
4. **Downloads**: Check downloads with Ctrl+J
5. **Settings**: Configure browser settings via the menu

## Security Notes

- The browser includes anti-detection features for compatibility with websites that block automated browsers
- Always use responsibly and respect website terms of service
- Passwords are stored locally in an encrypted database

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

See the [LICENSE](LICENSE) file for details.

## Author

JagaraTech

---

*JagaraBrowser - Fast, Private, Feature-Rich*