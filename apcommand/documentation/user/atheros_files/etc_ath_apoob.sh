cat /etc/ath/apoob
#!/bin/sh
apdown
cfg -x
cfg -a WPS_ENABLE=1
cfg -a WPS_ENABLE_2=1
cfg -c
apup
~ # 