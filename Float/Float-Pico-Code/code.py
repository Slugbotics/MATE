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
import socketpool


#---- Server/Wifi AP setup ----
wifi_ssid = "Slugbotics-MATE"
wifi_passwd = "slugbotics"
float_ip_addr = "192.168.4.1"
topside_ip_addr = "192.168.4.17"
Port = 5000
buffersize = 1024

#---- Modules set up ----

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

#---- create raspberry pi Wireless AP ----
if wifi.radio.connected or wifi.radio.ipv4_address:
    wifi.radio.stop_station()
if wifi.radio.ap_active or wifi.radio.ipv4_address_ap:
    wifi.radio.stop_ap()
#wifi.radio.enabled = True
wifi.radio.start_ap(ssid=wifi_ssid, password=wifi_passwd)
wifi.radio.start_dhcp_ap()
#wifi.radio.connect(wifi_ssid, wifi_passwd)
#time.sleep(5)
wifi.radio.start_station()

#time.sleep(5)
pool = socketpool.SocketPool(wifi.radio)
#wifi.radio.stop_dhcp()

# connect to your SSID
#wifi.radio.connect(wifi_ssid, wifi_passwd)

#---- Initialize Real time clock Module ----

rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))


#---- Initialize Motor ----

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

#---- Initialize socket TCP Client ----
#server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(topside_ip_addr, Port)[0][4][0])
#print("here", server_ipv4)
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

#print(wifi.radio.set_ipv4_address(ipv4=ipv4_address, netmask=netmask_address, gateway=gateway_address))

print("Access point created with SSID: {}, password: {}".format(wifi_ssid, wifi_passwd))
print("Self IP", wifi.radio.ipv4_address)
print("router", wifi.radio.ipv4_gateway_ap)
print("Subnet", wifi.radio.ipv4_subnet_ap)
while True: 
    time.sleep(5)
    print(mpr.pressure)
    time.sleep(1)
    t = rtc.datetime
    time.sleep(1)
    print(t)
    print(t.tm_hour, t.tm_min, t.tm_sec)
    print("pressure reading", mpr.pressure)
    movement(False)
    motor.release()




