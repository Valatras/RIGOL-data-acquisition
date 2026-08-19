import os

import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
matplotlib_config_dir = os.path.join(project_root, ".matplotlib")
cache_dir = os.path.join(project_root, ".cache")
os.makedirs(matplotlib_config_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", matplotlib_config_dir)
os.environ.setdefault("XDG_CACHE_HOME", cache_dir)

import matplotlib.pyplot as plt


df = pd.read_csv("square_signal.csv")
input_column = "signal_input" if "signal_input" in df.columns else "Capacitor_voltage"
plt.plot(df["timestamp"], df[input_column], label="Input")
plt.plot(df["timestamp"], df["signal_output"], label="Output")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)
plt.show()
