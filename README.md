# CSGO Demoparser in python

A CSGO .dem file parser in python

## Thanks to
1. (https://github.com/ValveSoftware/csgo-demoinfo)
2. (https://github.com/ibm-dev-incubator/demoparser)
3. (https://github.com/holosiek/csgodemo-python)
4. (https://github.com/markus-wa/demoinfocs-golang)
5. (https://github.com/SteamDatabase/GameTracking-CSGO)  
  
Without looking (and copying :D) at other projects it would have been impossible for me to understand how csgo demos work.  
Well, I still need to understand how to parse entities... whatever

## To use this:
```python
import DemoParser
parser = DemoParser(path_to_demo, dump=path_to_dumpfile, ent="ALL")
```
**dump** is a file to write some values in it (check [this file](https://github.com/ZaharX97/CSGOdemoPythonParser/blob/master/example/dump_with_player_entities.txt))  
**ent** is what entities to parse ("NONE", "P" players, "P+G" players + grenades, "ALL")  
```python
parser.parse()
```
  
## Info:
  
Now, the parser wont return anything  
You need to register some functions to use when certain events happen  
Check [this file](https://github.com/ZaharX97/CSGOdemoPythonParser/blob/master/example/round_stats.py)  
  
This parser will trigger events:  
* every time a [game event](https://github.com/ZaharX97/CSGOdemoPythonParser/blob/master/example/dump_with_player_entities.txt#L1146)  
* every demo packet message  
* any time the function *_sub_event* is called  
  
You can also add the function anywhere in code to create another event
