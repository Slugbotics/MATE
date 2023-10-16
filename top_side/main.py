import inputs

gamepads = inputs.devices.gamepads

print(str(len(gamepads)) + " gamepads connected.")

if len(gamepads) > 0:
    while True:
        for device in gamepads:
            events = device.read()
            for event in events:
                if event.ev_type == "Key" or event.ev_type == "Absolute":
                    print(str(event.device) + ": " + event.ev_type + "(" + str(event.code) + ") -> " + str(event.state))