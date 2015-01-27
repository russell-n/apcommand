Atheros Command Line
====================

.. note:: These are observations I made while trying to figure out how to set up the AP. Not everything here is necessarily correct but maybe you won't have to struggle quite so much if you at least start with someone else's notes.

Code references:

.. toctree::
   :maxdepth: 1
   
   apup and apdown <atheros_files/apup_apdown>
   apcfg <atheros_files/apcfg>

The Telnet Connection
---------------------

The Atheros AP5KAP has two command-line interface connections -- a serial port and and a telnet server. Since the telnet connection behaves more-or-less like the serial port and adds remote access I'll assume that that's the interface being used.

.. csv-table:: Login Information
   :header: Item,Value

   Default (LAN) IP, 10.10.10.21
   Username, root
   Password, 5up

The Atheros Commands
--------------------

The Atheros is running `BusyBox <http://www.busybox.net/>`_ so it has a unix-based command line. In addition the usual commands there are a set of shell scripts in ``/etc/ath/``, in particular there are two files called ``apup`` and ``apdown`` that will bring up the VAPs (and take them down).

The two commands (``apup`` and ``apdown``) along with the ``cfg`` command seem to be the main ones needed to configure the access point. 

The `/etc/ath/` shell scripts:

    * :download:`activateVAP <atheros_files/etc_ath_activate_VAP.sh>`
    * :download:`apcfg <atheros_files/etc_ath_apcfg.sh>`
    * :download:`apdown <atheros_files/etc_ath_apdown.sh>`
    * :download:`apoob <atheros_files/etc_ath_apoob.sh>`
    * :download:`apup <atheros_files/etc_ath_apup.sh>`
    * :download:`killVAP <atheros_files/etc_ath_killVAP.sh>`
    * :download:`makeVAP <atheros_files/etc_ath_makeVAP.sh>`

The `/etc/ath` folder also has what appear to be template configuration files for the access point:

    * :download:`eap.app_bss <atheros_files/etc_ath_eap_ap_bss.txt>`
    * :download:`psk.app_bss <atheros_files/etc_ath_psk_ap_bss.txt>`
    * :download:`psk.sta <atheros_files/etc_ath_psk_sta.txt>`
    * :download:`radius_mac.ap_bss <atheros_files/etc_ath_radius_mac.ap_bss.txt>`

Some of the shell-scripts are using `wlanconfig <http://linux.die.net/man/8/wlanconfig>`_ so you can use it directly if you know the syntax. If you try and follow a MadWifi tutorial you'll find some things work (like creating and destroying `VAPs <http://linux.die.net/man/8/wlanconfig>`_) but many things don't. When in doubt it's probably safest to take one of the shell scripts and if it doesn't do exactly what you need, try and alter it yourself.

The cfg Command
---------------

The `cfg` command is a symlink to `/usr/www/cgi-bin/cgiMain` and is the main way to set the access-points configurations. Judging by the file name `cgiMain` I'm guessing that it's using the `Common Gateway Interface <https://en.wikipedia.org/wiki/Common_Gateway_Interface>`_, but it's a binary and doesn't seem to have any help so it's not obvious how to use it. Through trial and error (and looking at the examples) I've found the following flags work:

.. csv-table:: cfg-options
   :header: Option,Meaning

   ``-a <setting>``,Set an AP parameter (e.g. ``cfg -a AP_SSID=ummagumma``)
   ``-c``, Commit the settings you changed with the -a flag
   ``-e``, Export the settings (adds the bash command 'export' in front of each parameter and dumps to stdout)
   ``-h ${ITER_AP_WEP_RADIO_NUM1_KEY} 1``, Don't know -- some WEP thing
   ``-s``, Show the settings (same as ``-e`` but without the word `export`)
   ``-t ${APINDEX} /etc/ath/${APNAME}.<suffix> > /tmp/<prefix>${APNAME}``, Translate settings to a config file
   ``-x``, Reset the settings to the defaults

As an example, to clear any changes you've made and set the SSID to AAAARGH::

    apdown
    cfg -x
    cfg -a AP_SSID=AAAARGH
    cfg -c
    apup

The Settings
------------

.. include:: atheros_files/cfg_s.txt

