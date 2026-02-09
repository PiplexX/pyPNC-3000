# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║ █▓▒░ Titre        : Interface graphique CNC                                 ░▒▓█ ║
# ║ █▓▒░ Explications : Interface pour commander la CNC                         ░▒▓█ ║
# ║ █▓▒░ Auteur       : Groupe CNC 2026 -> VACHEROT Raphaël                     ░▒▓█ ║
# ║ █▓▒░ Version      : 1.3                                                     ░▒▓█ ║
# ╚══════════════════════════════════════════════════════════════════════════════════╝


# ════════════════════════════════════════════════════════════
#                    IMPORTS & CONFIGURATION
# ════════════════════════════════════════════════════════════

import tkinter as tk
import serial.tools.list_ports
from functools import partial
from tkinter import filedialog
from PIL import Image, ImageTk
from cnc_lib import CNC

Machine = CNC()
fenetre_ports = None


# ════════════════════════════════════════════════════════════
#               FENÊTRE DE CHOIX DU PORT SÉRIE
# ════════════════════════════════════════════════════════════

def ouvrir_menu_ports():
    global fenetre_ports

    if fenetre_ports is not None and fenetre_ports.winfo_exists():
        fenetre_ports.lift()
        return

    fenetre_ports = tk.Toplevel()
    fenetre_ports.title("Choisir un port série")
    fenetre_ports.geometry("300x150")
    fenetre_ports.configure(bg="#E5E5E5")

    ports = [port.device for port in serial.tools.list_ports.comports()]
    if not ports:
        ports = ["Aucun port détecté"]

    port_selectionne = tk.StringVar(fenetre_ports)
    port_selectionne.set(ports[0])

    tk.Label(
        fenetre_ports,
        text="Sélectionnez un port :",
        font=("Arial", 12, "bold"),
        bg="#E5E5E5"
    ).pack(pady=5)

    menu = tk.OptionMenu(fenetre_ports, port_selectionne, *ports)
    menu.config(font=("Arial", 12), width=20)
    menu.pack(pady=5)

    def valider():
        port = port_selectionne.get()
        print("Port choisi :", port)
        Machine.port = port
        Machine.connecter()
        fenetre_ports.destroy()

    tk.Button(
        fenetre_ports,
        text="Valider",
        font=("Arial", 12, "bold"),
        bg="#0047AB",
        fg="white",
        width=12,
        height=1,
        command=valider
    ).pack(pady=10)


# ════════════════════════════════════════════════════════════
#                        MENU PRINCIPAL
# ════════════════════════════════════════════════════════════

def ouvrir_menu_principal():
    global root
    root = tk.Tk()
    root.title("Menu Principal")
    root.geometry("800x400")
    root.configure(bg="#E5E5E5")

    tk.Label(
        root,
        text="MENU PRINCIPAL",
        font=("Arial", 22, "bold"),
        bg="#E5E5E5"
    ).pack(pady=25)

    # Bouton principal
    tk.Button(
        root,
        text="Déplacement Manuelle",
        font=("Arial", 16, "bold"),
        bg="#0047AB",
        fg="white",
        width=20,
        height=2,
        command=ouvrir_fenetre_cnc
    ).place(x=20, y=120)

    # Image Paramètre
    img = Image.open("ParametreIcon.png").resize((70, 60))
    img = ImageTk.PhotoImage(img)
    label_img = tk.Label(root, image=img, bg="#E5E5E5", bd=0, highlightthickness=0)
    label_img.image = img
    label_img.place(x=660, y=15)

    # Bouton port série
    tk.Button(
        root,
        text="Choisir Port Série",
        font=("Arial", 12, "bold"),
        bg="#555555",
        fg="white",
        width=15,
        command=ouvrir_menu_ports
    ).place(x=620, y=100)

    root.mainloop()


# ════════════════════════════════════════════════════════════
#                           FENÊTRE CNC
# ════════════════════════════════════════════════════════════

def ouvrir_fenetre_cnc():
    root.withdraw()

    fenetre = tk.Toplevel()
    fenetre.title("Panneau de Contrôle")
    fenetre.geometry("800x400")
    fenetre.configure(bg="#E5E5E5")

    fenetre.protocol("WM_DELETE_WINDOW", lambda: (fenetre.destroy(), root.deiconify()))

    style_btn = {
        "font": ("Arial", 14, "bold"),
        "bg": "#A0A0A0",
        "fg": "black",
        "width": 5,
        "height": 2,
        "relief": "raised",
        "bd": 4
    }

    # --------- Zone de déplacement ---------
    tk.Button(fenetre, text="▲", command=partial(Machine.avant, 10), **style_btn).place(x=245, y=115)
    tk.Button(fenetre, text="◀", command=partial(Machine.gauche, 10), **style_btn).place(x=170, y=180)
    tk.Button(fenetre, text="▶", command=partial(Machine.droite, 10), **style_btn).place(x=320, y=180)
    tk.Button(fenetre, text="▼", command=partial(Machine.arriere, 10), **style_btn).place(x=245, y=245)

    # --------- Déplacements verticaux ---------
    tk.Button(fenetre, text="▲", command=partial(Machine.haut, 10), **style_btn).place(x=550, y=115)
    tk.Button(fenetre, text="▼", command=partial(Machine.bas, 10), **style_btn).place(x=550, y=240)
    
    # --------- Importer fichier ---------
    tk.Button(
        fenetre,
        text="IMPORTER",
        font=("Arial", 12, "bold"),
        bg="#FF0000",
        fg="white",
        width=10,
        height=2,
        command=lambda: filedialog.askopenfilename()
    ).place(x=675, y=15)

    # --------- HOME ---------
    tk.Button(
        fenetre,
        text="HOME",
        font=("Arial", 12, "bold"),
        bg="#0056b3",
        fg="white",
        width=10,
        height=2,
        command=Machine.home
    ).place(x=15, y=15)

    # --------- Retour menu ---------
    tk.Button(
        fenetre,
        text="Retour Menu",
        font=("Arial", 12, "bold"),
        bg="#1B5E20",
        fg="white",
        width=10,
        height=2,
        command=lambda: (fenetre.destroy(), root.deiconify())
    ).place(x=675, y=330)

    # --------- Gravure / Relever ---------
    tk.Button(
        fenetre,
        text="Gravure",
        font=("Arial", 12, "bold"),
        bg="#464646",
        fg="white",
        width=10,
        height=2,
        command=Machine.position_gravure
    ).place(x=15, y=280)

    tk.Button(
        fenetre,
        text="Relever",
        font=("Arial", 12, "bold"),
        bg="#464646",
        fg="white",
        width=10,
        height=2,
        command=Machine.position_releve
    ).place(x=15, y=330)

    # --------- Images CNC ---------
    image_cnc = Image.open("IconVertical.png").resize((70, 60))
    img_cnc = ImageTk.PhotoImage(image_cnc)
    tk.Label(fenetre, image=img_cnc, bg="#E5E5E5", bd=0, highlightthickness=0).place(x=550, y=180)

    image_cnc2 = Image.open("IconHorizontal.png").resize((70, 60))
    img_cnc2 = ImageTk.PhotoImage(image_cnc2)
    tk.Label(fenetre, image=img_cnc2, bg="#E5E5E5", bd=0, highlightthickness=0).place(x=245, y=180)

    fenetre.img1 = img_cnc
    fenetre.img2 = img_cnc2


# ════════════════════════════════════════════════════════════
#                    LANCEMENT DU PROGRAMME
# ════════════════════════════════════════════════════════════

ouvrir_menu_principal()
