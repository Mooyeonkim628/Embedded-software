import esp32
import socket
import sys
from machine import Pin, Timer
import network
from time import sleep

red_led = Pin(14, Pin.OUT)
green_led = Pin(15, Pin.OUT)
button = Pin(32, Pin.IN, Pin.PULL_DOWN)
temp = esp32.raw_temperature() 
hall = esp32.hall_sensor()
if red_led.value() == 1:
    red_led_state = 'ON'
else:
    red_led_state ='OFF'   
if green_led.value() == 1:
    green_led_state = 'ON'
else:
    green_led_state ='OFF'  
if button.value() == 1:
    button_state = 'ON'
else:
    button_state ='OFF'
    
def do_connect():
    ssid = 'ssid'
    pw = 'pw'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting')
        wlan.connect(ssid, pw)
        while not wlan.isconnected():
            pass
    print('Connected to ', ssid)    
    print('IP Address:', wlan.ifconfig()[0])

def web_page():
    temp = esp32.raw_temperature()  
    hall = esp32.hall_sensor()
    if red_led.value() == 1:
        red_led_state = 'ON'
    else:
        red_led_state ='OFF'    
    if green_led.value() == 1:
        green_led_state = 'ON'
    else:
        green_led_state ='OFF'
        
    if button.value() == 1:
        button_state = 'ON'
    else:
        button_state ='OFF'    
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    <p>
    SWITCH Current State: <strong>""" + button_state + """</strong>
    </p>
    <p>
    <a href="/?button=on"></a>
    </p>
    <p>
    <a href="/?button=off"></a>
    </p>
    </body>
    </html>"""
    return html_webpage

do_connect()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(1)

while True:
    conn, addr = s.accept()    
    request = conn.recv(1024)
    request = str(request)
    red_led_on = request.find('/?red_led=on')
    red_led_off = request.find('/?red_led=off')
    green_led_on = request.find('/?green_led=on')
    green_led_off = request.find('/?green_led=off')
    button_on = request.find('/?button=on')
    button_off = request.find('/?button=off')
    
    if red_led_on == 6:
        red_led.value(1)       
    if red_led_off == 6:
        red_led.value(0)        
    if green_led_on == 6:
        green_led.value(1)        
    if green_led_off == 6:
        green_led.value(0)
    if button_on == 6:
        button.value(1)        
    if button_off == 6:
        button.value(0)        
        
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()