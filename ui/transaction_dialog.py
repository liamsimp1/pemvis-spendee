from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QComboBox, QPushButton, QDateEdit, QDoubleSpinBox, QTextEdit, QMessageBox
)
from PySide6.QtCore import QDate
from logic.validator import TransactionValidator

class TransactionDialog(QDialog):
    def __init__(self, parent=None, existing_data=None):
        super().__init__(parent)
        self.existing_data = existing_data
        self.init_ui()
        
        if existing_data:
            self.setWindowTitle("Edit Transaction")
            self.load_existing_data()
        else:
            self.setWindowTitle("Add Transaction")
    
    def init_ui(self):
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        
        # Form
        form = QFormLayout()
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form.addRow("Date:", self.date_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        form.addRow("Type:", self.type_combo)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Salary", "Food", "Transport", "Shopping", "Other"])
        self.category_combo.setEditable(True)
        form.addRow("Category:", self.category_combo)
        
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0, 999999999)
        self.amount_spin.setPrefix("Rp ")
        self.amount_spin.setSingleStep(10000)
        form.addRow("Amount:", self.amount_spin)
        
        self.desc_text = QTextEdit()
        self.desc_text.setMaximumHeight(80)
        form.addRow("Description:", self.desc_text)
        
        layout.addLayout(form)
        
        # Tombol Simpan dan Batal
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
    
    def load_existing_data(self):
        if self.existing_data:
            date_parts = self.existing_data['date'].split('-')
            self.date_edit.setDate(QDate(int(date_parts[0]), int(date_parts[1]), int(date_parts[2])))
            
            idx = self.type_combo.findText(self.existing_data['type'])
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
            
            idx = self.category_combo.findText(self.existing_data['category'])
            if idx >= 0:
                self.category_combo.setCurrentIndex(idx)
            else:
                self.category_combo.setEditText(self.existing_data['category'])
            
            self.amount_spin.setValue(self.existing_data['amount'])
            self.desc_text.setPlainText(self.existing_data['description'])
    
    def get_transaction_data(self):
        return {
            'date': self.date_edit.date().toString("yyyy-MM-dd"),
            'type': self.type_combo.currentText(),
            'category': self.category_combo.currentText(),
            'amount': self.amount_spin.value(),
            'description': self.desc_text.toPlainText()
        }
    
    def save(self):
        data = self.get_transaction_data()
        valid, errors = TransactionValidator.validate_transaction(data)
        
        if valid:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "\n".join(errors))