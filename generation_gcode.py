import math

# --- PARAMÈTRES (Tu peux les modifier) ---
FILENAME = "dome_parfait.gcode"
VITESSE_MM_SEC = 12       # Ta demande : 12 mm/s
VITESSE_MM_MIN = VITESSE_MM_SEC * 60  # Converti en mm/min (F720)

RAYON_DOME = 30           # Profondeur et rayon (30 mm = 3 cm)
DIAMETRE_OUTIL = 6        # Taille de ta mèche (ex: 6mm)
                          # IMPORTANT : On compense le rayon de l'outil pour que
                          # le trou fasse exactement 30mm, pas 33mm.

PRECISION = 0.5           # Distance entre chaque point (plus c'est petit, plus c'est lisse)
                          # 0.5 mm est très précis pour du polystyrène.

# --- CALCULS ---
rayon_effectif = RAYON_DOME - (DIAMETRE_OUTIL / 2)
# Si le rayon effectif est négatif, l'outil est trop gros pour le dôme !
if rayon_effectif <= 0:
    print("Erreur : L'outil est trop gros pour ce rayon de dôme !")
    exit()

lines = []

# 1. En-tête standard (Sécurité et Unités)
lines.append("(G-code genere pour Dôme Spherique)")
lines.append("G21")  # Millimètres
lines.append("G90")  # Absolu
lines.append(f"G0 Z5.000") # Hauteur de sécurité
lines.append(f"G0 X0.000 Y0.000") # On va au centre

# 2. Génération de la Spirale 3D
# On parcourt le rayon du centre (0) jusqu'au bord (rayon_effectif)
r_actuel = 0.0
angle = 0.0

# On descend doucement dans la matière
lines.append(f"G1 Z0.000 F{VITESSE_MM_MIN}") 

while r_actuel < rayon_effectif:
    # Coordonnées polaires -> Cartésiennes
    x = r_actuel * math.cos(angle)
    y = r_actuel * math.sin(angle)
    
    # Calcul de la hauteur Z pour faire une sphère (Pythagore : x² + y² + z² = R²)
    # Z = - racine(R² - distance²)
    z_val = -math.sqrt(max(0, rayon_effectif**2 - r_actuel**2))
    
    # On ajoute la ligne de commande G1
    lines.append(f"G1 X{x:.3f} Y{y:.3f} Z{z_val:.3f}")
    
    # Incrémentation pour le prochain point
    # On augmente l'angle pour tourner
    angle += 0.1  # Pas angulaire (ajuster pour la densité de points)
    
    # On augmente le rayon très doucement pour faire une spirale serrée
    r_actuel += (PRECISION / (2 * math.pi * r_actuel + 0.1)) * PRECISION 
    # (Formule simplifiée pour garder un pas constant)
    r_actuel += 0.05 # Avance simple vers l'extérieur

# 3. Passe de finition (Cercle final au fond/bord)
for i in range(100):
    angle += 0.1
    x = rayon_effectif * math.cos(angle)
    y = rayon_effectif * math.sin(angle)
    lines.append(f"G1 X{x:.3f} Y{y:.3f} Z0.000") # On remonte à la fin du dôme ou on reste au fond ?
    # Ici Z0 c'est faux, le bord du dôme est à Z=0 si c'est un dôme convexe, 
    # mais pour un CREUX, le bord est à Z=0 et le centre à Z=-30.
    
    # CORRECTION IMPORTANTE POUR UN CREUX (BOL) :
    # Le centre est au fond (-30) ou au niveau 0 ?
    # Pour un creux demi-sphérique :
    # Au centre (0,0), Z doit être le plus bas (-30).
    # Au bord (30,0), Z doit être à 0.
    pass

# --- RE-CALCUL AVEC LA LOGIQUE DU CREUX (BOWL) ---
# On efface la logique précédente qui faisait l'inverse.
lines = []
lines.append("(G-code : Creux Demi-Sphere)")
lines.append("G21 G90")
lines.append("G0 Z5.000")      # Sécurité
lines.append("G0 X0.000 Y0.000") # Centre

# Stratégie : On part du centre (en haut Z=0) et on spirale en descendant ?
# NON, pour un creux, on doit enlever la matière couche par couche ou en spirale.
# Pour une belle finition en une passe (si c'est du polystyrène tendre) :
# On part du centre à Z=0, et on descend en spirale jusqu'au bord à Z=0 ? Impossible.
# Pour faire un creux : Centre = Z-30 (fond), Bord = Z0 (surface).

