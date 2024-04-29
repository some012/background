from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Функция для создания таблицы пользователей, если она еще не существует
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 login TEXT NOT NULL,
                 password TEXT NOT NULL,
                 name TEXT NOT NULL,
                 age INTEGER NOT NULL,
                 height INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

create_users_table()

# Метод для создания нового пользователя
@app.route('/sign_up/', methods=['POST'])
def sign_up():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    name = data.get('name')
    age = data.get('age')
    height = data.get('height')

    if not login or not password or not name or not age or not height:
        return jsonify({'error': 'All fields are required'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (login, password, name, age, height) VALUES (?, ?, ?, ?, ?)",
              (login, password, name, age, height))
    conn.commit()
    new_user_id = c.lastrowid
    conn.close()

    return jsonify({'id': new_user_id}), 201

# Метод для входа пользователя в аккаунт
@app.route('/sign_in/', methods=['POST'])
def sign_in():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    if not login or not password:
        return jsonify({'error': 'Login and password are required'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
    user = c.fetchone()
    conn.close()

    if user:
        user_data = {
            'login': user[1],
            'age': user[4],
            'height': user[5]
        }
        return render_template('log.html', user=user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
