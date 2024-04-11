import busio
import digitalio
import time
import adafruit_ds3231
import adafruit_mprls
import board
import adafruit_sdcard
import storage
import adafruit_motor

from adafruit_motor import stepper

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


rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))



DELAY = 0.01
STEPS = 360
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



while True: 
    print(mpr.pressure)

    time.sleep(1)
    t = rtc.datetime
    time.sleep(1)
    print(t)
    print(t.tm_hour, t.tm_min, t.tm_sec)
    with open("/sd/test_output.txt","a+") as out:
       out.write(f'{t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}_{mpr.pressure}\n')
    print(f'{t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}_{mpr.pressure}')
    
    print("pressure reading", mpr.pressure)
    
    for step in range(STEPS):
        # print("motor spin")
        motor.onestep()
        time.sleep(DELAY)
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD)
        time.sleep(DELAY)
    for step in range(STEPS):
        motor.onestep(style=stepper.DOUBLE)
        time.sleep(DELAY)
    
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        time.sleep(DELAY)
    for step in range(STEPS):
        motor.onestep(style=stepper.INTERLEAVE)
        time.sleep(DELAY)
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        time.sleep(DELAY)
    motor.release()
