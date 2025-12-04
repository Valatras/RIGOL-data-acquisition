# Importing Libraries
import time
import serial

class ArduinoInterface:
    def __init__(self, port="/dev/ttyACM0", baud=115200):
        self.ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # L’Arduino reboot au moment de l'ouverture du port

    def send_cmd(self, cmd):
        """
        Docstring for send_cmd
        
        :param self: Description
        :param cmd: Description
        """
        self.ser.write((cmd + "\n").encode())
        return self.ser.readline().decode().strip()

    def analog_read(self, pin):
        """
        Docstring for analog_read
        
        :param self: Description
        :param pin: Description
        """
        resp = self.send_cmd(f"ANALOG_READ A{pin}?")
        _, val = resp.split(":")
        return int(val)

    def digital_read(self, pin):
        """
        Docstring for digital_read
        
        :param self: Description
        :param pin: Description
        """
        resp = self.send_cmd(f"DIGITAL_READ D{pin}?")
        _, val = resp.split(":")
        return int(val)

    def pwm_write(self, pin, value):
        """
        Docstring for pwm_write
        
        :param self: Description
        :param pin: Description
        :param value: Description
        """
        resp = self.send_cmd(f"PWM D{pin} {value}")
        return resp  # "OK" normalement

    def analog_write(self, pin, value):
        return self.send_cmd(f"ANALOG_WRITE D{pin} {value}")

    def digital_write(self, pin, value):
        return self.send_cmd(f"DIGITAL_WRITE D{pin} {value}")

    def led_on(self):
        return self.send_cmd("LED ON")

    def led_off(self):
        return self.send_cmd("LED OFF")

    def blink(self, delay_ms):
        return self.send_cmd(f"BLINK {delay_ms}")


arduino = ArduinoInterface()

print(arduino.analog_read(0))
print("Digital D7:", arduino.digital_read(7))
print("PWM write:", arduino.pwm_write(5, 120))

print(arduino.analog_write(5, 128))
print("Digital HIGH:", arduino.digital_write(7, 0))
print("LED ON:", arduino.led_on())
print("LED OFF:", arduino.led_off())
print("Blink:", arduino.blink(300))


# Code de l'arduino sur /home/valatras/Arduino/labo3_exercice1_hardware_testing
