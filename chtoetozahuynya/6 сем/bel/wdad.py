import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_database():
    connection = sqlite3.connect("login_credentials.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    connection.commit()
    connection.close()

def register_user():
    username = username_entry.get()
    password = password_entry.get()

    connection = sqlite3.connect("login_credentials.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    connection.commit()
    connection.close()

    messagebox.showinfo("Успех", "Пользователь зарегистрирован")

def login_user():
    username = username_entry.get()
    password = password_entry.get()

    connection = sqlite3.connect("login_credentials.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        messagebox.showinfo("Успех", "Вход выполнен успешно")
        main_menu()
    else:
        messagebox.showerror("Ошибка", "Неверные логин или пароль")

def main_menu():
    login_window.withdraw()  # Скрыть окно входа
    main_window = tk.Tk()
    main_window.title("Главное меню")

    def logout():
        main_window.destroy()
        login_window.deiconify()

    button1 = tk.Button(main_window, text="Кнопка 1")
    button1.pack(pady=10)
    button2 = tk.Button(main_window, text="Кнопка 2")
    button2.pack(pady=10)
    button3 = tk.Button(main_window, text="Кнопка 3")
    button3.pack(pady=10)
    button4 = tk.Button(main_window, text="Выйти", command=logout)
    button4.pack(pady=10)

    main_window.mainloop()

# Создаем базу данных при первом запуске
create_database()

# Создаем окно входа
login_window = tk.Tk()
login_window.title("Вход")

# Создаем поля ввода для логина и пароля
username_label = tk.Label(login_window, text="Логин:")
username_label.pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Пароль:")
password_label.pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

# Создаем кнопки для регистрации и входа
register_button = tk.Button(login_window, text="Зарегистрироваться", command=register_user)
register_button.pack(pady=5)

login_button = tk.Button(login_window, text="Войти", command=login_user)
login_button.pack(pady=5)

login_window.mainloop()
