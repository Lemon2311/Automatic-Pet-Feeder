from hx711 import HX711
import time

hx711 = HX711(9, 8)

def Setup:
    hx711.tare()
    value = hx711.read()
    value = hx711.get_value()


while True:
    value = hx711.read()
    value = hx711.get_value()    
    print(value)
    time.sleep(1)