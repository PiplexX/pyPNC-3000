#Owner : PiplexX, CNC project 2026 BTS CIEL Loritz

import pygame
from cnc_lib import CNC

pygame.init()
MaCNC = CNC()

# --- gamepad init ---
liste_manettes = []
for i in range(pygame.joystick.get_count()):
    liste_manettes.append(pygame.joystick.Joystick(i))
    print(f"Manette détectée : '{liste_manettes[-1].get_name()}'")

if not liste_manettes:
    print("ERREUR: FONCTION=INIT, PROBLEME=AUCUNE MANETTE DETECTEE")
    pygame.quit()
    exit()

manette = liste_manettes[0]

DEADZONE = 0.2
pas_mm = 0.5
vitesse_cnc = 22
MaCNC.regler_vitesse(vitesse_cnc)

clock = pygame.time.Clock()
en_cours = True

while en_cours:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:     # A — tool down
                MaCNC.position_gravure()
            elif event.button == 1:   # B — tool up
                MaCNC.position_releve()
            elif event.button == 3:   # Y — back to home
                MaCNC.home()
            elif event.button == 4:   # LB — speed -2
                vitesse_cnc = max(1, vitesse_cnc - 2)
                MaCNC.regler_vitesse(vitesse_cnc)
                print(f"INFO: vitesse réglée à {vitesse_cnc}")
            elif event.button == 5:   # RB — speed +2
                vitesse_cnc = min(50, vitesse_cnc + 2)
                MaCNC.regler_vitesse(vitesse_cnc)
                print(f"INFO: vitesse réglée à {vitesse_cnc}")
            elif event.button == 7:
                en_cours = False

    axe_x = manette.get_axis(0)  # left stick X
    axe_y = manette.get_axis(1)  # left stick Y
    axe_z = manette.get_axis(4)  # right stick Y

    x_actif = abs(axe_x) > DEADZONE
    y_actif = abs(axe_y) > DEADZONE

    if x_actif and y_actif:
        if   axe_x > 0 and axe_y < 0: MaCNC.diag_HD(pas_mm)
        elif axe_x < 0 and axe_y < 0: MaCNC.diag_HG(pas_mm)
        elif axe_x > 0 and axe_y > 0: MaCNC.diag_BD(pas_mm)
        elif axe_x < 0 and axe_y > 0: MaCNC.diag_BG(pas_mm)
    elif x_actif:
        if axe_x > 0: MaCNC.droite(pas_mm * axe_x)
        else:         MaCNC.gauche(pas_mm * abs(axe_x))
    elif y_actif:
        if axe_y < 0: MaCNC.avant(pas_mm * abs(axe_y))
        else:         MaCNC.arriere(pas_mm * axe_y)

    if abs(axe_z) > DEADZONE:
        if axe_z < 0: MaCNC.haut(pas_mm * abs(axe_z))
        else:         MaCNC.bas(pas_mm * axe_z)

pygame.quit()