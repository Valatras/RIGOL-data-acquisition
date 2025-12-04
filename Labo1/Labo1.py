import time
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from tools.find_instruments import detect_rigol_instruments

generator, oscilloscope = detect_rigol_instruments()

# ==================================== FONCTIONS POUR LE GÉNÉRATEUR DE SIGNAL ====================================

# exercice 1 voir tools.find_instrument


# exercice 2
def generator_timed_signal():
    """Active et désactive un signal toutes les secondes pendant 10 secondes."""
    for i in range(10):
        generator.write("OUTP1 ON")
        time.sleep(1)
        generator.write("OUTP1 OFF")
        time.sleep(1)


# exercice 3
def generator_sine_signal():
    """Configure une onde sinusoïdale sur Channel 1 et une onde carrée sur Channel 2."""

    # Sine wave sur Channel 1 avec amplitude 5 V, fréquence 3000 Hz et offset 0 V
    generator.write("APPL:SIN 3000,5,0")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    generator.write("OUTP1 ON")
    time.sleep(5)  # Temps pour observer à l’oscillo
    generator.write("OUTP1 OFF")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    
    # Square wave sur Channel 2 avec amplitude 3 V, fréquence 1000 Hz et offset 0 V
    generator.write(" APPLy:SQUare:CH2 1000,3,0")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    generator.write("OUTP:CH2 ON")
    time.sleep(5)  # Temps pour observer à l’oscillo
    generator.write("OUTP:CH2 OFF")


# Exercice 4
def generator_exponential_signal():
    """Configure une onde exponentielle sur Channel 1."""

    # Exponential wave sur Channel 1 avec amplitude 5 V
    generator.write("APPL:USER EXP_RISE 1,5,0")
    
    time.sleep(1)
    generator.write("OUTP1 ON")
    time.sleep(50)  # Temps pour observer à l’oscillo
    generator.write("OUTP1 OFF")

# Exercice 5
def generator_square_signal():
    """signal carré"""
    
    generator.write("FUNCtion:SQUare:DCYCle 60")

    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    generator.write("OUTP1 ON")
    time.sleep(1)
    i = 1
    while i < 10:
        # Square wave sur Channel 1 
        if i % 2 == 0:
            generator.write("APPLy:SQUare 1250,2.3,2.3")
        else:
            generator.write("APPLy:SQUare 1250,4.3,2.3")
        time.sleep(2)
        i+=1

   # Temps pour observer à l’oscillo
    generator.write("OUTP1 OFF")


# ==================================== FONCTIONS POUR L'OSCILLOSCOPE ====================================

def test_channel_1():
    """Active l'affichage du Channel 1 de l'oscilloscope."""
    generator.write("OUTP1 ON")
    time.sleep(1)
    oscilloscope.write("CHAN1:DISP ON")
    time.sleep(3)
    oscilloscope.write("CHAN1:DISP OFF")


# ============================================= MAIN PROGRAM ============================================

def observe_exponential_signal():
    """Observe le signal exponentiel fournit par le générateur sur l'oscilloscope."""
    generator.write("APPL:USER EXP_RISE,1,5,0")
    time.sleep(1)
    generator.write("OUTP1 ON")
    oscilloscope.write("CHAN1:DISP ON")
    oscilloscope.write("TIM:SCAL 0.002")  # Ajuste l'échelle de temps pour mieux voir le signal
    time.sleep(15)  # Temps pour observer à l’oscillo
    
    generator.write("OUTP1 OFF")
    oscilloscope.write("CHAN1:DISP OFF")
    

if __name__ == "__main__":
    if generator:
        print("Générateur de signal détecté.")
        #generator_timed_signal()
        #generator_sine_signal()
        #generator_exponential_signal()
        generator_square_signal()
        
    else:
        print("Générateur de signal non détecté !")


    if oscilloscope:
        print("Oscilloscope détecté.")
        #test_channel_1()
        
    else:
        print("Oscilloscope non détecté !")

    if generator and oscilloscope:
        print("instruments détectés.")
        observe_exponential_signal()

    try:
        generator.close()
    except Exception as e:
        print("instrument unavailable : ", e)
    
    try:
        oscilloscope.close()
    except Exception as e:
        print("instrument unavailable : ", e)
    