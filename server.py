from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('distancia.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla para almacenar los datos del sensor
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS distancia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distancia REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Ruta para recibir los datos del sensor
@app.route('/sensor', methods=['POST'])
def sensor_data():
    data = request.get_json()
    distancia = data.get('distancia')
    
    if distancia is None:
        return jsonify({'error': 'No se proporcionaron datos de distancia'}), 400
    
    conn = get_db_connection()
    conn.execute('INSERT INTO distancia (distancia) VALUES (?)', (distancia,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Datos almacenados correctamente'})

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=8000)
