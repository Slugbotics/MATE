import busio
import digitalio
import time
import adafruit_ds3231
import adafruit_mprls
import board
import adafruit_sdcard
import storage
import adafruit_motor
import os
import wifi
import ipaddress
from adafruit_motor import stepper

wifi_ssid = "Slugbotics-MATE"
wifi_passwd = "slugbotics"
float_ip_addr = "192.168.1.10"
topside_ip_addr = "192.168.1.4"

rtc_i2c = busio.I2C(board.GP15, board.GP14)
sd_card_spi = busio.SPI(board.GP18, board.GP19, board.GP16)
sd_card_cs = digitalio.DigitalInOut(board.GP17)
#--- MPRLS needs to be pulled up/fixed for 3.3V ----
mprls_i2c = busio.I2C(board.GP13, board.GP12)
#mprls_i2c.pull = digitalio.Pull.UP
mpr = adafruit_mprls.MPRLS(mprls_i2c, psi_min=0, psi_max=25)
sdcard = adafruit_sdcard.SDCard(sd_card_spi, sd_card_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
rtc = adafruit_ds3231.DS3231(rtc_i2c)

#  set static IP address
ipv4 =  ipaddress.IPv4Address(float_ip_addr)
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("192.168.1.150")
wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
# connect to your SSID
# wifi.radio.connect(wifi_ssid, wifi_passwd)


rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))



DELAY = 0.01
STEPS = 200
coils= (
digitalio.DigitalInOut(board.GP1), # A1
digitalio.DigitalInOut(board.GP11), # A2
digitalio.DigitalInOut(board.GP9), # B1
digitalio.DigitalInOut(board.GP10), # B2
)


for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT
    
motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

# file_path = "test_output.txt"

def set_rtc(hrs, min, sec):    
    rtc.datetime = time.struct_time((2024,4,25,hrs,min,sec,3,9,-1))

# direction: up represented by true, down by false
def movement(direction):
    if(direction):
        for step in range(STEPS):
            motor.onestep(direction=stepper.FORWARD)
            time.sleep(DELAY)
            for step in range(STEPS):
                motor.onestep(direction=stepper.FORWARD)
                time.sleep(DELAY)
    else:
        for step in range(STEPS):
            motor.onestep(direction=stepper.BACKWARD)
            time.sleep(DELAY)
            for step in range(STEPS):
                motor.onestep(direction=stepper.BACKWARD)
                time.sleep(DELAY)

def write_file(drop, pressure, time):
    with open(f'/sd/test_output{drop}.txt',"a+") as out:
       out.write(f'{time.tm_hour}:{time.tm_min}:{time.tm_sec}_{pressure}\n')
    
while True: 
    print(mpr.pressure)
    time.sleep(1)
    t = rtc.datetime
    time.sleep(1)
    print(t)
    print(t.tm_hour, t.tm_min, t.tm_sec)
    print("pressure reading", mpr.pressure)
    movement(False)
    motor.release()
