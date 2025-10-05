from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QListWidget, 
                             QMessageBox, QStatusBar, QGroupBox, QListWidgetItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
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
        self.setWindowTitle("Riot Account Switcher")
        self.setGeometry(100, 100, 500, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Riot Games Account Switcher")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Current status group
        status_group = QGroupBox("Current Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Checking Riot Client status...")
        status_layout.addWidget(self.status_label)
        
        self.current_account_label = QLabel("No account detected")
        status_layout.addWidget(self.current_account_label)
        
        layout.addWidget(status_group)
        
        # Account management group
        accounts_group = QGroupBox("Saved Accounts")
        accounts_layout = QVBoxLayout(accounts_group)
        
        # Account list
        self.account_list = QListWidget()
        accounts_layout.addWidget(self.account_list)
        
        # Account management buttons
        account_buttons_layout = QHBoxLayout()
        
        self.add_account_btn = QPushButton("Add Account")
        self.add_account_btn.clicked.connect(self.add_account)
        account_buttons_layout.addWidget(self.add_account_btn)
        
        self.edit_account_btn = QPushButton("Edit Account")
        self.edit_account_btn.clicked.connect(self.edit_account)
        account_buttons_layout.addWidget(self.edit_account_btn)
        
        self.delete_account_btn = QPushButton("Delete Account")
        self.delete_account_btn.clicked.connect(self.delete_account)
        account_buttons_layout.addWidget(self.delete_account_btn)
        
        accounts_layout.addLayout(account_buttons_layout)
        
        # Switch button
        self.switch_btn = QPushButton("Switch to Selected Account")
        self.switch_btn.clicked.connect(self.switch_account)
        self.switch_btn.setEnabled(False)
        accounts_layout.addWidget(self.switch_btn)
        
        layout.addWidget(accounts_group)
        
        # Quick actions group
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QHBoxLayout(actions_group)
        
        self.refresh_btn = QPushButton("Refresh Status")
        self.refresh_btn.clicked.connect(self.refresh_status)
        actions_layout.addWidget(self.refresh_btn)
        
        self.backup_btn = QPushButton("Backup Current Session")
        self.backup_btn.clicked.connect(self.backup_session)
        actions_layout.addWidget(self.backup_btn)
        
        layout.addWidget(actions_group)
        
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
            if is_running:
                self.status_label.setText("✅ Riot Client is running")
                current_user = self.riot_client.get_current_user()
                if current_user:
                    self.current_account_label.setText(f"Current account: {current_user}")
                else:
                    self.current_account_label.setText("Account information not available")
            else:
                self.status_label.setText("❌ Riot Client is not running")
                self.current_account_label.setText("Start Riot Client to see account info")
        except Exception as e:
            self.status_label.setText(f"Error checking status: {str(e)}")
            
    def load_accounts(self):
        """Load saved accounts into the list"""
        self.account_list.clear()
        accounts = self.account_manager.get_all_accounts()
        
        for account in accounts:
            item = QListWidgetItem(f"{account['display_name']} ({account['username']})")
            item.setData(Qt.ItemDataRole.UserRole, account['id'])
            self.account_list.addItem(item)
            
    def on_account_selected(self):
        """Handle account selection"""
        selected_items = self.account_list.selectedItems()
        self.switch_btn.setEnabled(len(selected_items) > 0)
        self.edit_account_btn.setEnabled(len(selected_items) > 0)
        self.delete_account_btn.setEnabled(len(selected_items) > 0)
        
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
        
        # Confirm switch
        reply = QMessageBox.question(
            self,
            "Confirm Account Switch",
            f"Switch to account '{account['display_name']}'?\n\nThis will close the Riot Client if it's running.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.riot_client.switch_account(account)
                if success:
                    self.statusBar().showMessage("Account switched successfully!", 5000)
                    QMessageBox.information(self, "Success", f"Successfully switched to {account['display_name']}!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to switch account. Check the logs for details.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to switch account: {str(e)}")
                
    def refresh_status(self):
        """Manually refresh Riot Client status"""
        self.update_riot_status()
        self.statusBar().showMessage("Status refreshed", 2000)
        
    def backup_session(self):
        """Backup current Riot session"""
        try:
            if self.riot_client.backup_current_session():
                QMessageBox.information(self, "Success", "Current session backed up successfully!")
                self.statusBar().showMessage("Session backed up", 3000)
            else:
                QMessageBox.warning(self, "Warning", "No active session to backup")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to backup session: {str(e)}")