import serial
import time
from cnc_lib import CNC

#MaCNC = CNC('/dev/ttyUSB0') #Linux
MaCNC = CNC(1)  #Windows

MaCNC.position_releve()
MaCNC.attendre_pause()
MaCNC.avant(35)
print("On attend")
MaCNC.attendre_pause()
MaCNC.droite(15)
print("On attend")
MaCNC.attendre_pause()
MaCNC.graver_str("PROJET CNC", 9)
MaCNC.position_releve()
print("On attend")
MaCNC.attendre_pause()
MaCNC.gauche(50)
print("On attend")
MaCNC.attendre_pause()
MaCNC.arriere(15)
print("On attend")
MaCNC.attendre_pause()
MaCNC.graver_str("2026",9)
MaCNC.position_releve()
time.sleep(5)
MaCNC.home()

