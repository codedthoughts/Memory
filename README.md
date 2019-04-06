# Memory
A simple json-based config manager.

##Simple usage

```py
from memory import Memory

cfg = Memory(path='/home/kaiser/MyApp') 
#Creates a file called config.json in the directory if it doesnt exist, otherwise reads the file

cfg = Memory(path='/home/kaiser/MyApp/stuff.json')
#Same as above but makes the filename stuff.json instead

cfg._set('score', 1)
#Sets a config variable of score to 1

v = cfg._get('score')
#Returns the config variable for score

v = cfg._get('score', 0)
#Same as above, but defaults to 0 if score does not exist in config

#You can access the config object directly too

cfg.data['score'] = 10

#But if you edit the object, make sure to save after to save it to the config

cfg.save()

#If the config file was edited, you can reload it in memory

cfg.load()
```
