import inputs
import threading

right_stick = (0, 0)
left_stick = (0, 0)

x_pressed = False

def _run():
    global right_stick
    global left_stick
    global x_pressed
    while True:
        for device in inputs.devices.gamepads:
            for event in device.read():
                match str(event.code):
                    case "ABS_X":
                        left_stick = (event.state / 32768, left_stick[1])
                        break
                    case "ABS_Y":
                        left_stick = (left_stick[0], event.state / 32768)
                        break
                    case "ABS_RX":
                        right_stick = (event.state / 32768, right_stick[1])
                        break
                    case "ABS_RY":
                        right_stick = (right_stick[0], event.state / 32768)
                        break
                    case "BTN_NORTH":
                        x_pressed = (event.state == 1)
                        break
                    case "SYN_REPORT": break # don't care
                    case _:
                        print(str(event.code) + ": " + str(event.state))

_run_thread = threading.Thread(target=_run, daemon=True)
_run_thread.start()
