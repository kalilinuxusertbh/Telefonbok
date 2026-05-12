import csv
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pygame


BASE_DIR = Path(__file__).resolve().parent
CONTACTS_FILE = BASE_DIR / "contacts.csv"
RINGTONE_FILE = BASE_DIR / "ringtone.mp3"

contacts = {}


def load_from_csv():
    if not CONTACTS_FILE.exists() or CONTACTS_FILE.stat().st_size == 0:
        return

    with CONTACTS_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = (row.get("Name") or "").strip()
            number = (row.get("Number") or "").strip()

            if name and number:
                contacts[name] = {
                    "number": number,
                    "email": (row.get("Email") or "").strip(),
                    "tag": (row.get("Tag") or "MioOS kontakt").strip(),
                    "notes": (row.get("Notes") or "").strip(),
                }


def save_to_csv():
    with CONTACTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Number", "Email", "Tag", "Notes"])

        for name, details in contacts.items():
            writer.writerow(
                [
                    name,
                    details.get("number", ""),
                    details.get("email", ""),
                    details.get("tag", ""),
                    details.get("notes", ""),
                ]
            )


def update_total_contacts():
    total_contacts.set(f"TOTALA KONTAKTER: {len(contacts)}")


def play_ringtone():
    if not pygame.mixer.get_init() or not RINGTONE_FILE.exists():
        return

    try:
        pygame.mixer.music.load(str(RINGTONE_FILE))
        pygame.mixer.music.play()
    except pygame.error:
        print("Kunde inte spela mp3")


def stop_ringtone():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


load_from_csv()

try:
    pygame.mixer.init()
except pygame.error:
    print("Kunde inte starta ljud")

root = tk.Tk()
root.title("GhostOS Mobile")
root.attributes("-fullscreen", True)
root.configure(bg="black")

current_time = tk.StringVar()
total_contacts = tk.StringVar()
update_total_contacts()


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
        font=("Arial", 40, "bold"),
    ).pack(pady=100)

    tk.Label(
        call_screen,
        text=number,
        fg="gray",
        bg="black",
        font=("Arial", 20),
    ).pack()

    tk.Label(
        call_screen,
        text="Calling...",
        fg="lime",
        bg="black",
        font=("Arial", 20),
    ).pack(pady=20)

    def stop_call():
        stop_ringtone()
        call_screen.destroy()

    play_ringtone()

    tk.Button(
        call_screen,
        text="LÄGG PÅ",
        bg="red",
        fg="white",
        font=("Arial", 20, "bold"),
        width=15,
        height=2,
        command=stop_call,
    ).pack(side="bottom", pady=80)


def open_ring_menu():
    ring_menu = tk.Frame(root, bg="#000000")
    ring_menu.place(relwidth=1, relheight=1)

    tk.Label(
        ring_menu,
        text="VÄLJ VEM DU VILL RINGA",
        fg="lime",
        bg="black",
        font=("Arial", 25, "bold"),
    ).pack(pady=30)

    if not contacts:
        tk.Label(
            ring_menu,
            text="Inga kontakter",
            fg="gray",
            bg="black",
            font=("Arial", 18),
        ).pack()
    else:
        for name, details in contacts.items():
            number = details.get("number", "")
            tk.Button(
                ring_menu,
                text=f"{name} - {number}",
                bg="#222222",
                fg="white",
                font=("Arial", 16),
                width=30,
                command=lambda n=name, num=number: fake_call(n, num),
            ).pack(pady=5)

    tk.Button(
        ring_menu,
        text="BACK",
        bg="red",
        fg="white",
        font=("Arial", 18),
        command=ring_menu.destroy,
    ).pack(pady=40)


