cat /etc/ath/activateVAP
#!/bin/sh
####################################################################
## activateVAP
##
## This script is used to activate a VAP that was created earlier.
## Activation involves bringing the interface up, associating with
## a bridge, and configuring the security mode.  The VAP MUST EXIST
## prior to calling the activate script.
##
## The form of the command is
##
## activateVAP <vap> <BR> <Security> <SEC Args> <WSC>  <VAP_TIE>
##
## Where
##      vap:    Vap ID (e.g. ath0)
##       BR:    Bridge to join (or - if not bridged)
## Security:    Security mode (WEP,WPA,WSC,NONE)
## Sec Args:    File containing security configuration.  For WPA this is the hostapd
##              conf file.  For WEP this is a list of iwconfig commands setting the
##              keys.
##
## Examples:
##   Open Access Point
##      activateVAP ath0 br0 NONE
##   WPA Access Point
##      activateVAP ath1 br0 WPA wpa2-psk.conf
##   WEP Station
##      activateVAP ath0 br0 WEP wep.conf
##
###################################################################

. /etc/ath/apcfg

if [ "${1}" = "" ]; then
    echo "activateVAP usage"
    echo "activateVAP VAPid:Radio bridge Security Security_file"
    echo
    echo "vapid: e.g. ath0"
    echo "bridge:  Name of bridge to add to,(typically br0)"
    echo "Security: [ WPA | WEP | WSC | NONE ]"
    echo "Security_file: Name of file in /etc/ath containing security config"
    echo
    exit
fi

BRIDGE=$2
SECMODE=$3
SECFILE=$4
WSCMODE=$5
VAPTIE=$6

APNAME=`echo $1 | cut -d ':' -f 1`
RADIO=`echo $1 | cut -d ':' -f 2`

if [ "$RADIO" = "" ]; then
    RADIO="0"
fi

KVER=`uname -r | cut -f 1 -d '-'`
MODULE_PATH=/lib/modules/$KVER/net
MODE=`iwconfig ${APNAME} | grep "Mode:Master"`
HOSTAPD_VER=`hostapd -v 2>&1|grep hostapd|cut -f2 -d' '`

##
## Create an AP index, based on the VAP (ath) number
##

APINDEX=`echo ${APNAME}| cut -b 4-4`

if [ "$APINDEX" != "0" ]; then
    APINDEX=`expr ${APINDEX} + 1`
fi

##
## First, let us see if the indicated VAP exists.  If not, it must be created
##

VAPLIST=`iwconfig | grep ${APNAME} | cut -b 1-4`

if [ "${VAPLIST}" = "" ]; then
    echo "VAP ${APNAME} must be created first!! (use makeVAP)"
    exit
fi

##
## Must determine if the scan modules need to be loaded.  Remember, only once!
## This is in station mode if the MODE value is blank
##

STATIONSCAN=`lsmod | grep wlan_scan_sta`

if [ "${MODE}" = "" -a "${STATIONSCAN}" = "" ]; then
    
    #
    # Check for a specific MAC address that is specified.  Only valid for stations
    #

    if [ "${AP_REQ_MAC}" != "" ]; then
        iwconfig $APNAME ap $AP_REQ_MAC
    fi
fi

#
# Bring the interface up at this point!!
# configure bridge, or set an IP address for the WLAN interface
#

if [ "${BRIDGE}" != "none" -a "${BRIDGE}" != "-" ]; then
    ifconfig ${APNAME} up
    brctl addif ${BRIDGE} ${APNAME}
    echo -e "\tinterface ${APNAME}" >> /tmp/${BRIDGE}
    #
    # Add the arping command to ensure all nodes are updated on the network!
    #
    
    arping -U -c 1 -I ${BRIDGE} $AP_IPADDR

else
    ifconfig ${APNAME} up ${WAN_IPADDR}
fi

if [ ! -d /etc/wpa2 ]; then
        mkdir /etc/wpa2
fi

#
# We need to determine if WSC is enabled or not.  If not, we do the standard "stuff"
#

if [ "${WSCMODE}" = "1" -o "${WSCMODE}" = "2" ]; then
        echo ">>>>> WPS ENABLED, ${SECFILE}"
    iwpriv ${APNAME} wps 1 
    ##
    ## WSC VAP.  Determine the file correctly.
    ##

    if [ "${SECFILE}" = "EAP" ]; then
        echo "Cannot use EAP modes with WPS"
        exit 255
    fi

    if [ "${VAPTIE}" != "" ]; then
            echo ">>> VAP Tied: ${VAPTIE}"
            fname="WSC_${VAPTIE}.conf"
    else
            fname="WSC_${APNAME}.conf"
                fexist=`ls /etc/wpa2 | grep ${APNAME}`
            if [ "${HOSTAPD_VER}" != "v0.5.9" ]; then
                        unconf=`cat /etc/wpa2/WSC_${APNAME}.conf | grep "^wps_state=2"`
                else
                        unconf=`cat /etc/wpa2/WSC_${APNAME}.conf | grep "wps_configured=1"`
                fi
        if [ "${fexist}" = "" -o "${unconf}" = "" ]; then
            #
            # We have to use this file "in place" to have WSC work
            # properly.
            #
                echo ">>>>> WPS Translate, Index:${APINDEX}"
            cfg -t${APINDEX} /etc/ath/WSC.conf > /etc/wpa2/WSC_${APNAME}.conf
        fi
    fi
    
    if [ "${HOSTAPD_VER}" != "v0.5.9" ]; then
        echo -e "/etc/wpa2/WSC_${APNAME}.conf \c\h" >> /tmp/conf_filename
    else
        echo -e "\t\tbss ${APNAME}" >> /tmp/aplist$RADIO
        echo -e "\t\t{" >> /tmp/aplist$RADIO
        echo -e "\t\t\tconfig /etc/wpa2/${fname}" >> /tmp/aplist$RADIO
        echo -e "\t\t}" >> /tmp/aplist$RADIO
    fi
