import sys
import requests
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QFileDialog, QFormLayout, QComboBox, QTextEdit, QHeaderView)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

# API URL
API_BASE_URL = 'http://localhost:5000/api'


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        # Title
        title = QLabel("Law Firm CMS - Login")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        # Form layout
        form_layout = QFormLayout()

        # Email field
        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)

        self.layout.addLayout(form_layout)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Warning", "Please enter email and password")
            return

        try:
            response = requests.post(f"{API_BASE_URL}/auth/login", json={
                'email': email,
                'password': password
            })

            if response.status_code == 200:
                data = response.json()
                self.parent.token = data['token']
                self.parent.current_user = data['user']

                # Show main window
                self.parent.setup_main_ui()
                self.parent.show_main_window()
            else:
                QMessageBox.critical(self, "Error", "Invalid email or password")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")


class LawFirmCMS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.token = None
        self.current_user = None

        # Set window properties
        self.setWindowTitle('Law Firm Case Management System')
        self.setGeometry(100, 100, 1200, 800)

        # Start with login
        self.show_login()

    def show_login(self):
        self.login_widget = LoginWindow(self)
        self.setCentralWidget(self.login_widget)

    def show_main_window(self):
        self.setCentralWidget(self.main_widget)

    def setup_main_ui(self):
        # Create main widget with tab layout
        self.main_widget = QWidget()
        layout = QVBoxLayout()

        # Create tab widget
        self.tabs = QTabWidget()

        # Add tabs
        self.tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        self.tabs.addTab(self.create_cases_tab(), "Cases")
        self.tabs.addTab(self.create_clients_tab(), "Clients")
        self.tabs.addTab(self.create_documents_tab(), "Documents")
        self.tabs.addTab(self.create_calendar_tab(), "Calendar")

        layout.addWidget(self.tabs)
        self.main_widget.setLayout(layout)

    def create_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Welcome message
        welcome = QLabel(f"Welcome, {self.current_user['name']}")
        welcome.setFont(QFont('Arial', 16))
        layout.addWidget(welcome)

        # Stats summary
        stats_label = QLabel("Quick Stats")
        stats_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(stats_label)

        self.get_dashboard_stats(layout)

        tab.setLayout(layout)
        return tab

    def get_dashboard_stats(self, layout):
        try:
            headers = {'Authorization': f"Bearer {self.token}"}

            # Get active cases
            response = requests.get(f"{API_BASE_URL}/cases?status=open", headers=headers)
            if response.status_code == 200:
                active_cases = len(response.json().get('cases', []))
                layout.addWidget(QLabel(f"Active Cases: {active_cases}"))

            # Get total clients
            response = requests.get(f"{API_BASE_URL}/clients", headers=headers)
            if response.status_code == 200:
                total_clients = len(response.json().get('clients', []))
                layout.addWidget(QLabel(f"Total Clients: {total_clients}"))

        except Exception as e:
            layout.addWidget(QLabel(f"Error loading stats: {str(e)}"))

    def create_cases_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Case Management")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)

        # Add case button
        add_button = QPushButton("Add New Case")
        add_button.clicked.connect(self.show_add_case_dialog)
        layout.addWidget(add_button)

        # Cases table
        self.cases_table = QTableWidget()
        self.cases_table.setColumnCount(5)
        self.cases_table.setHorizontalHeaderLabels(["Case Number", "Title", "Client", "Status", "Open Date"])
        self.cases_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.cases_table)

        # Load cases
        self.load_cases()

        tab.setLayout(layout)
        return tab

    def load_cases(self):
        try:
            headers = {'Authorization': f"Bearer {self.token}"}
            response = requests.get(f"{API_BASE_URL}/cases", headers=headers)

            if response.status_code == 200:
                cases = response.json().get('cases', [])
                self.cases_table.setRowCount(len(cases))

                for i, case in enumerate(cases):
                    self.cases_table.setItem(i, 0, QTableWidgetItem(case['case_number']))
                    self.cases_table.setItem(i, 1, QTableWidgetItem(case['title']))

                    # Get client name
                    client_response = requests.get(f"{API_BASE_URL}/clients/{case['client_id']}", headers=headers)
                    if client_response.status_code == 200:
                        client = client_response.json()
                        self.cases_table.setItem(i, 2, QTableWidgetItem(client['name']))
                    else:
                        self.cases_table.setItem(i, 2, QTableWidgetItem("Unknown"))

                    self.cases_table.setItem(i, 3, QTableWidgetItem(case['status']))
                    self.cases_table.setItem(i, 4, QTableWidgetItem(case['open_date']))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load cases: {str(e)}")

    def show_add_case_dialog(self):
        # This would be implemented to show a dialog for adding a new case
        pass

    def create_clients_tab(self):
        # Similar to cases tab but for clients
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Clients Management"))
        tab.setLayout(layout)
        return tab

    def create_documents_tab(self):
        # Documents management tab
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Documents Management"))
        tab.setLayout(layout)
        return tab

    def create_calendar_tab(self):
        # Calendar tab
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Calendar & Appointments"))
        tab.setLayout(layout)
        return tab


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LawFirmCMS()
    window.show()
    sys.exit(app.exec_())