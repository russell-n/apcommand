The Firmware Page
=================

This is a module for getting information from the ``firmware.asp`` page. Since the page keeps the information in a table whose data lacks identifying meta-data, I am going to experiment with using pyparsing to get it out.

The page is structured as a collection of tables and forms (which contain tables):

.. digraph:: firmware_asp

   HTML -> Head
   HTML -> Body
   table_1 [label="Table: Navigation Header"]
   table_2 [label="Table: Logo, Title"]
   table_4 [label="Table: Select New Firmware"]
   table_5 [label="Table: Submit New Firmware"]
   form_2 [label="Table: Upload NVRAM"]
   form_3 [label="Table: Submit Upload"]
   tr_1 [label="Bootloader Version"]
   tr_2 [label="OS Version"]
   tr_3 [label="Driver Version"]
   Body -> table_1
   Body -> table_2
   Body -> form_1
   Body -> form_2
   Body -> form_3
   form_1 -> table_0
   table_0 -> tr_1
   table_0 -> tr_2
   table_0 -> tr_3
   form_1 -> table_4
   form_1 -> table_5
   
Looking at the graph it appears that ``table_0`` is the one we are interested here. This is what the html for that table looks like:

.. highlight:: html
.. include:: firmware_table.html
   :code: html


I had originally hoped to do this as a grammar, but it turns out to be kind of hard and I am apparently losing the AP so this will be brute-force BeautifulSoup:

::

    # python standard library
    import re
    
    # third-party
    from bs4 import BeautifulSoup
    



First, we can get the form directly because it has a unique ``action`` attribute:

::

    soup = BeautifulSoup(open('firmware_asp.html'))
    
    # find_all returns a list, but since we specified the attrs, we know it has what we want
    form = soup('form', attrs={'action': 'upgrade.cgi'})[0]
    



``form`` is a BeautfulSoup ``tag`` so it can be searched for the table. There are two ways I thought of to do this. One is to use the fact that we know that the table we want is the first:

::

    table = form('table')[0]
    



But that seems to be wrong, somehow, so I prefer to discover it:

::

    for table in form('table'):
        if any(['Version' in tag.next for tag in table('th')]):
            break
    print table
    

::

    <table border="0" cellpadding="0" cellspacing="0">
    <tr>
    <th onmouseout="return nd();" onmouseover="return overlib('Displays the current version of Boot Loader.', LEFT);" width="310">
    	Boot Loader Version:  
        </th>
    <td>  </td>
    <td>CFE 5.10.128.2</td>
    </tr>
    <tr>
    <th onmouseout="return nd();" onmouseover="return overlib('Displays the current version of OS.', LEFT);" width="310">
    	OS Version:  
        </th>
    <td>  </td>
    <td>Linux  5.70.63.1</td>
    </tr>
    <tr>
    <th onmouseout="return nd();" onmouseover="return overlib('Displays the current version of Wireless Driver.', LEFT);" width="310">
    	WL Driver Version:  
        </th>
    <td>  </td>
    <td>5.60.134 </td>
    </tr>
    </table>
    



Unfortunately, looking at the table-data, you can see that there is no really nice way to discover information. You either need to used the indices or assume the form of the versions will not change. At this point I will just give up and use the indices.

::

    data = table('td')
    extractor = re.compile('\s*<[/]*td>')
    for index in range(1,6,2):
        print extractor.sub('', str(data[index]))
    

::

    CFE 5.10.128.2
    Linux  5.70.63.1
    5.60.134
    



Since that was so convoluted I will do it again in one piece using indices:

::

    version_identifier = {1:'Bootloader', 3:'OS', 5:'Driver'}
    data = soup('form', attrs={'action': 'upgrade.cgi'})[0]('table')[0]('td')
    for index in range(1,6,2):
        print version_identifier[index] + ": " + extractor.sub('', str(data[index]))
    

::

    Bootloader: CFE 5.10.128.2
    OS: Linux  5.70.63.1
    Driver: 5.60.134
    

