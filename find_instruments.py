import pyvisa
import time

class RigolInstrument:
    def __init__(self, resource_name):
        self.inst = pyvisa.ResourceManager('@py').open_resource(resource_name)
        self.inst.timeout = 5000
        self.inst.encoding = 'utf-8'
        self.idn = self.get_idn()
        self.instrument_type = self.classify_instrument()

    def get_idn(self):
        try:
            self.inst.write('*IDN?')
            time.sleep(0.1)
            return self.inst.read().strip()
        except pyvisa.errors.VisaIOError:
            return "Unknown"

    def classify_instrument(self):
        idn_upper = self.idn.upper()
        if "RIGOL" in idn_upper and "DG" in idn_upper:
            return "generator"
        elif "RIGOL" in idn_upper and ("DS" in idn_upper or "MSO" in idn_upper):
            return "oscilloscope"
        else:
            return "unknown"

    def write(self, command):
        self.inst.write(command)

    def read(self):
        return self.inst.read()

    def close(self):
        self.inst.close()
    
    def __str__(self):
        return f"{self.instrument_type.capitalize()} - IDN: {self.idn}"


def detect_rigol_instruments():
    """Retourne un tuple (generator, oscilloscope) si présents, sinon None."""
    rm = pyvisa.ResourceManager('@py')
    devices = [d for d in rm.list_resources() if "USB" in d]

    generator = None
    oscilloscope = None
    print("Detecting Rigol instruments...")

    for dev in devices:
        rigol = RigolInstrument(dev)
        if rigol.instrument_type == "generator":
            generator = rigol
            print(f"Detected Generator: {generator}")
        elif rigol.instrument_type == "oscilloscope":
            oscilloscope = rigol
            print(f"Detected Oscilloscope: {oscilloscope}")

    return generator, oscilloscope
