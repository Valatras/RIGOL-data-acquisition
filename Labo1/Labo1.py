from tools.find_instruments import detect_rigol_instruments
import time
import sys
import os
import csv
# run python -m Labo1.Labo1 to execute this script

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


def generator_square_signal_record():
    """Signal carré et enregistrement CSV"""

    csv_file = "square_signal.csv"
    data = []

    # Configuration initiale
    generator.write("FUNCtion:SQUare:DCYCle 60")
    time.sleep(1)
    generator.write("OUTP1 ON")
    time.sleep(1)

    start_time = time.time()
    i = 1
    while i < 20:
        if i % 2 == 0:
            generator.write("APPLy:SQUare 1250,2.3,2.3")
        else:
            generator.write("APPLy:SQUare 1250,4.3,2.3")

        # Mesurer toutes les 0.1 s pendant 2 secondes
        t0 = time.time()
        while time.time() - t0 < 2:
            timestamp = time.time() - start_time
            # lecture des données
            vin = float(oscilloscope.query(":MEASure:VPP? CHAN1"))
            vout = float(oscilloscope.query(":MEASure:VPP? CHAN2"))

            data.append([timestamp, vin, vout])
            time.sleep(0.1)

        i += 1

    generator.write("OUTP1 OFF")

    # Sauvegarde CSV
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "signal_input", "signal_output"])
        writer.writerows(data)

    print(f"Données enregistrées dans {csv_file}")


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
    # Ajuste l'échelle de temps pour mieux voir le signal
    oscilloscope.write("TIM:SCAL 0.002")
    time.sleep(15)  # Temps pour observer à l’oscillo

    generator.write("OUTP1 OFF")
    oscilloscope.write("CHAN1:DISP OFF")


if __name__ == "__main__":
    if generator:
        print("Générateur de signal détecté.")
        # generator_timed_signal()
        generator_sine_signal()
        # generator_exponential_signal()
        # generator_square_signal_record()

    else:
        print("Générateur de signal non détecté !")

    if oscilloscope:
        print("Oscilloscope détecté.")
        test_channel_1()

    else:
        print("Oscilloscope non détecté !")

    if generator and oscilloscope:
        print("instruments détectés.")
        observe_exponential_signal()

    if generator is not None:
        generator.close()
    else:
        print("Générateur indisponible.")

    if oscilloscope is not None:
        oscilloscope.close()
    else:
        print("Oscilloscope indisponible.")
