contacts = {}
import csv

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
    with open("contacts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Number"])

        for name, number in contacts.items():
            writer.writerow([name, number])


def add_contact():
    name = input("Namn: ").strip()
    number = input("Nummer: ").strip()

    if name == "" or number == "":
        print("Fel: tom input.\n")
        return

    contacts[name] = number
    save_to_csv()
    print("Kontakt sparad.\n")


def show_contacts():
    if not contacts:
        print("Inga kontakter.\n")
        return

    print(f"Totalt kontakter: {len(contacts)}\n")

    for name in sorted(contacts):
        print(f"{name}: {contacts[name]}")
    print()


def search_contact():
    search = input("Sök namn: ").strip().lower()

    found = False
    for name, number in contacts.items():
        if search in name.lower():
            print(f"{name}: {number}")
            found = True

    if not found:
        print("Hittades inte.\n")
    else:
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


def menu():
    while True:
        print("1. Lägg till kontakt")
        print("2. Visa alla kontakter")
        print("3. Sök kontakt")
        print("4. Ta bort kontakt")
        print("5. Ändra kontakt")
        print("6. Avsluta")

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
            break
        else:
            print("Fel val.\n")


load_from_csv()
menu()