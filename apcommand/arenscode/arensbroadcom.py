
# I don't think Broadcom has a serial port
#import libD.serial.serialD as serial
import shlex
import subprocess
import time
import re
import logging


class Broadcom(object):
    """
    Wrapping all of the commands to configure the AP
    Adhere with Lab126 framework
    """    
    def __init__(self, IP, username, password, prompt="#"):
        """
        **Constructor**
        :param:

            - `IP`: string type the IP address of the AP
            - `username`: string type the username to login to the AP
            - `password`: string type the password to login to the AP

        """
        self.connection = None
        self.username = username
        self.password = password
        self.prompt = prompt
        self.interface = 0
        self.ip = IP
        self.sec_type = 0 
        self.cmd = "curl -d '{}' --user admin:admin http://" + self.ip + "/{}"

    def setAPWireless(self, SSID, Band, Channel, Mode, RTS=None, 
                      Fragmentation=None, WMM=True):
        """
        Setup the APs wireless broadcast
        :param: 
            
            - `SSID`: string type the desired ssid for the AP
            - `Band`: string type the desired band, '24G' or '5G'
            - `Channel`: string type the desired channel
            - `Mode`: string type the desired mode '11na', '11ng', '11a', '11g'
            - `RTS`: string type optional
            - `Fragmentation`: string type optional
            - `WMM`: boolean type optional

        :rtype: string type
        :returns: None on success and error string on failure
        """
        if Band.upper() == "24G":
            self.interface = 0
        else:
            self.interface = 1
        data = "page=radio.asp&wl_unit={}&wl_radio=0&action=Apply".format(self.interface)
        command = shlex.split(self.cmd.format(data, "radio.asp"))
        logging.debug("Setting band {}".format(Band))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)
        if self.interface == 0:
            phytype = "g"
        else:
            phytype = "a"
        data = ("page=radio.asp&wl_unit={}&wl_ap_isolate=0&wl_country_code="
                "US&wl_radio=1&wl_phytype={}&wl_channel={}&wl_gmode=1&action"
                "=Apply").format(self.interface, phytype, Channel)
        command = shlex.split(self.cmd.format(data, "radio.asp")) 
        logging.debug("Setting channel {}".format(Channel))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)
        data = ("page=ssid.asp&wl_unit={}&action=Select&wl_ssid={}&wl_closed"
                "=0&action=Apply").format(self.interface, SSID)
        logging.debug("Setting ssid {}".format(SSID))
        command = shlex.split(self.cmd.format(data, "ssid.asp"))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)
        if Mode.lower() in ["11a", "11b"]:
            data = ("page=radio.asp&wl_unit={}&action=Select&wl_nmode=0&wl_gmode"
                       "=0&wl_rateset=12&wl_closed=0&action=Apply").format(self.interface)
        if Mode.lower() == "11g": 
            data = ("page=radio.asp&wl_unit={}&action=Select&wl_nmode=0&wl_gmode"
                       "=1&wl_rateset=12&wl_closed=0&action=Apply").format(self.interface)
        if Mode.lower() == "11n":
            data = ("page=radio.asp&wl_unit={}&action=Select&wl_nmode=-1&wl_gmod"
                       "e=1wl_rateset=default&wl_closed=0&action=Apply").format(self.interface)
        if Mode.lower() == "11na":
            data = ("page=radio.asp&wl_unit={}&action=Select&wl_nmode=-1&wl_rate"
                       "set=default&wl_closed=0&action=Apply").format(self.interface)
        else:
            return "{} is not valid".format(Mode)
        logging.debug("Setting mode {}".format(Mode))
        command = shlex.split(self.cmd.format(data, "radio.asp"))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)
        if Fragmentation != "":
            data = ("page=radio.asp&wl_unit={}&action=Select&wl_frag={}&action=A"
                    "pply").format(self.interface, Fragmentation)
            logging.debug("Setting fragmentation {}".format(Fragmentation))
            command = shlex.split(self.cmd.format(data, "radio.asp"))
            process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            time.sleep(10)
        if RTS != "":
            data = ("page=radio.asp&wl_unit={}&action=Select&wl_rts={}&action=Ap"
                    "ply").format(self.interface, RTS)
            logging.debug("Setting rts {}".format(RTS))
            command = shlex.split(self.cmd.format(data, "radio.asp"))
            process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            time.sleep(10)
       
        return self.commit() 

    def setAPSecOpen(self):
        """
        Set the AP to open security
        :rtype: string type
        :returns: None on success and error string on failure
        """
        data = ("page=security.asp&wl_unit={}&action=Select&wl_auth=0&wl_auth_m"
                "ode=none&wl_akm=&wl_akm_wpa=disabled&wl_akm_psk=disabled&wl_ak"
                "m_wpa2=disabled&wl_akm_psk2=disabled&wl_wep=disabled&action=Ap"
                "ply").format(self.interface)
        logging.debug("Setting security none")
        command = shlex.split(self.cmd.format(data, "security.asp"))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)
       
        return self.commit() 

    def setAPSecPSK(self, Management, Passphrase, Encryption):
        """
        Set the AP security to WPA version 1 or WPA version 2
        :param:

            - `Management`: string type the key management, 'WPA' or 'WPA2'
            - `Passphrase`: string type the desired passphrase
            - `Encryption`: string type the desired encryption 'TKIP' or 'CCMP'

        :rtype: string type
        :returns: None on success and error string on failure
        """
        if Management.upper() == "WPA":
            data = ("page=security.asp&wl_unit={}&wl_auth=0&wl_auth_mode=none&wl_ak"
                    "m=&wl_akm_wpa=disabled&wl_akm_psk=disabled&wl_akm_wpa2=disable"
                    "d&wl_akm_psk2=enabled&wl_wep=disabled&wl_crypto=aes&wl_wpa_psk"
                    "={}&wl_wpa_gtk_rekey=0&action=Apply").format(self.interface, 
                                                                  Passphrase)
            logging.debug("Setting security WPA")
        if Management.upper() == "WPA2":
            data = ("page=security.asp&wl_unit={}&wl_auth=0&wl_auth_mode=none&wl_ak"
                    "m=&wl_akm_wpa=disabled&wl_akm_psk=disabled&wl_akm_wpa2=disable"
                    "d&wl_akm_psk2=enabled&wl_wep=disabled&wl_crypto=aes&wl_wpa_psk"
                    "={}&wl_wpa_gtk_rekey=0&action=Apply").format(self.interface, 
                                                                  Passphrase)
            logging.debug("Setting security WPA2")
        else:
            return "{} not valid".format(Management)
        command = shlex.split(self.cmd.format(data, "security.asp"))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)
        
        return self.commit() 

    def setAPSecWEP(self, Key):
        """
        Set the AP security to WEP
        :param `Key`: string type the desired WEP key
        :rtype: string type
        :returns: None on success and error string on failure
        """
        data = ("page=security.asp&wl_unit={}&action=Select&wl_auth=0&wl_auth_m"
                "ode=none&wl_akm=&wl_akm_wpa=disabled&wl_akm_psk=disabled&wl_ak"
                "m_wpa2=disabled&wl_akm_psk2=disabled&wl_wep=enabled&wl_key1={}"
                "&wl_key=1&action=Apply").format(self.interface, Key)
        logging.debug("Setting wep key {}".format(Key))
        command = shlex.split(self.cmd.format(data, "security.asp"))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)

        return self.commit()

    def deauthSTA(self, MAC):
        """
        :param `MAC`: string type the MAC address of STA
        :rtype: string type
        :returns: None for success and error string on failure
        """
        logging.debug("deauthSTA not implemented")
        return None

    def getMACAddress(self):
        """
        Return the MAC address of the AP
        :rtype: string type
        :returns: the MAC address of the AP
        """
        self.connection = serial.SerialPort("/dev/ttyUSB0", 115200, 8, "N", 1, 
                                            timeout=10, uname=self.username, 
                                            passwd=self.password, prompt=self.prompt)
        try:
            #ensure AP is up and running
            self.connection.write("ifconfig %s" % (self.interface))
            output = self.connection.readlines()
            mac = re.search("HWaddr ([a-fA-F0-9]{2}[:|\-]?){6}", output)
            if mac:
                return mac.group(0).split()[1]
        except Exception as err:
            logging.error(err)
            return "error occured while getting MAC address"
        
        return None 

    def commit(self):
        """
        Commit all the setting changes at once
        :rtype: string type
        :returns: None for success and error string on failure
        """
        while True:
            process = subprocess.Popen(["ping", "-c", "1", self.ip], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
            logging.debug("PINGING")
            if process.stderr.read() != "":
                logging.debug("Ping command error : {}".format(process.stderr.read()))
            if re.search("1 received", process.stdout.read()):
                break
            elif re.search("1 packets received", process.stdout.read()):
                break
            else:
                time.sleep(5)
        time.sleep(10)
        return None

    def setAPSecEnt(self, Type):
        """
        Set AP security to enterprise
        :param `Type`: the type of security 'WPA' or 'WPA2'
        """
        if Type.upper() == "WPA":
            self.sec_type = 0 
        elif Type.upper() == "WPA2":
            self.sec_type = 1 
        else:
            logging.error("%s is not valid" % Type)
            return "%s is not a vlid enterprise type" % (Type)
        
        logging.debug("Setting enterprise security type %s" % Type)

    def setDHCP(self, Enable):
        """
        Set or unset DHCP on the AP
        :param `Enable`: integer type, boolean on or off
        :rtype: string type
        :returns: None on success or error string on failure
        """
        logging.debug("DHCP not implemented")    
        return None

    def setRADIUS(self, IP, Port, Shared):
        """
        Set the AP to RADIUS settings
        :param:

            - `IP`: string type the IP address of the RADIUS server
            - `Port`: string type the port number of the RADIUS server
            - `Shared`: string type the shared secret between AP and the RADIUS 
                        server
       
        :rtype: string type
        :returns: None on success and error string on failure
        """
        if self.sec_type == 1:
            data = ("page=security.asp&wl_unit={}&action=Select&wl_auth=0&wl_au"
                    "th_mode=none&wl_akm=&wl_akm_wpa=disabled&wl_akm_psk=disabl"
                    "ed&wl_akm_wpa2=enabled&wl_akm_psk2=disabled&wl_wep=disable"
                    "d&wl_crypto=aes&wl_radius_ipaddr={}&wl_radius_port={}&wl_r"
                    "adius_key={}&wl_wpa_gtk_rekey=0&wl_net_reauth=36000&action"
                    "=Apply").format(self.interface, radius_ip, radius_port, 
                                     shared_key)
        if self.sec_type == 0:
            data = ("page=security.asp&wl_unit={}&action=Select&wl_auth=0&wl_au"
                    "th_mode=none&wl_akm=&wl_akm_wpa=enabled&wl_akm_psk=disable"
                    "d&wl_akm_wpa2=disabled&wl_akm_psk2=disabled&wl_wep=disable"
                    "d&wl_crypto=tkip&wl_radius_ipaddr={}&wl_radius_port={}&wl_"
                    "radius_key={}&wl_wpa_gtk_rekey=0&wl_net_reauth=36000&actio"
                    "n=Apply").format(self.interface, radius_ip, radius_port, 
                                      shared_key)
        
        logging.debug("Setting enterprise radius information")
        command = shlex.split(self.cmd.format(data, "security.asp"))
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(10)

        return self.commit() 

    def cleanup(self):
        """
        cleanup method just closes connection
        """
        if self.connection:
            self.connection.close()
