import math

# --- PARAMETERS (You can change them) ---
FILENAME = "dome_parfait.gcode"
VITESSE_MM_SEC = 12       # Your request: 12 mm/s
VITESSE_MM_MIN = VITESSE_MM_SEC * 60  # Converted to mm/min (F720)

RAYON_DOME = 30           # Depth and radius (30 mm = 3 cm)
DIAMETRE_OUTIL = 6        # Size of your bit (ex: 6mm)
                          # IMPORTANT: We compensate for the tool radius so that
                          # the hole is exactly 30mm, not 33mm.

# --- CALCULATIONS ---
rayon_effectif = RAYON_DOME - (DIAMETRE_OUTIL / 2)
# If the effective radius is negative, the tool is too big for the dome!
if rayon_effectif <= 0:
    print("Erreur : L'outil est trop gros pour ce rayon de dôme !")
    exit()

lines = ["(Debut Gcode)", "G21", "G90", "G0 Z5", f"F{VITESSE_MM_MIN}"]

# We generate concentric circles going down (Waterline)
# That's what gives the "cleanest" look visually.
z_step = 0.2 # 0.2mm down on each turn (very fine!)
current_z = 0

# We go from the surface (Z=0) to the bottom (-rayon_effectif)
while current_z > -rayon_effectif:
    current_z -= z_step
    if current_z < -rayon_effectif: current_z = -rayon_effectif

    # Sphere centred on (0, 0, 0), we machine the lower half: x² + y² + z² = R².
    # At depth z, the circle radius is therefore r = sqrt(R² - z²).
    r_circle = math.sqrt(rayon_effectif**2 - current_z**2)

    # Generating the circle at this Z level (approximated with segments)
    nb_segments = int(2 * math.pi * r_circle / 1.0) + 10 # Segments of about 1mm.
    if r_circle > 0.5: # We don't make a circle if it's really tiny (the bottom)
        lines.append(f"(Niveau Z {current_z:.2f})")
        # Approach
        lines.append(f"G0 X{r_circle:.3f} Y0.000")
        lines.append(f"G1 Z{current_z:.3f}")

        for i in range(nb_segments + 1):
            ang = (2 * math.pi * i) / nb_segments
            px = r_circle * math.cos(ang)
            py = r_circle * math.sin(ang)
            lines.append(f"G1 X{px:.3f} Y{py:.3f} Z{current_z:.3f}")

lines.append("G0 Z10") # End, we go back up
lines.append("M2") # End of program

# Writing the file
with open(FILENAME, "w") as f:
    f.write("\n".join(lines))

print(f"Fichier '{FILENAME}' généré avec succès !")
print(f"Rayon trou: {RAYON_DOME}mm | Profondeur: {RAYON_DOME}mm")
