"""
Simple secure password storage using hashlib + base64 (no external dependencies).
"""
import sqlite3
import os
import hashlib
import base64
from database.db_manager import DatabaseManager

class PasswordVault:
    def __init__(self, master_password: str):
        # Derive key using SHA‑256
        self.key = hashlib.sha256(master_password.encode()).digest()
        # Buat tabel jika belum ada
        DatabaseManager._connection.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                site TEXT PRIMARY KEY,
                username TEXT,
                encrypted_password TEXT
            )
        """)
        DatabaseManager._connection.commit()

    def _xor_encrypt(self, plaintext: str) -> str:
        """Simple XOR encryption with the derived key (repeating)."""
        key = self.key
        encrypted = bytes([ord(c) ^ key[i % len(key)] for i, c in enumerate(plaintext)])
        return base64.urlsafe_b64encode(encrypted).decode()

    def _xor_decrypt(self, ciphertext: str) -> str:
        encrypted = base64.urlsafe_b64decode(ciphertext.encode())
        key = self.key
        plain = ''.join([chr(b ^ key[i % len(key)]) for i, b in enumerate(encrypted)])
        return plain

    def save_password(self, site: str, username: str, password: str):
        enc = self._xor_encrypt(password)
        DatabaseManager._connection.execute(
            "INSERT OR REPLACE INTO passwords (site, username, encrypted_password) VALUES (?, ?, ?)",
            (site, username, enc)
        )
        DatabaseManager._connection.commit()

    def get_password(self, site: str):
        cur = DatabaseManager._connection.execute(
            "SELECT username, encrypted_password FROM passwords WHERE site = ?", (site,)
        )
        row = cur.fetchone()
        if row:
            username, enc = row
            return username, self._xor_decrypt(enc)
        return None, None

    def delete_password(self, site: str):
        DatabaseManager._connection.execute(
            "DELETE FROM passwords WHERE site = ?", (site,)
        )
        DatabaseManager._connection.commit()

    def list_sites(self):
        cur = DatabaseManager._connection.execute("SELECT site, username FROM passwords")
        return cur.fetchall()