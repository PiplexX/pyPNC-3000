import serial
import time

#choix port série
#PORT_SERIE = '/dev/ttyUSB0'
PORT_SERIE = 'COM1'

def test_mouvement():
    try:
        # Ouverture avec les paramètres PNC-3000 standards
        # rtscts=True active le contrôle de flux matériel du câble NanoCable
        ser = serial.Serial(
            port=PORT_SERIE,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
			dsrdtr=True,
            rtscts=True  
        )

        print(f"Connexion établie sur {PORT_SERIE}")
        
        # Reset machine
        print("Initialisation...")
        #ser.write(b"IN;") 
        #time.sleep(2) # On laisse 2 secs

        # On ne grave pas donc commande lever d'outil
        #ser.write(b"PU;")

        # 3. Déplacement de 10mm (1000 unités car 0.01mm/step)
        # Commande PA = Plot Absolute
        print("Déplacement vers X=10mm, Y=10mm...")
        ser.write(b"^PA 5000,3000;")
        
        # 4. Attente de la fin du mouvement
        time.sleep(7)
        ser.write(b"H;")
        print("Test terminé avec succès.")
        ser.close()

    except Exception as e:
        print(f"Erreur de communication : {e}")

if __name__ == "__main__":
    test_mouvement()