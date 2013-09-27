The Broadcom BCM94718NR Parser
==============================
.. currentmodule:: apcommand.accesspoints.broadcom.broadcom_parser
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

    
If you look at the `soup.find` parameters you can see that it chose the sub-tree that had a tag attribute matching the dictionary I passed in (there is also a `find_all` method that will return a list of all matching sub-trees, but in this case I know there is only one). 

The lines with the `option` tags can be interpreted this way:

    * if it has ``selected`` then that is the current Wireless Interface that the user would see if this were in a browser (when the GET request was made ``data={'wl_unit':'0'}`` was passed in as a parameter or it is the default) 

    * If the ``selected`` text is 'Disabled', the radio is off, if 'Enabled' the radio is on

.. warning:: Although it looks like a string when you print the output of `soup.find` what you actually get is a `bs4.element.Tag` object.

The previous warning means that you cannot search it directly with a regular expression or string search, but you can cast it to a string::

    state_string = str(state)

It also means that you can use the `find` method to burrow your way down to the right child without regular expressions::

    select = soup.find(attrs={'name':'wl_radio'})
    band_24 = select.find(attrs={'value':'0'})
    state_string = band_24.text

The variable `state_string` now contains the (unicode) string 'Disabled'. You could also do it as one line::

    state_string = soup.find(attrs={'name':'wl_radio'}).find(attrs={'value':'0'}).text

The question now -- *is this a better solution than using regular expressions?* From a personal standpoint I would say no, regular expressions are more generalizable, while this is a specific package. Then again, it would be impossible to decompose the html tree with just regular expressions (okay, hard, not impossible), so why would it be worse to use it to get the rest?

The answer for now will be to use BeautifulSoup function calls instead of regular expressions, until a case arises where they are needed.

The Selected Case
~~~~~~~~~~~~~~~~~

So, it appears that the Broadcom web interface adds a selected="" tag to drop-down options that are currently selected. You can get the surrounding tags but BeautifulSoup seems to not be able to find the `selected` tag (or it returns the wrong tag). I have not figured out why, but this may be where switching to string searches and regular expressions would make sense.

In the soup I use a named expression::

    SELECTED_EXPRESSION = r'\bselected\b.*>(?P<{0}>.*)<'

So, for instance, to get the current DHCP-service state you could pull the HTML from the ``lan.asp`` page, feed it to a BeautfulSoup instance (call it ``soup``) and do something like this to get the current state::

    dhcp_selected = SELECTED_EXPRESSION.format('DHCP')
    
    lan_proto = soup.find(attrs={'name':'lan_proto'})
    state = re.search(dhcp_selected, str(lan_proto)).group('DHCP')


.. _broadcom-parser-wireless-interface:
The Wireless Interface
~~~~~~~~~~~~~~~~~~~~~~

This is the drop-down that selects the current interface shown to the user (and which is what you need to choose if you are making changes or queries that are specific to a band).

The output of ``soup.find(attrs={'name':'wl_unit'})``::

    <select name="wl_unit" onchange="submit();">
    <option selected value="0">(00:90:4C:09:11:03)</option>
    <option value="1">(00:90:4C:13:11:03)</option>
    </select>


The SoupError
-------------

Right now I am not sure what kind of errors are going to come up, but for runtime errors that I anticipate I will raise a `SoupError` to try and make it more obvious what happened.

.. uml::

   SoupError -|> RuntimeError



.. _broadcom-base-soup:
The BroadcomBaseSoup
--------------------

Although I have decided to move to aggregation over inheritance, the soups seem to have some common code that is just easier with inheritance -- so here we go again once more for the last time.

.. autosummary::
   :toctree: api

   BroadcomBaseSoup
   BroadcomBaseSoup.html
   BroadcomBaseSoup.soup
   BroadcomBaseSoup.selected_expression



.. _broadcom-radio-soup:
The BroadcomRadioSoup
---------------------

This is a class to hold BeautifulSoup for the Broadcom Access point ``radio.asp`` page. I had hoped to do a single class for the Broadcom Web Interface but inspecting the pages reveals that the names have conflicts which would likely make it too confusing (the exception being the SSID which is on a different page but gets thrown in here anyway).

The Soup Queries
~~~~~~~~~~~~~~~~

