# pyPNC-3000

Pilotage en Python d'une fraiseuse Roland PNC-3000 par liaison série. Le projet envoie des commandes CAMM-GL à la machine et traduit du G-code vers ces commandes.

Projet CNC 2026, BTS CIEL, lycée Loritz.

## Installation

Il faut Python 3 et un port série relié à la machine.

```
pip install -r requirements.txt
```

`pygame` ne sert qu'à la manette et `Pillow` qu'à l'interface graphique.

## Utilisation

```python
from cnc_lib import CNC

machine = CNC(port="COM3")    # profondeur de gravure par défaut : 50 mm
machine.position_releve()
machine.droite(10)            # distances en mm
machine.home()
```

Le premier argument de `CNC` est la profondeur de gravure, pas le port : `CNC(3)` règle 3 mm et utilise le port par défaut, `COM1`. Le port doit être passé par son nom. S'il n'existe pas, `CNC` lève une erreur qui liste les ports disponibles, sans rien envoyer.

Pour lister les ports :

```
python -m serial.tools.list_ports
```

## Fichiers

| Fichier | Rôle |
|---|---|
| `cnc_lib.py` | Classe `CNC` : déplacements, outil, vitesse, lecture de position |
| `parsing_gcode.py` | Lecture d'un fichier G-code |
| `sender_gcode.py` | Envoi d'un fichier G-code à la machine |
| `generation_gcode.py` | Génération de `dome_parfait.gcode` |
| `controle_manette.py` | Pilotage à la manette |
| `InterfaceGraphique2026CNC2.py` | Interface graphique Tkinter |
| `utilisation_cnc.py` | Démonstration : gravure de texte |
| `surfacage.py` | Surfaçage d'une pièce |
| `premier_pas.py`, `test.py` | Premiers essais de communication |
| `commandes_emul.txt` | Commandes `socat` pour émuler le port série sous Linux |
| `test.gcode`, `test2.gcode`, `dome_parfait.gcode` | Fichiers G-code d'exemple |

## Limites connues

- L'interface graphique ne démarre pas en l'état : les images qu'elle charge ne sont pas dans le dépôt et son choix de port appelle une méthode absente de `CNC`.
- `aller_a` refuse les X et Y négatifs. `dome_parfait.gcode`, centré sur l'origine, ne peut donc pas être usiné tel quel.
