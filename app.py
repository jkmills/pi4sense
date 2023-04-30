from flask import Flask, render_template
from flask_socketio import SocketIO
from sense_hat import SenseHat
from threading import Thread
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
sense = SenseHat()

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
        socketio.emit('sensor-data', data)
        sleep(1)

sensor_thread = Thread(target=read_sensor_data)
sensor_thread.daemon = True
sensor_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('toggle-led')
def toggle_led():
    sense.clear() if sense.get_pixels()[0][0] == (0, 0, 0) else sense.clear((255, 255, 255))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
