from machine import Pin
import machine
from time import sleep
import dht
import urequests
import ujson
import onewire
import ds18x20

# For Network Connection
import network
import esp
esp.osdebug(None)
import gc

# Configure network
ssid = "Nani"
password = "00000000"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
    pass
print("Connection Established")
print(station.ifconfig())

url = "http://192.168.126.194:8000/dhtreading"

# DHT Sensor
dhtsensor = dht.DHT11(Pin(2))

# Temperature Sensor
tempsensor = ds18x20.DS18X20(onewire.OneWire(Pin(23)))
roms = tempsensor.scan()

# GPS Module
TX_PIN = 17
RX_PIN = 16
uart = machine.UART(2, tx=TX_PIN, rx=RX_PIN, baudrate=9600)

# LED Controls
led1 = Pin(15, Pin.OUT)
led2 = Pin(5, Pin.OUT)
led3 = Pin(18, Pin.OUT)
led4 = Pin(19, Pin.OUT)

def temperaturesensing():
    try:
        tempsensor.convert_temp()
    except Exception as e:
        return e
    for rom in roms:
        temp = tempsensor.read_temp(rom)
        return temp

def dhtreading():
    try:
        sleep(1)
        dhtsensor.measure()
        temp = dhtsensor.temperature()
        humidity = dhtsensor.humidity()
        data = {"Temperature": temp, "humidity": humidity, "IPAddress": station.ifconfig()[0]}
        print(data)
        return data
    except OSError as e:
        data = {"Temperature": 0, "humidity": 0, "IPAddress": 0}
        print(data)
        return data

def gpsmodule():
    if uart.any():
        gps_data = uart.readline()
        try:
            data_list = gps_data.decode('utf-8').strip().split(',')
        except Exception as e:
            return {"Unicode Error": e}
          
        if data_list[0] == '$GPRMC':
            return {"GPRMC": data_list}
        elif data_list[0] == '$GPGGA':
            return {"GPGGA": data_list}
        else:
            pass

def ledcontrol(sequence):
    if sequence[0]:
        led1.value(True)
    else:
        led1.value(False)
    if sequence[1]:
        led2.value(True)
    else:
        led2.value(False)
    if sequence[2]:
        led3.value(True)
    else:
        led3.value(False)
    if sequence[3]:
        led4.value(True)
    else:
        led4.value(False)

while True:
    data = dhtreading()
    print(temperaturesensing())
    data["Temperature"] = temperaturesensing()

    gps_data = gpsmodule()
    print(gps_data)

    try:
        print("Data Sending")
        try:
            data = {"EXAMPLE": 1232}
            json_data = ujson.dumps(data)
            print(json_data)
            print("Json Data", json_data)
            # Send POST request with JSON data
            response = urequests.post(url, headers={'Content-Type': 'application/json'}, data=json_data)
            if response.status_code == 200:
                print("Response Text:", response.text)
                lights = ujson.loads(response.text)
                time.sleep(1)
                ledcontrol(lights['LED'])
            else:
                print("HTTP request failed with status code:", response.status_code)
            response.close()
        except:
            print("Server Is Off")
    except Exception as e:
        print(e)
