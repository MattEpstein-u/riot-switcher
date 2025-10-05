import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QListWidget, 
                             QMessageBox, QListWidgetItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from core.account_manager import AccountManager
from core.riot_client import RiotClient
from gui.account_dialog import AccountDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.account_manager = AccountManager()
        self.riot_client = RiotClient()
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        self.setWindowTitle("🎮 Riot Account Switcher")
        self.setGeometry(100, 100, 600, 500)  # Larger size as shown in screenshot
        self.setMinimumSize(580, 480)
        
        # Modern dark theme optimized for account switching
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #404040;
                border-radius: 6px;
                margin: 4px 0px;
                padding-top: 8px;
                background-color: #252525;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 6px 12px;
                color: white;
                font-weight: 500;
                min-height: 16px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border-color: #666666;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
                border-color: #333333;
            }
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 4px;
                selection-background-color: #0078d4;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 3px;
                margin: 1px;
            }
            QListWidget::item:hover {
                background-color: #373737;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QLabel {
                color: #ffffff;
            }
            QStatusBar {
                background-color: #1e1e1e;
                color: #cccccc;
                border-top: 1px solid #404040;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with reduced spacing
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(8)  # Reduced spacing
        layout.setContentsMargins(12, 12, 12, 12)  # Tighter margins
        
        # Compact status bar at top
        status_frame = QWidget()
        status_frame.setStyleSheet("QWidget { background-color: #2b2b2b; border-radius: 6px; padding: 8px; }")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setSpacing(4)
        status_layout.setContentsMargins(8, 6, 8, 6)
        
        self.status_label = QLabel("⟳ Checking...")
        self.status_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        self.current_account_label = QLabel("No account detected")
        self.current_account_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        status_layout.addWidget(self.current_account_label)
        
        layout.addWidget(status_frame)
        
        # Main accounts section
        main_section = QHBoxLayout()
        
        # Left side - Account list (compact)
        left_panel = QVBoxLayout()
        
        # Compact accounts section
        accounts_label = QLabel("🎯 Your Accounts")
        accounts_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
        left_panel.addWidget(accounts_label)
        
        # Account list - larger size for better visibility
        self.account_list = QListWidget()
        self.account_list.setMaximumHeight(220)  # More space for better viewing
        self.account_list.setAlternatingRowColors(True)
        self.account_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QListWidget::item {
                padding: 10px 8px;
                border-radius: 4px;
                margin: 1px;
                border-bottom: 1px solid #333333;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
                font-weight: 500;
            }
            QListWidget::item:hover {
                background-color: #373737;
            }
            QListWidget::item:hover {
                background-color: #484848;
            }
        """)
        left_panel.addWidget(self.account_list)
        
        # Small account management buttons
        small_buttons_layout = QHBoxLayout()
        small_buttons_layout.setSpacing(4)
        
        self.add_account_btn = QPushButton("+ Add")
        self.add_account_btn.clicked.connect(self.add_account)
        self.add_account_btn.setFixedHeight(24)
        small_buttons_layout.addWidget(self.add_account_btn)
        
        self.edit_account_btn = QPushButton("✏ Edit")
        self.edit_account_btn.clicked.connect(self.edit_account)
        self.edit_account_btn.setEnabled(False)
        self.edit_account_btn.setFixedHeight(24)
        small_buttons_layout.addWidget(self.edit_account_btn)
        
        self.delete_account_btn = QPushButton("🗑 Del")
        self.delete_account_btn.clicked.connect(self.delete_account)
        self.delete_account_btn.setEnabled(False)
        self.delete_account_btn.setFixedHeight(24)
        small_buttons_layout.addWidget(self.delete_account_btn)
        
        left_panel.addLayout(small_buttons_layout)
        
        # Right side - Action buttons
        right_panel = QVBoxLayout()
        right_panel.setSpacing(6)
        
        self.switch_btn = QPushButton("� SWITCH")
        self.switch_btn.clicked.connect(self.switch_account)
        self.switch_btn.setEnabled(False)
        self.switch_btn.setFixedHeight(40)
        self.switch_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        right_panel.addWidget(self.switch_btn)
        
        self.login_help_btn = QPushButton("� Setup Guide")
        self.login_help_btn.clicked.connect(self.show_login_guide)
        self.login_help_btn.setEnabled(False)
        self.login_help_btn.setFixedHeight(30)
        self.login_help_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        right_panel.addWidget(self.login_help_btn)
        
        # Quick actions in right panel
        self.backup_btn = QPushButton("💾 Backup Session")
        self.backup_btn.clicked.connect(self.backup_session)
        self.backup_btn.setFixedHeight(30)
        self.backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        right_panel.addWidget(self.backup_btn)
        
        right_panel.addStretch()  # Push everything to top
        
        # Add panels to main section
        main_section.addLayout(left_panel, 2)  # Give more space to accounts
        main_section.addLayout(right_panel, 1)  # Less space for buttons
        
        layout.addLayout(main_section)
        
        # Bottom toolbar - compact utility buttons
        bottom_toolbar = QHBoxLayout()
        bottom_toolbar.setSpacing(6)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.refresh_status)
        self.refresh_btn.setFixedHeight(24)
        self.refresh_btn.setToolTip("Refresh Riot Client status and account information")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: 500;
                padding: 4px 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.refresh_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        bottom_toolbar.addWidget(self.refresh_btn)
        
        self.logout_btn = QPushButton("⚠ Logout")
        self.logout_btn.clicked.connect(self.force_logout)
        self.logout_btn.setFixedHeight(24)
        self.logout_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; border-radius: 4px; }")
        bottom_toolbar.addWidget(self.logout_btn)
        
        self.clear_session_btn = QPushButton("🧹 Clear")
        self.clear_session_btn.clicked.connect(self.clear_session)
        self.clear_session_btn.setFixedHeight(24)
        self.clear_session_btn.setStyleSheet("QPushButton { background-color: #FF5722; color: white; border-radius: 4px; }")
        bottom_toolbar.addWidget(self.clear_session_btn)
        
        bottom_toolbar.addStretch()  # Push buttons to left
        
        layout.addLayout(bottom_toolbar)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Connect list selection
        self.account_list.itemSelectionChanged.connect(self.on_account_selected)
        
        # Load saved accounts
        self.load_accounts()
        
    def setup_timer(self):
        """Setup timer to periodically check Riot Client status"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_riot_status)
        self.timer.start(5000)  # Check every 5 seconds
        self.update_riot_status()  # Initial check
        
    def update_riot_status(self):
        """Update the Riot Client status display"""
        try:
            is_running = self.riot_client.is_running()
            is_logged_in = self.riot_client.is_logged_in()
            
            if is_running and is_logged_in:
                self.status_label.setText("🟢 Riot Client - Active & Logged In")
                current_user = self.riot_client.get_current_user()
                self.current_account_label.setText(f"{current_user}")
            elif is_running:
                self.status_label.setText("🟡 Riot Client - Running (Not Logged In)")
                self.current_account_label.setText("Ready for login")
            else:
                self.status_label.setText("🔴 Riot Client - Not Running")
                self.current_account_label.setText("Start client or use switcher")
        except Exception as e:
            self.status_label.setText(f"⚠️ Status Error")
            self.current_account_label.setText(f"Error: {str(e)[:50]}...")
            
    def load_accounts(self):
        """Load saved accounts into the list"""
        self.account_list.clear()
        accounts = self.account_manager.get_all_accounts()
        
        for account in accounts:
            # Check if account has saved session
            account_backup_dir = self.riot_client._get_account_backup_path(account['display_name'])
            has_session = os.path.exists(account_backup_dir)
            
            # Create status indicator
            if has_session:
                status_icon = "✅"
                status_text = "Ready"
            else:
                status_icon = "⚙"
                status_text = "Setup needed"
            
            # Format: "🎮 Display Name (username) ✅ Ready"
            display_text = f"🎮 {account['display_name']} ({account['username']}) {status_icon}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, account['id'])
            
            # Add tooltip with more info
            if has_session:
                item.setToolTip(f"Ready for instant switching\nLast used: {account.get('last_used', 'Never')}")
            else:
                item.setToolTip(f"Needs first-time setup\nClick 'Setup Guide' after selecting")
            
            self.account_list.addItem(item)
            
    def on_account_selected(self):
        """Handle account selection"""
        selected_items = self.account_list.selectedItems()
        has_selection = len(selected_items) > 0
        self.switch_btn.setEnabled(has_selection)
        self.edit_account_btn.setEnabled(has_selection)
        self.delete_account_btn.setEnabled(has_selection)
        self.login_help_btn.setEnabled(has_selection)
        
    def add_account(self):
        """Open dialog to add new account"""
        dialog = AccountDialog(self)
        if dialog.exec() == AccountDialog.DialogCode.Accepted.value:
            account_data = dialog.get_account_data()
            try:
                self.account_manager.add_account(
                    account_data['username'],
                    account_data['password'],
                    account_data['display_name']
                )
                self.load_accounts()
                self.statusBar().showMessage("Account added successfully", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to add account: {str(e)}")
                
    def edit_account(self):
        """Edit selected account"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            return
            
        account_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        account = self.account_manager.get_account(account_id)
        
        dialog = AccountDialog(self, account)
        if dialog.exec() == AccountDialog.DialogCode.Accepted.value:
            account_data = dialog.get_account_data()
            try:
                self.account_manager.update_account(
                    account_id,
                    account_data['username'],
                    account_data['password'],
                    account_data['display_name']
                )
                self.load_accounts()
                self.statusBar().showMessage("Account updated successfully", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to update account: {str(e)}")
                
    def delete_account(self):
        """Delete selected account"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            return
            
        account_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        account = self.account_manager.get_account(account_id)
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete the account '{account['display_name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.account_manager.delete_account(account_id)
                self.load_accounts()
                self.statusBar().showMessage("Account deleted successfully", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete account: {str(e)}")
                
    def switch_account(self):
        """Switch to selected account"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            return
            
        account_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        account = self.account_manager.get_account(account_id)
        
        # Switch immediately without confirmation
        try:
            self.statusBar().showMessage(f"Switching to {account['display_name']}...", 0)
            success = self.riot_client.switch_account(account)
            if success:
                # Mark account as used
                self.account_manager.mark_account_used(account_id)
                self.load_accounts()  # Refresh the list
                
                # Check if this was first time setup (only show message for first-time setup)
                account_backup_dir = self.riot_client._get_account_backup_path(account['display_name'])
                if not account_backup_dir or not os.path.exists(account_backup_dir):
                    # Only show dialog for first-time setup guidance
                    QMessageBox.information(
                        self, 
                        "First Time Setup", 
                        f"Successfully initiated switch to {account['display_name']}!\n\n"
                        "IMPORTANT: After logging in successfully:\n"
                        "1. Close Riot Client\n"
                        "2. Click '💾 Backup Session'\n"
                        "3. Future switches will be instant!"
                    )
                    self.statusBar().showMessage("First-time setup initiated - follow the instructions", 8000)
                else:
                    # For established accounts, just show status bar message
                    self.statusBar().showMessage(f"✅ Switched to {account['display_name']}", 4000)
            else:
                QMessageBox.warning(self, "Switch Failed", "Failed to switch account. Please try again or check Riot Client status.")
                self.statusBar().showMessage("Switch failed", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to switch account: {str(e)}")
            self.statusBar().showMessage("Switch failed", 3000)
                    
    def refresh_status(self):
        """Manually refresh Riot Client status"""
        self.update_riot_status()
        self.statusBar().showMessage("Status refreshed", 2000)
        
    def backup_session(self):
        """Backup current Riot session for the logged-in account"""
        # Check if someone is logged in
        if not self.riot_client.is_logged_in():
            QMessageBox.warning(
                self, 
                "No Session Found", 
                "No active session detected.\n\n"
                "To create a session backup:\n"
                "1. Log into Riot Client\n"
                "2. ✅ Check 'Stay logged in' box\n"
                "3. Complete login\n"
                "4. Try backup again"
            )
            return
            
        # Ask which account this session belongs to
        accounts = self.account_manager.get_all_accounts()
        if not accounts:
            QMessageBox.warning(
                self,
                "No Accounts Found",
                "You need to add accounts first before backing up sessions.\n\nClick 'Add Account' to get started."
            )
            return
            
        # If only one account, use it automatically
        if len(accounts) == 1:
            target_account = accounts[0]
            full_account = self.account_manager.get_account(target_account['id'])
        else:
            # Let user choose which account this session belongs to
            from PyQt6.QtWidgets import QInputDialog
            account_names = [f"{acc['display_name']} ({acc['username']})" for acc in accounts]
            
            selected_name, ok = QInputDialog.getItem(
                self,
                "Select Account",
                "Which account does this session belong to?",
                account_names,
                0,
                False
            )
            
            if not ok:
                return
                
            # Find the selected account
            selected_index = account_names.index(selected_name)
            target_account = accounts[selected_index]
            full_account = self.account_manager.get_account(target_account['id'])
        
        try:
            self.statusBar().showMessage("Creating session backup...", 0)
            success = self.riot_client.backup_account_session(full_account)
            
            if success:
                QMessageBox.information(
                    self, 
                    "Session Backed Up!", 
                    f"✅ Session successfully backed up for {full_account['display_name']}!\n\n"
                    "This account can now be switched to automatically.\n"
                    "The session will persist as long as 'Stay logged in' was checked."
                )
                self.statusBar().showMessage(f"Session backed up for {full_account['display_name']}", 5000)
                
                # Mark account as used and refresh
                self.account_manager.mark_account_used(full_account['id'])
                self.load_accounts()
            else:
                QMessageBox.warning(
                    self, 
                    "Backup Failed", 
                    "Failed to backup session.\n\nMake sure:\n"
                    "• You're logged into Riot Client\n"
                    "• 'Stay logged in' was checked\n"
                    "• The application has file write permissions"
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to backup session: {str(e)}")
            self.statusBar().showMessage("Backup failed", 3000)
            
    def force_logout(self):
        """Force logout from current account"""
        reply = QMessageBox.question(
            self,
            "Confirm Force Logout",
            "This will force logout from the current Riot account.\nAny unsaved progress may be lost.\n\nContinue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.statusBar().showMessage("Forcing logout...", 0)
                success = self.riot_client.force_logout()
                if success:
                    QMessageBox.information(self, "Success", "Successfully logged out!")
                    self.statusBar().showMessage("Logged out successfully", 3000)
                    self.update_riot_status()  # Refresh status
                else:
                    QMessageBox.warning(self, "Warning", "Logout completed but some files couldn't be cleared")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to logout: {str(e)}")
                self.statusBar().showMessage("Logout failed", 3000)
                
    def clear_session(self):
        """Clear session data without closing client"""
        reply = QMessageBox.question(
            self,
            "Confirm Clear Session",
            "This will clear session data while keeping Riot Client running.\nYou may need to restart the client.\n\nContinue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.statusBar().showMessage("Clearing session data...", 0)
                success = self.riot_client.clear_current_session()
                if success:
                    QMessageBox.information(self, "Success", "Session data cleared!")
                    self.statusBar().showMessage("Session data cleared", 3000)
                else:
                    QMessageBox.information(self, "Info", "No session data found to clear")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clear session: {str(e)}")
                self.statusBar().showMessage("Clear failed", 3000)
                
    def show_login_guide(self):
        """Show login guide for selected account"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            return
            
        account_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        account = self.account_manager.get_account(account_id)
        
        # Check if account already has a saved session
        account_backup_dir = self.riot_client._get_account_backup_path(account['display_name'])
        has_saved_session = os.path.exists(account_backup_dir)
        
        if has_saved_session:
            guide_text = f"""🎮 Account: {account['display_name']}
✅ Status: Ready for automatic switching!

This account already has a saved session.
Click "Switch to Selected Account" for instant login.

💡 Tip: If switching doesn't work, the saved session might be expired. 
You can create a fresh session by:
1. Manually logging in again
2. Checking "Stay logged in"  
3. Clicking "Backup Current Session"
            """
        else:
            guide_text = f"""🎮 Account: {account['display_name']}
⚠️  Status: First-time setup required

📋 SETUP STEPS:
1. Click "Switch to Selected Account" below
2. Riot Client will open to login screen
3. Enter credentials:
   • Username: {account['username']}
   • Password: [your password]
4. ✅ IMPORTANT: Check "Stay logged in" box!
5. Complete login process
6. Close Riot Client when done
7. Come back here and click "Backup Current Session"

🏆 After setup: Future switches will be instant!
            """
            
        QMessageBox.information(
            self,
            f"Login Guide - {account['display_name']}",
            guide_text
        )