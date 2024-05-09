# Haptic Feedback

## Thonny
You will need to download [Thonny](https://thonny.org/) to get this working.

You will need to connect the Pico W to the computer and switch the interpreter at the bottom right of Thonny (once you open main.py) to the MicroPython one. The option will only show up when the Pico W is connected to the computer, and as these devices are finicky, they may need to be plugged/ unplugged a couple of times before they connect (give it at least 10 seconds each time, though). 

Make sure to configure your WiFi ssid and password within the code. Also, you will have to change the gpio_pin variable's output pin on some Picos to 18 instead of 17. Some of them were soldered to 17, and some to 18. 

You can then hit the play button to load the program onto the Pico W.

You'll see the IP address of the Pico in the console. Make sure to put that IP in the client-side Python code or C# code when you run either.

## Client-side
You can run the client.py program if you want to test the haptic feedback by itself, or if you're running the Unity project, it *should* automatically send commands. Again, make sure the IP address in either client.py or CollisionManager.cs matches the IP address you see in the console in Thonny.
