#!/usr/bin/bash



#data=$(zenity \
#	--entry \
#	--text="Please enter your data" \
#	--entry-text="default") 
#echo $data

#MOUSE_ID=$(xinput --list | grep -i -m 1 'mouse' | grep -o 'id=[0-9]\+' | grep -o '[0-9]\+')
#
#STATE1=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
#while true; do
#    sleep 0.2
#    STATE2=$(xinput --query-state $MOUSE_ID | grep 'button\[' | sort)
#    comm -13 <(echo "$STATE1") <(echo "$STATE2")
#    STATE1=$STATE2
#done


#xdotool getmouselocation --shell
#eval $(xdotool getmouselocation --shell)
#echo $X,$Y


