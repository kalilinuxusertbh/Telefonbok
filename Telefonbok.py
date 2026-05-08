import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import threading
import time
import random
import csv

contacts = {}


#csv
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


load_from_csv()


# fönster

root = tk.Tk()
root.title("GhostOS Mobile")
root.attributes("-fullscreen", True)
root.configure(bg="black")

current_time = tk.StringVar()


# tid

def update_time():
    while True:
        current_time.set(time.strftime("%H:%M"))
        time.sleep(1)


threading.Thread(target=update_time, daemon=True).start()


# ring

def fake_call(name, number):
    call_screen = tk.Frame(root, bg="black")
    call_screen.place(relwidth=1, relheight=1)

    caller = tk.Label(
        call_screen,
        text=name,
        fg="white",
        bg="black",
        font=("Arial", 40, "bold")
    )
    caller.pack(pady=100)

    number_label = tk.Label(
        call_screen,
        text=number,
        fg="gray",
        bg="black",
        font=("Arial", 20)
    )
    number_label.pack()

    status = tk.Label(
        call_screen,
        text="Calling...",
        fg="lime",
        bg="black",
        font=("Arial", 20)
    )
    status.pack(pady=20)

    def ringtone():
        try:
            playsound("ringtone.mp3")
        except:
            print("kunde inte spela mp3")

    threading.Thread(target=ringtone, daemon=True).start()

    end_button = tk.Button(
        call_screen,
        text="END CALL",
        bg="red",
        fg="white",
        font=("Arial", 20, "bold"),
        width=15,
        height=2,
        command=call_screen.destroy
    )
    end_button.pack(side="bottom", pady=80)


# kontakter

def open_contacts():
    contacts_screen = tk.Frame(root, bg="#111111")
    contacts_screen.place(relwidth=1, relheight=1)

    title = tk.Label(
        contacts_screen,
        text="CONTACTS",
        fg="white",
        bg="#111111",
        font=("Arial", 30, "bold")
    )
    title.pack(pady=20)

    contacts_frame = tk.Frame(contacts_screen, bg="#111111")
    contacts_frame.pack()

    def refresh_contacts():
        for widget in contacts_frame.winfo_children():
            widget.destroy()

        if not contacts:
            no_contacts = tk.Label(
                contacts_frame,
                text="Inga kontakter",
                fg="gray",
                bg="#111111",
                font=("Arial", 20)
            )
            no_contacts.pack()

        for name, number in contacts.items():

            row = tk.Frame(contacts_frame, bg="#111111")
            row.pack(pady=5)

            call_btn = tk.Button(
                row,
                text=f" {name} - {number}",
                bg="#222222",
                fg="white",
                font=("Arial", 16),
                width=25,
                command=lambda n=name, num=number: fake_call(n, num)
            )
            call_btn.pack(side="left", padx=5)

            delete_btn = tk.Button(
                row,
                text="❌",
                bg="red",
                fg="white",
                font=("Arial", 12),
                command=lambda n=name: delete_contact_gui(n, refresh_contacts)
            )
            delete_btn.pack(side="left")

    refresh_contacts()

    add_frame = tk.Frame(contacts_screen, bg="#111111")
    add_frame.pack(pady=20)

    name_entry = tk.Entry(add_frame, font=("Arial", 16))
    name_entry.grid(row=0, column=0, padx=10)

    number_entry = tk.Entry(add_frame, font=("Arial", 16))
    number_entry.grid(row=0, column=1, padx=10)

    def add_contact_gui():
        name = name_entry.get().strip()
        number = number_entry.get().strip()

        if name == "" or number == "":
            messagebox.showerror("Error", "Empty input")
            return

        contacts[name] = number
        save_to_csv()

        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)

        refresh_contacts()

    add_btn = tk.Button(
        add_frame,
        text="LÄGG TILL",
        bg="lime",
        fg="black",
        font=("Arial", 14, "bold"),
        command=add_contact_gui
    )
    add_btn.grid(row=0, column=2, padx=10)

    back = tk.Button(
        contacts_screen,
        text="BACK",
        bg="gray",
        fg="white",
        font=("Arial", 18),
        command=contacts_screen.destroy
    )
    back.pack(side="bottom", pady=20)


#ta bort

def delete_contact_gui(name, refresh_function):
    if name in contacts:
        del contacts[name]
        save_to_csv()
        refresh_function()



topbar = tk.Frame(root, bg="#111111", height=50)
topbar.pack(fill="x")

time_label = tk.Label(
    topbar,
    textvariable=current_time,
    fg="white",
    bg="#111111",
    font=("Arial", 20)
)
time_label.pack(side="right", padx=20)



home = tk.Frame(root, bg="black")
home.pack(expand=True)

title = tk.Label(
    home,
    text="MioOS",
    fg="lime",
    bg="black",
    font=("Arial", 45, "bold")
)
title.pack(pady=50)

phone_button = tk.Button(
    home,
    text="KONTAKTER",
    bg="#1f1f1f",
    fg="white",
    font=("Arial", 25),
    width=18,
    height=3,
    command=open_contacts
)
phone_button.pack(pady=20)

stats_button = tk.Button(
    home,
    text=f"TOTALA KONTAKTER: {len(contacts)}",
    bg="#1f1f1f",
    fg="lime",
    font=("Arial", 20),
    width=25,
    height=2
)
stats_button.pack(pady=20)

exit_button = tk.Button(
    home,
    text="EXIT",
    bg="red",
    fg="white",
    font=("Arial", 20),
    width=10,
    command=root.destroy
)
exit_button.pack(pady=50)

root.mainloop()