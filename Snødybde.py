
import csv
import datetime as dt
import matplotlib.pyplot as plt


# Velger hvilke værstasjoner som skal brukes
def velg_filer():

    filer = {
        "1": "sinnes_1954_2025_med_makstemperatur.csv",
        "2": "oslo_blindern_1954_2025_med_makstemperatur.csv",
        "3": "roeros_1954_2025_med_makstemperatur.csv",
        "4": "tromsoe_1954_2025_med_makstemperatur.csv",
        "5": "vaernes_1954_2025_med_makstemperatur.csv",
        "6": "venabu_1954_2025_med_makstemperatur.csv"
    }

    while True:
        print("\nVelg værstasjoner:")
        print("1. Sinnes")
        print("2. Oslo Blindern")
        print("3. Røros")
        print("4. Tromsø")
        print("5. Værnes")
        print("6. Venabu")

        valg = input(
            "Velg en eller flere værstasjoner (f.eks. 1, 3, 5): "
        )

        valgte_filer = valg.split(",")
        resultat = []
        ugyldig_valg = False

        for nummer in valgte_filer:
            nummer = nummer.strip()

            if nummer in filer:
                if filer[nummer] not in resultat:
                    resultat.append(filer[nummer])
            else:
                print(
                    "Feil: Valget", nummer,
                    "finnes ikke. Velg et tall mellom 1 og 6."
                )
                ugyldig_valg = True

        if len(resultat) == 0:
            print("Feil: Ingen gyldige værstasjoner ble valgt.")
            continue

        if ugyldig_valg:
            print("De gyldige valgene blir brukt.")

        return resultat


# Programmet fortsetter helt til brukeren velger å avslutte
fortsett = True

while fortsett:

    valgte_filer = velg_filer()

    plt.figure()

    # Går gjennom hver valgte værstasjon
    for filnavn in valgte_filer:

        datoer = []
        snoedybder = []

        # Leser CSV-filen
        try:
            with open(filnavn, "r", encoding="utf-8") as fil:
                leser = csv.reader(fil, delimiter=";")
                next(leser, None)

                for rad in leser:

                    # Hopper over ugyldige eller ufullstendige rader
                    if len(rad) < 8:
                        continue

                    if rad[2].strip() == "":
                        continue

                    try:
                        dato = dt.datetime.strptime(
                            rad[2].strip(), "%d.%m.%Y"
                        ).date()
                    except ValueError:
                        continue

                    # Leser snødybden
                    snoe = rad[7].strip()

                    if snoe == "" or snoe == "-":
                        snoedybde = None
                    else:
                        try:
                            snoedybde = float(snoe.replace(",", "."))
                        except ValueError:
                            continue

                    datoer.append(dato)
                    snoedybder.append(snoedybde)

        except FileNotFoundError:
            print("Feil: Fant ikke filen", filnavn)
            continue

        # Finner skisesong for hver dato
        sesong_aar = []
        antall_skidager = []
        antall_registreringer = []

        for i in range(len(datoer)):

            dato = datoer[i]

            # Skisesongen går fra oktober til og med april
            if dato.month >= 10:
                sesong = dato.year + 1
            elif dato.month <= 4:
                sesong = dato.year
            else:
                continue

            if sesong not in sesong_aar:
                sesong_aar.append(sesong)
                antall_skidager.append(0)
                antall_registreringer.append(0)

            indeks = sesong_aar.index(sesong)

            # Teller dager med registrert snødybde
            if snoedybder[i] is not None:
                antall_registreringer[indeks] += 1

                # Teller dager med minst 20 cm snø
                if snoedybder[i] >= 20:
                    antall_skidager[indeks] += 1

        # Fjerner skisesonger med for få registreringer
        gyldige_sesonger = []
        gyldige_skidager = []

        for i in range(len(sesong_aar)):

            start = dt.date(sesong_aar[i] - 1, 10, 1)
            slutt = dt.date(sesong_aar[i], 5, 1)

            antall_dager = (slutt - start).days

            # Minst halvparten av dagene må ha registrert snødybde
            if antall_registreringer[i] >= antall_dager / 2:
                gyldige_sesonger.append(sesong_aar[i])
                gyldige_skidager.append(antall_skidager[i])

        # Lager kurve for værstasjonen
        navn = filnavn.replace(
            "_1954_2025_med_makstemperatur.csv", ""
        )

        if gyldige_sesonger:
            plt.plot(
                gyldige_sesonger,
                gyldige_skidager,
                marker="o",
                label=navn
            )

    # Sjekker om det finnes data å vise
    if not plt.gca().has_data():
        print("Feil: Ingen data kunne leses fra de valgte filene.")
        plt.close()
        continue

    # Viser grafen
    plt.xlabel("Skisesong")
    plt.ylabel("Antall dager med skiføre")
    plt.title("Antall dager med skiføre for ulike værstasjoner")
    plt.legend()
    plt.grid()
    plt.show()

    # Spør om brukeren vil fortsette
    svar = input(
        "\nVil du lage en ny graf? Skriv ja eller nei: "
    ).strip().lower()

    if svar != "ja":
        fortsett = False

print("Programmet er avsluttet.")
