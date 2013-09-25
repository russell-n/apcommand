
import shelve
from contextlib import closing

SHELF_NAME = 'test.shelf'
KEY_1 = 'aoeu'

with closing(shelve.open(SHELF_NAME)) as s:
    s[KEY_1] = {'alpha':0, 'omega':1}


with closing(shelve.open(SHELF_NAME)) as s:
    data = s[KEY_1]

print data


KEY_2 = 'snth'
KEYS = (KEY_1, KEY_2)

with closing(shelve.open(SHELF_NAME)) as s:
    s[KEY_1]['gamma'] = 2
    s[KEY_2] = 'ummagumma'

    print "Using the still-open shelf:"
    for key in KEYS:
        print "   {0}".format(s[key])

print "\nUsing the re-opened shelf:"
with closing(shelve.open(SHELF_NAME)) as s:
    for key in KEYS:
        print "   {0}".format(s[key])


with closing(shelve.open(SHELF_NAME, writeback=True)) as object_shelf:
    object_shelf[KEY_1]['gamma'] = 2
    object_shelf[KEY_2] = 'abbadabba'

with closing(shelve.open(SHELF_NAME)) as s:
    for key in KEYS:
        print "   {0}".format(s[key])    
