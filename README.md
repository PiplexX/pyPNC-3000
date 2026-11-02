# pyPNC-3000

Python control for a Roland PNC-3000 milling machine over a serial link. The project sends CAMM-GL commands to the machine and translates G-code into those commands.

CNC 2026 project, BTS CIEL, Loritz high school.

This guide explains how to install the software, connect to the machine and run a machining job.

## 1. Safety

The machine moves as soon as a script starts. Before each run:

- keep the machine's power switch within reach;
- check that the workpiece is firmly clamped and that nothing is in the tool's way;
- keep your hands and clothing away from the work area;
- do a dry run first, with the tool above the workpiece.

**The software does not check everything.** Work area limits are only enforced by the direction functions (see section 5). `aller_a`, `haut`, `bas` and G-code files can send the tool further than intended, including into the workpiece.

## 2. Installation

1. Install Python 3 from [python.org](https://www.python.org/downloads/), ticking "Add Python to PATH".
2. Open a terminal in the project folder, then run:

   ```
   pip install -r requirements.txt
   ```

3. Connect the machine to the computer with the serial cable and turn it on.

Settings used by the software: 9600 baud, 8 data bits, no parity, 1 stop bit, hardware flow control.

## 3. Choosing the serial port

List the available ports:

```
python -m serial.tools.list_ports
```

Then give the port **by name**:

```python
from cnc_lib import CNC

machine = CNC(port="COM3")
```

At startup, the program prints the port and the engraving depth in use. Check this line:

```
INFO: connexion sur le port COM3, profondeur de gravure 50 mm
```

### Watch out for the first argument

The first argument of `CNC` is the **engraving depth**, not the port:

| Code | Result |
|---|---|
| `CNC(port="COM3")` | Port COM3, depth of 50 mm |
| `CNC(4, port="COM3")` | Port COM3, depth of 4 mm |
| `CNC(3)` | Port **COM1**, depth of 3 mm |
| `CNC("COM3")` | Error: the port took the place of the depth |

### The provided scripts use COM1

`utilisation_cnc.py`, `surfacage.py`, `sender_gcode.py` and `controle_manette.py` do not specify a port. If your machine is not on COM1, edit the line that creates the machine. For example, in `surfacage.py`:

```python
MaCNC = CNC(4, port="COM3")
```

### If the port is rejected

If the port does not exist, the program stops without sending anything and lists the available ports:

```
ERREUR: FONCTION=INIT, PROBLEME=PORT COM3 INTROUVABLE, PORTS DISPONIBLES=['COM1']
```

This check only confirms that the port exists. It does not confirm that the milling machine is connected to it: check this yourself if several devices are plugged in.

## 4. Preparing the machine

**Z0 (the workpiece surface) is set manually** on the machine, before starting a script. Depths depend on it.

Distances are given in millimetres. The software converts them to machine steps (1 mm = 100 steps).

## 5. Controlling the machine from Python

```python
from cnc_lib import CNC

machine = CNC(4, port="COM3")
machine.position_releve()
machine.attendre_pause()
machine.droite(10)
machine.attendre_pause()
machine.home()
```

Commands are sent without waiting for the previous move to finish. Call `attendre_pause()` between two moves when the order matters: it waits until the position stops changing, for 120 seconds at most.

### Moves

| Command | Effect | Limit enforced |
|---|---|---|
| `droite(mm)`, `gauche(mm)` | Relative move in X (right, left) | X from 0 to 180 mm |
| `avant(mm)`, `arriere(mm)` | Relative move in Y (forward, back) | Y from 0 to 150 mm |
| `diag_HG(mm)`, `diag_HD(mm)`, `diag_BG(mm)`, `diag_BD(mm)` | Diagonals (up/down, left/right) | X and Y |
| `haut(mm)`, `bas(mm)` | Relative move in Z (up, down) | **None** |
| `aller_a(x, y, z)` | Move to a position | Non-negative X and Y only |
| `home()` | Return to the origin | |

If a move goes outside the limits, it is not executed and an `ERREUR` message is printed. **The script still continues** with the next commands.

### Tool, speed and engraving

| Command | Effect |
|---|---|
| `position_gravure()` | Lowers the tool to the engraving depth |
| `position_releve()` | Raises the tool |
| `regler_vitesse(v)` | Sets the speed |
| `surfacage(x, y)` | Surfaces an area of x by y mm |
| `graver_str(text, size)` | Engraves text (function still marked "to test" in the code) |
| `lecture_pos()` | Returns the position in steps, as `{'x':..., 'y':..., 'z':...}` |
| `lecture_erreur()` | Reads the machine's error state |

## 6. Controlling the machine with a gamepad

Plug in the gamepad before starting the script, then run:

```
python controle_manette.py
```

| Control | Effect |
|---|---|
| Left stick | X and Y moves, including diagonals |
| Right stick, vertical | Raises or lowers the tool |
| A | Lowers the tool to the engraving position |
| B | Raises the tool |
| Y | Returns to the origin |
| LB / RB | Speed -2 / +2 (from 1 to 50, starts at 22) |
| Button 7 (Start on an Xbox controller) | Quits the program |

These buttons match an Xbox-style layout. They may differ on another gamepad: test them with a dry run.

## 7. Machining a G-code file

1. Open `sender_gcode.py` and change the last line to use your file:

   ```python
   lecture = Lecteur_Code("my_file.gcode", 1)
   ```

   The second number multiplies the X and Y coordinates: `1` keeps the original size.

2. Set the port and depth on the `self.machine = CNC(3)` line (section 3).
3. Start the job. **It begins immediately:**

   ```
   python sender_gcode.py
   ```

Supported instructions: `G0`, `G1`, `X`, `Y`, `Z` and `F` (in mm/min, converted to mm/s). Everything else is ignored, and coordinates are always treated as absolute.

**Negative coordinates:** negative X and Y values are rejected and the point is skipped, without stopping the job. Make sure your file stays positive. This is the case for `test2.gcode`, the example file run by default.

**Do not run `dome_parfait.gcode` as is:** it is centred on the origin and most of its points would be skipped. The part would be ruined.

`generation_gcode.py` regenerates this file; the radius, tool diameter and speed are set at the top of the script.

## 8. Other scripts

- `utilisation_cnc.py` engraves "PROJET CNC" and "2026".
- `surfacage.py` surfaces a 170 × 110 mm area: **the tool goes down immediately** to the configured depth.

Read a script before running it to check its moves and dimensions.

## 9. Functions to avoid for now

- **`dessiner_cercle()` and `start_conf()`**: they raise an error.

## 10. Troubleshooting

Program messages are in French and are shown here as they appear.

| Problem | What to do |
|---|---|
| `PORT ... INTROUVABLE` (port not found) | Check the cable and the port name (section 3) |
| `PROFONDEUR '...' INVALIDE` (invalid depth) | Write `CNC(port="...")` |
| `LE PORT DOIT ETRE UN TEXTE` (the port must be text) | Write the name in quotes, for example `"COM3"` |
| `could not open port` or `Access is denied` | Close the program already using the port |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `TypeError: 'NoneType' object is not subscriptable` | The machine did not answer the position read: check that it is on, then check the cable and the port |
| The script seems stuck | Check that the machine is on and the cable is plugged in: hardware flow control can block sending |
| `X DOIT ETRE ENTRE...` message (X must be between...) | The move goes outside the work area and was not executed |
| `AUCUNE MANETTE DETECTEE` (no gamepad detected) | Plug in the gamepad, then restart the script |
