from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AccountDialog(QDialog):
    def __init__(self, parent=None, account=None):
        super().__init__(parent)
        self.account = account
        self.init_ui()
        
        if account:
            self.load_account_data()
            
    def init_ui(self):
        self.setWindowTitle("Add Account" if not self.account else "Edit Account")
        self.setModal(True)
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Add New Account" if not self.account else "Edit Account")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Display name
        self.display_name_edit = QLineEdit()
        self.display_name_edit.setPlaceholderText("e.g., Main Account, Smurf, etc.")
        form_layout.addRow("Display Name:", self.display_name_edit)
        
        # Username
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Riot Games username/email")
        form_layout.addRow("Username:", self.username_edit)
        
        # Password
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Account password")
        form_layout.addRow("Password:", self.password_edit)
        
        layout.addLayout(form_layout)
        
        # Show/Hide password button
        password_layout = QHBoxLayout()
        self.show_password_btn = QPushButton("Show")
        self.show_password_btn.setFixedWidth(60)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addStretch()
        password_layout.addWidget(self.show_password_btn)
        layout.addLayout(password_layout)
        
        # Warning label
        warning_label = QLabel("⚠️ Passwords are encrypted and stored locally only")
        warning_label.setStyleSheet("color: orange; font-size: 11px;")
        warning_label.setWordWrap(True)
        layout.addWidget(warning_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Save" if self.account else "Add Account")
        self.save_btn.clicked.connect(self.save_account)
        self.save_btn.setDefault(True)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        # Connect enter key to save
        self.display_name_edit.returnPressed.connect(self.save_account)
        self.username_edit.returnPressed.connect(self.save_account)
        self.password_edit.returnPressed.connect(self.save_account)
        
    def load_account_data(self):
        """Load existing account data into the form"""
        if self.account:
            self.display_name_edit.setText(self.account['display_name'])
            self.username_edit.setText(self.account['username'])
            self.password_edit.setText(self.account['password'])
            
    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        if self.password_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password_btn.setText("Hide")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password_btn.setText("Show")
            
    def save_account(self):
        """Validate and save account data"""
        display_name = self.display_name_edit.text().strip()
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        # Validation
        if not display_name:
            QMessageBox.warning(self, "Validation Error", "Please enter a display name.")
            self.display_name_edit.setFocus()
            return
            
        if not username:
            QMessageBox.warning(self, "Validation Error", "Please enter a username.")
            self.username_edit.setFocus()
            return
            
        if not password:
            QMessageBox.warning(self, "Validation Error", "Please enter a password.")
            self.password_edit.setFocus()
            return
            
        if len(password) < 3:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 3 characters long.")
            self.password_edit.setFocus()
            return
            
        self.accept()
        
    def get_account_data(self):
        """Get the account data from the form"""
        return {
            'display_name': self.display_name_edit.text().strip(),
            'username': self.username_edit.text().strip(),
            'password': self.password_edit.text()
        }