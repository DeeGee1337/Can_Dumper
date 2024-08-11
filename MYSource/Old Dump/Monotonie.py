import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Neue Dateien einlesen
file_paths = [
    'can0_dump.csv',
    'can1_dump.csv',
    'can2_dump.csv',
    'can3_dump.csv',
    'can4_dump.csv',
    'can5_dump.csv'
]

data_frames = []
for file in file_paths:
    df = pd.read_csv(file, header=None, names=['ID', 'Timestamp', 'Data'])
    data_frames.append(df)

# Funktion zur Berechnung der Bitflips
def count_bitflips(data1, data2):
    bitflips = 0
    for byte1, byte2 in zip(data1, data2):
        bitflips += bin(byte1 ^ byte2).count('1')
    return bitflips

# Funktion zur Umwandlung der Daten in Dezimalwerte
def data_to_decimal(data):
    return [int(byte, 16) for byte in data.split()]

# Funktion zur Überprüfung auf monoton steigende oder fallende Werte
def is_monotonic(data):
    decimal_data = data_to_decimal(data)
    return (all(x <= y for x, y in zip(decimal_data, decimal_data[1:])) or
            all(x >= y for x, y in zip(decimal_data, decimal_data[1:])))

bitflip_data = {}
monotonic_data = {}
for i, df in enumerate(data_frames):
    df['Previous_Data'] = df['Data'].shift(1).fillna(df['Data'].iloc[0])
    df['Bitflips'] = df.apply(lambda row: count_bitflips(bytearray.fromhex(row['Data'].replace(" ", "")), bytearray.fromhex(row['Previous_Data'].replace(" ", ""))), axis=1)
    bitflips_per_id = df.groupby('ID')['Bitflips'].sum().reset_index()
    bitflips_per_id.columns = ['ID', f'Bitflips_CAN{i}']
    bitflip_data[f'CAN{i}'] = bitflips_per_id
    
    # Überprüfen auf monoton steigende oder fallende Werte und Aggregieren der Ergebnisse pro Nachrichten-ID
    monotonic_per_id = df.groupby('ID')['Data'].apply(lambda x: all(is_monotonic(data) for data in x)).reset_index()
    monotonic_per_id.columns = ['ID', f'Monotonic_CAN{i}']
    monotonic_data[f'CAN{i}'] = monotonic_per_id

# Zusammenführen der Bitflip-Daten
bitflips_df = pd.concat(bitflip_data.values(), axis=1)
bitflips_df = bitflips_df.loc[:, ~bitflips_df.columns.duplicated()]

# Zusammenführen der Monotonie-Daten
monotonic_df = pd.concat(monotonic_data.values(), axis=1)
monotonic_df = monotonic_df.loc[:, ~monotonic_df.columns.duplicated()]

# Sicherstellen, dass die Bitflip-Daten korrekt formatiert sind und NaN-Werte entfernt werden
bitflips_df.reset_index(drop=True, inplace=True)
bitflips_df.dropna(subset=['ID'], inplace=True)
bitflips_df.set_index('ID', inplace=True)
bitflips_df = bitflips_df.fillna(0).astype(int)

# Sicherstellen, dass die Monotonie-Daten korrekt formatiert sind und NaN-Werte entfernt werden
monotonic_df.reset_index(drop=True, inplace=True)
monotonic_df.dropna(subset=['ID'], inplace=True)
monotonic_df.set_index('ID', inplace=True)
monotonic_df = monotonic_df.fillna(False).astype(bool)

# Erstellen der Heatmap für Bitflips ohne Index-Spalte
plt.figure(figsize=(14, 10))
sns.heatmap(bitflips_df, cmap="YlGnBu", annot=True, fmt="d", annot_kws={"size": 8}, linewidths=0.5, linecolor='gray')
plt.title("Heatmap of Bitflips per ID across CAN Dumps", fontsize=16)
plt.xlabel("CAN Dumps", fontsize=12)
plt.ylabel("Message IDs", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, rotation=0)
plt.savefig("bitflips_heatmap.png")
plt.show()

# Erstellen der Monotonie-Heatmap ohne Index-Spalte
plt.figure(figsize=(14, 10))
sns.heatmap(monotonic_df, cmap="coolwarm", annot=True, fmt="d", annot_kws={"size": 8}, linewidths=0.5, linecolor='gray')
plt.title("Heatmap of Monotonic Data per ID across CAN Dumps", fontsize=16)
plt.xlabel("CAN Dumps", fontsize=12)
plt.ylabel("Message IDs", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, rotation=0)
plt.savefig("monotonic_heatmap.png")
plt.show()

