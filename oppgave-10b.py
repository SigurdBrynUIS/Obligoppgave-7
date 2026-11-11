import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


TEMPERATURGRENSER = (
    ("Sommerdager (>20 °C)", 20),
    ("Høysommerdager (>25 °C)", 25),
    ("Tropedager (>30 °C)", 30),
)


def tell_varme_dager(filnavn):
    antall = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))

    with filnavn.open(encoding="utf-8-sig", newline="") as fil:
        leser = csv.DictReader(fil, delimiter=";")
        nødvendige_kolonner = {
            "Navn",
            "Tid(norsk normaltid)",
            "Maksimumstemperatur (døgn)",
        }
        if leser.fieldnames is None or not nødvendige_kolonner.issubset(leser.fieldnames):
            raise ValueError(f"{filnavn} mangler nødvendige kolonner.")

        for rad in leser:
            try:
                dato = datetime.strptime(rad["Tid(norsk normaltid)"], "%d.%m.%Y")
            except (TypeError, ValueError):
                continue  # Hopper over eventuell informasjonstekst etter dataene.

            temperatur = rad["Maksimumstemperatur (døgn)"].strip()
            if temperatur in {"", "-"}:
                continue

            try:
                maksimum = float(temperatur.replace(",", "."))
            except ValueError as feil:
                raise ValueError(
                    f"Ugyldig maksimumstemperatur i {filnavn}: {temperatur!r}"
                ) from feil

            stasjon = rad["Navn"].strip()
            if not stasjon:
                raise ValueError(f"Mangler stasjonsnavn i {filnavn}.")

            årsantall = antall[stasjon][dato.year]
            for indeks, (_, grense) in enumerate(TEMPERATURGRENSER):
                if maksimum > grense:
                    årsantall[indeks] += 1

    return antall


def main():
    datamappe = Path(__file__).resolve().parent / "flere_vaerstasjoner_med_makstemperatur"
    filer = sorted(datamappe.glob("*_med_makstemperatur.csv"))
    if not filer:
        raise FileNotFoundError(f"Fant ingen værstasjonsfiler i {datamappe}.")

    antall_per_stasjon = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    for filnavn in filer:
        for stasjon, årstall in tell_varme_dager(filnavn).items():
            for år, antall in årstall.items():
                for indeks, verdi in enumerate(antall):
                    antall_per_stasjon[stasjon][år][indeks] += verdi

    if not any("Oslo" in stasjon and "Blindern" in stasjon for stasjon in antall_per_stasjon):
        raise ValueError("Fant ikke værstasjonen Oslo Blindern i CSV-filene.")

    stasjoner = sorted(antall_per_stasjon)
    figur, akser = plt.subplots(
        len(stasjoner),
        1,
        figsize=(12, 3.5 * len(stasjoner)),
        sharex=True,
        squeeze=False,
    )

    for akse, stasjon in zip(akser.flat, stasjoner):
        år = sorted(antall_per_stasjon[stasjon])
        for indeks, (etikett, _) in enumerate(TEMPERATURGRENSER):
            verdier = [antall_per_stasjon[stasjon][årstall][indeks] for årstall in år]
            akse.plot(år, verdier, marker=".", label=etikett)

        akse.set_title(stasjon)
        akse.set_ylabel("Antall dager")
        akse.yaxis.set_major_locator(MaxNLocator(integer=True))
        akse.grid(True)
        akse.legend()

    akser[-1, 0].set_xlabel("År")
    akser[-1, 0].xaxis.set_major_locator(MaxNLocator(integer=True, nbins=12))
    figur.suptitle("Sommerdager, høysommerdager og tropedager per år")
    figur.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()