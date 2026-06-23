from flask import Flask, render_template, jsonify, send_from_directory
import mysql.connector
from mysql.connector import Error as MySQLError
import os

app = Flask(__name__)

# MySQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'your_database',
    'port': 3306
}

# MySQL 연결 관리
mysql_connection = None

def get_mysql_connection():
    global mysql_connection
    if mysql_connection is None:
        try:
            mysql_connection = mysql.connector.connect(**DB_CONFIG)
        except MySQLError as e:
            print(f"MySQL 연결 실패: {e}")
    return mysql_connection

@app.route('/')
def index():
    return send_from_directory('dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('dist', path)

@app.route('/api/data')
def get_data():
    conn = get_mysql_connection()
    if conn.is_connected():
        conn.close()
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM your_table")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except MySQLError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)