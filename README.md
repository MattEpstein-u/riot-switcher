# Riot Account Switcher

A desktop application to easily switch between multiple Riot Games accounts without manually logging in and out each time.

## Features

- 🔐 **Secure Account Storage**: Encrypted local storage of account credentials
- 🔄 **Quick Account Switching**: One-click switching between saved accounts
- 📊 **Real-time Status**: Monitor Riot Client status and current logged-in account
- 💾 **Session Backup**: Automatic backup and restore of Riot Client sessions
- 🖥️ **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.8 or higher
- Riot Games Client installed

### Setup

1. Clone this repository:
```bash
git clone https://github.com/MattEpstein-u/riot-switcher.git
cd riot-switcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## How It Works

The application leverages Riot's **"Stay logged in"** feature for seamless account switching:

1. **Account Management**: Stores your account credentials securely using encryption
2. **Session Capture**: Backs up your "Stay logged in" sessions after you log in manually
3. **Session Switching**: Swaps between saved sessions to instantly switch accounts
4. **Process Management**: Automatically handles closing and restarting the Riot Client
5. **Smart Detection**: Knows when accounts are ready for automatic switching vs. need setup

## Usage

### Adding Accounts

1. Click "Add Account" in the main window
2. Enter your account details:
   - **Display Name**: A friendly name for this account (e.g., "Main Account", "Smurf")
   - **Username**: Your Riot Games username or email
   - **Password**: Your account password
3. Click "Add Account" to save

### Switching Accounts

#### For Accounts with Saved Sessions (Instant Switch):
1. Select an account from the list
2. Click "🔄 Switch to Selected Account"
3. Confirm the switch
4. Riot Client will open already logged in! 🚀

#### First-Time Setup per Account:
1. Select a new account and click "🚀 Quick Login Guide"
2. Follow the step-by-step instructions
3. **Critical**: When logging in, check the ✅ **"Stay logged in"** box
4. After successful login, close Riot Client
5. Click "Backup Current Session" in the app
6. Future switches to this account will be instant!

### The "Stay Logged In" Workflow

This app is designed around Riot's "Stay logged in" feature:
- ✅ **Check "Stay logged in"** when setting up each account
- 🔄 App swaps these saved sessions for instant switching  
- 🔐 Sessions persist until you manually log out in Riot Client
- ⚡ Switching takes ~5 seconds instead of manual typing

## File Structure

```
riot-switcher/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── build_simple.bat             # Windows build script
├── build_for_friend.py          # Package creation script
├── RiotAccountSwitcher.spec     # PyInstaller specification
├── gui/
│   ├── main_window.py           # Main application window
│   └── account_dialog.py        # Account management dialog
├── core/
│   ├── account_manager.py       # Account storage and encryption
│   └── riot_client.py           # Riot Client interaction
├── backups/                     # Session backups (created at runtime)
└── account_backups/             # Account-specific backups (created at runtime)
```

## Security

- All passwords are encrypted using the `cryptography` library
- Encryption keys are stored locally and never transmitted
- Account data is stored in a local SQLite database
- No network communication - everything works offline

## Troubleshooting

### Common Issues

**"Riot Client not detected"**
- Make sure Riot Games Client is installed in the default location
- Try running the application as administrator (Windows)

**"Failed to switch account"**
- Ensure Riot Client is completely closed before switching
- Check that you have write permissions to the Riot Games config directory

**"Account backup failed"**
- Verify you have sufficient disk space
- Check file permissions in the application directory

### Platform-Specific Notes

**Windows**: Config files are stored in `%LOCALAPPDATA%\Riot Games`
**macOS**: Config files are stored in `~/Library/Application Support/Riot Games`
**Linux**: Config files are stored in `~/.config/Riot Games` (Wine installations)

## Development

### Running from Source

```bash
# Install development dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

This application interacts with Riot Games Client configuration files. Use at your own risk and ensure you comply with Riot Games' Terms of Service. Always keep backups of your important data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.