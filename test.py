import serial


#emplacement de ma liaison série virtuelle ou physique
port = '/tmp/ttyV0' 


# ouverture de la session série on utilise 9600 bauds, le standard de la PNC-3000
ser = serial.Serial(port, 9600)

#Envoi d'un texte simple
# Le 'b' avant les guillemets transforme le texte en "octets" (bytes)
# Le ';' est indispensable pour que la CNC comprenne la fin de l'ordre
ser.write(b"IN;PA 1000,1000;")

print("Texte envoyé !")

#fermeture
ser.close()