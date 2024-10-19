from machine import Pin, Timer, PWM, RTC, ADC
from time import sleep

def rtc_output():
    a = rtc.datetime()
    print(week[a[3]] + ", " + str(a[1]) + '/' + str(a[2]) + '/' + str(a[0]) + ', ' + str(a[4]) + ':'
          + ("%02d" % (a[5])) + ':' + ("%02d" % (a[6])) + '.' + str(a[7]))

def pwm_output():
    if cnt % 2 == 1:
        pot = int(adc.read() / 128)
        pwm.freq(pot)
    if cnt % 2 == 0 and cnt != 0:
        pot = int(adc.read() / 4)
        pwm.duty(pot)
        
def handle_interrupt(pin):
    global cnt
    cnt = cnt + 1

cnt = 0

year = int(input("Year? "))
month = int(input("Month? "))
day = int(input("Day? "))
weekday = int(input("Weekday? "))
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
microsecond = int(input("Microsecond? "))

rtc = RTC()
rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))
timer_rtc = Timer(0)
week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
timer_rtc.init(period=30000, mode=Timer.PERIODIC, callback = lambda t: rtc_output())

pwm = PWM(Pin(14), freq=10, duty=256)
button = Pin(32, Pin.IN)
adc = ADC(Pin(34))

button.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)
timer_pot = Timer(1)
timer_pot.init(period=100, mode=Timer.PERIODIC, callback = lambda t: pwm_output())

while(1):
    sleep(0.05)