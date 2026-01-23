import serial
import time
from cnc_lib import CNC

#MaCNC = CNC('/dev/ttyUSB0') #Linux
MaCNC = CNC(5)  #Windows
print(MaCNC.lecture_erreur())

