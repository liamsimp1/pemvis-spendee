import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="database/finance.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        # Create tables if they don't exist
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User table for name
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        
        # Insert default user if empty
        cursor.execute('SELECT COUNT(*) FROM user')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO user (name) VALUES (?)', ("[Your Name]",))
        
        conn.commit()
        conn.close()
    
    # TRANSACTIONS CRUD
    def create_transaction(self, transaction_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            transaction_data['date'],
            transaction_data['type'],
            transaction_data['category'],
            transaction_data['amount'],
            transaction_data['description']
        ))
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return transaction_id
    
    def read_transactions(self, limit=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT id, date, type, category, amount, description FROM transactions ORDER BY date DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        transactions = cursor.fetchall()
        conn.close()
        
        return transactions
    
    def update_transaction(self, transaction_id, transaction_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE transactions 
            SET date=?, type=?, category=?, amount=?, description=?
            WHERE id=?
        ''', (
            transaction_data['date'],
            transaction_data['type'],
            transaction_data['category'],
            transaction_data['amount'],
            transaction_data['description'],
            transaction_id
        ))
        
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows
    
    def delete_transaction(self, transaction_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows
    
    def get_summary(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = "income"')
        total_income = cursor.fetchone()[0]
        
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = "expense"')
        total_expense = cursor.fetchone()[0]
        
        balance = total_income - total_expense
        
        conn.close()
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance
        }
    
    # USER RU
    def get_user(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT name FROM user LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'name': result[0]}
        return {'name': '[Your Name]'}
    
    def update_user(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE user SET name = ?', (name,))
        
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows