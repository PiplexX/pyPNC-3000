from cnc_lib import CNC
import time

MaCNC = CNC(4)
MaCNC.position_gravure()
MaCNC.surfacage(170,110)
time.sleep(10)
MaCNC.home()