Shelving Objects
================

These are notes for the python `shelve <http://docs.python.org/2/library/shelve.html>`_ module which I am using to allow ``undo`` and ``redo`` calls for the ``commands``.

``shelve`` combines `pickle <http://docs.python.org/2/library/pickle.html>`_ and `anydbm <http://docs.python.org/2/library/anydbm.html>`_ to create a dictionary-like interface to store and retrieve objects.

Creating a New Shelf
--------------------

Creating a new shelf is like opening a file but instead of calling file-methods (like ``read``) you treat the opened shelf like a dictionary:

::

    import shelve
    from contextlib import closing
    
    SHELF_NAME = 'test.shelf'
    KEY_1 = 'aoeu'
    
    with closing(shelve.open(SHELF_NAME)) as s:
        s[KEY_1] = {'alpha':0, 'omega':1}
    



.. note:: Even though it looks like you are opening a file, shelve for python 2.7 doesn't have an ``__exit__`` method so you can't use the ``with`` statement with it directly (thus the ``closing`` import).

Loading a Shelf
---------------

It works basically like you would expect:

::

    with closing(shelve.open(SHELF_NAME)) as s:
        data = s[KEY_1]
    
    print data
    

::

    {'alpha': 0, 'omega': 1}
    



Modifying a Shelf
-----------------

This did not seem intuitive to me, but by default ``shelve`` does **not** let you make changes to loaded objects, but it **does** let you add new items (key:object pairs) to the database:

::

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
    

::

    Using the still-open shelf:
       {'alpha': 0, 'omega': 1}
       ummagumma
    
    Using the re-opened shelf:
       {'alpha': 0, 'omega': 1}
       ummagumma
    



The Writeback
-------------

The solution to the previous problem of trying to modify an existing shelved object is to use the ``writeback`` option when opening the shelve (shelf?):

::

    with closing(shelve.open(SHELF_NAME, writeback=True)) as object_shelf:
        object_shelf[KEY_1]['gamma'] = 2
        object_shelf[KEY_2] = 'abbadabba'
    
    with closing(shelve.open(SHELF_NAME)) as s:
        for key in KEYS:
            print "   {0}".format(s[key])    
    

::

       {'alpha': 0, 'omega': 1, 'gamma': 2}
       abbadabba
    

