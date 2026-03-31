contacts = {}

def load_from_csv():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
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
    name = input("Namn: ")
    number = input("Nummer: ")
    contacts[name] = number
    save_to_csv()
    print("Kontakt sparad.\n")

def show_contacts():
    if not contacts:
        print("Inga kontakter.\n")
        return
    for name, number in contacts.items():
        print(f"{name}: {number}")
    print()

def search_contact():
    name = input("Sök namn: ")
    if name in contacts:
        print(f"{name}: {contacts[name]}\n")
    else:
        print("Hittades inte.\n")

def menu():
    while True:
        print("1. Lägg till kontakt")
        print("2. Visa alla kontakter")
        print("3. Sök kontakt")
        print("4. Avsluta")

        choice = input("Välj: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            break
        else:
            print("Fel val.\n")

menu()