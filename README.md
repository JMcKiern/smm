# Spider-Man: Mysterio's Menace - Password Decoder/Encoder

Script to encode/decode the passwords used in the GBA game

## Passwords Discovered

- `26B9F` - all items, no levels completed, Normal difficulty
- `TB31T` - all items, all levels completed, Super Hero difficulty

## How to Use

```
(deck@steamdeck smm)$ python3
Python 3.11.5 (main, Aug 24 2023, 12:23:19) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import smm
>>> from pprint import pprint
>>> state = smm.decode("SP1DY")
>>> pprint(state)
{'amusement_park': 0,
 'armor_suit': 0,
 'belt': 1,
 'chemcorp': 1,
 'compressor': 0,
 'difficulty': 2,
 'downtown': 0,
 'electric_suit': 0,
 'empire_metals': 1,
 'fluid_upgrade': 0,
 'heavy_impact': 1,
 'left_wrist': 1,
 'museum': 0,
 'nightclub': 0,
 'pier_54': 0,
 'right_wrist': 1,
 'symbiote_suit': 1,
 'thermal_suit': 1}
>>> state['difficulty'] = 0
>>> pprint(state)
{'amusement_park': 0,
 'armor_suit': 0,
 'belt': 1,
 'chemcorp': 1,
 'compressor': 0,
 'difficulty': 0,
 'downtown': 0,
 'electric_suit': 0,
 'empire_metals': 1,
 'fluid_upgrade': 0,
 'heavy_impact': 1,
 'left_wrist': 1,
 'museum': 0,
 'nightclub': 0,
 'pier_54': 0,
 'right_wrist': 1,
 'symbiote_suit': 1,
 'thermal_suit': 1}
>>> smm.encode(state)
'S51PW'
```
