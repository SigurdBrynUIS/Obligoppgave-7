import csv
from datetime import datetime, timedelta
from pathlib import Path
def read_number(text):
    if text == "-" or text == "":
        return None  # Manglende verdi, ikke null.
    return float(text.replace(",", "."))
def get_date(day):
    return day[0]
def les_csv(filename):
    data = []
    with open(filename, encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file, delimiter=";")
        header = next(reader)
        temp_column = header.index("Middeltemperatur (døgn)")
        rain_column = header.index("Nedbør (døgn)")
        for row in reader:
            if len(row) != len(header):
                continue
            try:
                date = datetime.strptime(row[2], "%d.%m.%Y")
            except ValueError:
                continue  # Hopper over informasjonsteksten nederst i fila.
            temp = read_number(row[temp_column])
            rain = read_number(row[rain_column])
            data.append((date, temp, rain))
    return data
def plant_growth(data, year):
    total_growth = 0
    for day in data:
        date = day[0]
        temp = day[1]
        if date.year == year and temp is not None:
            if temp > 5:
                total_growth += temp - 5
    return total_growth
def longest_dry_period(data):
    data = sorted(data, key=get_date)
    current_streak = 0
    max_streak = 0
    start = None
    best_start = None
    best_end = None
    previous_date = None
    for day in data:
        date = day[0]
        rain = day[2]
        # Et hull i datoene bryter perioden.
        if previous_date is not None:
            if date - previous_date != timedelta(days=1):
                current_streak = 0
        if rain == 0:
            if current_streak == 0:
                start = date
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
                best_start = start
                best_end = date
        else:
            current_streak = 0  # Regn eller manglende måling bryter perioden.
        previous_date = date
    return max_streak, best_start, best_end
def main():
    # Ser først i arbeidsmappa, deretter ved siden av Python-fila.
    filename = Path("sinnes_2014_2025.csv")
    if not filename.exists():
        filename = Path(__file__).with_name("sinnes_2014_2025.csv")
    if not filename.exists():
        print("Legg f_g.py og sinnes_2014_2025.csv i samme mappe.")
        return
    data = les_csv(filename)
    year = int(input("Skriv inn årstall: "))
    growth = plant_growth(data, year)
    print(f"f: Samlet plantevekst i {year}: {growth:.1f}")
    print("Beregnet fra kjente middeltemperaturer. Manglende verdier er utelatt.")
    length, start, end = longest_dry_period(data)
    print(f"g: Lengste bekreftede periode uten nedbør i hele fila: {length} dager")
    if length > 0:
        print("Start:", start.strftime("%d.%m.%Y"))
        print("Slutt:", end.strftime("%d.%m.%Y"))
if __name__ == "__main__":
    main()