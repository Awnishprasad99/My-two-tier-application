"""
Flask application for the two-tier architecture.
This serves as the application tier that connects to a MySQL database.
"""

import os
import time
import logging
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_db_connection(retries=5, delay=5):
    """Create a database connection with retry logic."""
    for attempt in range(retries):
        try:
            connection = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'db'),
                database=os.environ.get('MYSQL_DATABASE', 'myapp'),
                user=os.environ.get('MYSQL_USER', 'root'),
                password=os.environ.get('MYSQL_PASSWORD', 'rootpassword')
            )
            return connection
        except Error as e:
            logger.warning(f"Database connection attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    logger.error("Failed to connect to database after all retries")
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
            logger.info("Database initialized successfully")
        except Error as e:
            logger.error(f"Error initializing database: {e}")


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
            logger.error(f"Error fetching messages: {e}")
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
                logger.error(f"Error adding message: {e}")
    return redirect(url_for('index'))


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy'}


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
