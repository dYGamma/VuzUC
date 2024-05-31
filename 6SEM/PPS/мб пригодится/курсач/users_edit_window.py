import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QFormLayout, QComboBox, QGroupBox
import sqlite3
# from app import InfoPage


class UserManagementWindow(QWidget):
    def __init__(self, previous_window, username):
        super().__init__()

        self.setWindowTitle("User Management")
        self.setFullScreen()
        
        self.previous_window = previous_window
        self.username = username
        self.init_db()
        self.init_ui()

    def setFullScreen(self):
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry()
        self.setGeometry(screen_geometry)

    def init_db(self):
        # Connect to SQLite database (create a new one if it doesn't exist)
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()

        # Create a table to store user information if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                permissions TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def init_ui(self):
        # Widgets
        user_table_label = QLabel("User Database:")
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Full Name", "Username", "Password", "Permissions"])

        back_button = QPushButton("Back")
        logout_button = QPushButton("Logout")
        # clear_db_button = QPushButton("Clear Database")

        add_user_label = QLabel("Add New User:")
        self.full_name_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.permissions_combo = QComboBox()
        self.permissions_combo.addItems(["Full", "Limited"])

        add_button = QPushButton("Add User")
        # load_button = QPushButton("Load Database")
        # save_button = QPushButton("Save Database")

        search_label = QLabel("Search User by ID:")
        self.search_id_input = QLineEdit()
        search_button = QPushButton("Search")
        delete_button = QPushButton("Delete User")

        edit_label = QLabel("Edit User:")
        self.edit_id_input = QLineEdit()
        self.edit_full_name_input = QLineEdit()
        self.edit_username_input = QLineEdit()
        self.edit_password_input = QLineEdit()
        self.edit_permissions_combo = QComboBox()
        self.edit_permissions_combo.addItems(["Full", "Limited"])
        save_edit_button = QPushButton("Save Changes")


        # Left Half: User Table Section
        user_table_layout = QVBoxLayout()
        user_table_layout.addWidget(user_table_label)
        user_table_layout.addWidget(self.user_table)
        user_table_layout.addWidget(back_button)
        user_table_layout.addWidget(logout_button)
        # user_table_layout.addWidget(clear_db_button)

        # Right Half: Divided Vertically
        right_half_layout = QVBoxLayout()

        # GroupBox 1: User Info
        user_info_groupbox = QGroupBox("User Info")
        user_info_layout = QVBoxLayout()
        user_info_layout.addWidget(user_table_label)
        user_info_layout.addWidget(self.user_table)
        user_info_layout.addWidget(back_button)
        user_info_layout.addWidget(logout_button)
        # user_info_layout.addWidget(clear_db_button)
        user_info_groupbox.setLayout(user_info_layout)

        # GroupBox 2: Adding Users
        add_users_groupbox = QGroupBox("Adding Users")
        add_users_layout = QFormLayout()
        add_users_layout.addRow(add_user_label)
        add_users_layout.addRow("Full Name:", self.full_name_input)
        add_users_layout.addRow("Username:", self.username_input)
        add_users_layout.addRow("Password:", self.password_input)
        add_users_layout.addRow("Permissions:", self.permissions_combo)
        add_users_layout.addRow(add_button)
        # add_users_layout.addRow(load_button)
        # add_users_layout.addRow(save_button)
        add_users_groupbox.setLayout(add_users_layout)

        # GroupBox 3: Editing Users
        edit_users_groupbox = QGroupBox("Editing Users")
        edit_users_layout = QFormLayout()
        edit_users_layout.addRow(edit_label)
        edit_users_layout.addRow("User ID:", self.edit_id_input)
        edit_users_layout.addRow("Full Name:", self.edit_full_name_input)
        edit_users_layout.addRow("Username:", self.edit_username_input)
        edit_users_layout.addRow("Password:", self.edit_password_input)
        edit_users_layout.addRow("Permissions:", self.edit_permissions_combo)
        edit_users_layout.addRow(save_edit_button)
        edit_users_groupbox.setLayout(edit_users_layout)

        # GroupBox 4: Load/Save Database
        # load_save_groupbox = QGroupBox("Load/Save Database")
        # load_save_layout = QVBoxLayout()
        # load_save_layout.addWidget(load_button)
        # load_save_layout.addWidget(save_button)
        # load_save_groupbox.setLayout(load_save_layout)

        # GroupBox 5: Search/Delete Users
        search_delete_groupbox = QGroupBox("Search/Delete Users")
        search_delete_layout = QVBoxLayout()
        search_delete_layout.addWidget(search_label)
        search_delete_layout.addWidget(self.search_id_input)
        search_delete_layout.addWidget(search_button)
        search_delete_layout.addWidget(delete_button)
        search_delete_groupbox.setLayout(search_delete_layout)

        # Add GroupBoxes to Right Half Layout
        right_half_layout.addWidget(user_info_groupbox)
        right_half_layout.addWidget(add_users_groupbox)
        right_half_layout.addWidget(edit_users_groupbox)
        # right_half_layout.addWidget(load_save_groupbox)
        right_half_layout.addWidget(search_delete_groupbox)


        # Top Layout: Back, Logout, and Username
        top_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        logout_button = QPushButton("Logout")
        username_label = QLabel(f"Username: {self.username}")

        top_layout.addWidget(back_button)
        top_layout.addWidget(logout_button)
        top_layout.addWidget(username_label)

        # Signals and slots
        back_button.clicked.connect(self.back_function)
        add_button.clicked.connect(self.add_user)
        # load_button.clicked.connect(self.load_user_data)
        # save_button.clicked.connect(self.save_user_data)
        search_button.clicked.connect(self.search_user)
        delete_button.clicked.connect(self.delete_user)
        save_edit_button.clicked.connect(self.save_edit_user)

        # Layout
        main_layout = QHBoxLayout()
        # main_layout.addLayout(top_layout)
        main_layout.addLayout(user_table_layout)
        main_layout.addLayout(right_half_layout)

        full_window_layout = QVBoxLayout()
        full_window_layout.addLayout(top_layout)
        full_window_layout.addLayout(main_layout)


        self.setLayout(full_window_layout)
        
        # Reload user data
        self.load_user_data()

    def back_function(self):

        self.previous_window.show()
        self.hide()

    def load_user_data(self):
        # Load user data from the database and update the table
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()

        self.user_table.setRowCount(0)
        for user in users:
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            for column, data in enumerate(user):
                self.user_table.setItem(row_position, column, QTableWidgetItem(str(data)))


    def add_user(self):
        # Get input values
        full_name = self.full_name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        permissions = self.permissions_combo.currentText()

        # Insert the new user into the database
        query = "INSERT INTO users (full_name, username, password, permissions) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (full_name, username, password, permissions))
        self.conn.commit()

        # Clear input fields
        self.full_name_input.clear()
        self.username_input.clear()
        self.password_input.clear()

        # Reload user data
        self.load_user_data()

    def save_user_data(self):
        # Save user data to a file (or take any other necessary action)
        pass

    def search_user(self):

        self.edit_full_name_input.clear()
        self.edit_username_input.clear()
        self.edit_password_input.clear()
        self.edit_permissions_combo.clear()
        # Search for a user by ID and populate the edit fields
        user_id = self.search_id_input.text()
        query = "SELECT * FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        user = self.cursor.fetchone()
        if user:
            # Populate edit fields
            self.edit_full_name_input.setText(user[1])
            self.edit_username_input.setText(user[2])
            self.edit_password_input.setText(user[3])
            self.edit_permissions_combo.setCurrentText(user[4])

            # Reload user data
            # self.load_user_data()

    def delete_user(self):
        # Delete a user by ID
        user_id = self.search_id_input.text()
        query = "DELETE FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

        # Reload user data
        self.load_user_data()

    def save_edit_user(self):
        # Save edited user data to the database
        user_id = self.edit_id_input.text()
        full_name = self.edit_full_name_input.text()
        username = self.edit_username_input.text()
        password = self.edit_password_input.text()
        permissions = self.edit_permissions_combo.currentText()

        print(full_name, username, password, permissions, user_id)


        query = """
        UPDATE users 
        SET 
            full_name = CASE WHEN ? != '' THEN ? ELSE full_name END,
            username = CASE WHEN ? != '' THEN ? ELSE username END,
            password = CASE WHEN ? != '' THEN ? ELSE password END,
            permissions = CASE WHEN ? != '' THEN ? ELSE permissions END
        WHERE id=?
        """
        
        self.cursor.execute(query, (full_name, full_name,
                                    username, username,
                                    password, password,
                                    permissions, permissions,
                                    user_id))        
        self.conn.commit()

        # Clear edit fields
        self.edit_id_input.clear()
        self.edit_full_name_input.clear()
        self.edit_username_input.clear()
        self.edit_password_input.clear()

        # Reload user data
        self.load_user_data()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = "YourUsername"  # Replace with the actual username
    user_management_window = UserManagementWindow(username)
    user_management_window.show()
    sys.exit(app.exec_())