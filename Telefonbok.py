<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import csv
import pygame

contacts = {}

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

pygame.mixer.init()

root = tk.Tk()
root.title("GhostOS Mobile")
root.attributes("-fullscreen", True)
root.configure(bg="black")

current_time = tk.StringVar()

def update_time():
    while True:
        current_time.set(time.strftime("%H:%M"))
        time.sleep(1)

threading.Thread(target=update_time, daemon=True).start()

def fake_call(name, number):
    call_screen = tk.Frame(root, bg="black")
    call_screen.place(relwidth=1, relheight=1)

    tk.Label(
        call_screen,
        text=name,
        fg="white",
        bg="black",
        font=("Arial", 40, "bold")
    ).pack(pady=100)

    tk.Label(
        call_screen,
        text=number,
        fg="gray",
        bg="black",
        font=("Arial", 20)
    ).pack()

    tk.Label(
        call_screen,
        text="Calling...",
        fg="lime",
        bg="black",
        font=("Arial", 20)
    ).pack(pady=20)

    def stop_call():
        pygame.mixer.music.stop()
        call_screen.destroy()

    try:
        pygame.mixer.music.load("ringtone.mp3")
        pygame.mixer.music.play()
    except Exception:
        print("kunde inte spela mp3")

    tk.Button(
        call_screen,
        text="LÄGG PÅ",
        bg="red",
        fg="white",
        font=("Arial", 20, "bold"),
        width=15,
        height=2,
        command=stop_call
    ).pack(side="bottom", pady=80)

def open_ring_menu():
    ring_menu = tk.Frame(root, bg="#000000")
    ring_menu.place(relwidth=1, relheight=1)

    tk.Label(
        ring_menu,
        text="VÄLJ VEM DU VILL RINGA",
        fg="lime",
        bg="black",
        font=("Arial", 25, "bold")
    ).pack(pady=30)

    if not contacts:
        tk.Label(
            ring_menu,
            text="Inga kontakter",
            fg="gray",
            bg="black",
            font=("Arial", 18)
        ).pack()
    else:
        for name, number in contacts.items():
            tk.Button(
                ring_menu,
                text=f"{name} - {number}",
                bg="#222222",
                fg="white",
                font=("Arial", 16),
                width=30,
                command=lambda n=name, num=number: fake_call(n, num)
            ).pack(pady=5)

    tk.Button(
        ring_menu,
        text="BACK",
        bg="red",
        fg="white",
        font=("Arial", 18),
        command=ring_menu.destroy
    ).pack(pady=40)

def open_contacts():
    contacts_screen = tk.Frame(root, bg="#111111")
    contacts_screen.place(relwidth=1, relheight=1)

    tk.Label(
        contacts_screen,
        text="KONTAKTER",
        fg="white",
        bg="#111111",
        font=("Arial", 30, "bold")
    ).pack(pady=20)

    search_var = tk.StringVar()

    tk.Label(
        contacts_screen,
        text="SÖK KONTAKT",
        fg="white",
        bg="#111111",
        font=("Arial", 14, "bold")
    ).pack()

    search_entry = tk.Entry(
        contacts_screen,
        textvariable=search_var,
        font=("Arial", 16),
        width=25,
        fg="black"
    )
    search_entry.pack(pady=10)

    contacts_frame = tk.Frame(contacts_screen, bg="#111111")
    contacts_frame.pack()

    def refresh_contacts():
        for widget in contacts_frame.winfo_children():
            widget.destroy()

        search_text = search_var.get().strip().lower()
        filtered_contacts = {
            name: number
            for name, number in contacts.items()
            if search_text in name.lower() or search_text in number.lower()
        }

        if not contacts:
            tk.Label(
                contacts_frame,
                text="Inga kontakter",
                fg="gray",
                bg="#111111",
                font=("Arial", 20)
            ).pack()
            return

        if not filtered_contacts:
            tk.Label(
                contacts_frame,
                text="Ingen kontakt hittades",
                fg="gray",
                bg="#111111",
                font=("Arial", 20)
            ).pack()
            return

        for name, number in filtered_contacts.items():
            row = tk.Frame(contacts_frame, bg="#111111")
            row.pack(pady=5)

