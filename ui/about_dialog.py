from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumWidth(350)
        self.setMinimumHeight(280)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        title = QLabel("Spendee: Spend Less, Save More")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #1e40af;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel("Manage your income and expenses easily")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #64748b;")
        layout.addWidget(desc)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e2e8f0;")
        layout.addWidget(line)
        
        name = QLabel("Nama: Baiq Mutia Dewi Edelweis")
        name.setStyleSheet("color: #334155;")
        nim = QLabel("NIM: F1D02310107")
        nim.setStyleSheet("color: #334155;")
        
        layout.addWidget(name)
        layout.addWidget(nim)
        
        version = QLabel("Version 1.0")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #94a3b8; font-size: 11px; margin-top: 12px;")
        layout.addWidget(version)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)