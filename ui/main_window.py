from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QPushButton, 
    QLabel, QMessageBox, QHeaderView, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction
from database.db_manager import DatabaseManager
from ui.transaction_dialog import TransactionDialog
from ui.about_dialog import AboutDialog
from ui.account_dialog import AccountDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setWindowTitle("Spendee: Spend Less, Save More")
        self.init_ui()
        self.load_user_info()
        
        self.load_transactions()
        self.update_summary()
    
    def init_ui(self):
        self.setMinimumSize(950, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)
        
        # Header
        header = QLabel("Spendee: Spend Less, Save More")
        header.setObjectName("header")
        main_layout.addWidget(header)
        
        # User Info
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QHBoxLayout(info_frame)
        
        self.name_label = QLabel("👤 Nama: Loading...")
        self.name_label.setObjectName("userName")
        
        info_layout.addWidget(self.name_label)
        info_layout.addStretch()
        
        main_layout.addWidget(info_frame)
        
        # Summary Keuangan
        summary_frame = QFrame()
        summary_frame.setObjectName("summaryFrame")
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setSpacing(20)
        
        # Income
        income_box = QWidget()
        income_layout = QVBoxLayout(income_box)
        income_layout.setSpacing(4)
        income_title = QLabel("INCOME")
        income_title.setObjectName("incomeTitle")
        self.income_value = QLabel("Rp 0")
        self.income_value.setObjectName("incomeValue")
        income_layout.addWidget(income_title)
        income_layout.addWidget(self.income_value)
        
        # Expense
        expense_box = QWidget()
        expense_layout = QVBoxLayout(expense_box)
        expense_layout.setSpacing(4)
        expense_title = QLabel("EXPENSE")
        expense_title.setObjectName("expenseTitle")
        self.expense_value = QLabel("Rp 0")
        self.expense_value.setObjectName("expenseValue")
        expense_layout.addWidget(expense_title)
        expense_layout.addWidget(self.expense_value)
        
        # Balance
        balance_box = QWidget()
        balance_layout = QVBoxLayout(balance_box)
        balance_layout.setSpacing(4)
        balance_title = QLabel("BALANCE")
        balance_title.setObjectName("balanceTitle")
        self.balance_value = QLabel("Rp 0")
        self.balance_value.setObjectName("balanceValue")
        balance_layout.addWidget(balance_title)
        balance_layout.addWidget(self.balance_value)
        
        summary_layout.addWidget(income_box)
        summary_layout.addWidget(expense_box)
        summary_layout.addWidget(balance_box)
        
        main_layout.addWidget(summary_frame)
        
        # Fitur CRUD
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_btn = QPushButton("+ Add")
        self.add_btn.clicked.connect(self.add_transaction)
        
        self.edit_btn = QPushButton("✎ Edit")
        self.edit_btn.clicked.connect(self.edit_transaction)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_transaction)
        
        self.refresh_btn = QPushButton("↻ Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(button_layout)
        
        # Tabel Transaksi
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Type", "Category", "Amount", "Note"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        main_layout.addWidget(self.table)
        
        hint = QLabel("⚡ Double-click row to edit")
        hint.setObjectName("statusHint")
        hint.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(hint)
        
        self.create_menu_bar()
    
    def load_user_info(self):
        # Load info user dari database
        user = self.db.get_user()
        self.name_label.setText(f"Halo, {user['name']}!")
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu Akun
        account_menu = menubar.addMenu("👤 Account")
        
        edit_profile_action = QAction("✎ Edit Profile", self)
        edit_profile_action.triggered.connect(self.edit_profile)
        account_menu.addAction(edit_profile_action)
        
        account_menu.addSeparator()
        
        # Menu Help
        help_menu = menubar.addMenu("? Help")
        
        about_action = QAction("ℹ About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        help_menu.addSeparator()
        
        exit_action = QAction("✖ Exit", self)
        exit_action.triggered.connect(self.close)
        help_menu.addAction(exit_action)
    
    def edit_profile(self):
        current_user = self.db.get_user()
        
        dialog = AccountDialog(self, current_user['name'])
        if dialog.exec():
            new_data = dialog.get_user_data()
            self.db.update_user(new_data['name'])
            self.load_user_info()
            QMessageBox.information(self, "Success", "✓ Profile updated successfully!")
    
    def load_transactions(self):
        transactions = self.db.read_transactions()
        self.table.setRowCount(len(transactions))
        
        for row, trans in enumerate(transactions):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(trans[0])))
            
            # Date
            date_item = QTableWidgetItem(trans[1])
            date_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, date_item)
            
            # Type
            if trans[2] == 'income':
                type_text = "▲ INCOME"
                type_color = QColor(5, 150, 105)
            else:
                type_text = "▼ EXPENSE"
                type_color = QColor(220, 38, 38)
            
            type_item = QTableWidgetItem(type_text)
            type_item.setTextAlignment(Qt.AlignCenter)
            type_item.setForeground(type_color)
            self.table.setItem(row, 2, type_item)
            
            # Category
            self.table.setItem(row, 3, QTableWidgetItem(trans[3]))
            
            # Amount
            amount_text = f"Rp {trans[4]:,.0f}"
            amount_item = QTableWidgetItem(amount_text)
            amount_item.setTextAlignment(Qt.AlignRight)
            if trans[2] == 'income':
                amount_item.setForeground(QColor(5, 150, 105))
            else:
                amount_item.setForeground(QColor(220, 38, 38))
            self.table.setItem(row, 4, amount_item)
            
            # Description
            desc = trans[5] if trans[5] else "-"
            self.table.setItem(row, 5, QTableWidgetItem(desc))
        
        self.table.doubleClicked.connect(self.edit_transaction)
    
    def update_summary(self):
        summary = self.db.get_summary()
        self.income_value.setText(f"Rp {summary['total_income']:,.0f}")
        self.expense_value.setText(f"Rp {summary['total_expense']:,.0f}")
        self.balance_value.setText(f"Rp {summary['balance']:,.0f}")
    
    def add_transaction(self):
        dialog = TransactionDialog(self)
        if dialog.exec():
            data = dialog.get_transaction_data()
            self.db.create_transaction(data)
            self.load_transactions()
            self.update_summary()
            QMessageBox.information(self, "Success", "✓ Transaction added")
    
    def edit_transaction(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "⚠ Select a transaction to edit")
            return
        
        tid = int(self.table.item(row, 0).text())
        amount_raw = self.table.item(row, 4).text().replace('Rp ', '').replace(',', '')
        
        type_raw = self.table.item(row, 2).text().replace("▲ ", "").replace("▼ ", "").lower()
        
        data = {
            'date': self.table.item(row, 1).text(),
            'type': type_raw,
            'category': self.table.item(row, 3).text(),
            'amount': float(amount_raw),
            'description': self.table.item(row, 5).text() if self.table.item(row, 5).text() != "-" else ""
        }
        
        dialog = TransactionDialog(self, data)
        if dialog.exec():
            new_data = dialog.get_transaction_data()
            self.db.update_transaction(tid, new_data)
            self.load_transactions()
            self.update_summary()
            QMessageBox.information(self, "Success", "✓ Transaction updated")
    
    def delete_transaction(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "⚠ Select a transaction to delete")
            return
        
        tid = int(self.table.item(row, 0).text())
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Delete this transaction?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_transaction(tid)
            self.load_transactions()
            self.update_summary()
            QMessageBox.information(self, "Success", "✓ Transaction deleted")
    
    def refresh_data(self):
        self.load_transactions()
        self.update_summary()
    
    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()