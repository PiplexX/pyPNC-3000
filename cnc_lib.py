import serial
import time

class CNC():
        def __init__(self,profondeur_gravure=50, port='COM1', vitesse_bauds=9600) :
            self.port = port
            self.vitesse_bauds = vitesse_bauds
            self.__config(profondeur_gravure)
            self.profondeur_gravure = profondeur_gravure
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
            #Initialisation du niveau de gravure et du niveau de repos (Attention Z0 doit être set manuellement)
            self.ser.write((f"@ {self.__convertion(profondeur_gravure, -1)} , 100").encode("ascii"))
        def __convertion(self, mm ,multi): #convertit les mm pour le pas de la machine
            return (mm*100)*multi
        def droite(self, nb_mm, multi=1):
            self.ser.write((f"^PR {self.__convertion(nb_mm, multi)},0;").encode('ascii'))
            return 0
        def gauche(self, nb_mm, multi=-1):
            self.ser.write((f"^PR {self.__convertion(nb_mm, multi)},0;").encode('ascii'))
            return 0
        def avant(self, nb_mm, multi=1):
            self.ser.write((f"^PR 0,{self.__convertion(nb_mm, multi)};").encode('ascii'))
            return 0
        def arriere(self, nb_mm, multi=-1):
            self.ser.write((f"^PR 0,{self.__convertion(nb_mm, multi)};").encode('ascii'))
            return 0
        def bas(self, nb_mm, multi=-1):
            self.ser.write((f"Z 0,0,{self.__convertion(nb_mm,multi)};").encode('ascii'))
            return 0
        def haut(self, nb_mm, multi=1):
            self.ser.write((f"Z 0,0,{self.__convertion(nb_mm,multi)};").encode('ascii'))
            return 0
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
        def aller_a(self, x, y, multi=1):
            self.ser.write(f"^PA {int(self.__convertion(x, 1)*multi)},{int(self.__convertion(y, 1)*multi)};".encode('ascii'))
            return 0
        def actualiser(self):
            self.ser.write(f"@{self.__convertion(self.profondeur_gravure, 1)};".encode('ascii'))
        def surfacage(self, taille_x, taille_y):
            self.ser.write(f"T3, {self.__convertion(taille_x,1)},{self.__convertion(taille_y,1)},200,1;".encode('ascii'))