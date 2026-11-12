from pathlib import Path
from oblig7_f_g import les_csv
import matplotlib.pyplot as plt

mappe = Path(__file__).resolve().parent / "flere_vaerstasjoner_med_makstemperatur"
def beregn_aarsgjennomsnitt(data):
    per_aar = {}

    for dato, temperatur, _ in data:
        if temperatur is None:
            continue

        aar = dato.year
        if aar not in per_aar:
            per_aar[aar] = {}

        per_aar[aar][dato.date()] = temperatur

    aarsgjennomsnitt = {}

    for aar in sorted(per_aar):
        temperaturer = per_aar[aar].values()
        antall = len(temperaturer)

        if antall >= 300:
            snitt = sum(temperaturer) / antall
            aarsgjennomsnitt[aar] = snitt

    return aarsgjennomsnitt


stasjoner = {
    "Oslo - Blindern": mappe / "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": mappe / "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": mappe / "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": mappe / "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": mappe / "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": Path(__file__).resolve().parent / "sinnes_2014_2025.csv",
}

resultater = {}

for navn, fil in stasjoner.items():
    data = les_csv(fil)
    aarsgjennomsnitt = beregn_aarsgjennomsnitt(data)
    resultater[navn] = aarsgjennomsnitt

plt.figure(figsize=(11, 5))

for navn, aarsgjennomsnitt in resultater.items():
    if not aarsgjennomsnitt:
        continue

    aarstall = list(range(min(aarsgjennomsnitt), max(aarsgjennomsnitt) + 1))
    temperaturer = []

    for aar in aarstall:
        temperaturer.append(aarsgjennomsnitt.get(aar, float("nan")))

    plt.plot(aarstall, temperaturer, marker=".", label=navn)

plt.xlabel("År")
plt.ylabel("Gjennomsnittstemperatur (°C)")
plt.title("Årsgjennomsnitt for seks værstasjoner")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()