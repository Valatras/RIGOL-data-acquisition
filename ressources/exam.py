import pyvisa
import time
import os
import csv
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
matplotlib_config_dir = os.path.join(project_root, ".matplotlib")
cache_dir = os.path.join(project_root, ".cache")
os.makedirs(matplotlib_config_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", matplotlib_config_dir)
os.environ.setdefault("XDG_CACHE_HOME", cache_dir)

import matplotlib.pyplot as plt


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
    
    def query(self, command):
        return self.inst.query(command)

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
        time.sleep(0.1)
        rigol = RigolInstrument(dev)
        if rigol.instrument_type == "generator":
            generator = rigol
            print(f"Detected Generator: {generator}")
        elif rigol.instrument_type == "oscilloscope":
            oscilloscope = rigol
            print(f"Detected Oscilloscope: {oscilloscope}")

    return generator, oscilloscope


generator, oscilloscope = detect_rigol_instruments()

print(generator)
print(oscilloscope)

def low_pulse(freq, amp, offset, Dcycle) :

    
    # ======= générateur
    generator.write(f"APPLy:Pulse {freq},{amp},{offset}")
    time.sleep(1)
    generator.write(f"PULSe:DCYCle {Dcycle}")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    generator.write("OUTP1 ON")

    # ======= Oscilloscope

    oscilloscope.write("CHAN1:DISP ON")
    time.sleep(1) 
    oscilloscope.write("TIM:SCAL 0.002")  # Ajuste l'échelle de temps pour mieux voir le signal
    time.sleep(1) 
    oscilloscope.write("CHAN2:DISP ON")

    


    generator.write("OUTP1 OFF")
    time.sleep(1) 

    oscilloscope.write("CHAN1:DISP OFF")
    time.sleep(1) 
    oscilloscope.write("CHAN2:DISP OFF")



def low_pulse_with_csv(freq, amp, offset, Dcycle) :

    csv_file = "exam.csv"
    data = []

    # ======= générateur
    generator.write(f"APPLy:Pulse {freq},{amp},{offset}")
    time.sleep(1)
    generator.write(f"PULSe:DCYCle {Dcycle}")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    generator.write("OUTP1 ON")

    # ======= Oscilloscope

    oscilloscope.write("CHAN1:DISP ON")
    time.sleep(1) 
    oscilloscope.write("TIM:SCAL 0.002")  # Ajuste l'échelle de temps pour mieux voir le signal
    time.sleep(1) 
    oscilloscope.write("CHAN2:DISP ON")

    i = 0
    start_time = time.time()
    while i < 10:
        t0 = time.time()
        while time.time() - t0 < 2:
            timestamp = time.time() - start_time
            # lecture des données
            vin = float(oscilloscope.query(":MEASure:VPP? CHAN1"))
            vout = float(oscilloscope.query(":MEASure:VPP? CHAN2"))
            data.append([timestamp, vin, vout])
            
            time.sleep(0.1)

        i += 1

    
    
    
    

    # Sauvegarde CSV
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "signal_input", "signal_output"])
        writer.writerows(data)

    generator.write("OUTP1 OFF")
    time.sleep(1) 

    oscilloscope.write("CHAN1:DISP OFF")
    time.sleep(1) 
    oscilloscope.write("CHAN2:DISP OFF")

    

def plot_csv(csv_file="square_signal.csv"):
    df = pd.read_csv(csv_file)
    input_column = "signal_input" if "signal_input" in df.columns else "Capacitor_voltage"
    plt.plot(df["timestamp"], df[input_column], label="Input")
    plt.plot(df["timestamp"], df["signal_output"], label="Output")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    
    low_pulse(10, 5, 2, 90)
    time.sleep(1)
    plot_csv()
    time.sleep(1)

    #low_pulse_with_csv(10, 5, 2, 90)


    generator.close()
    time.sleep(1)

    oscilloscope.close()
    
