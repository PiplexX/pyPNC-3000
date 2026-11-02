#Owner : PiplexX, CNC project 2026 BTS CIEL Loritz

import serial
import serial.tools.list_ports
import os
import time

class CNC():
        #constructor, lets you set the default engraving depth, the serial port and the link speed
        def __init__(self,profondeur_gravure=50, port='COM1', vitesse_bauds=9600) :
            self.port = port
            self.vitesse_bauds = vitesse_bauds
            self.__verifier_port(port, profondeur_gravure)
            print(f"INFO: connexion sur le port {port}, profondeur de gravure {profondeur_gravure} mm")
            self.__config(profondeur_gravure)
            self.profondeur_gravure = profondeur_gravure
            #last Z variable, unused for now but designed to patch the Z axis control with the GUI
            self.dernier_z = 0
        #config function run after init, starts the serial communication and sends the command to set the PU and PD positions
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
        #checks the port before opening it: if the choice is invalid, nothing is sent over the serial link
        def __verifier_port(self, port, profondeur_gravure):
            #the first argument of CNC is the depth: CNC('COM3') does not choose the port
            if isinstance(profondeur_gravure, str):
                raise ValueError(f"ERREUR: FONCTION=INIT, PROBLEME=PROFONDEUR '{profondeur_gravure}' INVALIDE, POUR CHOISIR LE PORT UTILISER CNC(port='{profondeur_gravure}')")
            if not isinstance(port, str):
                raise ValueError(f"ERREUR: FONCTION=INIT, PROBLEME=LE PORT DOIT ETRE UN TEXTE COMME 'COM3', RECU {port!r}")
            ports = [p.device for p in serial.tools.list_ports.comports()]
            if os.name == 'nt':
                port_trouve = port.upper() in [p.upper() for p in ports]
            else:
                #virtual ports (socat) are not listed but exist as files
                port_trouve = port in ports or os.path.exists(port)
            if not port_trouve:
                raise ValueError(f"ERREUR: FONCTION=INIT, PROBLEME=PORT {port} INTROUVABLE, PORTS DISPONIBLES={ports or 'AUCUN'}")
        def __convertion(self, mm ,multi): #converts the mm to the machine's step
            return (mm*100)*multi
        # ---------------------------------- DIRECTION FUNCTIONS ----------------------------------
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
        # ---------------------------------- HEIGHT FUNCTIONS ----------------------------------
        def bas(self, nb_mm, multi=-1):
            self.ser.write((f"^PR Z 0,0,{self.__convertion(nb_mm,multi)};").encode('ascii'))
            self.dernier_z += self.__convertion(nb_mm, multi)
            return 0
        def haut(self, nb_mm, multi=1):
            self.ser.write((f"^PR Z 0,0,{self.__convertion(nb_mm,multi)};").encode('ascii'))
            self.dernier_z += self.__convertion(nb_mm, multi)
            return 0
        # ---------------------------------- SPECIAL FUNCTIONS ----------------------------------
        def start_conf(self):
            #Init of the engraving level and the rest level (Careful, Z0 must be set manually)
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
        def graver_str(self, text, taille): # to test
            self.ser.write(f"S {taille} P {text}\r\n".encode('ascii'))
            return 0
        def dessiner_cercle(self, rayon):
            coo = self.lecture_pos
            self.ser.write(f"^PR C {coo['x']},{coo['y']},{self.__convertion(rayon,1)}".encode('ascii'))
        # ---------------------------------- READING FUNCTIONS ----------------------------------
        def lecture_erreur(self):
            #we empty the buffer
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