import sqlite3
import os
import uuid
from datetime import datetime
from cryptography.fernet import Fernet

class AccountManager:
    def __init__(self, db_path="accounts.db"):
        self.db_path = db_path
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        self.init_database()
        
    def _get_or_create_key(self):
        """Get or create encryption key"""
        key_file = "key.key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
            
    def init_database(self):
        """Initialize the accounts database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            password_encrypted BLOB NOT NULL,
            display_name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_used TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_account(self, username, password, display_name):
        """Add a new account"""
        account_id = str(uuid.uuid4())
        encrypted_password = self.cipher.encrypt(password.encode())
        created_at = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO accounts (id, username, password_encrypted, display_name, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (account_id, username, encrypted_password, display_name, created_at))
        
        conn.commit()
        conn.close()
        
        return account_id
        
    def get_account(self, account_id):
        """Get account by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, username, password_encrypted, display_name, created_at, last_used
        FROM accounts WHERE id = ?
        ''', (account_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            decrypted_password = self.cipher.decrypt(row[2]).decode()
            return {
                'id': row[0],
                'username': row[1],
                'password': decrypted_password,
                'display_name': row[3],
                'created_at': row[4],
                'last_used': row[5]
            }
        return None
        
    def get_all_accounts(self):
        """Get all accounts (without passwords)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, username, display_name, created_at, last_used
        FROM accounts ORDER BY display_name
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        accounts = []
        for row in rows:
            accounts.append({
                'id': row[0],
                'username': row[1],
                'display_name': row[2],
                'created_at': row[3],
                'last_used': row[4]
            })
        return accounts
        
    def update_account(self, account_id, username, password, display_name):
        """Update an existing account"""
        encrypted_password = self.cipher.encrypt(password.encode())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE accounts 
        SET username = ?, password_encrypted = ?, display_name = ?
        WHERE id = ?
        ''', (username, encrypted_password, display_name, account_id))
        
        conn.commit()
        conn.close()
        
    def delete_account(self, account_id):
        """Delete an account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
        
        conn.commit()
        conn.close()
        
    def mark_account_used(self, account_id):
        """Mark an account as recently used"""
        last_used = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE accounts SET last_used = ? WHERE id = ?
        ''', (last_used, account_id))
        
        conn.commit()
        conn.close()