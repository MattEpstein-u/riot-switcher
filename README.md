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

The application works by:

1. **Account Management**: Stores your account credentials securely using encryption
2. **Session Switching**: Backs up and restores Riot Client configuration files
3. **Process Management**: Automatically handles closing and restarting the Riot Client
4. **Configuration Sync**: Manages Riot's private settings and session data

## Usage

### Adding Accounts

1. Click "Add Account" in the main window
2. Enter your account details:
   - **Display Name**: A friendly name for this account (e.g., "Main Account", "Smurf")
   - **Username**: Your Riot Games username or email
   - **Password**: Your account password
3. Click "Add Account" to save

### Switching Accounts

1. Select an account from the list
2. Click "Switch to Selected Account"
3. Confirm the switch (this will close Riot Client if running)
4. The application will handle the rest automatically

### First-Time Setup per Account

The first time you switch to an account:
1. The Riot Client will start but you'll need to log in manually
2. Once logged in, the application will automatically backup this session
3. Future switches to this account will be automatic

## File Structure

```
riot-switcher/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── gui/
│   ├── main_window.py      # Main application window
│   └── account_dialog.py   # Account management dialog
├── core/
│   ├── account_manager.py  # Account storage and encryption
│   └── riot_client.py      # Riot Client interaction
├── backups/                # Session backups (created at runtime)
└── account_backups/        # Account-specific backups (created at runtime)
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