=======
import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import csv
import pygame

contacts = {}

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

pygame.mixer.init()

root = tk.Tk()
root.title("GhostOS Mobile")
root.attributes("-fullscreen", True)
root.configure(bg="black")

current_time = tk.StringVar()

def update_time():
    while True:
        current_time.set(time.strftime("%H:%M"))
        time.sleep(1)

threading.Thread(target=update_time, daemon=True).start()

def fake_call(name, number):
    call_screen = tk.Frame(root, bg="black")
    call_screen.place(relwidth=1, relheight=1)

    tk.Label(
        call_screen,
        text=name,
        fg="white",
        bg="black",
        font=("Arial", 40, "bold")
    ).pack(pady=100)

    tk.Label(
        call_screen,
        text=number,
        fg="gray",
        bg="black",
        font=("Arial", 20)
    ).pack()

    tk.Label(
        call_screen,
        text="Calling...",
        fg="lime",
        bg="black",
        font=("Arial", 20)
    ).pack(pady=20)

    def stop_call():
        pygame.mixer.music.stop()
        call_screen.destroy()

    try:
        pygame.mixer.music.load("ringtone.mp3")
        pygame.mixer.music.play()
    except Exception:
        print("kunde inte spela mp3")

    tk.Button(
        call_screen,
        text="LÄGG PÅ",
        bg="red",
        fg="white",
        font=("Arial", 20, "bold"),
        width=15,
        height=2,
        command=stop_call
    ).pack(side="bottom", pady=80)

def open_ring_menu():
    ring_menu = tk.Frame(root, bg="#000000")
    ring_menu.place(relwidth=1, relheight=1)

    tk.Label(
        ring_menu,
        text="VÄLJ VEM DU VILL RINGA",
        fg="lime",
        bg="black",
        font=("Arial", 25, "bold")
    ).pack(pady=30)

    if not contacts:
        tk.Label(
            ring_menu,
            text="Inga kontakter",
            fg="gray",
            bg="black",
            font=("Arial", 18)
        ).pack()
    else:
        for name, number in contacts.items():
            tk.Button(
                ring_menu,
                text=f"{name} - {number}",
                bg="#222222",
                fg="white",
                font=("Arial", 16),
                width=30,
                command=lambda n=name, num=number: fake_call(n, num)
            ).pack(pady=5)

    tk.Button(
        ring_menu,
        text="BACK",
        bg="red",
        fg="white",
        font=("Arial", 18),
        command=ring_menu.destroy
    ).pack(pady=40)

def open_contacts():
    contacts_screen = tk.Frame(root, bg="#111111")
    contacts_screen.place(relwidth=1, relheight=1)

    tk.Label(
        contacts_screen,
        text="KONTAKTER",
        fg="white",
        bg="#111111",
        font=("Arial", 30, "bold")
    ).pack(pady=20)

    search_var = tk.StringVar()

    tk.Label(
        contacts_screen,
        text="SÖK KONTAKT",
        fg="white",
        bg="#111111",
        font=("Arial", 14, "bold")
    ).pack()

    search_entry = tk.Entry(
        contacts_screen,
        textvariable=search_var,
        font=("Arial", 16),
        width=25,
        fg="black"
    )
    search_entry.pack(pady=10)

    contacts_frame = tk.Frame(contacts_screen, bg="#111111")
    contacts_frame.pack()

    def refresh_contacts():
        for widget in contacts_frame.winfo_children():
            widget.destroy()

        search_text = search_var.get().strip().lower()
        filtered_contacts = {
            name: number
            for name, number in contacts.items()
            if search_text in name.lower() or search_text in number.lower()
        }

        if not contacts:
            tk.Label(
                contacts_frame,
                text="Inga kontakter",
                fg="gray",
                bg="#111111",
                font=("Arial", 20)
            ).pack()
            return

        if not filtered_contacts:
            tk.Label(
                contacts_frame,
                text="Ingen kontakt hittades",
                fg="gray",
                bg="#111111",
                font=("Arial", 20)
            ).pack()
            return

        for name, number in filtered_contacts.items():
            row = tk.Frame(contacts_frame, bg="#111111")
            row.pack(pady=5)

