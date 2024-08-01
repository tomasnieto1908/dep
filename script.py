import serial
import sqlite3
from datetime import datetime

# Configuración del puerto serie
puerto_serial = '/dev/ttyUSB0'  # Cambia esto según tu sistema
baud_rate = 9600

# Conectar al puerto serie
ser = serial.Serial(puerto_serial, baud_rate, timeout=1)

# Conectar a la base de datos SQLite
conn = sqlite3.connect('sensores.db')
c = conn.cursor()

while True:
    try:
        # Leer datos del puerto serie
        if ser.in_waiting > 0:
            valor_sensor = ser.readline().decode().strip()
            
            if valor_sensor.isdigit():
                # Insertar datos en la base de datos
                c.execute('''
                    INSERT INTO mediciones (valor_sensor)
                    VALUES (?)
                ''', (int(valor_sensor),))
                
                # Confirmar los cambios
                conn.commit()
                print(f"Datos almacenados: {valor_sensor}")
    
    except KeyboardInterrupt:
        print("Interrupción del teclado. Cerrando...")
        break

# Cerrar conexiones
ser.close()
conn.close()

