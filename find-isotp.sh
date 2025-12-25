

for i in `seq 0x7e0 0x7e8`
do 
	echo "A" | isotpsend can0 -s $( printf "%x" $i ) -d 0x444 
done
