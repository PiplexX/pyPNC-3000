#Owner : PiplexX, projet CNC 2026 BTS CIEL Loritz

import serial
import time

class CNC():
        #constructeur, permet de paramètrer la profondeur de gravure par défaut, le port de communication série et la vitesse de la liaison
        def __init__(self,profondeur_gravure=50, port='COM1', vitesse_bauds=9600) :
            self.port = port
            self.vitesse_bauds = vitesse_bauds
            self.__config(profondeur_gravure)
            self.profondeur_gravure = profondeur_gravure
            #variable dernier Z, inutilisée pour le moment mais conçue pour patch le controle de l'axe Z avec l'IHM
            self.dernier_z = 0
        #fonction de config lancé après initialisation, lance la communication série et envoie la commande pour définir les positions PU et PD
        def __config(self, profondeur_gravure):
            self.ser = serial.Serial(
            port=self.port,
            baudrate=self.vitesse_bauds,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=4,
			dsrdtr=True,
            rtscts=True  
        )
            self.ser.write(f"@{self.__convertion(profondeur_gravure, -1)},100;".encode('ascii'))
        def __convertion(self, mm ,multi): #convertit les mm pour le pas de la machine
            return (mm*100)*multi
        # ---------------------------------- FONCTIONS DE DIRECTION ----------------------------------
        def droite(self, nb_mm, multi=1):
            self.ser.write((f"^PR Z {self.__convertion(nb_mm, multi)},0,0;").encode('ascii'))
            return 0
        def gauche(self, nb_mm, multi=-1):
            self.ser.write((f"^PR Z{self.__convertion(nb_mm, multi)},0,0;").encode('ascii'))
            return 0
        def avant(self, nb_mm, multi=1):
            self.ser.write((f"^PR Z 0,{self.__convertion(nb_mm, multi)},0;").encode('ascii'))
            return 0
        def arriere(self, nb_mm, multi=-1):
            self.ser.write((f"^PR Z 0,{self.__convertion(nb_mm, multi)},0;").encode('ascii'))
            return 0
        def diag_HG(self, nb_mm, multix = -1, multiy = 1):
            self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            return 0
        def diag_HD(self, nb_mm, multix = 1, multiy = 1):
            self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            return 0
        def diag_BG(self, nb_mm, multix = -1, multiy = -1):
            self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            return 0
        def diag_BD(self, nb_mm, multix = 1, multiy = -1):
            self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            return 0
        # ---------------------------------- FONCTIONS DE HAUTEUR ----------------------------------
        def bas(self, nb_mm, multi=-1):
            self.ser.write((f"^PR Z 0,0,{self.__convertion(nb_mm,multi)};").encode('ascii'))
            self.dernier_z += self.__convertion(nb_mm, multi)
            return 0
        def haut(self, nb_mm, multi=1):
            self.ser.write((f"^PR Z 0,0,{self.__convertion(nb_mm,multi)};").encode('ascii'))
            self.dernier_z += self.__convertion(nb_mm, multi)
            return 0
        # ---------------------------------- FONCTIONS PARTICULIERES ----------------------------------
        def start_conf(self):
            #Initialisation du niveau de gravure et du niveau de repos (Attention Z0 doit être set manuellement)
            self.ser.write((f"@ {self.__convertion(self.profondeur_gravure, -1)} , 100").encode("ascii"))
            cords = self.lecture_pos()
            self.dernier_x,self.dernier_y,self.dernier_z= cords.split(',')
        def home(self):
            self.ser.write(b"H;")
            return 0
        def position_gravure(self):
            self.ser.write(b"^PD;")
            time.sleep(0.5)
            return 0
        def position_releve(self):
            self.ser.write(b"^PU;")
            time.sleep(0.5)
            return 0
        def aller_a(self, x, y, z, multi=1):
            self.ser.write(f"Z {int(self.__convertion(x, 1)*multi)},{int(self.__convertion(y, 1)*multi)},{int(self.__convertion(z, 1))};".encode('ascii'))
            return 0
        def surfacage(self, taille_x, taille_y):
            self.regler_vitesse(22)
            self.ser.write(f"T3, {self.__convertion(taille_x,1)},{self.__convertion(taille_y,1)},300,1; V 22".encode('ascii'))
            return 0
        def regler_vitesse(self, vitesse):
            self.ser.write(f"V {vitesse}".encode('ascii'))
            print("vitesse")
            return 0
        def graver_str(self, text): # a test
            self.ser.write(f"S 20 P {text}\r\n".encode('ascii'))
            return 0
        def dessiner_cercle(self, rayon):
            coo = self.lecture_pos
            self.ser.write(f"^PR C {coo['x']},{coo['y']},{self.__convertion(rayon,1)}".encode('ascii'))
        # ---------------------------------- FONCTIONS DE LECTURE ----------------------------------
        def lecture_erreur(self): #ne marche pas pour le moment ou alors pas compris
            #on vide le tampon
            self.ser.reset_input_buffer()
            self.ser.write(b"OS;")
            reponse = self.ser.read(10).decode("ascii").strip()
            return(reponse)
        def lecture_pos(self):
            self.ser.reset_input_buffer()
            self.ser.write(b"O;")
            reponse = self.ser.read(16).decode('ascii').strip().split(',')
            dico_rep = {}
            dico_rep['x'] = reponse[0]
            dico_rep['y'] = reponse[1]
            dico_rep['z'] = reponse[2]
            return dico_rep
        def vider_cache(self):
            self.ser.reset_input_buffer()
            return 0