import csv
from datetime import datetime
import matplotlib.pyplot as plt

def les_csv(filnavn):
    data = []

    with open(filnavn, encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)

        for rad in reader:
            try:
                dato = datetime.strptime(rad[2], "%d.%m.%Y")
                temp = float(rad[3].replace(",", "."))
                nedbør = float(rad[4].replace(",", "."))
                vind = float(rad[5].replace(",", "."))
                snø = float(rad[6].replace(",", "."))

                data.append((dato, temp, nedbør, vind, snø))

            except:
                continue

    return data


fil = "sinnes_2014_2025.csv"
data = les_csv(fil)

# grupper etter måned
måneder = {}

for dato, temp, nedbør, vind, snø in data:

    nøkkel = (dato.year, dato.month)

    if nøkkel not in måneder:
        måneder[nøkkel] = {
            "temp": [],
            "nedbør": [],
            "vind": [],
            "snø": []
        }

    måneder[nøkkel]["temp"].append(temp)
    måneder[nøkkel]["nedbør"].append(nedbør)
    måneder[nøkkel]["vind"].append(vind)
    måneder[nøkkel]["snø"].append(snø)


dato_liste = []
maks_snø_liste = []
total_nedbør_liste = []
maks_temp_liste = []
min_temp_liste = []
maks_vind_liste = []

for nøkkel in sorted(måneder):

    år, måned = nøkkel

    temp = måneder[nøkkel]["temp"]
    nedbør = måneder[nøkkel]["nedbør"]
    vind = måneder[nøkkel]["vind"]
    snø = måneder[nøkkel]["snø"]

    dato_liste.append(datetime(år, måned, 1))

    maks_snø_liste.append(max(snø))

    if len(nedbør) > 20:
        total_nedbør_liste.append(sum(nedbør))
    else:
        total_nedbør_liste.append(None)

    maks_temp_liste.append(max(temp))
    min_temp_liste.append(min(temp))
    maks_vind_liste.append(max(vind))


plt.figure(figsize=(12, 6))

plt.plot(dato_liste, maks_snø_liste, label="Maks snødybde")
plt.plot(dato_liste, total_nedbør_liste, label="Total nedbør")
plt.plot(dato_liste, maks_temp_liste, label="Maks middeltemperatur")
plt.plot(dato_liste, min_temp_liste, label="Min middeltemperatur")
plt.plot(dato_liste, maks_vind_liste, label="Maks middelvind")

plt.title("Månedsstatistikk for Sinnes")
plt.xlabel("År")
plt.ylabel("Verdi")
plt.legend()
plt.grid()

plt.show()