The Broadcom BCM94718NR Parser
==============================
.. currentmodule:: apcommand.accesspoints.broadcom.broadcom_expressions
This is a module to hold an interpreter to pull information from the Broadcom html pages. It uses `BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`_ to break the html tree apart and then regular expressions to extract the specific bits of text.

The `radio.asp` HTML
--------------------

I know very little about HTML and web scraping and am making this empirically so I will use this document as a lab-report as much as a code-module.

Radio State
~~~~~~~~~~~

Assuming that there is a `response` object that was returned from a 'GET' request to the `radio.asp` page, the 
state of the radio can be pulled using beautiful soup::

    soup = BeautifulSoup(response.text)
    state = soup.find(attrs={'name':'wl_radio'})

The `state` variable now should have some text like this::

    <select name="wl_radio">
    <option selected value="0">Disabled</option>
    <option value="1">Enabled</option>
    </select>

    
If you look at the `soup.find_all` parameters you can see that it chose the sub-tree that had a tag attribute matching the dictionary I passed in (there is also a `find_all` method that will return a list of all matching sub-trees, but in this case I know there is only one). 

The lines with the `option` tags can be interpreted this way:

    * if it has ``selected`` then that is the current Wireless Interface that the user would see if this were in a browser (when the GET request was made ``data={'wl_unit':'0'}`` was passed in as a parameter or it is the default) 

    * ``value='0'`` means the 2.4 GHz wireless interface, ``value='1'`` means the 5 GHz interface

    * If the text is 'Disabled', the radio is off, if 'Enabled' the radio is on

.. warning:: Although it looks like a string when you print the output of `soup.find` what you actually get is a `bs4.element.Tag` object.

The previous warning means that you can search it directly with a regular expression or string search, but you can cast it to a string::

    state_string = str(state)

It also means that you can use it to burrow your way down to the right child without regular expressions::

    select = soup.find(attrs={'name':'wl_radio'})
    band_24 = select.find(attrs={'value':'0'})
    state_string = band_24.text

The variable `state_string` now contains the (unicode) string 'Disabled'. You could also do it as one line::

    state_string = soup.find(attrs={'name':'wl_radio'}).find(attrs={'value':'0'}).text

The question now -- *is this a better solution than using regular expressions?* From a personal standpoint I would say no, regular expressions are more generalizabel, while this is a specific package. Then again, it would be impossible to decompose the html tree with just regular expressions (okay, hard, not impossible), so why would it be worse to use it to get the rest?

The answer for now will be to use BeautifulSoup function calls instead of regular expressions, until a case arises where they are needed.

.. note:: So, it appears that the Broadcom web interface adds a selected="" tag to drop-down options that are currently selected. You can get the surrounding tags but BeautifulSoup seems to not be able to find the `selected` tag. I have not figured out why, but this may be where switching to string searches and regular expressions would make sense.

The Wireless Interface
~~~~~~~~~~~~~~~~~~~~~~

This is the drop-down that selects the current interface shown to the user (and which is configured if you are pushing changes).

The output of ``soup.find(attrs={'name':'wl_unit'})``::

::

    <select name="wl_unit" onchange="submit();">
    <option selected value="0">(00:90:4C:09:11:03)</option>
    <option value="1">(00:90:4C:13:11:03)</option>
    </select>
    
    



The SoupError
-------------

Right now I am not sure what kind of errors are going to come up, but for runtime errors that I anticipate I will raise a `SoupError` to try and make it more obvious what happened.

.. uml::

   SoupError -|> RuntimeError



The BroadcomRadioSoup
---------------------

This is a class to hold BeautifulSoup for the Broadcom Access point ``radio.asp`` page. I had hoped to do a single version but inspecting the pages reveals that the names have conflicts which would likely make it too confusing.


<select name="wl_unit" onchange="submit();">
<option selected value="0">(00:90:4C:09:11:03)</option>
<option value="1">(00:90:4C:13:11:03)</option>
</select>

