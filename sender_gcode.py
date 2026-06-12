from parsing_gcode import parsing_code
from cnc_lib import CNC

class Lecteur_Code():
    def __init__(self, chemin_fichier,multi=1):
        self.liste_instructions = parsing_code(chemin_fichier)
        self.machine = CNC(3)
        self.dernier_etat = 'H'
        self.dernier_x = 0
        self.dernier_y = 0
        self.dernier_z = 0
        self.derniere_vitesse = 2
        self.multi = multi
        self.traduire_code()
        print("test")
    def traduire_code(self):
        for instruction in self.liste_instructions:
            if 'G' in instruction:
                if instruction['G'] == 0:
                    self.machine.regler_vitesse(22)
                if instruction['G'] == 1:
                    self.machine.regler_vitesse(self.derniere_vitesse)
                    self.dernier_etat = 'B'
            if 'F' in instruction:
                vitesse_seconde = int(instruction['F'] / 60)
                self.machine.regler_vitesse(vitesse_seconde)
                self.derniere_vitesse = vitesse_seconde
                print(str(vitesse_seconde) + " mm/s")

            if 'X' in instruction or 'Y' in instruction or 'Z' in instruction:
                x = instruction.get('X', self.dernier_x)
                y = instruction.get('Y', self.dernier_y)
                z = instruction.get('Z', self.dernier_z)
                self.dernier_x = x
                self.dernier_y = y
                self.dernier_z = z
                print("x : " + str(x) + " y : " + str(y) + " z : " + str(z))
                self.machine.aller_a(x, y, z, self.multi)

lecture = Lecteur_Code("test2.gcode",1)