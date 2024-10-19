import esp32
import socket
from machine import Timer
import network
from time import sleep

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

def senddata():
    t = esp32.raw_temperature()
    h = esp32.hall_sensor()
    print("Temperature(°F): " + str(t))
    print("Hall Sensor: " + str(h))
    
    api = '2TC78875U7J995ZS'
    host = 'api.thingspeak.com'
    path = 'update?api_key=' + api + '&field1=' + str(t) + '&field2=' + str(h)
    try:
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /' + path + ' HTTP/1.0\r\n\r\n', 'utf8'))
        s.close()

do_connect()
tim = Timer(0)
tim.init(period=16000, mode=Timer.PERIODIC, callback = lambda t: senddata())