You won't see this exactly, there are 16 VAPs setup on the AP and the `-s` option will show all their settings, even if only one is enabled (so I filtered out the other VAP parameters). 

.. include:: atheros_files/tmp_secath0.txt

This the `secath0` file won't show you as much as ``cfg -s`` but most of the changes you make using ``cfg -a`` will be there.

What you'll notice is that the two ``cfg -s`` and ``secauth0`` have variable names that are similar but not the same. From what I can tell the `cfg` command is setting the variables that ``cfg -s`` shows and then saving them in a file `/tmp/secath0` which is then used to configure the AP. So when you use ``cfg -a`` you should be using the variable names shown by ``cfg -s``. To see the defaults look at the :download:`apcfg <atheros_files/etc_ath_apcfg.sh>` file.

The `apcfg` Settings
~~~~~~~~~~~~~~~~~~~~

Since there are so many I'm just going to pull out the descriptions from the file that I think are most interesting. Assume where you see a variable that there's an implicit ``cfg -a`` in front of it.

apcfg:

  Configuration file for Atheros AP.
  This file will "predefine" default configuration data for the AP.  This
  will first read all configuration data from flash (cfg -e), then fill in any
  defaults that are missing.  Thus the defaults will appear on the web pages
  even if the configuration store has been cleared.

Set Network configuration
+++++++++++++++++++++++++

I don't know that anything other than the AP_IPADDR might need to be set::

 AP_IPADDR  = IP address of the bridge
 WAN_IPADDR = Fixed IP address of the WAN, if it's not bridged
 WAN_MODE   = bridged for attached to bridged, Get address if dhcp, fixed address
              if static

AP Start Mode
+++++++++++++

This can be overridden by environmental variables. For testing you will probably want *standard* -- the default is *dual* which will leave two VAPs up (one 2.4 GHz and one 5 GHz).

.. csv-table::
   :header: Value, Meaning

   standard , standard single AP start mode
   rootap , WDS root AP for WDS modes
   repeater , WDS repeater station
   repeater-ind , WDS repeater station independent mode
   client , WDS "virtual wire" client
   multi , Multiple BSSID with all encryption types
   dual , Dual concurrent automatically configure interface
   stafwd , Station mode with address forwarding enabled

Channel and Mode
++++++++++++++++

AP_PRIMARY_CH (the channel, e.g. 6 for 2.4GHz) could be:

   * a number
   * 11na (which means auto-scan in 11na mode) or
   * 11ng (which means auto-scan in 11ng mode)

AP_CHMODE (the width):

   * 11NGHT20
   * 11NAHT40MINUS
   * 11NAHT40PLUS

