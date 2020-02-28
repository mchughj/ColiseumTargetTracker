# ColiseumTargetTracker

In the last week in February my brother visited Seattle and showed me a new addition to the 
[Coliseum V Facility](https://coliseumv.com/).  On the playfield are two separate mounted 
slingshots from which players attempt to launch a ball into their opponent's goal.  The goals 
are converted 250 gallon water containers with an aluminum housing around them.  They look like
this.

![Entire Goal](images/Goal-Full.jpg)

The goal in the center of the target is 18" wide by 23" tall. 

My brother asked if I could build a system for tracking successful goals and showing a point total for an ongoing game.  

To keep things simple we decided to go with Raspberry Pi with directly connected monitors for the display.  While I was 
really excited to replicate a huge 7 segment display that I had seen before (the 
[ninja timer project](https://learn.adafruit.com/ninja-timer-giant-7-segment-display)) a monitor requires far less
manual labor (no need to build the custom 7 segment display) and it provides the option to create animations and 
future flexibility.  

## Sensors

An important component of the installation is the ability to detect when a shot goes into the goal and react 
automatically.  While there will be buttons on the control panel to manually increase or decrease the score 
(to handle false positives and false negatives) these are intended to be used rarely if at all.  There are a 
number of options that are being considered.

### Ultrasonic

The idea here is to mount, within an acrylic enclosure, a simple HC-SR04 Ultrasonic sensor.  Using a voltage divider 
to protect the 3.3v pin (1k resistor and then 2k resistor) we can meansure the distance to the nearest object and then react if there is a change.  See [this example](https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi) for a general tutorial.

### Vibration sensor

The idea is that a ball striking the interior of the enclosure can be recognized using a tuned vibration sensor 
similar to the [Hiletgo SW-420](https://www.amazon.com/gp/product/B00HJ6ACY2/).  I am thinking that this one will 
be difficult to tune and get correct - even when using multiple of them.  The potential for false positives when
a ball strikes the outside exists even when using multiple sensors.  I won't really know until I get to the facility.

### Weight sensor

The idea here is that a board across the bottom of the goal area can have weight sensors on it to recognize when the 
ball is within the goal.  This won't recognize when the ball hits in and bounces out.  Something like the [HX711](https://www.amazon.com/gp/product/B079FTXR7Y/) may work.
