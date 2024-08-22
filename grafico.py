from flask import Flask, render_template_string
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Ruta al archivo de base de datos SQLite (en el mismo directorio que app.py)
    db_path = os.path.join(os.path.dirname(__file__), 'distancia.db')

    # Verificar si el archivo de base de datos existe
    if not os.path.isfile(db_path):
        return f"El archivo de base de datos no existe en la ruta: {db_path}"
    
    # Conectar a la base de datos SQLite
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        return f"Error al conectar con la base de datos: {e}"

    # Consultar los datos de la tabla 'distancia'
    query = "SELECT distancia, timestamp FROM distancia ORDER BY timestamp"
    try:
        data = pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        return f"Error al ejecutar la consulta: {e}"
    finally:
        conn.close()

    # Verificar si se obtuvieron datos
    if not data.empty:
        # Convertir la columna 'timestamp' a un objeto datetime
        data['timestamp'] = pd.to_datetime(data['timestamp'])

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data['timestamp'], data['distancia'], marker='o', linestyle='-', color='b')
        ax.set_title('Serie Temporal de Mediciones de Distancia')
        ax.set_xlabel('Fecha y Hora')
        ax.set_ylabel('Distancia (cm)')
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Convertir el gráfico a una imagen en base64
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        # Renderizar el HTML con el gráfico
        html = '''
        <!doctype html>
        <html>
        <head><title>Gráfico de Distancia</title></head>
        <body>
            <h1>Serie Temporal de Mediciones de Distancia</h1>
            <img src="data:image/png;base64,{{ img_base64 }}" alt="Gráfico de Distancia">
        </body>
        </html>
        '''

        return render_template_string(html, img_base64=img_base64)
    else:
        return "No se encontraron datos para graficar."

if __name__ == '__main__':
    app.run(debug=True)
