import re

def parsing_code(chemin):
    liste_instructions = []
    fichier = open(chemin, mode="r", encoding="utf-8")
    lignes = fichier.readlines()
    for ligne in lignes:
        #retire les espaces les \n ...
        ligne.strip()
        if not ligne.startswith("(") and ligne != "\n":
            #Decomposition de la ligne sous la forme de pair lettre valeur (utilisation d'un regex)
            paires = re.findall(r'([GXYZF])([-+]?\d*\.?\d+)', ligne)
            ligne_d = {paire[0]: float(paire[1]) for paire in paires}
            liste_instructions.append(ligne_d)
    return liste_instructions