>>>>>>> 9d99c0f560751667e93aa48c6214b92ff1c06520
            tk.Label(
                row,
                text=f"{name} - {number}",
                bg="#222222",
                fg="white",
                font=("Arial", 16),
                width=25,
            ).pack(side="left", padx=5)
<<<<<<< HEAD

            tk.Button(
                row,
                text="❌",
                bg="red",
                fg="white",
                font=("Arial", 12),
                command=lambda n=name: delete_contact_gui(n, refresh_contacts)
            ).pack(side="left")

    search_var.trace_add("write", lambda *args: refresh_contacts())

    add_frame = tk.Frame(contacts_screen, bg="#111111")
    add_frame.pack(pady=25)

    tk.Label(
        add_frame,
        text="LÄGG TILL KONTAKT",
        fg="white",
        bg="#111111",
        font=("Arial", 16, "bold")
    ).pack(pady=5)

    form = tk.Frame(add_frame, bg="#111111")
    form.pack()

    name_entry = tk.Entry(form, font=("Arial", 16), width=20, fg="black")
    name_entry.insert(0, "Namn")
    name_entry.grid(row=0, column=0, padx=5)

    number_entry = tk.Entry(form, font=("Arial", 16), width=20, fg="black")
    number_entry.insert(0, "Nummer")
    number_entry.grid(row=0, column=1, padx=5)

    def clear_name(event):
        if name_entry.get() == "Namn":
            name_entry.delete(0, tk.END)

    def clear_number(event):
        if number_entry.get() == "Nummer":
            number_entry.delete(0, tk.END)

    name_entry.bind("<FocusIn>", clear_name)
    number_entry.bind("<FocusIn>", clear_number)

    def add_contact_gui(event=None):
        name = name_entry.get().strip()
        number = number_entry.get().strip()

        if name == "" or number == "" or name == "Namn" or number == "Nummer":
            messagebox.showerror("Error", "Fyll i båda fälten")
            return

        if name in contacts:
            messagebox.showerror("Error", "Kontakt finns redan")
            return

        contacts[name] = number
        save_to_csv()

        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)

        name_entry.insert(0, "Namn")
        number_entry.insert(0, "Nummer")

        refresh_contacts()

    tk.Button(
        add_frame,
        text="ADD",
        bg="lime",
        fg="black",
        font=("Arial", 14, "bold"),
        width=15,
        command=add_contact_gui
    ).pack(pady=10)

    number_entry.bind("<Return>", add_contact_gui)

    def delete_contact_gui(name, refresh_function):
        if name in contacts:
            del contacts[name]
            save_to_csv()
            refresh_function()

    refresh_contacts()

    tk.Button(
        contacts_screen,
        text="BACK",
        bg="gray",
        fg="white",
        font=("Arial", 18),
        command=contacts_screen.destroy
    ).pack(side="bottom", pady=20)

topbar = tk.Frame(root, bg="#111111", height=50)
topbar.pack(fill="x")

tk.Label(
    topbar,
    textvariable=current_time,
    fg="white",
    bg="#111111",
    font=("Arial", 20)
).pack(side="right", padx=20)

home = tk.Frame(root, bg="black")
home.pack(expand=True)

tk.Label(
    home,
    text="MioOS",
    fg="lime",
    bg="black",
    font=("Arial", 45, "bold")
).pack(pady=50)

tk.Button(
    home,
    text="KONTAKTER",
    bg="#1f1f1f",
    fg="white",
    font=("Arial", 25),
    width=18,
    height=3,
    command=open_contacts
).pack(pady=20)

tk.Button(
    home,
    text="RING KONTAKTER",
    bg="#1f1f1f",
    fg="white",
    font=("Arial", 20),
    width=25,
    height=2,
    command=open_ring_menu
).pack(pady=10)

tk.Button(
    home,
    text=f"TOTALA KONTAKTER: {len(contacts)}",
    bg="#1f1f1f",
    fg="lime",
    font=("Arial", 20),
    width=25,
    height=2
).pack(pady=20)