def open_contacts():
    contacts_screen = tk.Frame(root, bg="#050505")
    contacts_screen.place(relwidth=1, relheight=1)

    header = tk.Frame(contacts_screen, bg="#050505")
    header.pack(fill="x", padx=44, pady=(26, 12))

    tk.Label(
        header,
        text="MioOS // Kontakter",
        fg="lime",
        bg="#050505",
        font=("Arial", 13, "bold"),
    ).pack(anchor="w")

    tk.Label(
        header,
        text="KONTAKTBOK",
        fg="white",
        bg="#050505",
        font=("Arial", 34, "bold"),
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Spara nummer, mail och detaljer.",
        fg="#8c8c8c",
        bg="#050505",
        font=("Arial", 13),
    ).pack(anchor="w", pady=(2, 0))

    tk.Label(
        header,
        textvariable=total_contacts,
        fg="lime",
        bg="#050505",
        font=("Arial", 13, "bold"),
    ).pack(anchor="e")

    body = tk.Frame(contacts_screen, bg="#050505")
    body.pack(fill="both", expand=True, padx=44, pady=10)

    left_panel = tk.Frame(body, bg="#101010", bd=1, relief="solid")
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 12))

    right_panel = tk.Frame(body, bg="#151515", bd=1, relief="solid", width=430)
    right_panel.pack(side="right", fill="y")
    right_panel.pack_propagate(False)

    tk.Label(
        left_panel,
        text="SYSTEMREGISTER",
        fg="#d8d8d8",
        bg="#101010",
        font=("Arial", 16, "bold"),
    ).pack(anchor="w", padx=18, pady=(16, 4))

    search_var = tk.StringVar()
    selected_contact = tk.StringVar()

    search_shell = tk.Frame(left_panel, bg="#1d1d1d")
    search_shell.pack(fill="x", padx=18, pady=(6, 12))

    tk.Label(
        search_shell,
        text="SÖK",
        fg="lime",
        bg="#1d1d1d",
        font=("Arial", 11, "bold"),
    ).pack(side="left", padx=(12, 8), pady=10)

    search_entry = tk.Entry(
        search_shell,
        textvariable=search_var,
        font=("Arial", 14),
        fg="white",
        bg="#1d1d1d",
        insertbackground="lime",
        relief="flat",
    )
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 12), pady=10)

    contacts_frame = tk.Frame(left_panel, bg="#101010")
    contacts_frame.pack(fill="both", expand=True, padx=18, pady=(0, 14))

    profile_header = tk.Frame(right_panel, bg="#151515")
    profile_header.pack(fill="x", padx=22, pady=(20, 8))

    avatar_label = tk.Label(
        profile_header,
        text="?",
        fg="black",
        bg="lime",
        font=("Arial", 34, "bold"),
        width=3,
        height=1,
    )
    avatar_label.pack(side="left", padx=(0, 14))

    title_stack = tk.Frame(profile_header, bg="#151515")
    title_stack.pack(side="left", fill="x", expand=True)

    profile_name = tk.Label(
        title_stack,
        text="Ny kontakt",
        fg="white",
        bg="#151515",
        font=("Arial", 23, "bold"),
        anchor="w",
    )
    profile_name.pack(anchor="w")

    profile_tag = tk.Label(
        title_stack,
        text="MioOS identitet",
        fg="#8f8f8f",
        bg="#151515",
        font=("Arial", 12),
        anchor="w",
    )
    profile_tag.pack(anchor="w")

    form = tk.Frame(right_panel, bg="#151515")
    form.pack(fill="both", expand=True, padx=22, pady=8)
    form.columnconfigure(0, weight=1)
    form.rowconfigure(9, weight=1)

    fields = {}
    placeholders = {
        "name": "Namn",
        "number": "Nummer",
        "email": "mail@exempel.se",
        "tag": "Familj, kompis, jobb...",
        "notes": "Sma detaljer som MioOS ska komma ihag.",
    }

    def make_field(label, placeholder, row, height=1):
        tk.Label(
            form,
            text=label,
            fg="lime",
            bg="#151515",
            font=("Arial", 11, "bold"),
        ).grid(row=row, column=0, sticky="w", pady=(10, 3))

        if height == 1:
            entry = tk.Entry(
                form,
                font=("Arial", 14),
                fg="white",
                bg="#222222",
                insertbackground="lime",
                relief="flat",
            )
            entry.insert(0, placeholder)
            entry.grid(row=row + 1, column=0, sticky="ew", ipady=8)
        else:
            entry = tk.Text(
                form,
                font=("Arial", 13),
                fg="white",
                bg="#222222",
                insertbackground="lime",
                relief="flat",
                height=height,
                wrap="word",
            )
            entry.insert("1.0", placeholder)
            entry.grid(row=row + 1, column=0, sticky="nsew")

        return entry

    fields["name"] = make_field("NAMN", placeholders["name"], 0)
    fields["number"] = make_field("NUMMER", placeholders["number"], 2)
    fields["email"] = make_field("MAIL", placeholders["email"], 4)
    fields["tag"] = make_field("SYSTEMTAGG", placeholders["tag"], 6)
    fields["notes"] = make_field("ANTECKNINGAR", placeholders["notes"], 8, height=5)

    def entry_value(widget):
        if isinstance(widget, tk.Text):
            return widget.get("1.0", tk.END).strip()
        return widget.get().strip()

    def set_entry(widget, value):
        if isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
            widget.insert("1.0", value)
        else:
            widget.delete(0, tk.END)
            widget.insert(0, value)

    def clear_form():
        selected_contact.set("")
        for key, placeholder in placeholders.items():
            set_entry(fields[key], placeholder)
        avatar_label.config(text="?", bg="lime")
        profile_name.config(text="Ny kontakt")
        profile_tag.config(text="MioOS identitet")

    def select_contact(name):
        details = contacts[name]
        selected_contact.set(name)
        set_entry(fields["name"], name)
        set_entry(fields["number"], details.get("number", ""))
        set_entry(fields["email"], details.get("email", ""))
        set_entry(fields["tag"], details.get("tag", ""))
        set_entry(fields["notes"], details.get("notes", ""))
        avatar_label.config(text=name[:1].upper() or "?")
        profile_name.config(text=name)
        profile_tag.config(text=details.get("tag", "MioOS kontakt"))

    def delete_selected():
        name = selected_contact.get()
        if not name:
            messagebox.showerror("Error", "Valj en kontakt att ta bort")
            return

        if name in contacts:
            del contacts[name]
            save_to_csv()
            update_total_contacts()
            clear_form()
            refresh_contacts()

    def call_selected():
        name = selected_contact.get()
        if not name:
            messagebox.showerror("Error", "Valj en kontakt att ringa")
            return

        number = contacts.get(name, {}).get("number", "")
        fake_call(name, number)

    def save_contact_gui(event=None):
        old_name = selected_contact.get()
        name = entry_value(fields["name"])
        number = entry_value(fields["number"])
        email = entry_value(fields["email"])
        tag = entry_value(fields["tag"])
        notes = entry_value(fields["notes"])

        if name in ("", placeholders["name"]) or number in ("", placeholders["number"]):
            messagebox.showerror("Error", "Namn och nummer behovs")
            return

        if email == placeholders["email"]:
            email = ""
        if tag == placeholders["tag"]:
            tag = "MioOS kontakt"
        if notes == placeholders["notes"]:
            notes = ""

        if old_name and old_name != name:
            contacts.pop(old_name, None)

        if not old_name and name in contacts:
            messagebox.showerror("Error", "Kontakt finns redan")
            return

        contacts[name] = {
            "number": number,
            "email": email,
            "tag": tag or "MioOS kontakt",
            "notes": notes,
        }

        selected_contact.set(name)
        save_to_csv()
        update_total_contacts()
        select_contact(name)
        refresh_contacts()

    button_row = tk.Frame(right_panel, bg="#151515")
    button_row.pack(fill="x", padx=22, pady=(0, 22))

    tk.Button(
        button_row,
        text="NY",
        bg="#2f2f2f",
        fg="white",
        font=("Arial", 12, "bold"),
        width=9,
        command=clear_form,
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_row,
        text="SPARA",
        bg="lime",
        fg="black",
        font=("Arial", 12, "bold"),
        width=10,
        command=save_contact_gui,
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_row,
        text="RING",
        bg="#202d20",
        fg="lime",
        font=("Arial", 12, "bold"),
        width=9,
        command=call_selected,
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_row,
        text="RADERA",
        bg="#421818",
        fg="white",
        font=("Arial", 12, "bold"),
        width=10,
        command=delete_selected,
    ).pack(side="left")

    def refresh_contacts():
        for widget in contacts_frame.winfo_children():
            widget.destroy()

        search_text = search_var.get().strip().lower()
        filtered_contacts = {
            name: details
            for name, details in contacts.items()
            if search_text in name.lower()
            or search_text in details.get("number", "").lower()
            or search_text in details.get("email", "").lower()
            or search_text in details.get("tag", "").lower()
        }

        if not contacts:
            tk.Label(
                contacts_frame,
                text="Inga kontakter i systemet",
                fg="#777777",
                bg="#101010",
                font=("Arial", 18),
            ).pack(pady=40)
            return

        if not filtered_contacts:
            tk.Label(
                contacts_frame,
                text="Ingen kontakt hittades",
                fg="#777777",
                bg="#101010",
                font=("Arial", 18),
            ).pack(pady=40)
            return

        for name, details in filtered_contacts.items():
            row = tk.Frame(contacts_frame, bg="#181818", bd=1, relief="solid")
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=name[:1].upper(),
                bg="lime",
                fg="black",
                font=("Arial", 18, "bold"),
                width=3,
            ).pack(side="left", fill="y", padx=(10, 12), pady=10)

            info = tk.Frame(row, bg="#181818")
            info.pack(side="left", fill="x", expand=True, pady=9)

            tk.Label(
                info,
                text=name,
                fg="white",
                bg="#181818",
                font=("Arial", 15, "bold"),
                anchor="w",
            ).pack(anchor="w")

            email = details.get("email", "") or "ingen mail"
            tk.Label(
                info,
                text=f"{details.get('number', '')}  |  {email}",
                fg="#9d9d9d",
                bg="#181818",
                font=("Arial", 11),
                anchor="w",
            ).pack(anchor="w")

            tk.Label(
                row,
                text=details.get("tag", "MioOS kontakt"),
                fg="lime",
                bg="#181818",
                font=("Arial", 10, "bold"),
            ).pack(side="right", padx=12)

            row.bind("<Button-1>", lambda event, n=name: select_contact(n))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda event, n=name: select_contact(n))

    search_var.trace_add("write", lambda *args: refresh_contacts())
    fields["number"].bind("<Return>", save_contact_gui)
    fields["email"].bind("<Return>", save_contact_gui)

    refresh_contacts()

    tk.Button(
        contacts_screen,
        text="BACK",
        bg="#2f2f2f",
        fg="white",
        font=("Arial", 18),
        command=contacts_screen.destroy,
    ).pack(side="bottom", pady=20)


