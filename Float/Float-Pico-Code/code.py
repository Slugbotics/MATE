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
import time
import supervisor


#---- Server/Wifi AP setup ----
wifi_ssid = "Slugbotics-MATE"
wifi_passwd = "slugbotics"
float_ip_addr = "192.168.4.1"
topside_ip_addr = "192.168.4.16"
Port = 5000
buffersize = 20
packet_timeout = 30
number_of_turns = 2
holding_time_sec = 20
drop = 0
sink_time = 20
drop_total_time = 100
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
s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
s.settimeout(packet_timeout)
try: 
    s.bind((float_ip_addr, Port))
    s.listen(2)
except OSError as e:
    print("Error", e.errno )
    print("Error", e)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(topside_ip_addr, Port)[0][4][0])



def tcp_send_file(drop):
    #---- Create float as server ----
    print("Listening")
    filetosend = open(f'/sd/test_output{drop}.txt', "rb+")
    #buf = bytearray(buffersize)
    try: 
        conn, addr = s.accept()
        conn.settimeout(packet_timeout)
        print("Accepted from", addr)
        data = filetosend.read(buffersize)
        conn.send(data)
        while data:
            print("Sending...")
            conn.send(data)
            data = filetosend.read(buffersize)
        filetosend.close()
        conn.send(b"DONE")
        print("Done Sending.")
        # print(client_socket.recv(1024))
        conn.close()  # close the connection
    except OSError as e:
        print("Error: ", e.errno)
        print("Error", e)
    except IndexError as e:
        print("Error", e.errno )
        print("Error", e)
    

def tcp_recv_text():
    try:
        conn, addr = s.accept()
        conn.settimeout(packet_timeout)
        buf = bytearray(buffersize)
        print("Accepted from", addr)
        data = conn.recv_into(buf, buffersize)
        converted = buf.decode('utf-8')
        converted = converted.replace('\x00', '')
        if "ip" in converted.lower():
            print("here")
            topside_ip_addr = converted.split(" ")[1]
            conn.send(b"RECEIVED")
            print("DONE Sending")
            conn.close()
            return topside_ip_addr
        elif "rtc" in converted.lower():
            hours = converted.split(" ")[1]
            minutes = converted.split(" ")[2]
            seconds = converted.split(" ")[3]
            set_rtc(int(hours), int(minutes), int(seconds))
            conn.send(b"RECEIVED")
            print("DONE Sending")
            conn.close()
            return "RTC"
        elif "down" in converted.lower():
            #movement(False, number_of_turns, holding_time_sec)
            conn.send(b"RECEIVED")
            print("DONE Sending")
            conn.close()
            return "DOWN"
        elif "up" in converted.lower():
            print("UP")
            #movement(True, number_of_turns, holding_time_sec)
        else:
            print(converted)
        conn.send(b"RECEIVED")
        print("DONE Sending")
        conn.close()
    except OSError as e:
        print("Error", e.errno )
        print("Error", e)
    except IndexError as e:
        print("Error", e.errno )
        print("Error", e)
    return None

def set_rtc(hrs, min, sec):    
    rtc.datetime = time.struct_time((2024,4,25,hrs,min,sec,3,9,-1))

# direction: up represented by true, down by false
def movement(direction, amount_turns, time_run, drop, pressure, timertc):
    # time run in seconds
    if(direction):
        start_time = time.time()
        total_time = 0
        while time_run >= total_time: 
            while amount_turns > 0:
                for step in range(STEPS):
                    motor.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                    write_file(drop, pressure, timertc)
                    time.sleep(DELAY)
                amount_turns -= 1
            end_time = time.time()
            total_time = end_time - start_time
    else:
        start_time = time.time()
        total_time = 0
        while time_run >= total_time: 
            while amount_turns > 0:
                for step in range(STEPS):
                    motor.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                    write_file(drop, pressure, timertc)
                    time.sleep(DELAY)
                amount_turns -= 1
            end_time = time.time()
            total_time = end_time - start_time
    motor.release()

def write_file(drop, pressure, timertc):
    with open(f'/sd/test_output{drop}.txt',"a+") as out:
       out.write(f'{timertc.tm_hour}:{timertc.tm_min}:{timertc.tm_sec}_{pressure}\n')

def send_the_file(drop, time):
    return
#print(wifi.radio.set_ipv4_address(ipv4=ipv4_address, netmask=netmask_address, gateway=gateway_address))

print("Access point created with SSID: {}, password: {}".format(wifi_ssid, wifi_passwd))
print("Self IP", wifi.radio.ipv4_address)
print("router", wifi.radio.ipv4_gateway_ap)
print("Subnet", wifi.radio.ipv4_subnet_ap)
while True: 
    time.sleep(5)
    print(mpr.pressure)
    time.sleep(1)
    ip_address_topside_ipv4 = ipaddress.IPv4Address(topside_ip_addr)
    print(ip_address_topside_ipv4)
    t = rtc.datetime
    time.sleep(1)
    print(t)
    print(t.tm_hour, t.tm_min, t.tm_sec)
    print("pressure reading", mpr.pressure)

    # topside_ip_addr = tcp_recv_text()
    # print(str(topside_ip_addr))
    ip_address_topside_ipv4 = ipaddress.IPv4Address(str(topside_ip_addr))
    print("topside ip", topside_ip_addr)
    #---- Runs the motor in 2 rotations and for 20 seconds ----
    # start time
    #movement(False, number_of_turns, holding_time_sec)
    ping = wifi.radio.ping(ip=ip_address_topside_ipv4)
    while ping is None:
        topside_ip_addr = tcp_recv_text()
        if topside_ip_addr is not None:
            print("topside ip 2", topside_ip_addr)
            ip_address_topside_ipv4 = ipaddress.IPv4Address(str(topside_ip_addr).replace('"', ''))
            print("failed to connect")
            ping = wifi.radio.ping(ip=ip_address_topside_ipv4)
    if drop == 0:
        result = tcp_recv_text()
        while result != "RTC":
            print("Waiting for RTC Set Module")
            result = tcp_recv_text()
        
    result = tcp_recv_text()
    while result != "DOWN":
        print("Waiting for DOWN Command")
        result = tcp_recv_text()
    total_time = 0
    start_time = time.time()
    while drop_total_time >= total_time: 
        movement(False, number_of_turns, holding_time_sec, drop, mpr.pressure, t)
        time.sleep(sink_time)
        movement(True, number_of_turns, holding_time_sec, drop, mpr.pressure, t)
        end_time = time.time()
        total_time = end_time - start_time
    tcp_send_file(drop)
    drop+=1
