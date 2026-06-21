import tkinter as tk
from tkinter import ttk

def settings():
    root = tk.Tk()
    root.title("Hands-On Sound Settings")
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="Key").grid(column=0, row=0)
    key = tk.StringVar(value="C")
    key_dropdown = ttk.Combobox(
        frm, textvariable=key, values=["C", "D", "E", "G", "A", "B", "F#", "C#", "Ab", "Eb", "Bb", "F"]
    )
    key_dropdown.grid(column=1, row=0)

    mode = tk.StringVar(value="major")
    major_radio = ttk.Radiobutton(
        frm, text="Major", variable=mode, value="major"
    ).grid(column=0, row=2)
    minor_radio = ttk.Radiobutton(
        frm, text="Minor", variable=mode, value="minor"
    ).grid(column=1, row=2)

    settings = {}
    def confirm():
        settings['key'] = key.get()
        settings['mode'] = mode.get()
        root.destroy()

    ttk.Button(frm, text="Confirm", command=confirm).grid(column=0, row=3)
    root.mainloop()
    return settings['key'], settings['mode']