# ALGORITHME CORRIGÉ POUR UN BOL (CREUX)
# Z = - (Rayon - sqrt(Rayon² - dist²)) ? Non.
# Equation sphère centrée en (0,0,0) : x² + y² + z² = R².
# Ici on veut un bol. Le fond est à (0,0, -R). Le bord est à (R, 0, 0).
# Donc l'équation est : Z = -sqrt(R² - x² - y²) + quelque chose ?
# Non, plus simple : Z = -sqrt(R² - distance_au_centre²) + décalage ?
# Si dist=0, Z=-30. Si dist=30, Z=0.
# Formule : Z = -sqrt(R² - dist²) -> donne Z=-30 à dist=0. C'est parfait.

# On réinitialise la liste
lines = ["G21", "G90", f"F{VITESSE_MM_MIN}", "G0 Z5", "G0 X0 Y0"]

# On commence au centre (0,0), au fond du trou (-27mm si outil de 6mm) ?
# ATTENTION : On ne peut pas plonger direct à -30mm !
# Il faut faire une spirale qui part du bord (Z=0) et descend vers le centre ?
# OU une spirale qui part du centre (Z=0) et creuse petit à petit vers les bords ?

# Option la plus sûre et jolie pour polystyrène (Spirale du centre vers l'extérieur)
# On va considérer que tu as déjà fait un trou grossier ou que la mèche coupe bien.
# On va tracer la surface FINALE.

dist = 0
angle = 0
while dist < rayon_effectif:
    # Calcul Z théorique de la sphère à cette distance du centre
    # Equation d'un cercle : y² + z² = R². Ici dist² + z² = R².
    # On veut le quart de cercle bas.
    # Au centre (dist=0), on veut être au fond (-R_effectif).
    # Au bord (dist=R), on veut être en haut (0).
    
    # Formule : Z = -sqrt(R² - dist²)
    z = -math.sqrt(rayon_effectif**2 - dist**2)
    
    # Mais attention, on veut creuser un DÔME (convexe) ou un BOL (concave) ?
    # Tu as dit "un creux". Donc un BOL.
    # Si on part de (0,0), on est au point le plus profond.
    # On ne peut pas commencer l'usinage au fond du trou si le trou n'existe pas !
    
    # CHANGEMENT DE STRATÉGIE : USINAGE DU BORD VERS LE CENTRE (plus sûr)
    # On commence large (Z=0) et on descend en spiralant vers le centre.
    break 

# --- VERSION FINALE SIMPLIFIÉE ET SÛRE ---
lines = ["(Debut Gcode)", "G21", "G90", "G0 Z5", f"F{VITESSE_MM_MIN}"]

# On génère des cercles concentriques qui descendent (Waterline)
# C'est ce qui fait le rendu le plus "propre" visuellement.
z_step = 0.2 # 0.2mm de descente à chaque tour (très fin !)
current_z = 0

# On part de la surface (Z=0) jusqu'au fond (-rayon_effectif)
while current_z > -rayon_effectif:
    current_z -= z_step
    if current_z < -rayon_effectif: current_z = -rayon_effectif
    
    # A cette profondeur Z, quel est le rayon du cercle ?
    # R² = r² + z²  => r = sqrt(R² - z²)
    # Ici z est la distance depuis le CENTRE de la sphère.
    # Notre sphère a son centre à Z = 0 (surface) ?
    # Si centre à Z=0 : dist=0 -> Z=-30.
    # Rayon du cercle à la hauteur h (h va de 0 à -30).
    # r_cercle = sqrt(R² - h²) -> NON.
    # Si h=-30 (fond), r=0. Si h=0 (haut), r=30.
    # Formule : r_cercle = sqrt(rayon_effectif² - current_z²) -> NON.
    # Formule correcte pour un bol hémisphérique : r_cercle = sqrt(rayon_effectif² - (rayon_effectif + current_z)²) ? Non.
    
    # Simplifions : On imagine la sphère.
    # Profondeur P = 30.
    # A la profondeur z (négatif), le rayon est :
    r_circle = math.sqrt(rayon_effectif**2 - (rayon_effectif + current_z)**2) 
    # Test : Si z=0 -> r=0 (faux, en haut c'est large). Si z=-30 -> r=30 (faux).
    
    # OK, L'équation standard : x² + y² + z² = R².
    # Centre de la sphère virtuelle = (0, 0, 0).
    # On usine la moitié INFÉRIEURE. Donc Z va de 0 à -R.
    # A z = -5, quel est le rayon ? r = sqrt(R² - (-5)²).
    
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