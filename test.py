import time
import hak_lib


if __name__ == "__main__":
    # Create a device
    device = hak_lib.HAKServoDevice("COM7")

    # Activate a servo
    motorID = 0x02
    device.servo_activate(motorID)

    input("Press Enter to continue...")

    while(True):
        command = input("Enter a command: ")

        if command == "l": #load
            device.set_position(motorID, 0x00)
        elif command == "u": #unload
            device.set_position(motorID, 0xFF)
        
        elif command == "sl": #slow load
            device.set_position(motorID, 0x0)

            # Slowly move the motor to the desired position
            for i in range(0xFF):
                device.set_position(motorID, i)
                time.sleep(0.1)
            
        elif command == "10": # 10 shots
            device.set_position(motorID, 0xFF)

            for i in range(1,11):
                device.set_position(motorID, 0xFF - i*(0xFF//10))
                time.sleep(1)
            
            time.sleep(1)
            device.set_position(motorID, 0xFF)
                

