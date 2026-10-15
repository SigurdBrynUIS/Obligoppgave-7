import csv
from datetime import datetime
import matplotlib.pyplot as plt

def brukerinput():
        #godkjente input av data er årstall fra 2014 - 2025(2026 er ikke fullstending)
        #Her er det nok mulig å kode inn begrensning direkte fra filen - men jeg hardkoder denne. Det er lettere ;-)
    while True:
        try: 
            svar = int(input("Skriv inn ett gyldig årstall: (2014-2025) "))
                
            if 2014 <= svar <= 2025:
                print(f"Viser data for årstall: {svar} ")
                break
            else:
                print("Du har ikke valgt ett gyldig årstall!")
                continue

        except ValueError:
            print("prøv på nytt")

    return svar

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

def skiføre(data, svar):
    antall_skidager = 0

    for d in data:
        dato = d[0]
        snødybde = d[4]

        forrige_år = dato.year == svar - 1 and dato.month >= 11
        valgt_år = dato.year == svar and dato.month <= 5

        if (forrige_år or valgt_år) and snødybde >= 20:
            antall_skidager += 1

    print(
        f"Skisesongen november {svar - 1} til mai {svar}: "
        f"{antall_skidager} dager med skiføre"
    )

def plotting(svar):
    datoer = []
    temp = []
    nedbør = []
    vind = []
    snø = []

    for d in data:
        if d[0].year == svar:
            datoer.append(d[0])
            temp.append(d[1])
            nedbør.append(d[2])
            vind.append(d[3])
            snø.append(d[4])

    plt.plot(datoer, temp)
    plt.title(f"Middeltemperatur ved Sinnes værstasjon {svar}")
    plt.xlabel("Dato")
    plt.ylabel("Temperatur (°C)")
    plt.show()

svar = brukerinput()
skiføre(data, svar)
plotting(svar)