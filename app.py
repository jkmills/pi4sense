from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime
from sense_hat import SenseHat
from threading import Thread, Lock
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading', transports=['polling'])

sense = SenseHat()

# Define colors for the orientation indicators
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Define the orientation indicators
roll_indicator = [[GREEN if i == 4 else YELLOW for i in range(8)] for j in range(2)]
pitch_indicator = [[GREEN if i == 4 else YELLOW for i in range(8)] for j in range(2)]
yaw_indicator = [[GREEN if i == 4 else YELLOW for i in range(8)] for j in range(2)]

# Define a lock to prevent multiple threads from accessing the LED matrix simultaneously
led_lock = Lock()

def draw_orientation():
    while True:
        # Clear the LED matrix
        led_lock.acquire()
        sense.clear()
        led_lock.release()

        # Get the orientation data
        orientation = sense.get_orientation()

        # Calculate the roll, pitch, and yaw indicators
        roll = round(orientation['roll'])
        pitch = round(orientation['pitch'])
        yaw = round(orientation['yaw'])

        roll_index = int(roll / 45) + 4
        pitch_index = int(pitch / 45) + 4
        yaw_index = int(yaw / 45) + 4

        for i in range(2):
            roll_indicator[i][roll_index] = RED
            pitch_indicator[i][pitch_index] = RED
            yaw_indicator[i][yaw_index] = RED

        # Draw the orientation indicators on the LED matrix
        led_lock.acquire()
        sense.set_pixels(sum(roll_indicator + pitch_indicator + yaw_indicator, []))
        led_lock.release()

        sleep(0.1)

orientation_thread = Thread(target=draw_orientation)
orientation_thread.daemon = True
orientation_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

def read_sensor_data():
    while True:
        data = {
            'temperature': round(sense.get_temperature(), 1),
            'humidity': round(sense.get_humidity(), 1),
            'pressure': round(sense.get_pressure(), 1),
            'roll': round(sense.get_orientation()['roll'], 1),
            'pitch': round(sense.get_orientation()['pitch'], 1),
            'yaw': round(sense.get_orientation()['yaw'], 1),
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Send the sensor data and the orientation data to the client
        socketio.emit('sensor-data', data)
        socketio.emit('orientation-data', {
            'roll': data['roll'],
            'pitch': data['pitch'],
            'yaw': data['yaw']
        })

        sleep(1)

if __name__ == '__main__':
    sensor_thread = Thread(target=read_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
