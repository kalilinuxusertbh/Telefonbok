import csv
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pygame
from PIL import Image, ImageTk


BASE_DIR = Path(__file__).resolve().parent
CONTACTS_FILE = BASE_DIR / "contacts.csv"
RINGTONE_FILE = BASE_DIR / "ringtone.mp3"
ICONS_DIR = BASE_DIR / "assets" / "icons"

contacts = []
next_contact_id = 1
icon_cache = {}


def get_next_contact_id():
    global next_contact_id
    contact_id = str(next_contact_id)
    next_contact_id += 1
    return contact_id


def find_contact(contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    return None


def load_from_csv():
    global next_contact_id
    if not CONTACTS_FILE.exists() or CONTACTS_FILE.stat().st_size == 0:
        return

    with CONTACTS_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = (row.get("Name") or "").strip()
            number = (row.get("Number") or "").strip()

            if name and number:
                contact_id = (row.get("ID") or "").strip() or get_next_contact_id()
                contacts.append(
                    {
                        "id": contact_id,
                        "name": name,
                        "number": number,
                        "email": (row.get("Email") or "").strip(),
                        "tag": (row.get("Tag") or "MioOS kontakt").strip(),
                        "notes": (row.get("Notes") or "").strip(),
                    }
                )
                if contact_id.isdigit():
                    next_contact_id = max(next_contact_id, int(contact_id) + 1)


def save_to_csv():
    with CONTACTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Number", "Email", "Tag", "Notes"])

        for contact in contacts:
            writer.writerow(
                [
                    contact.get("id", ""),
                    contact.get("name", ""),
                    contact.get("number", ""),
                    contact.get("email", ""),
                    contact.get("tag", ""),
                    contact.get("notes", ""),
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
root.configure(bg="black")


def set_start_fullscreen():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.state("zoomed")
    root.attributes("-fullscreen", True)


set_start_fullscreen()

current_time = tk.StringVar()
total_contacts = tk.StringVar()
update_total_contacts()


def update_time():
    while True:
        current_time.set(time.strftime("%H:%M"))
        time.sleep(1)


threading.Thread(target=update_time, daemon=True).start()


def open_placeholder_app(title, subtitle, accent="#6aa9ff"):
    screen = tk.Frame(root, bg="#050505")
    screen.place(relwidth=1, relheight=1)

    status_bar = tk.Frame(screen, bg="#111111", height=52)
    status_bar.pack(fill="x")
    status_bar.pack_propagate(False)

    tk.Label(
        status_bar,
        text=title,
        fg=accent,
        bg="#111111",
        font=("Arial", 14, "bold"),
    ).pack(side="left", padx=20, pady=10)

    tk.Label(
        status_bar,
        textvariable=current_time,
        fg="white",
        bg="#111111",
        font=("Arial", 16, "bold"),
    ).pack(side="right", padx=20, pady=10)

    content = tk.Frame(screen, bg="#050505")
    content.pack(fill="both", expand=True, padx=54, pady=36)

    tk.Label(
        content,
        text=title,
        fg="white",
        bg="#050505",
        font=("Arial", 36, "bold"),
    ).pack(anchor="w")

    tk.Label(
        content,
        text=subtitle,
        fg="#8c8c8c",
        bg="#050505",
        font=("Arial", 14),
    ).pack(anchor="w", pady=(8, 0))

    tk.Label(
        content,
        text="bara för att det coolt ut",
        fg=accent,
        bg="#050505",
        font=("Arial", 14, "bold"),
    ).pack(anchor="w", pady=(28, 0))

    tk.Button(
        screen,
        text="BACK",
        bg="#2f2f2f",
        fg="white",
        font=("Arial", 18),
        command=screen.destroy,
    ).pack(side="bottom", pady=26)


def load_icon(filename, size=(120, 120)):
    cache_key = (filename, size)
    if cache_key in icon_cache:
        return icon_cache[cache_key]

    icon_path = ICONS_DIR / filename
    if not icon_path.exists():
        return None

    image = Image.open(icon_path).convert("RGBA")
    image = image.resize(size, Image.Resampling.LANCZOS)
    icon_cache[cache_key] = ImageTk.PhotoImage(image)
    return icon_cache[cache_key]


def fake_call(name, number):
    call_screen = tk.Frame(root, bg="#050505")
    call_screen.place(relwidth=1, relheight=1)

    status_bar = tk.Frame(call_screen, bg="#111111", height=52)
    status_bar.pack(fill="x")
    status_bar.pack_propagate(False)

    tk.Label(
        status_bar,
        text="MioOS Phone",
        fg="lime",
        bg="#111111",
        font=("Arial", 14, "bold"),
    ).pack(side="left", padx=20, pady=10)

    tk.Label(
        status_bar,
        textvariable=current_time,
        fg="white",
        bg="#111111",
        font=("Arial", 16, "bold"),
    ).pack(side="right", padx=20, pady=10)

    call_body = tk.Frame(call_screen, bg="#050505")
    call_body.pack(fill="both", expand=True, padx=60, pady=24)

    tk.Label(
        call_body,
        text="UTGÅENDE SAMTAL",
        fg="lime",
        bg="#050505",
        font=("Arial", 15, "bold"),
    ).pack(pady=(10, 18))

    avatar_shell = tk.Frame(call_body, bg="#0f0f0f", bd=1, relief="solid")
    avatar_shell.pack(pady=(6, 18))

    tk.Label(
        avatar_shell,
        text=name[:1].upper() if name else "?",
        fg="black",
        bg="lime",
        font=("Arial", 48, "bold"),
        width=5,
        height=2,
    ).pack(padx=18, pady=18)

    tk.Label(
        call_body,
        text=name,
        fg="white",
        bg="#050505",
        font=("Arial", 34, "bold"),
    ).pack()

    tk.Label(
        call_body,
        text=number or "Okänt nummer",
        fg="#8a8a8a",
        bg="#050505",
        font=("Arial", 20),
    ).pack(pady=(8, 12))

    call_status = tk.StringVar(value="Ringer...")
    call_timer = tk.StringVar(value="00:00")
    call_state = {"connected": False, "seconds": 0, "after_id": None}

    tk.Label(
        call_body,
        textvariable=call_status,
        fg="#d6ffd6",
        bg="#050505",
        font=("Arial", 16, "bold"),
    ).pack()

    tk.Label(
        call_body,
        textvariable=call_timer,
        fg="#8a8a8a",
        bg="#050505",
        font=("Arial", 18),
    ).pack(pady=(6, 22))

    controls = tk.Frame(call_body, bg="#050505")
    controls.pack(pady=(8, 26))

    mute_state = tk.StringVar(value="MUTE")
    speaker_state = tk.StringVar(value="HÖGTALARE")

    def update_timer():
        if not call_state["connected"]:
            return
        minutes = call_state["seconds"] // 60
        seconds = call_state["seconds"] % 60
        call_timer.set(f"{minutes:02d}:{seconds:02d}")
        call_state["seconds"] += 1
        call_state["after_id"] = call_screen.after(1000, update_timer)

    def connect_call():
        call_state["connected"] = True
        call_state["seconds"] = 0
        call_status.set("Ansluten")
        update_timer()

    def toggle_mute():
        mute_state.set("UNMUTE" if mute_state.get() == "MUTE" else "MUTE")

    def toggle_speaker():
        speaker_state.set(
            "HOGTALARE AV" if speaker_state.get() == "HÖGTALARE" else "HÖGTALARE"
        )

    def open_keypad():
        messagebox.showinfo(
            "Knappsats",
            "fake knapp lol",
        )

    def stop_call():
        if call_state["after_id"] is not None:
            call_screen.after_cancel(call_state["after_id"])
        stop_ringtone()
        call_screen.destroy()

    def make_control(parent, textvariable=None, text=None, command=None, bg="#171717"):
        return tk.Button(
            parent,
            text=text,
            textvariable=textvariable,
            command=command,
            bg=bg,
            fg="white",
            activebackground="#262626",
            activeforeground="white",
            relief="flat",
            font=("Arial", 13, "bold"),
            width=14,
            height=2,
        )

    make_control(controls, textvariable=mute_state, command=toggle_mute).grid(
        row=0, column=0, padx=10, pady=10
    )
    make_control(
        controls, textvariable=speaker_state, command=toggle_speaker
    ).grid(row=0, column=1, padx=10, pady=10)
    make_control(controls, text="KNAPPSATS", command=open_keypad).grid(
        row=1, column=0, padx=10, pady=10
    )
    make_control(controls, text="KONTAKTINFO", bg="#102410").grid(
        row=1, column=1, padx=10, pady=10
    )
    make_control(
        controls,
        text="LÄGG PÅ",
        command=stop_call,
        bg="#7a1010",
    ).grid(row=2, column=0, columnspan=2, padx=10, pady=(18, 0), sticky="ew")

    play_ringtone()
    call_screen.after(2200, connect_call)


def open_ring_menu():
    ring_menu = tk.Frame(root, bg="#050505")
    ring_menu.place(relwidth=1, relheight=1)

    status_bar = tk.Frame(ring_menu, bg="#111111", height=52)
    status_bar.pack(fill="x")
    status_bar.pack_propagate(False)

    tk.Label(
        status_bar,
        text="Ring kontakter",
        fg="lime",
        bg="#111111",
        font=("Arial", 14, "bold"),
    ).pack(side="left", padx=20, pady=10)

    tk.Label(
        status_bar,
        textvariable=current_time,
        fg="white",
        bg="#111111",
        font=("Arial", 16, "bold"),
    ).pack(side="right", padx=20, pady=10)

    header = tk.Frame(ring_menu, bg="#050505")
    header.pack(fill="x", padx=44, pady=(26, 18))

    tk.Label(
        header,
        text="MioOS // Telefon",
        fg="lime",
        bg="#050505",
        font=("Arial", 13, "bold"),
    ).pack(anchor="w")

    tk.Label(
        header,
        text="RING KONTAKTER",
        fg="white",
        bg="#050505",
        font=("Arial", 34, "bold"),
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Välj en kontakt för att starta ett samtal.",
        fg="#8c8c8c",
        bg="#050505",
        font=("Arial", 13),
    ).pack(anchor="w", pady=(2, 0))

    contacts_shell = tk.Frame(ring_menu, bg="#101010", bd=1, relief="solid")
    contacts_shell.pack(fill="both", expand=True, padx=44, pady=(0, 24))

    tk.Label(
        contacts_shell,
        text="SNABBVAL",
        fg="#d8d8d8",
        bg="#101010",
        font=("Arial", 16, "bold"),
    ).pack(anchor="w", padx=18, pady=(18, 10))

    contacts_list = tk.Frame(contacts_shell, bg="#101010")
    contacts_list.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    if not contacts:
        tk.Label(
            contacts_list,
            text="Inga kontakter att ringa",
            fg="gray",
            bg="#101010",
            font=("Arial", 18),
        ).pack(pady=40)
    else:
        for contact in contacts:
            name = contact.get("name", "")
            number = contact.get("number", "")
            tag = contact.get("tag", "MioOS kontakt")
            card = tk.Frame(contacts_list, bg="#181818", bd=1, relief="solid")
            card.pack(fill="x", pady=6)

            tk.Label(
                card,
                text=name[:1].upper() if name else "?",
                bg="lime",
                fg="black",
                font=("Arial", 18, "bold"),
                width=3,
            ).pack(side="left", padx=(12, 14), pady=12)

            info = tk.Frame(card, bg="#181818")
            info.pack(side="left", fill="x", expand=True, pady=10)

            tk.Label(
                info,
                text=name,
                fg="white",
                bg="#181818",
                font=("Arial", 16, "bold"),
                anchor="w",
            ).pack(anchor="w")

            tk.Label(
                info,
                text=number or "Saknar nummer",
                fg="#a2a2a2",
                bg="#181818",
                font=("Arial", 12),
                anchor="w",
            ).pack(anchor="w")

            tk.Label(
                info,
                text=tag,
                fg="lime",
                bg="#181818",
                font=("Arial", 10, "bold"),
                anchor="w",
            ).pack(anchor="w", pady=(4, 0))

            tk.Button(
                card,
                text="RING",
                bg="#203420",
                fg="lime",
                activebackground="#2b482b",
                activeforeground="white",
                font=("Arial", 12, "bold"),
                width=10,
                command=lambda n=name, num=number: fake_call(n, num),
            ).pack(side="right", padx=14, pady=14)

    tk.Button(
        ring_menu,
        text="BACK",
        bg="#2f2f2f",
        fg="white",
        font=("Arial", 18),
        command=ring_menu.destroy,
    ).pack(pady=(0, 26))


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
        text="SOK",
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

    def select_contact(contact_id):
        contact = find_contact(contact_id)
        if not contact:
            return

        name = contact.get("name", "")
        selected_contact.set(contact_id)
        set_entry(fields["name"], name)
        set_entry(fields["number"], contact.get("number", ""))
        set_entry(fields["email"], contact.get("email", ""))
        set_entry(fields["tag"], contact.get("tag", ""))
        set_entry(fields["notes"], contact.get("notes", ""))
        avatar_label.config(text=name[:1].upper() or "?")
        profile_name.config(text=name)
        profile_tag.config(text=contact.get("tag", "MioOS kontakt"))

    def delete_selected():
        contact_id = selected_contact.get()
        if not contact_id:
            messagebox.showerror("Error", "Valj en kontakt att ta bort")
            return

        contact = find_contact(contact_id)
        if contact:
            contacts.remove(contact)
            save_to_csv()
            update_total_contacts()
            clear_form()
            refresh_contacts()

    def call_selected():
        contact_id = selected_contact.get()
        if not contact_id:
            messagebox.showerror("Error", "Valj en kontakt att ringa")
            return

        contact = find_contact(contact_id)
        if not contact:
            return

        fake_call(contact.get("name", ""), contact.get("number", ""))

    def save_contact_gui(event=None):
        contact_id = selected_contact.get()
        existing_contact = find_contact(contact_id) if contact_id else None
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

        if existing_contact:
            existing_contact["name"] = name
            existing_contact["number"] = number
            existing_contact["email"] = email
            existing_contact["tag"] = tag or "MioOS kontakt"
            existing_contact["notes"] = notes
        else:
            contact_id = get_next_contact_id()
            contacts.append(
                {
                    "id": contact_id,
                    "name": name,
                    "number": number,
                    "email": email,
                    "tag": tag or "MioOS kontakt",
                    "notes": notes,
                }
            )

        selected_contact.set(contact_id)
        save_to_csv()
        update_total_contacts()
        select_contact(contact_id)
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
        filtered_contacts = [
            contact
            for contact in contacts
            if search_text in contact.get("name", "").lower()
            or search_text in contact.get("number", "").lower()
            or search_text in contact.get("email", "").lower()
            or search_text in contact.get("tag", "").lower()
        ]

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

        for contact in filtered_contacts:
            contact_id = contact.get("id", "")
            name = contact.get("name", "")
            row = tk.Frame(contacts_frame, bg="#181818", bd=1, relief="solid")
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=(name[:1].upper() if name else "?"),
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

            email = contact.get("email", "") or "ingen mail"
            tk.Label(
                info,
                text=f"{contact.get('number', '')}  |  {email}",
                fg="#9d9d9d",
                bg="#181818",
                font=("Arial", 11),
                anchor="w",
            ).pack(anchor="w")

            tk.Label(
                row,
                text=contact.get("tag", "MioOS kontakt"),
                fg="lime",
                bg="#181818",
                font=("Arial", 10, "bold"),
            ).pack(side="right", padx=12)

            row.bind("<Button-1>", lambda event, cid=contact_id: select_contact(cid))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda event, cid=contact_id: select_contact(cid))

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
    text="4G  |  WiFi  |  67%",
    fg="#a4fca4",
    bg="#111111",
    font=("Arial", 12, "bold"),
).pack(side="left", padx=20)

tk.Label(
    topbar,
    textvariable=current_time,
    fg="white",
    bg="#111111",
    font=("Arial", 20),
).pack(side="right", padx=20)

home = tk.Frame(root, bg="black")
home.pack(fill="both", expand=True)

wallpaper = tk.Frame(home, bg="black")
wallpaper.pack(fill="both", expand=True, padx=26, pady=(18, 24))

hero = tk.Frame(wallpaper, bg="black")
hero.pack(fill="x", pady=(8, 24))

tk.Label(
    hero,
    text="MioOS",
    fg="lime",
    bg="black",
    font=("Arial", 45, "bold"),
).pack(anchor="w")

tk.Label(
    hero,
    text="Telefonen är redo. Öppna appar fran hemskärmen.",
    fg="#7f7f7f",
    bg="black",
    font=("Arial", 14),
).pack(anchor="w", pady=(4, 0))

summary_card = tk.Frame(wallpaper, bg="#101010", bd=1, relief="solid")
summary_card.pack(fill="x", pady=(0, 22))

tk.Label(
    summary_card,
    text="SYSTEMÖVERSIKT",
    fg="lime",
    bg="#101010",
    font=("Arial", 12, "bold"),
).pack(anchor="w", padx=18, pady=(14, 4))

tk.Label(
    summary_card,
    textvariable=total_contacts,
    fg="white",
    bg="#101010",
    font=("Arial", 24, "bold"),
).pack(anchor="w", padx=18, pady=(0, 14))

app_grid = tk.Frame(wallpaper, bg="black")
app_grid.pack(fill="both", expand=True)
app_grid.columnconfigure(0, weight=1)
app_grid.columnconfigure(1, weight=1)
app_grid.rowconfigure(0, weight=1)
app_grid.rowconfigure(1, weight=1)


def create_home_icon(parent, row, column, icon_file, label, command):
    card = tk.Frame(parent, bg="#141414", bd=1, relief="solid")
    card.grid(row=row, column=column, sticky="nsew", padx=14, pady=14)

    icon_image = load_icon(icon_file)

    tk.Button(
        card,
        image=icon_image,
        command=command,
        bg="#141414",
        activebackground="#141414",
        relief="flat",
        bd=0,
        highlightthickness=0,
    ).pack(pady=(20, 12))

    tk.Label(
        card,
        text=label,
        fg="white",
        bg="#141414",
        font=("Arial", 15, "bold"),
    ).pack()

    tk.Label(
        card,
        text="Tryck for att oppna",
        fg="#8c8c8c",
        bg="#141414",
        font=("Arial", 11),
    ).pack(pady=(4, 18))


create_home_icon(app_grid, 0, 0, "phone_ios.png", "Telefon", open_ring_menu)
create_home_icon(app_grid, 0, 1, "contacts_ios.png", "Kontakter", open_contacts)
create_home_icon(
    app_grid,
    1,
    0,
    "messages_ios.png",
    "Meddelanden",
    lambda: open_placeholder_app("Meddelanden", "Konversationer och notiser.", "#7fb6ff"),
)
create_home_icon(
    app_grid,
    1,
    1,
    "settings_ios.png",
    "Installningar",
    lambda: open_placeholder_app("Inställningar", "System, ljud och visning.", "#ffd36c"),
)

dock = tk.Frame(wallpaper, bg="#111111", bd=1, relief="solid")
dock.pack(fill="x", pady=(18, 0))

tk.Button(
    dock,
    text="Telefon",
    bg="#111111",
    fg="lime",
    activebackground="#1f1f1f",
    activeforeground="white",
    relief="flat",
    font=("Arial", 14, "bold"),
    command=open_ring_menu,
).pack(side="left", expand=True, fill="x", padx=12, pady=14)

tk.Button(
    dock,
    text="Kontakter",
    bg="#111111",
    fg="white",
    activebackground="#1f1f1f",
    activeforeground="white",
    relief="flat",
    font=("Arial", 14, "bold"),
    command=open_contacts,
).pack(side="left", expand=True, fill="x", padx=12, pady=14)

tk.Button(
    dock,
    text="Hem",
    bg="#111111",
    fg="#9e9e9e",
    activebackground="#1f1f1f",
    activeforeground="white",
    relief="flat",
    font=("Arial", 14, "bold"),
).pack(side="left", expand=True, fill="x", padx=12, pady=14)

tk.Button(
    dock,
    text="Stang",
    bg="#111111",
    fg="#ff8f8f",
    activebackground="#1f1f1f",
    activeforeground="white",
    relief="flat",
    font=("Arial", 14, "bold"),
    command=root.destroy,
).pack(side="left", expand=True, fill="x", padx=12, pady=14)

root.mainloop()
