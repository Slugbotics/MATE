import inputs
import threading
import array

import bitarray

#index is the controller value [First controller: 0, Second Controller: 1, etc.]
class controller:
    def __init__(self, index):
        self.right_stick = (0, 0)
        self.left_stick = (0, 0)
        self.a_pressed = 0
        self.x_pressed = 0
        self.b_pressed = 0
        self.start_pressed = 0
        self.btn_tl = 0
        self.btn_tr = 0
        self.device = inputs.devices.gamepads[index]
        self._thread()
        self.activate_arm = False

    def _run(self):
        while True:
            for event in self.device.read():
                match str(event.code):
                    case "ABS_X":
                        self.left_stick = (event.state / 32768, self.left_stick[1])
                        break
                    case "ABS_Y":
                        self.left_stick = (self.left_stick[0], event.state / 32768)
                        break
                    case "ABS_RX":
                        self.right_stick = (event.state / 32768, self.right_stick[1])
                        break
                    case "ABS_RY":
                        self.right_stick = (self.right_stick[0], event.state / 32768)
                        break
                    case "BTN_SELECT":
                        if event.state == 1 and self.activate_arm == False:
                            self.activate_arm = True
                            self.start_pressed = '1'
                        elif event.state ==1 and self.activate_arm == True:
                            self.start_pressed = '0'
                            self.activate_arm = False
                        # self.a_pressed = (if event.state == 1: '1')
                        break
                    case "BTN_EAST":
                        self.b_pressed = ('1' if event.state == 1 else '0')
                    case "BTN_NORTH":
                        self.x_pressed = ('1' if event.state == 1 else '0')
                    case "BTN_TL":
                        self.btn_tl = ('1' if event.state == 1 else '0')
                    case "BTN_TR":
                        self.btn_tr = ('1' if event.state == 1 else '0')
                    case "SYN_REPORT": break # don't care YET
                    case _:
                        print(str(event.code) + ": " + str(event.state))
    
    def _thread(self):
        _run_thread = threading.Thread(target=self._run, daemon=True)
        _run_thread.start()
    
    def gen_packet(self):
        x = self.left_stick
        y = self.right_stick

        BTN_X = int(self.x_pressed)
        BTN_B = int(self.b_pressed)
        BTN_START = int(self.start_pressed)

        Left_Bumper = int(self.btn_tl)
        Right_Bumper = int(self.btn_tr)
        
        button_array = bitarray.bitarray([BTN_X, BTN_B, BTN_START, Left_Bumper, Right_Bumper, 0, 0, 0])
          
        horizontal = x[0]
        vertical = y[1]
        if abs(horizontal) < 0.19:
            horizontal = 0
        if abs(vertical) < 0.19:
            vertical = 0 

        horizontal = (round((horizontal) * 10)) + 10
        vertical = (round((vertical) * 10)) + 10

        # Create and send packet
        packet = bytearray() 
        for field in [horizontal, vertical]:
            packet.extend(field.to_bytes(1, byteorder="big", signed=True))
        packet.extend(button_array.tobytes())
        return packet