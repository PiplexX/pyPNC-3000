import math

# --- PARAMÈTRES (Tu peux les modifier) ---
FILENAME = "dome_parfait.gcode"
VITESSE_MM_SEC = 12       # Ta demande : 12 mm/s
VITESSE_MM_MIN = VITESSE_MM_SEC * 60  # Converti en mm/min (F720)

RAYON_DOME = 30           # Profondeur et rayon (30 mm = 3 cm)
DIAMETRE_OUTIL = 6        # Taille de ta mèche (ex: 6mm)
                          # IMPORTANT : On compense le rayon de l'outil pour que
                          # le trou fasse exactement 30mm, pas 33mm.

# --- CALCULS ---
rayon_effectif = RAYON_DOME - (DIAMETRE_OUTIL / 2)
# Si le rayon effectif est négatif, l'outil est trop gros pour le dôme !
if rayon_effectif <= 0:
    print("Erreur : L'outil est trop gros pour ce rayon de dôme !")
    exit()

lines = ["(Debut Gcode)", "G21", "G90", "G0 Z5", f"F{VITESSE_MM_MIN}"]

# On génère des cercles concentriques qui descendent (Waterline)
# C'est ce qui fait le rendu le plus "propre" visuellement.
z_step = 0.2 # 0.2mm de descente à chaque tour (très fin !)
current_z = 0

# On part de la surface (Z=0) jusqu'au fond (-rayon_effectif)
while current_z > -rayon_effectif:
    current_z -= z_step
    if current_z < -rayon_effectif: current_z = -rayon_effectif

    # Sphère centrée en (0, 0, 0), on usine la moitié inférieure : x² + y² + z² = R².
    # A la profondeur z, le rayon du cercle est donc r = sqrt(R² - z²).
    r_circle = math.sqrt(rayon_effectif**2 - current_z**2)

    # Génération du cercle à ce niveau Z (approximation par segments)
    nb_segments = int(2 * math.pi * r_circle / 1.0) + 10 # Segments de 1mm env.
    if r_circle > 0.5: # On ne fait pas de cercle si c'est tout petit (le fond)
        lines.append(f"(Niveau Z {current_z:.2f})")
        # Approche
        lines.append(f"G0 X{r_circle:.3f} Y0.000")
        lines.append(f"G1 Z{current_z:.3f}")

        for i in range(nb_segments + 1):
            ang = (2 * math.pi * i) / nb_segments
            px = r_circle * math.cos(ang)
            py = r_circle * math.sin(ang)
            lines.append(f"G1 X{px:.3f} Y{py:.3f} Z{current_z:.3f}")

lines.append("G0 Z10") # Fin, on remonte
lines.append("M2") # Fin programme

# Écriture du fichier
with open(FILENAME, "w") as f:
    f.write("\n".join(lines))

print(f"Fichier '{FILENAME}' généré avec succès !")
print(f"Rayon trou: {RAYON_DOME}mm | Profondeur: {RAYON_DOME}mm")
