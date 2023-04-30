import time
import requests

from sense_hat import SenseHat

# Initialize the Sense HAT.
sense = SenseHat()

# Get the current time.
now = time.time()

# Get the sensor data.
temperature = sense.temperature
humidity = sense.humidity
pressure = sense.pressure

# Create a JSON object with the sensor data.
sensor_data = {
  "temperature": temperature,
  "humidity": humidity,
  "pressure": pressure,
  "timestamp": now
}

# Send the sensor data to the web server.
requests.post("http://localhost:5000/sensor_data", json=sensor_data)

# Wait 1 second before reading the sensor data again.
time.sleep(1)

# Repeat the process indefinitely.
while True:
  get_sensor_data()