There are different kinds of queries going on in the BroadcomRadioSoup and since I'm already having trouble remembering what is going on, I'll document some of them here.

Find
++++

The query::

    self.soup.find(attrs={'name':'wl_unit'})

Returns a `tag <http://www.crummy.com/software/BeautifulSoup/bs4/doc/#tag>`_ which is an HTML sub-tree whose root has the name attribute that was passed in to the ``find`` call ('wl_unit' in this case). See the :ref:`Wireless Interface <broadcom-parser-wireless-interface>` section above for a sample output. Because it is a tag, you can do further searches within it. *Use the ``find`` method to narrow the HTML tree down to just the part you are interested in.*

Tag Attributes
++++++++++++++

The query::

    self.soup.find(attrs={'name':'wl_country_code'}).option['value']

First uses find to narrow the tree down to the subtree::

    <select name="wl_country_code" onchange="wl_recalc();">
    <option selected value="US"></option>
    </select>


Within this sub-tree the tag named `option`  has an attribute  named `value`, so the ``.option['value']`` returns the right-hand-side of ``value="US"``. *Use this syntax to get text from tag-attributes (as opposed to text between tags).*

Text
~~~~

This query::

    self.soup.find(attrs={'name':'wl_radio'}).find(attrs={'value':'0'}).text

First uses ``find`` to narrow the HTML tree down to the 'wl_radio' subtree (a BeautifulSoup tag)::

    <select name="wl_radio">
    <option selected value="0">Disabled</option>
    <option value="1">Enabled</option>
    </select>

Then it uses ``find`` again to get the ``option`` tag that has the ``value="0"`` attribute (the '0' indicates this is the first item in the drop-down menu)::

    <option selected value="0">Disabled</option>

Then uses ``.text`` to get the state of the interface::

   Disabled

*Use ``.text`` to get the text between tags.*



.. uml::

   BroadcomRadioSoup -|> BaseClass

User (client) API
+++++++++++++++++

This is the interface for those who want to use this to get text from an html input.
   
.. autosummary::
   :toctree: api

   BroadcomRadioSoup
   BroadcomRadioSoup.html
   BroadcomRadioSoup.mac_24_ghz
   BroadcomRadioSoup.mac_5_ghz
   BroadcomRadioSoup.country
   BroadcomRadioSoup.interface_state
   BroadcomRadioSoup.channel
   BroadcomRadioSoup.bandwidth
   BroadcomRadioSoup.sideband

Developer API
+++++++++++++

This is the interface for those who want to add to the Soup.

.. uml::

   BroadcomRadioSoup -|> BroadcomBaseSoup

.. autosummary::
   :toctree: api

   BroadcomRadioSoup
   BroadcomRadioSoup.wireless_interface
   BroadcomRadioSoup.get_value_one
   BroadcomRadioSoup.get_value_zero
   


The BroadcomLANSoup
-------------------

Since the Radio Soup is getting so big I am going back to the idea of one soup per page. The only interesting thing I can think of for this page is the DHCP server state (to make sure it is off). I was going to get the IP address but since you need the IP address to get to the server to ask it its IP address I decided not to.

.. uml::

   BroadcomLANSoup -|> BroadcomBaseSoup


.. autosummary::
   :toctree: api

   BroadcomLANSoup
   BroadcomLANSoup.dhcp_state



The BroadcomSSIDSoup
--------------------

Continuing with the one-class one-page pattern...

.. uml::

   BroadcomSSIDSoup -|> BroadcomBaseSoup

.. autosummary::
   :toctree: api

   BroadcomSSIDSoup
   BroadcomSSIDSoup.ssid




Some Cases
----------

This is a scratchpad for BeautfulSoup commands to get specific things.

To get the `DHCP` state (from ``lan.asp``) (for the internal network, use ``lan1_proto`` for the guest network)::

    selected_expression = r'\bselected\b=.*>(?P<{0}>.*)<'.format('DHCP')
    
    lan_proto = soup.find(attrs={'name':'lan_proto'})
    state = re.search(selected_expression, str(lan_proto)).group('DHCP')

* This is one of those cases where you need to find the 'selected' keyword in the tag to figure out which of the drop-down-menu choices is the current one (thus the regular expression)

* State should be one of ``Enabled`` or ``Disabled``.

* The expression is set up in this module as a constant named SELECTED_EXPRESSION

