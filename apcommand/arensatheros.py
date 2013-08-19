
#python standard library
import time
import re
import logging
import subprocess

# lab126 or aren
#import libD.serial.serialD as serial


class Atheros(object):
    """
    Wrapping all of the commands to configure the AP
    Adhere with Lab126 framework
    """
    def __init__(self, IP, username, password, prompt = "~ #"):
        """
        **Constructor**
        
        :param:

            - `IP`: string type the IP address of the AP
            - `username`: string type the username to login to the AP
            - `password`: string type the password to login to the AP
        """
        self.ip = IP
        self.user_name = username
        self.pass_word = password
        self.prompt = "~ #"

    def establish_connection(self):
        """
        Create a serial connection

        :postcondition: self.connection is a pyserial connection

        :return: True
        """
        self.connection = serial.SerialPort("/dev/ttyUSB1", 115200, 8, "N", 1, 
                                            timeout=10, uname=self.user_name, 
                                            passwd=self.pass_word, prompt=self.prompt)
        return True

    def setAPWireless(self, SSID, Band, Channel, Mode, RTS=None, Fragmentation=None, WMM=True):
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
        if not self.establish_connection():
            logging.error("Could not establish connection")
        try:
            if Band.upper() not in ["24G", "5G"]:
                return "{} not a recognized band. '24G' or '5G' only".format(Band)
            if Mode.lower() not in ["11na", "11ng", "11a", "11g"]:
                return "{} is not a valid mode, only '11na', '11ng', '11a', '11g'".format(Mode)
            
            self.connection.write("apdown\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -x\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            
            if Band == "24G":
                self.band = 2
                self.connection.write("cfg -a AP_CHMODE={}HT20\n".format(Mode.upper()))
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("AP set mode to %s" % Mode)
                self.connection.write("cfg -a AP_PRIMARY_CH={}\n".format(Channel))
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("AP set channel to %s" % Channel)
                #set dual radio device to single radio
                self.connection.write("cfg -a AP_STARTMODE=standard\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                self.connection.write("cfg -a AP_RADIO_ID=0\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("AP set primary radio to 2.4GHz")
            elif Band == "5G":
                self.band = 5
                self.connection.write("cfg -a AP_CHMODE_2={}HT20\n".format(Mode.upper()))
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("AP set mode to %s" % Mode)
                self.connection.write("cfg -a AP_PRIMARY_CH_2={}\n".format(Channel))
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("AP set channel to %s" % Channel)
                #set dual radio device to single radio
                self.connection.write("cfg -a AP_STARTMODE=standard\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                self.connection.write("cfg -a AP_RADIO_ID=1\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("AP set primary radio to 5GHz")
            
            self.connection.write("cfg -a AP_SSID={}\n".format(SSID))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("AP set ssid to %s" % SSID)
            if RTS is not None and RTS != "":
                self.connection.write("iwconfig ath0 rts {}\n".format(RTS))
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("RTS threshold = %s" % RTS)
            if Fragmentation is not None and Fragmentation != "":
                self.connection.write("iwconfig ath0 frag {}\n".format(Fragmentation))
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("Fragmentation = %s" % Fragmentation)
                    
        except Exception as err:
            logging.error(err)
            return "{} occured during setAPWireless".format(err)
        
        return self.commit() 

    def setAPSecOpen(self):
        """
        Set the AP to open security
        
        :rtype: string type
        :returns: None on success and error string on failure
        """
        if not self.establish_connection():
            logging.error("Could not establish connection")
        try:
            self.connection.write("apdown\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_SECMODE=None\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("security mode = Open")
        except Exception as err:
            logging.error(err)
            return "{} occured during setAPSecOpen".format(err)
        
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
        if not self.establish_connection():
            logging.error("Could not establish connection")
        try:
            if Encryption.upper() not in ["TKIP", "CCMP"]:
                logging.error("%s is not valid" % Encryption)
                return "{} is not a valid encryption type, 'TKIP' or 'CCMP' only"
            if Management.upper() not in ["WPA", "WPA2"]:
                logging.error("%s is not valid" % Management)
                return "{} is not a valid management type, 'WPA' or 'WPA2' only"

            self.connection.write("apdown\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_SECMODE=WPA\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            
            if Management.upper() == "WPA":
                self.connection.write("cfg -a AP_WPA=1\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("security mode = wpa version 1")
            
            elif Management.upper() == "WPA2":
                self.connection.write("cfg -a AP_WPA=2\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("security mode = wpa version 2")
            
            self.connection.write("cfg -a AP_SECFILE=PSK\n") 
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_CYPHER={}\n".format(Encryption.upper()))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("security cypher = %s" % Encryption)
            self.connection.write("cfg -a PSK_KEY={}\n".format(Passphrase))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("security psk = %s" % Passphrase)
        except Exception as err:
            logging.error(err)
            return "{} occured during setAPSecPSK"
        
        return self.commit() 

    def setAPSecWEP(self, Key):
        """
        Set the AP security to WEP
        
        :param `Key`: string type the desired WEP key
        :rtype: string type
        :returns: None on success and error string on failure
        """
        if not self.establish_connection():
            logging.error("Could not establish connection")
        try:
            if self.band == 2:
                suffix = 0
            else:
                suffix = 1
            self.connection.write("apdown\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_SECMODE=WEP\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_SECFILE=WEP\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_WEP_MODE_{}=2\n".format(suffix))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a WEP_RADIO_NUM{}_KEY_1={}\n".format(suffix, Key))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("security WEP w/WEP key = %s" % key)
        except Exception as err:
            logging.error(err)
            return "{} error occured during setAPSecWEP".format(err)

        return self.commit()

    def deauthSTA(self, MAC):
        """
        Deauth the station?
        **Not Implemented**
        
        :param `MAC`: string type the MAC address of STA
        :rtype: string type
        :returns: None for success and error string on failure
        """
        #TODO find out how to send deauth packet to specific MAC 
        return None

    def getMACAddress(self):
        """
        Return the MAC address of the AP
        
        :rtype: string type
        :returns: the MAC address of the AP
        """
        if not self.establish_connection():
            logging.error("Could not establish connection")
        try:
            #ensure AP is up and running
            self.connection.write("apup\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("ifconfig ath0\n")
            logging.debug("getting AP MAC from interface ath0")
            output = self.connection.readlines()
            result = re.search("HWaddr ([a-fA-F0-9]{2}[:|\-]?){6}", output)
            if result:
                return result.group(0).split()[1]
        except Exception as err:
            logging.error(err)
            return "{} occured while getting MAC address".format(err)
        
        return None 

    def commit(self):
        """
        Save changes ??
        
        :rtype: string type
        :returns: None for success and error string on failure
        """
        try:
            self.connection.write("cfg -c\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("apup\n")
            time.sleep(10)
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
        except Exception as err:
            logging.error(err)
            return str(err)
       
        logging.debug("AP configuration commited")
        self.connection.close()
        while True:
            process = subprocess.Popen(["ping", "-c", "1", self.ip], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
            if process.stderr.read() != "":
                logging.debug("Ping command error : {}".format(process.stderr.read()))
            if re.search("1 received", process.stdout.read()):
                break
            elif re.search("1 packets received", process.stdout.read()):
                break
            else:
                time.sleep(5)
        return None

    def setAPSecEnt(self, Type):
        """
        Set AP security to enterprise
        
        :param `Type`: the type of security 'WPA' or 'WPA2'
        """
        if not self.establish_connection():
            logging.error("Could not establish connection")
        if Type.upper() not in ["WPA", "WPA2"]:
            return "{} is not a valid type, 'WPA' or 'WPA2' only"
        try:
            self.connection.write("apdown\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_SECMODE=WPA\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            if Type.upper() == "WPA":
                self.connection.write("cfg -a AP_WPA=1\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("enterprise sec = wpa1")
            else:
                self.connection.write("cfg -a AP_WPA=2\n")
                if not re.search(self.prompt, self.connection.readlines()):
                    self.cleanup()
                    return
                logging.debug("enterprise sec = wpa2")
            self.connection.write("cfg -a AP_SECFILE=EAP\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_CYPHER=CCMP\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_EAP_MODE=WPA\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
        except Exception as err:
            logging.error(err)
            return "{} occured durint setAPSecEnt".format(err)

        return self.commit()

    def setDHCP(self, Enable):
        """
        Set or unset DHCP on the AP

        ** Not Implemented**
        
        :param `Enable`: integer type, boolean on or off
        :rtype: string type
        :returns: None on success or error string on failure
        """
        logging.debug("DHCP not enablable")
        return "DHCP not enablable"

    def setRADIUS(self, IP, Port, Shared):
        """
        Set the AP to RADIUS settings
        
        :param:

            - `IP`: string type the IP address of the RADIUS server
            - `Port`: string type the port number of the RADIUS server
            - `Shared`: string type the shared secret between AP and the RADIUS server
       
        :rtype: string type
        :returns: None on success and error string on failure
        """
        if not self.establish_connection():
            logging.error("Could not establish connection")
        try:
            self.connection.write("apdown\n")
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            self.connection.write("cfg -a AP_AUTH_SERVER={}\n".format(IP))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("radius server = %s" % IP)
            self.connection.write("cfg -a AP_AUTH_PORT={}\n".format(Port))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("radius server port = %s" % Port)
            self.connection.write("cfg -a AP_AUTH_SECRET={}\n".format(Shared))
            if not re.search(self.prompt, self.connection.readlines()):
                self.cleanup()
                return
            logging.debug("radius server shared key = %s" % Shared)
        except Exception as err:
            logging.error(err)
            return "{} occured during setRADIUS".format(err)
        
        return self.commit() 

    def cleanup(self):
        """
        Close the connection with the AP
        """
        logging.debug("cleanup, closing serial connection")
        self.connection.close()
