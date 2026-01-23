from parsing_gcode import parsing_code
from cnc_lib import CNC

class Lecteur_Code():
    def __init__(self, chemin_fichier, multi=1):
        self.liste_instructions = parsing_code(chemin_fichier)
        self.machine = CNC(3)
        self.dernier_etat = 'H'
        self.dernier_x = 0
        self.dernier_y = 0
        self.multi = multi
        self.traduire_code()
        print("test")
    def traduire_code(self):
        for instruction in self.liste_instructions:
            if 'G' in instruction:
                if instruction['G'] == 0:
                    self.machine.position_releve()
                    self.dernier_etat = 'H'
            if 'F' in instruction:
                vitesse_seconde = instruction['F'] / 60
                #self.machine.regler_vitesse(vitesse_seconde)
                print(str(vitesse_seconde) + " mm/s")

            if 'Z' in instruction:
                print("Z : " + str(instruction['Z']))
                Z = int(instruction['Z'])
                if Z < 0:
                    if self.dernier_etat == 'H':
                        self.machine.position_gravure()
                    self.dernier_etat = "B"
                else:
                    if self.dernier_etat == 'B':
                        self.machine.position_releve()
                    self.dernier_etat = "H"

            if 'X' in instruction or 'Y' in instruction:
                x = instruction.get('X', self.dernier_x)
                y = instruction.get('Y', self.dernier_y)
                self.dernier_x = x
                self.dernier_y = y
                print("x : " + str(x) + " y : " + str(y))
                self.machine.aller_a(x, y, self.multi)

lecture = Lecteur_Code("test.gcode", 0.3)