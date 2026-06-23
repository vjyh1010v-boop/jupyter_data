import os
import mysql.connector
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'your_database',
    'port': 3306
}

# In-memory storage for demo purposes (replace with actual DB operations)
data_store = []

# Create tables in MySQL
def create_tables():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully")

# Initialize database
create_tables()

# CRUD Operations
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return jsonify({'id': item_id, 'message': 'Item created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if item is None:
            return jsonify({'error': 'Item not found'}), 404
        
        return jsonify(item)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET name = %s, description = %s WHERE id = %s", 
                     (name, description, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Item updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve React build files
@app.route('/<path:path>')
def serve_static(path):
    if path == '':
        return send_from_directory('dist', 'index.html')
    return send_from_directory('dist', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)