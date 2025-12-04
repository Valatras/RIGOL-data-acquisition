import pyvisa
import time


# ID de ton instrument (détecté précédemment)
ID = "USB0::1024::2500::DG1D210100024::0::INSTR"


def timed_signal():
    """Active et désactive un signal toutes les secondes pendant 10 secondes."""
    rm = pyvisa.ResourceManager('@py')  
    inst = rm.open_resource(ID)

    for i in range(10):
        inst.write("OUTP1 ON")
        time.sleep(1)
        inst.write("OUTP1 OFF")
        time.sleep(1)

    inst.close()
    rm.close()


def sine_signal():
    """Configure une onde sinusoïdale sur Channel 1 et une onde carrée sur Channel 2."""
    rm = pyvisa.ResourceManager('@py')
    inst = rm.open_resource(ID)

    # Sine wave sur Channel 1 avec amplitude 5 V, fréquence 3000 Hz et offset 0 V
    inst.write("APPL:SIN 3000,5,0")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    inst.write("OUTP1 ON")
    time.sleep(5)  # Temps pour observer à l’oscillo
    inst.write("OUTP1 OFF")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    
    # Square wave sur Channel 2 avec amplitude 3 V, fréquence 1000 Hz et offset 0 V
    inst.write(" APPLy:SQUare:CH2 1000,3,0")
    time.sleep(1)  # Pause pour s’assurer que la commande est prise en compte
    inst.write("OUTP2 ON")
    time.sleep(5)  # Temps pour observer à l’oscillo
    inst.write("OUTP2 OFF")

    inst.close()
    rm.close()


def exponential_signal():
    """Configure une onde exponentielle sur Channel 1."""
    rm = pyvisa.ResourceManager('@py')
    inst = rm.open_resource(ID)

    # Exponential wave sur Channel 1 avec amplitude 5 V
    inst.write("APPL:USER EXP_RISE,1,5,0")
    time.sleep(1)
    inst.write("OUTP1 ON")

    time.sleep(5)  # Temps pour observer à l’oscillo

    inst.write("OUTP1 OFF")

    inst.close()
    rm.close()


if __name__ == "__main__":
    # 🔧 Exemple : exécuter la fonction désirée
    exponential_signal()
    # sine_signal()
    # timed_signal()
