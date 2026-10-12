import csv
from datetime import datetime
import matplotlib.pyplot as plt

def les_csv(filnavn):
    data = []
    with open(filnavn, encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # hopp over header

        for rad in reader:
            try:
                dato = datetime.strptime(rad[2], "%d.%m.%Y")
                temp = float(rad[3].replace(',', '.'))
                nedbor = float(rad[4].replace(',', '.'))
                vind = float(rad[5].replace(',', '.'))
                sno = float(rad[6].replace(',', '.'))
                data.append((dato, temp, nedbor, vind, sno))
            except:
                continue
    return data

fil = "sinnes_2014_2025.csv" #  kan vi bytte til den andre fila

data = les_csv(fil)

# Plotting av temperatur
datoer = [d[0] for d in data]
temp = [d[1] for d in data]

plt.plot(datoer, temp)
plt.title("Middeltemperatur ved Sinnes værstasjon")
plt.xlabel("Dato")
plt.ylabel("Temperatur (°C)")
plt.show()
