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
                nedbor = float(rad[4].replace(",", "."))
                vind = float(rad[5].replace(",", "."))
                sno = float(rad[6].replace(",", "."))

                data.append((dato, temp, nedbor, vind, sno))

            except:
                continue

    return data


fil = "sinnes_2014_2025.csv"
data = les_csv(fil)

# grupper etter måned
maneder = {}

for dato, temp, nedbor, vind, sno in data:

    nøkkel = (dato.year, dato.month)

    if nøkkel not in maneder:
        maneder[nøkkel] = {
            "temp": [],
            "nedbor": [],
            "vind": [],
            "sno": []
        }

    maneder[nøkkel]["temp"].append(temp)
    maneder[nøkkel]["nedbor"].append(nedbor)
    maneder[nøkkel]["vind"].append(vind)
    maneder[nøkkel]["sno"].append(sno)


dato_liste = []
maks_sno_liste = []
total_nedbor_liste = []
maks_temp_liste = []
min_temp_liste = []
maks_vind_liste = []

for nøkkel in sorted(maneder):

    år, måned = nøkkel

    temp = maneder[nøkkel]["temp"]
    nedbor = maneder[nøkkel]["nedbor"]
    vind = maneder[nøkkel]["vind"]
    sno = maneder[nøkkel]["sno"]

    dato_liste.append(datetime(år, måned, 1))

    maks_sno_liste.append(max(sno))

    if len(nedbor) > 20:
        total_nedbor_liste.append(sum(nedbor))
    else:
        total_nedbor_liste.append(None)

    maks_temp_liste.append(max(temp))
    min_temp_liste.append(min(temp))
    maks_vind_liste.append(max(vind))


plt.figure(figsize=(12, 6))

plt.plot(dato_liste, maks_sno_liste, label="Maks snødybde")
plt.plot(dato_liste, total_nedbor_liste, label="Total nedbør")
plt.plot(dato_liste, maks_temp_liste, label="Maks middeltemperatur")
plt.plot(dato_liste, min_temp_liste, label="Min middeltemperatur")
plt.plot(dato_liste, maks_vind_liste, label="Maks middelvind")

plt.title("Månedsstatistikk for Sinnes")
plt.xlabel("År")
plt.ylabel("Verdi")
plt.legend()
plt.grid()

plt.show()