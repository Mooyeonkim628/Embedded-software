from machine import RTC, Timer, deepsleep, TouchPad, Pin
import machine
import network
import ubinascii
import esp32
import ntptime
from time import sleep

def do_connect():
    import network 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to ',ssid)    
    print('IP Address:', wlan.ifconfig())

def printtime(datetime):
    print('Date: '+ "{:02d}".format(datetime[1])+'/'+"{:02d}".format(datetime[2])+'/'+"{:02d}".format(datetime[0]))
    print('Time: ' + "{:02d}".format(datetime[4])+':'+"{:02d}".format(datetime[5])+':'+"{:02d}".format(datetime[6])+' '+'HRS')

def TouchSensor(timer):
    if t0.read() < 300 and sleepflag is True:
        led_green.on()
    else:
        led_green.off()

def sleeper(timer):
    print("I am going to sleep for 1 minute.")
    led_red.value(0)
    sleepflag = False
    esp32.wake_on_ext0(button, level=esp32.WAKEUP_ANY_HIGH)
    deepsleep(60000)
 
do_connect() 
rtc = RTC()
year, month, day, weekday, hours, minutes, seconds, microseconds = rtc.datetime()
rtc.datetime((year, month, day, weekday, hours, minutes, seconds, microseconds))
ntptime.host = "pool.ntp.org"
    
t0 = TouchPad(Pin(33))
led_green = Pin(15, Pin.OUT)
led_red = Pin(14, Pin.OUT)
led_red.value(1)
button = Pin(32, Pin.IN)

sleepflag = True
esp32.wake_on_ext0(pin = button, level = esp32.WAKEUP_ANY_HIGH)

timer1 = Timer(1)
timer1.init(period=15000, mode=Timer.PERIODIC, callback=lambda t:printtime(rtc.datetime()))
timer2 = Timer(2)
timer2.init(period = 10, mode = Timer.PERIODIC, callback = TouchSensor)
timer3 = Timer(3)
timer3.init(period = 30000, mode = Timer.PERIODIC, callback = sleeper)

if machine.wake_reason() == 4:
    print("\n")
    print("Woke up due to timer")
    print("\n")
elif machine.wake_reason() == 2:
    print("\n")
    print("Woke up due to EXT0")
    print("\n")