else
    ##
    ## Non WSC VAP.  Use Standard Security
    ##
    if [ "${SECMODE}" = "WPA" ]; then
        #
        # WPA now processes all WPA sub modes
        # Here the file is "translated" from the template.
        #
        if [ "${MODE}" != "" ]; then
            #
            # This is the method using the "translation" mode of cgiMain to
            # create an appropriate security file for PSK or Enterprise mode
            #
                cfg -t${APINDEX} /etc/ath/${SECFILE}.ap_bss ${APNAME} > /tmp/sec${APNAME}

                if [ "${HOSTAPD_VER}" != "v0.5.9" ]; then
                        echo -e "/tmp/sec${APNAME} \c\h" >> /tmp/conf_filename
                else
                        echo -e "\t\tbss ${APNAME}" >> /tmp/aplist$RADIO
                        echo -e "\t\t{" >> /tmp/aplist$RADIO
                        echo -e "\t\t\tconfig /tmp/sec${APNAME}" >> /tmp/aplist$RADIO
                        echo -e "\t\t}" >> /tmp/aplist$RADIO
                fi
        else
            #
            # This is a managed (station) node
            #
            cfg -t${APINDEX} /etc/ath/${SECFILE}.sta ${APNAME} > /tmp/sup${APNAME}
            if [ "${HOSTAPD_VER}" != "v0.5.9" ]; then
                echo -e "-c/tmp/sup${APNAME} -i${APNAME} -bbr0" > /tmp/sta_conf_filename

            else
                echo -e "\tsta ${APNAME}" >> /tmp/stalist$RADIO
                echo -e "\t{" >> /tmp/stalist$RADIO
                echo -e "\t\tconfig /tmp/sup${APNAME}" >> /tmp/stalist$RADIO
                echo -e "\t}" >> /tmp/stalist$RADIO
                fi
        fi
    fi

    if [ "${SECMODE}" = "WEP" ]; then
        NUM_KEY=1
        #
        # Insert the keys as required
        #
        my_wep_keys=" _1 _2 _3 _4 "
        for i in $my_wep_keys;
        do
            ITER_AP_WEP_RADIO_NUM0_KEY="WEP_RADIO_NUM0_KEY$i"
            ITER_AP_WEP_RADIO_NUM1_KEY="WEP_RADIO_NUM1_KEY$i"
            eval ITER_AP_WEP_RADIO_NUM0_KEY=\$$ITER_AP_WEP_RADIO_NUM0_KEY
            eval ITER_AP_WEP_RADIO_NUM1_KEY=\$$ITER_AP_WEP_RADIO_NUM1_KEY

            if [ "${RADIO}" = "0" ]; then
                if [ "${ITER_AP_WEP_RADIO_NUM0_KEY}" != "" ]; then
                                        cfg -h ${ITER_AP_WEP_RADIO_NUM0_KEY} 1
                    if [ $? = 1 ]; then
                        iwconfig ${APNAME} enc ${ITER_AP_WEP_RADIO_NUM0_KEY} [$NUM_KEY]
                    else
                        iwconfig ${APNAME} enc s:${ITER_AP_WEP_RADIO_NUM0_KEY} [$NUM_KEY]
                    fi
                fi
            fi
            if [ "${RADIO}" = "1" ]; then
                if [ "${ITER_AP_WEP_RADIO_NUM1_KEY}" != "" ]; then
                                        cfg -h ${ITER_AP_WEP_RADIO_NUM1_KEY} 1
                    if [ $? = 1 ]; then
                        iwconfig ${APNAME} enc ${ITER_AP_WEP_RADIO_NUM1_KEY} [$NUM_KEY]
                    else
                        iwconfig ${APNAME} enc s:${ITER_AP_WEP_RADIO_NUM1_KEY} [$NUM_KEY]
                    fi
                fi
            fi
            NUM_KEY=$(($NUM_KEY+1))
        done
        if [ "${RADIO}" = "0" ]; then
            if [ "${AP_WEP_MODE_0}" != "" -a "${AP_WEP_MODE_0}" != "1" ]; then
                iwpriv ${APNAME} authmode ${AP_WEP_MODE_0}
            fi
            if [ "${AP_PRIMARY_KEY_0}" != "" ]; then
                iwconfig ${APNAME} enc [${AP_PRIMARY_KEY_0}]
            fi
        fi
        if [ "${RADIO}" = "1" ]; then
            if [ "${AP_WEP_MODE_1}" != "" -a "${AP_WEP_MODE_1}" != "1" ]; then
                iwpriv ${APNAME} authmode ${AP_WEP_MODE_1}
            fi
            if [ "${AP_PRIMARY_KEY_1}" != "" ]; then
                iwconfig ${APNAME} enc [${AP_PRIMARY_KEY_1}]
            fi
        fi
    fi
fi
~ # 