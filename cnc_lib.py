#Owner : PiplexX, projet CNC 2026 BTS CIEL Loritz

import serial
import serial.tools.list_ports
import os
import time

class CNC():
        #constructeur, permet de paramètrer la profondeur de gravure par défaut, le port de communication série et la vitesse de la liaison
        def __init__(self,profondeur_gravure=50, port='COM1', vitesse_bauds=9600) :
            self.port = port
            self.vitesse_bauds = vitesse_bauds
            self.__verifier_port(port, profondeur_gravure)
            print(f"INFO: connexion sur le port {port}, profondeur de gravure {profondeur_gravure} mm")
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
        #vérifie le port avant de l'ouvrir : si le choix est invalide, rien n'est envoyé sur la liaison série
        def __verifier_port(self, port, profondeur_gravure):
            #le premier argument de CNC est la profondeur : CNC('COM3') ne choisit pas le port
            if isinstance(profondeur_gravure, str):
                raise ValueError(f"ERREUR: FONCTION=INIT, PROBLEME=PROFONDEUR '{profondeur_gravure}' INVALIDE, POUR CHOISIR LE PORT UTILISER CNC(port='{profondeur_gravure}')")
            if not isinstance(port, str):
                raise ValueError(f"ERREUR: FONCTION=INIT, PROBLEME=LE PORT DOIT ETRE UN TEXTE COMME 'COM3', RECU {port!r}")
            ports = [p.device for p in serial.tools.list_ports.comports()]
            if os.name == 'nt':
                port_trouve = port.upper() in [p.upper() for p in ports]
            else:
                #les ports virtuels (socat) ne sont pas listés mais existent comme fichiers
                port_trouve = port in ports or os.path.exists(port)
            if not port_trouve:
                raise ValueError(f"ERREUR: FONCTION=INIT, PROBLEME=PORT {port} INTROUVABLE, PORTS DISPONIBLES={ports or 'AUCUN'}")
        def __convertion(self, mm ,multi): #convertit les mm pour le pas de la machine
            return (mm*100)*multi
        # ---------------------------------- FONCTIONS DE DIRECTION ----------------------------------
        def droite(self, nb_mm, multi=1):
            coo = self.lecture_pos()
            if (18000>=coo['x']+self.__convertion(nb_mm, multi) >=0):
                self.ser.write((f"^PR Z {self.__convertion(nb_mm, multi)},0,0;").encode('ascii'))
                return 0
            else:
                print("ERREUR: FONCTION=DROITE, PROBLEME=X DOIT ETRE ENTRE 0 ET 18000")
                return -1
        def gauche(self, nb_mm, multi=-1):
            coo = self.lecture_pos()
            if (18000>=coo['x']+self.__convertion(nb_mm, multi) >=0):
                self.ser.write((f"^PR Z{self.__convertion(nb_mm, multi)},0,0;").encode('ascii'))
                return 0
            else:
                print("ERREUR: FONCTION=GAUCHE, PROBLEME=X DOIT ETRE ENTRE 0 ET 18000")
                return -1
        def avant(self, nb_mm, multi=1):
            coo = self.lecture_pos()
            if (15000>=coo['y']+self.__convertion(nb_mm, multi) >=0):
                self.ser.write((f"^PR Z 0,{self.__convertion(nb_mm, multi)},0;").encode('ascii'))
                return 0
            else:
                print("ERREUR: FONCTION=AVANT, PROBLEME=Y DOIT ETRE ENTRE 0 ET 15000")
                return -1
        def arriere(self, nb_mm, multi=-1):
            coo = self.lecture_pos()
            if (15000>=coo['y']+self.__convertion(nb_mm, multi) >=0):
                self.ser.write((f"^PR Z 0,{self.__convertion(nb_mm, multi)},0;").encode('ascii'))
                return 0
            else:
                print("ERREUR: FONCTION=ARRIERE, PROBLEME=Y DOIT ETRE ENTRE 0 ET 15000")
                return -1
        def diag_HG(self, nb_mm, multix = -1, multiy = 1):
            coo = self.lecture_pos()
            if (18000>=coo['x']+self.__convertion(nb_mm, multix) >=0) and (15000>=coo['y']+self.__convertion(nb_mm, multiy) >=0):
                self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            else:
                print("ERREUR: FONCTION=diag_HG, PROBLEME=X DOIT ETRE ENTRE 0 ET 18000 ET Y DOIT ETRE ENTRE 0 ET 15000")
                return -1
            return 0
        def diag_HD(self, nb_mm, multix = 1, multiy = 1):
            coo = self.lecture_pos()
            if (18000>=coo['x']+self.__convertion(nb_mm, multix) >=0) and (15000>=coo['y']+self.__convertion(nb_mm, multiy) >=0):
                self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            else:
                print("ERREUR: FONCTION=diag_HD, PROBLEME=X DOIT ETRE ENTRE 0 ET 18000 ET Y DOIT ETRE ENTRE 0 ET 15000")
                return -1
        def diag_BG(self, nb_mm, multix = -1, multiy = -1):
            coo = self.lecture_pos()
            if (18000>=coo['x']+self.__convertion(nb_mm, multix) >=0) and (15000>=coo['y']+self.__convertion(nb_mm, multiy) >=0):
                self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            else:
                print("ERREUR: FONCTION=diag_BG, PROBLEME=X DOIT ETRE ENTRE 0 ET 18000 ET Y DOIT ETRE ENTRE 0 ET 15000")
                return -1
        def diag_BD(self, nb_mm, multix = 1, multiy = -1):
            coo = self.lecture_pos()
            if (18000>=coo['x']+self.__convertion(nb_mm, multix) >=0) and (15000>=coo['y']+self.__convertion(nb_mm, multiy) >=0):
                self.ser.write((f"^PR Z {self.__convertion(nb_mm, multix)},{self.__convertion(nb_mm, multiy)},0;").encode('ascii'))
            else:
                print("ERREUR: FONCTION=diag_BD, PROBLEME=X DOIT ETRE ENTRE 0 ET 18000 ET Y DOIT ETRE ENTRE 0 ET 15000")
                return -1
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
            if(x>=0 and y>=0):
                self.ser.write(f"Z {int(self.__convertion(x, 1)*multi)},{int(self.__convertion(y, 1)*multi)},{int(self.__convertion(z, 1))};".encode('ascii'))
                return 0
            else:
                print("ERREUR: FONCTION=ALLER_A, PROBLEME=X OU Y NE PEUVENT ETRE NEGATIFS")
                return -1
        def surfacage(self, taille_x, taille_y):
            self.regler_vitesse(22)
            self.ser.write(f"T3, {self.__convertion(taille_x,1)},{self.__convertion(taille_y,1)},300,1; V 22".encode('ascii'))
            return 0
        def regler_vitesse(self, vitesse):
            self.ser.write(f"V {vitesse}".encode('ascii'))
            print("vitesse")
            return 0
        def graver_str(self, text, taille): # a test
            self.ser.write(f"S {taille} P {text}\r\n".encode('ascii'))
            return 0
        def dessiner_cercle(self, rayon):
            coo = self.lecture_pos
            self.ser.write(f"^PR C {coo['x']},{coo['y']},{self.__convertion(rayon,1)}".encode('ascii'))
        # ---------------------------------- FONCTIONS DE LECTURE ----------------------------------
        def lecture_erreur(self):
            #on vide le tampon
            self.ser.reset_input_buffer()
            self.ser.write(b"OS;")
            reponse = self.ser.read_until(b'\r').decode("ascii").strip()
            return(reponse)
        def attendre_pause(self):
            debut = time.time()
            timeout = 120
            derniere = None
            stable = 0
            while time.time() - debut < timeout:
                pos = self.lecture_pos()
                if pos is None:
                    stable = 0
                elif pos == derniere:
                    stable += 1
                    if stable >= 2:
                        return pos
                else:
                    stable = 0
                    derniere = pos
            time.sleep(0.1)
        def lecture_pos(self):
            self.ser.reset_input_buffer()
            time.sleep(0.07)
            self.ser.write(b"O;")
            reponse = self.ser.read_until(b'\r').decode('ascii').strip().split(',')
            if reponse[0] != '' and len(reponse)==3:
                dico_rep = {}
                dico_rep['x'] = int(reponse[0])
                dico_rep['y'] = int(reponse[1])
                dico_rep['z'] = int(reponse[2])
                print(dico_rep)
                return dico_rep
            else:
                return None
        def vider_cache(self):
            self.ser.reset_input_buffer()
            return 0