topbar = tk.Frame(root, bg="#111111", height=50)
topbar.pack(fill="x")

tk.Label(
    topbar,
    textvariable=current_time,
    fg="white",
    bg="#111111",
    font=("Arial", 20),
).pack(side="right", padx=20)

home = tk.Frame(root, bg="black")
home.pack(expand=True)

tk.Label(
    home,
    text="MioOS",
    fg="lime",
    bg="black",
    font=("Arial", 45, "bold"),
).pack(pady=50)

tk.Button(
    home,
    text="KONTAKTER",
    bg="#1f1f1f",
    fg="white",
    font=("Arial", 25),
    width=18,
    height=3,
    command=open_contacts,
).pack(pady=20)

tk.Button(
    home,
    text="RING KONTAKTER",
    bg="#1f1f1f",
    fg="white",
    font=("Arial", 20),
    width=25,
    height=2,
    command=open_ring_menu,
).pack(pady=10)

tk.Button(
    home,
    textvariable=total_contacts,
    bg="#1f1f1f",
    fg="lime",
    font=("Arial", 20),
    width=25,
    height=2,
).pack(pady=20)

tk.Button(
    home,
    text="EXIT",
    bg="red",
    fg="white",
    font=("Arial", 20),
    width=10,
    command=root.destroy,
).pack(pady=50)

root.mainloop()
