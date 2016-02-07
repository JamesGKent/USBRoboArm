# USBRoboArm
This python library provides an interface to control the USB robotic arm available from maplin:  
http://www.maplin.co.uk/p/usb-controlled-robotic-arm-kit-a37jn  
the libary exposes a simple interface by creating an object for the arm, and calling methods of it to move:
```
from usbroboarm import Arm
import time

arm = Arm()
arm.base_left()
time.sleep(0.5)
arm.base_stop()
```

Every movement command except the stop commands can be passed an optional duration argument:
```
arm.base_left(0.5)
```
This argument is in seconds, and is a blocking call, ie you cannot do anything else until the move has completed.  
calling with a duration as above is equivelant to doing:
```
arm.base_left()
time.sleep(0.5)
arm.base_stop()
```

By exposing a method to start a movement and a method to stop the movement means we can 'add' movements together:
```
arm.base_left()
arm.shoulder_up()
arm.wrist_up()
time.sleep(0.5)
arm.base_stop()
arm.shoulder_stop()
arm.wrist_stop()
```  
To halt all movement the function
```
arm.stop_moving()
```

Planned improvements:  
1) asyncronous delays (non blocking call with a duration)  
2) add connect and disconnect methods