Quote: `This is for pure G or pure N operations.  Hmmmm...` (I don't know what the Hmmmm is about):

   * PUREG= 0 or 1
   * PUREN= 0 or 1

Channel Configuration
+++++++++++++++++++++

I'll just quote the file since I have know idea what the values should be::

    cfg -a TXQUEUELEN=${TXQUEUELEN:=1000}
    cfg -a SHORTGI=${SHORTGI:=1}
    cfg -a SHORTGI_2=${SHORTGI_2:=1}

Aggregation.  First parameter enables/disables, second parameter sets the size limit::

    cfg -a AMPDUENABLE=${AMPDUENABLE:=1}
    cfg -a AMPDUENABLE_2=${AMPDUENABLE_2:=1}
    cfg -a AMPDUFRAMES=${AMPDUFRAMES:=32}
    cfg -a AMPDUFRAMES_2=${AMPDUFRAMES_2:=32}
    cfg -a AMPDULIMIT=${AMPDULIMIT:=50000}
    cfg -a AMPDULIMIT_2=${AMPDULIMIT_2:=50000}
    cfg -a AMPDUMIN=${AMPDUMIN:=32768}
    cfg -a AMPDUMIN_2=${AMPDUMIN_2:=32768}
    cfg -a CWMMODE=${CWMMODE:=1}
    cfg -a CWMMODE_2=${CWMMODE_2:=1}
    cfg -a RATECTL=${RATECTL:="auto"}
    cfg -a MANRATE=${MANRATE:=0x8c8c8c8c}
    cfg -a MANRETRIES=${MANRETRIES:=0x04040404}
    cfg -a RX_CHAINMASK=${RX_CHAINMASK:=3}
    cfg -a RX_CHAINMASK_2=${RX_CHAINMASK_2:=3}
    cfg -a TX_CHAINMASK=${TX_CHAINMASK:=3}
    cfg -a TX_CHAINMASK_2=${TX_CHAINMASK_2:=3}

AP Identification Section (SSID)
++++++++++++++++++++++++++++++++

To set the SSID:

    * AP_SSID=<some string (no spaces please)>

Security
++++++++

This is a work in progress, I'm just showing the defaults since I don't know what some things mean::

    AP_MODE = 'ap'
    AP_SECMODE = 'None'
    AP_SECFILE = 'PSK
    WPS_ENABLE = '0'



The Other Commands
------------------

I don't use most of the other code directly so I'm just pulling this from the files directly.

activateVAP
~~~~~~~~~~~

    This script is used to activate a VAP that was created earlier. Activation involves bringing the interface up, associating with a bridge, and configuring the security mode.  The VAP MUST EXIST prior to calling the activate script.

The form of the command is::

    activateVAP <vap> <BR> <Security> <SEC Args> <WSC>  <VAP_TIE>

.. csv-table:: activateVAP
   :header: Variable, Description
   :delimiter: :

   vap:    Vap ID (e.g. ath0)
   BR:    Bridge to join (or - if not bridged)
   Security:    Security mode (WEP,WPA,WSC,NONE)
   Sec Args:    File containing security configuration.  For WPA this is the hostapd conf file.  For WEP this is a list of iwconfig commands setting the keys.

Examples:

  * Open Access Point::

     activateVAP ath0 br0 NONE
  
  * WPA Access Point::

     activateVAP ath1 br0 WPA wpa2-psk.conf

  * WEP Station::

     activateVAP ath0 br0 WEP wep.conf

killVAP
+++++++

 This script is used to destroy a VAP, or if you want complete destruction, specify 'all`.  Using the all option will also unload the wlan module.

The form of the command is::

    killVAP <VAP>

Where VAP is the name of the VAP (e.g. ath0).  

Examples::

    killVAP ath1
    killVAP all

makeVAP
+++++++

This script is used to create AP or Station instances (VAPs).  It will NOT actually join the bridge or do any RF configuration.

The form of the command is::

    makeVAP <Mode> <ESSID> <Channel_String> <beaconint>

.. csv-table:: makeVap
   :header: Variable,Description
   :delimiter: :
    
    Mode:    Either ap, ap-wds, sta, or sta-wds (access point or station)
    ESSID:   ESSID String
    Channel: String indicating the channel configuration.  


beaconint:   This is the beacon interval desired for this VAP.  Note
             that this is system wide, and will override the current
             beacon interval for ALL vaps.  You MUST also include the
             RF command for this option.


The Channel option given above has the form <inst>:<RF>:<channel>:<mode>. Where:

 * Inst = Interface instance (which radio, 0 or 1)

 * RF   = RF indicates radio should be configured with the specified parameters

 * channel = channel to put the AP on, use 11A or 11G to scan

 * mode = operating mode

The *mode* can be one of:

 * 11AST         : 11 A Static Turbo (Legacy)
 * AUTO          : Legacy Scan Mode
 * 11A           : Legacy 11A mode
 * 11B
 * 11G
 * FH
 * TA
 * TG
 * 11NAHT20
 * 11NGHT20
 * 11NAHT40PLUS
 * 11NAHT40MINUS
 * 11NGHT40PLUS  
 * 11NGHT40MINUS
 * 11NAHT40 (valid only when channel=11na)
 * 11NGHT40 (valid only when channel=11ng)

Examples.

Access Point with RF::

     makeVAP ap OpenAP 0:RF:6:

Access Point with RF, beacon interval of 400 ms::

    makeVAP ap OpenAP RF 400

Access Point w/o RF::

     makeVAP ap NormAP

WDS Root AP::

     makeVAP ap-wds RootAP RF

WDS Repeater (two commands)::

     makeVAP sta-wds RPTR RF
     makeVAP ap-wds RPTR
