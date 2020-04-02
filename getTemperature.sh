for i in `seq 10`; do
	sudo /opt/vc/bin/vcgencmd measure_temp;
	sleep 1;
done;
