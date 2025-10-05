import psutil
import os
import platform
import shutil
import yaml
import json
import time
import subprocess

class RiotClient:
    def __init__(self):
        self.system = platform.system()
        self.riot_paths = self._get_riot_paths()
        self.process_names = [
            'RiotClientServices.exe',
            'RiotClientUx.exe', 
            'RiotClientUxRender.exe',
            'LeagueClient.exe',
            'VALORANT.exe'
        ]
        
    def _get_riot_paths(self):
        """Get Riot Games installation and config paths based on OS"""
        if self.system == "Windows":
            return {
                'config': os.path.expandvars(r'%LOCALAPPDATA%\Riot Games'),
                'install': r'C:\Riot Games',
                'settings_file': 'RiotGamesPrivateSettings.yaml'
            }
        elif self.system == "Darwin":  # macOS
            return {
                'config': os.path.expanduser('~/Library/Application Support/Riot Games'),
                'install': '/Applications/Riot Games',
                'settings_file': 'RiotGamesPrivateSettings.yaml'
            }
        else:  # Linux
            return {
                'config': os.path.expanduser('~/.config/Riot Games'),
                'install': os.path.expanduser('~/.local/share/Riot Games'),
                'settings_file': 'RiotGamesPrivateSettings.yaml'
            }
            
    def is_running(self):
        """Check if any Riot Client process is running"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] in self.process_names:
                    return True
            return False
        except Exception as e:
            print(f"Error checking if Riot Client is running: {e}")
            return False
            
    def get_running_processes(self):
        """Get list of running Riot processes"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] in self.process_names:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'exe': proc.info['exe']
                    })
        except Exception as e:
            print(f"Error getting Riot processes: {e}")
        return processes
        
    def terminate_riot_client(self):
        """Terminate all Riot Client processes"""
        terminated = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] in self.process_names:
                    try:
                        p = psutil.Process(proc.info['pid'])
                        p.terminate()
                        terminated.append(proc.info['name'])
                    except psutil.NoSuchProcess:
                        pass
                    except psutil.AccessDenied:
                        print(f"Access denied when terminating {proc.info['name']}")
                        
            # Wait for processes to terminate
            time.sleep(2)
            
            # Force kill if still running
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] in self.process_names:
                    try:
                        p = psutil.Process(proc.info['pid'])
                        p.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                        
        except Exception as e:
            print(f"Error terminating Riot Client: {e}")
            
        return terminated
        
    def get_current_user(self):
        """Try to get current logged in user from Riot Client"""
        try:
            # Check multiple possible session file locations
            possible_files = [
                os.path.join(self.riot_paths['config'], 'Riot Client', 'RiotGamesPrivateSettings.yaml'),
                os.path.join(self.riot_paths['config'], 'Riot Client', 'Data', 'RiotGamesPrivateSettings.yaml'),
                os.path.join(self.riot_paths['config'], 'Riot Client', 'RiotClientPrivateSettings.yaml'),
                os.path.join(self.riot_paths['config'], 'Riot Client', 'Data', 'RiotClientPrivateSettings.yaml')
            ]
            
            session_files_found = []
            for settings_path in possible_files:
                if os.path.exists(settings_path):
                    session_files_found.append(os.path.basename(settings_path))
                    
                    try:
                        with open(settings_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Try to parse as YAML first
                        try:
                            settings = yaml.safe_load(content)
                            if settings and isinstance(settings, dict):
                                # Look for username in various possible locations
                                for key, value in settings.items():
                                    if 'username' in str(key).lower() or 'user' in str(key).lower() or 'account' in str(key).lower():
                                        if isinstance(value, str) and ('@' in value or len(value) > 3):
                                            return f"Logged in as: {value}"
                        except yaml.YAMLError:
                            # If YAML parsing fails, try to find email patterns in raw content
                            import re
                            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                            emails = re.findall(email_pattern, content)
                            if emails:
                                return f"Logged in as: {emails[0]}"
                                
                    except Exception as e:
                        print(f"Error reading {settings_path}: {e}")
                        
            # If we found session files but couldn't extract username
            if session_files_found:
                return f"User logged in (session active, files: {', '.join(session_files_found)})"
            else:
                return "Not logged in (no session files found)"
                
        except Exception as e:
            print(f"Error getting current user: {e}")
            return "Status unknown (error occurred)"
            
    def backup_current_session(self):
        """Backup current Riot Client session"""
        try:
            source_dir = os.path.join(self.riot_paths['config'], 'Riot Client')
            if not os.path.exists(source_dir):
                return False
                
            # Create backup directory
            backup_dir = os.path.join(os.getcwd(), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f'riot_session_backup_{timestamp}')
            
            # Copy Riot Client directory
            shutil.copytree(source_dir, backup_path, dirs_exist_ok=True)
            
            print(f"Session backed up to: {backup_path}")
            return True
            
        except Exception as e:
            print(f"Error backing up session: {e}")
            return False
            
    def restore_session(self, backup_path):
        """Restore a Riot Client session from backup"""
        try:
            target_dir = os.path.join(self.riot_paths['config'], 'Riot Client')
            
            # Remove current session
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
                
            # Restore from backup
            shutil.copytree(backup_path, target_dir, dirs_exist_ok=True)
            
            print(f"Session restored from: {backup_path}")
            return True
            
        except Exception as e:
            print(f"Error restoring session: {e}")
            return False
            
    def _get_account_backup_path(self, display_name):
        """Get the backup path for a specific account"""
        return os.path.join(os.getcwd(), 'account_backups', display_name)
            
    def backup_account_session(self, account):
        """Create a backup of the current session for a specific account (for 'Stay logged in' sessions)"""
        try:
            print(f"Creating session backup for {account['display_name']}...")
            
            # Ensure user is actually logged in before backing up
            if not self.is_logged_in():
                print("⚠️  Warning: No active session detected. Make sure you're logged in with 'Stay logged in' checked.")
                return False
            
            # Create account-specific backup directory
            backup_dir = self._get_account_backup_path(account['display_name'])
            
            # Remove old backup if exists
            if os.path.exists(backup_dir):
                print("Removing old session backup...")
                shutil.rmtree(backup_dir)
                
            os.makedirs(backup_dir, exist_ok=True)
            
            source_dir = os.path.join(self.riot_paths['config'], 'Riot Client')
            if os.path.exists(source_dir):
                print("Copying session files...")
                # Copy current session to account backup
                shutil.copytree(source_dir, backup_dir, dirs_exist_ok=True)
                
                # Save account info with session details
                account_info = {
                    'username': account['username'],
                    'display_name': account['display_name'],
                    'backup_created': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'session_type': 'stay_logged_in',
                    'riot_client_running': self.is_running(),
                    'backup_size_mb': round(self._get_directory_size(backup_dir) / (1024*1024), 2)
                }
                
                with open(os.path.join(backup_dir, 'account_info.json'), 'w') as f:
                    json.dump(account_info, f, indent=2)
                
                print(f"✅ Session backup created successfully!")
                print(f"   Size: {account_info['backup_size_mb']} MB")
                print(f"   Location: {backup_dir}")
                return True
            else:
                print("❌ No Riot Client config directory found")
                return False
            
        except Exception as e:
            print(f"Error creating account session backup: {e}")
            return False
            
    def _get_directory_size(self, directory):
        """Get total size of directory in bytes"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception as e:
            print(f"Error calculating directory size: {e}")
        return total_size


    def clear_current_session(self):
        """Clear current Riot session data to force logout"""
        try:
            print("Clearing current session data...")
            
            # Main config directory
            config_dir = os.path.join(self.riot_paths['config'], 'Riot Client')
            
            # Files and directories to clear for logout
            logout_targets = [
                'RiotGamesPrivateSettings.yaml',
                'RiotClientPrivateSettings.yaml', 
                'Data/RiotGamesPrivateSettings.yaml',
                'Data/RiotClientPrivateSettings.yaml',
                'Data/Cache',
                'Data/Logs', 
                'Data/CrashReporting',
                'Data/RiotClientInstalls.json',
                'Data/RiotGamesPrivateSettings.json',  # JSON variant
                'Plugins/Authentication',
                'Plugins/rcp-fe-lol-auth',
                'Plugins/rcp-fe-common-libs',
                'RSOData',  # Riot Single Sign-On data
                'LocalStorage',  # Browser-like local storage
                'sessionStorage'  # Session storage
            ]
            
            cleared_items = []
            
            for target in logout_targets:
                target_path = os.path.join(config_dir, target)
                
                if os.path.exists(target_path):
                    try:
                        if os.path.isfile(target_path):
                            os.remove(target_path)
                            cleared_items.append(f"File: {target}")
                        elif os.path.isdir(target_path):
                            shutil.rmtree(target_path)
                            cleared_items.append(f"Dir: {target}")
                    except Exception as e:
                        print(f"Warning: Could not clear {target}: {e}")
                        
            if cleared_items:
                print(f"Cleared {len(cleared_items)} session items:")
                for item in cleared_items:
                    print(f"  - {item}")
                return True
            else:
                print("No session files found to clear")
                return False
                
        except Exception as e:
            print(f"Error clearing session: {e}")
            return False
            
    def is_logged_in(self):
        """Check if someone is currently logged into Riot Client"""
        try:
            # Check for existence of key session files
            session_indicators = [
                os.path.join(self.riot_paths['config'], 'Riot Client', 'Data', 'RiotGamesPrivateSettings.yaml'),
                os.path.join(self.riot_paths['config'], 'Riot Client', 'RiotGamesPrivateSettings.yaml'),
                os.path.join(self.riot_paths['config'], 'Riot Client', 'RSOData'),
                os.path.join(self.riot_paths['config'], 'Riot Client', 'Plugins', 'Authentication')
            ]
            
            active_sessions = 0
            for indicator in session_indicators:
                if os.path.exists(indicator):
                    active_sessions += 1
                    
            # If we have multiple session indicators, likely logged in
            return active_sessions >= 1
            
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False
            
    def force_logout(self):
        """Force logout by clearing session and restarting client"""
        try:
            print("Forcing logout...")
            
            # Step 1: Close Riot Client
            if self.is_running():
                print("Closing Riot Client...")
                self.terminate_riot_client()
                time.sleep(3)
                
            # Step 2: Clear session data
            self.clear_current_session()
            
            # Step 3: Wait a moment for file system
            time.sleep(2)
            
            print("Logout completed!")
            return True
            
        except Exception as e:
            print(f"Error during logout: {e}")
            return False

    def switch_account(self, account):
        """Switch to a different Riot account"""
        try:
            print(f"Switching to account: {account['display_name']}")
            
            # Step 1: Handle current session
            current_logged_in = False
            if self.is_running():
                current_logged_in = self.is_logged_in()
                if current_logged_in:
                    print("Backing up current session...")
                    self.backup_current_session()
                
                print("Closing Riot Client...")
                self.terminate_riot_client()
                time.sleep(3)  # Wait for complete shutdown
            
            # Step 2: Clear current session data to ensure clean switch
            print("Clearing session data...")
            self.clear_current_session()
            time.sleep(1)
                
            # Step 3: Check if we have a saved session for target account
            account_backup_dir = self._get_account_backup_path(account['display_name'])
            
            if os.path.exists(account_backup_dir):
                print(f"Restoring saved session for {account['display_name']}...")
                self.restore_session(account_backup_dir)
                print("✅ Session restored!")
                print("Starting Riot Client...")
                time.sleep(2)
                self.start_riot_client()
                print(f"🎮 Riot Client should now open logged into {account['display_name']}")
                
            else:
                print(f"No saved session found for {account['display_name']}")
                print("Starting Riot Client for manual login...")
                time.sleep(1)
                self.start_riot_client()
                
                print(f"\n📋 SETUP INSTRUCTIONS FOR {account['display_name'].upper()}:")
                print(f"1. Log in with username: {account['username']}")
                print("2. ⚠️  IMPORTANT: Check 'Stay logged in' checkbox!")
                print("3. Complete login process")
                print("4. Close Riot Client when done")
                print("5. Return to this app and click 'Backup Current Session'")
                print("6. ✅ Future switches to this account will be automatic!")
                print("=" * 60)
                
            return True
            
        except Exception as e:
            print(f"Error switching account: {e}")
            return False
            
    def start_riot_client(self):
        """Start the Riot Client"""
        try:
            if self.system == "Windows":
                riot_exe = os.path.join(self.riot_paths['install'], 'Riot Client', 'RiotClientServices.exe')
            elif self.system == "Darwin":
                riot_exe = os.path.join(self.riot_paths['install'], 'Riot Client.app')
            else:  # Linux
                # This would depend on how Riot is installed on Linux (Wine, etc.)
                riot_exe = None
                
            if riot_exe and os.path.exists(riot_exe):
                subprocess.Popen([riot_exe])
                return True
            else:
                print("Riot Client executable not found")
                return False
                
        except Exception as e:
            print(f"Error starting Riot Client: {e}")
            return False