tk.Button(
    home,
    text="EXIT",
    bg="red",
    fg="white",
    font=("Arial", 20),
    width=10,
    command=root.destroy
).pack(pady=50)

root.mainloop()
=======

            tk.Button(
                row,
                text="❌",
                bg="red",
                fg="white",
                font=("Arial", 12),
                command=lambda n=name: delete_contact_gui(n, refresh_contacts)
            ).pack(side="left")

    search_var.trace_add("write", lambda *args: refresh_contacts())

    add_frame = tk.Frame(contacts_screen, bg="#111111")
    add_frame.pack(pady=25)

    tk.Label(
        add_frame,
        text="LÄGG TILL KONTAKT",
        fg="white",
        bg="#111111",
        font=("Arial", 16, "bold")
    ).pack(pady=5)

    form = tk.Frame(add_frame, bg="#111111")
    form.pack()

    name_entry = tk.Entry(form, font=("Arial", 16), width=20, fg="black")
    name_entry.insert(0, "Namn")
    name_entry.grid(row=0, column=0, padx=5)

    number_entry = tk.Entry(form, font=("Arial", 16), width=20, fg="black")
    number_entry.insert(0, "Nummer")
    number_entry.grid(row=0, column=1, padx=5)

    def clear_name(event):
        if name_entry.get() == "Namn":
            name_entry.delete(0, tk.END)

    def clear_number(event):
        if number_entry.get() == "Nummer":
            number_entry.delete(0, tk.END)

    name_entry.bind("<FocusIn>", clear_name)
    number_entry.bind("<FocusIn>", clear_number)

    def add_contact_gui(event=None):
        name = name_entry.get().strip()
        number = number_entry.get().strip()

        if name == "" or number == "" or name == "Namn" or number == "Nummer":
            messagebox.showerror("Error", "Fyll i båda fälten")
            return

        if name in contacts:
            messagebox.showerror("Error", "Kontakt finns redan")
            return

        contacts[name] = number
        save_to_csv()

        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)

        name_entry.insert(0, "Namn")
        number_entry.insert(0, "Nummer")

        refresh_contacts()

    tk.Button(
        add_frame,
        text="ADD",
        bg="lime",
        fg="black",
        font=("Arial", 14, "bold"),
        width=15,
        command=add_contact_gui
    ).pack(pady=10)

    number_entry.bind("<Return>", add_contact_gui)

    def delete_contact_gui(name, refresh_function):
        if name in contacts:
            del contacts[name]
            save_to_csv()
            refresh_function()

    refresh_contacts()

    tk.Button(
        contacts_screen,
        text="BACK",
        bg="gray",
        fg="white",
        font=("Arial", 18),
        command=contacts_screen.destroy
    ).pack(side="bottom", pady=20)

topbar = tk.Frame(root, bg="#111111", height=50)
topbar.pack(fill="x")

tk.Label(
    topbar,
    textvariable=current_time,
    fg="white",
    bg="#111111",
    font=("Arial", 20)
).pack(side="right", padx=20)

home = tk.Frame(root, bg="black")
home.pack(expand=True)

tk.Label(
    home,
    text="MioOS",
    fg="lime",
    bg="black",
    font=("Arial", 45, "bold")
).pack(pady=50)

tk.Button(
    home,
    text="KONTAKTER",
    bg="#1f1f1f",
    fg="white",
    font=("Arial", 25),
    width=18,
    height=3,
    command=open_contacts
).pack(pady=20)

tk.Button(
    home,
    text="RING KONTAKTER",
    bg="#1f1f1f",
    fg="white",
    font=("Arial", 20),
    width=25,
    height=2,
    command=open_ring_menu
).pack(pady=10)

tk.Button(
    home,
    text=f"TOTALA KONTAKTER: {len(contacts)}",
    bg="#1f1f1f",
    fg="lime",
    font=("Arial", 20),
    width=25,
    height=2
).pack(pady=20)

tk.Button(
    home,
    text="EXIT",
    bg="red",
    fg="white",
    font=("Arial", 20),
    width=10,
    command=root.destroy
).pack(pady=50)

root.mainloop()
>>>>>>> 9d99c0f560751667e93aa48c6214b92ff1c06520
