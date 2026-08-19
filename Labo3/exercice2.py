import time
import sys
import os
import csv


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from tools.find_instruments import detect_rigol_instruments

generator, oscilloscope = detect_rigol_instruments()

def lm741_mesure_protocol():
    freq = 1500000
    amp = 1
    offset = 15

    def sinus():
        generator.write(f"APPLy:SIN {freq},{amp},{offset}")
        generator.write("OUTP1 ON")
        time.sleep(3)

    def triangle():

        generator.write(f"APPLy:tri {freq},{amp},{offset}")
        generator.write("OUTP1 ON")
        time.sleep(3)
    
    generator.write("OUTP1 OFF")
    generator.close()


lm741_mesure_protocol()