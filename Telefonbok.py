contacts = {}

import csv
from playsound import playsound


def load_from_csv():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) == 2:
                    name, number = row
                    contacts[name] = number
    except FileNotFoundError:
        pass


def save_to_csv():
    try:
        with open("contacts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Number"])

            for name, number in contacts.items():
                writer.writerow([name, number])
    except Exception as e:
        print("Kunde inte spara:", e)


def add_contact():
    name = input("Namn: ").strip()
    number = input("Nummer: ").strip()

    if name == "" or number == "":
        print("Fel: tom input.\n")
        return

    if name in contacts:
        print("Finns redan, använd ändra istället.\n")
        return

    contacts[name] = number
    save_to_csv()
    print("Kontakt sparad.\n")


def show_contacts():
    if not contacts:
        print("Inga kontakter.\n")
        return

    print(f"\nTotalt kontakter: {len(contacts)}\n")

    for name in sorted(contacts):
        print(f"{name}: {contacts[name]}")
    print()


def search_contact():
    search = input("Sök namn: ").strip().lower()

    results = []

    for name, number in contacts.items():
        if search in name.lower():
            results.append((name, number))

    if not results:
        print("Hittades inte.\n")
        return

    for name, number in results:
        print(f"{name}: {number}")
    print()


def delete_contact():
    name = input("Ta bort namn: ").strip()

    if name in contacts:
        del contacts[name]
        save_to_csv()
        print("Kontakt borttagen.\n")
    else:
        print("Finns inte.\n")


def edit_contact():
    name = input("Vilken kontakt vill du ändra?: ").strip()

    if name in contacts:
        new_number = input("Nytt nummer: ").strip()

        if new_number == "":
            print("Fel: tom input.\n")
            return

        contacts[name] = new_number
        save_to_csv()
        print("Kontakt uppdaterad.\n")
    else:
        print("Finns inte.\n")


def fake_call():
    name = input("Vem vill du ringa?: ").strip()

    if name not in contacts:
        print("Kontakten finns inte.\n")
        return

    print(f"\nRinger {name}...")
    print(f"Nummer: {contacts[name]}")
    print("Ringer...\n")

    try:
        playsound("ringtone.mp3")
    except:
        print("Kunde inte spela ringtone.mp3")


def stats():
    print(f"\nTotalt kontakter: {len(contacts)}")
    print("Fil: contacts.csv\n")


def menu():
    while True:
        print("\n--- TELEFONBOK ---")
        print("1. Lägg till kontakt")
        print("2. Visa alla kontakter")
        print("3. Sök kontakt")
        print("4. Ta bort kontakt")
        print("5. Ändra kontakt")
        print("6. Statistik")
        print("7. Ring")
        print("8. Avsluta")

        choice = input("Välj: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            edit_contact()
        elif choice == "6":
            stats()
        elif choice == "7":
            fake_call()
        elif choice == "8":
            break
        else:
            print("Fel val.\n")


load_from_csv()
menu()