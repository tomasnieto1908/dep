from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

color_temperatura = [255, 0, 0]    # Rojo
color_presion = [0, 255, 0] # Verde
color_humedad = [0, 0, 255] # Azul

def show_value_on_leds(value, color):
    sense.show_message(str(value), scroll_speed=0.1, text_colour=color)

def read_sensors():
    temp = sense.get_temperature()
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()
   
    return temp, pressure, humidity

def main():
    selected_sensor = 0
    sensors = ["Temperature", "Pressure", "Humidity"]

    while True:
        temp, pressure, humidity = read_sensors()
       
        if selected_sensor == 0:
            value = round(temp, 1)
            print("Temperatura: {} °C".format(value))
            show_value_on_leds(value, color_temperatura)
        elif selected_sensor == 1:
            value = round(pressure, 1)
            print("Presion: {} hPa".format(value))
            show_value_on_leds(value, color_presion)
        else:
            value = round(humidity, 1)
            print("Humedad: {} %".format(value))
            show_value_on_leds(value, color_humedad)
       
        # Cambio de sensor con teclas de flecha
        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "left":
                    selected_sensor = (selected_sensor - 1) % 3
                elif event.direction == "right":
                    selected_sensor = (selected_sensor + 1) % 3
       
        time.sleep(1)

if __name__ == "__main__":
    main()