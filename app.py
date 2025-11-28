"""
Flask application for the two-tier architecture.
This serves as the application tier that connects to a MySQL database.
"""

import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


def get_db_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST', 'db'),
            database=os.environ.get('MYSQL_DATABASE', 'myapp'),
            user=os.environ.get('MYSQL_USER', 'root'),
            password=os.environ.get('MYSQL_PASSWORD', 'rootpassword')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def init_db():
    """Initialize the database with required tables."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    content VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error initializing database: {e}")


@app.route('/')
def index():
    """Display all messages."""
    messages = []
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
            messages = cursor.fetchall()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error fetching messages: {e}")
    return render_template('index.html', messages=messages)


@app.route('/add', methods=['POST'])
def add_message():
    """Add a new message."""
    content = request.form.get('content')
    if content:
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO messages (content) VALUES (%s)', (content,))
                connection.commit()
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Error adding message: {e}")
    return redirect(url_for('index'))


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy'}


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
