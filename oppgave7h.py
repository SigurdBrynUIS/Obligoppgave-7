import csv
from datetime import datetime


def les_csv(filnavn):
    data = []

    with open(filnavn, encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # hopp over header

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


def antall_per_år(data, år):
    sommer = 0
    høysommer = 0
    trope = 0

    for dato, temp, nedbor, vind, sno in data:
        if dato.year == år:

            if temp > 20:
                sommer += 1

            if temp > 25:
                høysommer += 1

            if temp > 30:
                trope += 1

    print(f"I {år}:")
    print(f"Sommerdager (>20°C): {sommer}")
    print(f"Høysommerdager (>25°C): {høysommer}")
    print(f"Tropedager (>30°C): {trope}")


data = les_csv("sinnes_2014_2025_med_makstemperatur.csv")
antall_per_år(data, 2025)