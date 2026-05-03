from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

class AccountDialog(QDialog):
    def __init__(self, parent=None, current_name=""):
        super().__init__(parent)
        self.current_name = current_name
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("👤 Account Settings")
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        form = QFormLayout()
        form.setSpacing(15)
        
        self.name_input = QLineEdit()
        self.name_input.setText(self.current_name)
        self.name_input.setPlaceholderText("Enter your full name")
        form.addRow("Full Name:", self.name_input)
        
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def save(self):
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Warning", "Name cannot be empty")
            return
        
        self.accept()
    
    def get_user_data(self):
        return {
            'name': self.name_input.text().strip()
        }