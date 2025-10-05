import psutil
import os
import platform
import shutil
import yaml
import json
import time
from pathlib import Path
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
            settings_path = os.path.join(
                self.riot_paths['config'],
                'Riot Client',
                self.riot_paths['settings_file']
            )
            
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = yaml.safe_load(f)
                    
                # Try to extract username from settings
                # Note: This might not always work as Riot may store encrypted data
                if settings and isinstance(settings, dict):
                    # Look for username in various possible locations
                    for key, value in settings.items():
                        if 'username' in str(key).lower() or 'user' in str(key).lower():
                            if isinstance(value, str) and '@' in value:
                                return value
                                
                return "User logged in (username not accessible)"
            else:
                return None
                
        except Exception as e:
            print(f"Error getting current user: {e}")
            return None
            
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
            
    def create_account_backup(self, account):
        """Create a backup for a specific account"""
        try:
            # Create account-specific backup directory
            backup_dir = self._get_account_backup_path(account['display_name'])
            os.makedirs(backup_dir, exist_ok=True)
            
            source_dir = os.path.join(self.riot_paths['config'], 'Riot Client')
            if os.path.exists(source_dir):
                # Copy current session to account backup
                shutil.copytree(source_dir, backup_dir, dirs_exist_ok=True)
                
                # Save account info
                account_info = {
                    'username': account['username'],
                    'display_name': account['display_name'],
                    'backup_created': time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                with open(os.path.join(backup_dir, 'account_info.json'), 'w') as f:
                    json.dump(account_info, f, indent=2)
                    
                return True
            return False
            
        except Exception as e:
            print(f"Error creating account backup: {e}")
            return False
            
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
                'Plugins/Authentication',
                'Plugins/rcp-fe-lol-auth'
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
            
            # Step 1: Force logout from current account
            print("Logging out from current account...")
            if self.is_running():
                # First backup current session if logged in
                current_user = self.get_current_user()
                if current_user and current_user != "User logged in (username not accessible)":
                    print("Backing up current session...")
                    self.backup_current_session()
                
                # Force logout
                self.force_logout()
            else:
                # Even if not running, clear any lingering session data
                self.clear_current_session()
                
            # Step 2: Check if we have a backup for this account
            account_backup_dir = self._get_account_backup_path(account['display_name'])
            
            if os.path.exists(account_backup_dir):
                print(f"Restoring session for {account['display_name']}...")
                time.sleep(2)  # Wait after clearing before restoring
                self.restore_session(account_backup_dir)
                print("Session restored! Starting Riot Client...")
                time.sleep(1)
                self.start_riot_client()
            else:
                print(f"No existing session backup for {account['display_name']}")
                print("Starting Riot Client for first-time setup...")
                print(f"Please log in manually with: {account['username']}")
                time.sleep(1)
                self.start_riot_client()
                print("\n=== IMPORTANT ===")
                print("After logging in successfully:")
                print("1. Close Riot Client")
                print("2. Click 'Backup Current Session' in the app")
                print("3. Future switches will be automatic!")
                print("================")
                
            print("Account switch process completed!")
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