import network
import socket
from machine import Pin
from hx711 import HX711
import time
from wifi_credentials import WIFI_SSID, WIFI_PASSWORD
from servo import Servo

hx711 = HX711(9, 8)

def init_HX711():
    hx711.tare()
    value = hx711.read() #check if needed, might delete these two lines
    value = hx711.get_value() #

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass

    print('Connection successful')
    print(station.ifconfig())

def web_page():
    if led.value():
        gpio_state="ON"
    else:
        gpio_state="OFF"

    html = """<!DOCTYPE html>
<html>
<head>
    <title>Pet Feeder</title>
    <style>
        body {
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 90vh;
        }
        .centered-div {
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center;
            padding: 20px;
        }
        button {
            padding: 10px 20px;
            margin-bottom: 10px;
        }
        .input-container {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        input[type="number"] {
            padding: 5px;
            margin-right: 10px;
        }
        .positive {
            color: green;
        }
        .negative {
            color: red;
        }
    </style>
</head>
<body>
    <div class="centered-div">
        <button>Button 1</button>
        <div class="input-container">
            <input id="numberInput" type="number" value="0" autocomplete="off">
            <p id="changeDisplay"></p>
        </div>
        <button id="saveButton">Button 2</button>
    </div>
    <script>
        var input = document.getElementById('numberInput');
        var display = document.getElementById('changeDisplay');
        var saveButton = document.getElementById('saveButton');
        var initialValue = input.value;

        if (sessionStorage.getItem('saveClicked') === 'true') {
            initialValue = localStorage.getItem('savedValue') || initialValue;
        }

        input.value = initialValue;

        input.addEventListener('change', function() {
            var newValue = this.value;
            var difference = newValue - initialValue;
            display.textContent = difference > 0 ? "+" + difference : difference;
            display.className = difference >= 0 ? "positive" : "negative";
        });

        saveButton.addEventListener('click', function() {
            localStorage.setItem('savedValue', input.value);
            sessionStorage.setItem('saveClicked', 'true');
        });
    </script>
</body>
</html>"""
    return html

def weight():
    value = hx711.read()
    value = hx711.get_value()    
    return value

servo = Servo(Pin(21))

deg = 0

def pour_food():
    servo.move(deg+=30) #adjust to pour exactly one portion
    # also code to make it spin slowly back needs to be added after the servo rotates completely

weight_low_threshold = 0

weight_high_threshold = 100000

tolerance = 100 # adjust tolerance for weight

def loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 8080))
    s.listen(5)

    full = True

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        
        if weight() <= weight_low_threshold:
            full = False 
            
        if not full:
            pour_food()
            
        if weight() >= weight_high_threshold:
            full = True            
        
#add routing in js on button press to work with the following functionalities
        food_amount_index = request.find('/?food_amount=')

        if food_amount_index != -1:
            food_amount_start = food_amount_index + len('/?food_amount=')
            weight_high_threshold = request[food_amount_start:]
        
        tare_index = request.find('/request')
       
        if tare_index != -1:
            hx711.tare()
            weight_low_threshold = weight() + tolerance
#
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    
def main():
    init_HX711()
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    loop()

if __name__ == "__main__":
    main()