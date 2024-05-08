import network
import socket
import time
from machine import Pin
import _thread
import gc

def setup_socket():
    global s
    try:
        s.close()  # Close the socket if it's already open
    except:
        pass  # Ignore errors if the socket is not open
    
    # Set up socket to listen for UDP packets
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    print('Listening on', addr)

def yellow_thread():
    global yellow_thread_running
    while yellow_thread_running:
        gpio_pin.value(0)
        time.sleep(0.25)
        gpio_pin.value(1)
        time.sleep(0.25)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid = ''
password = ''
wlan.connect(ssid, password)

max_wait = 30  # Increase the timeout to 30 seconds

while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection... ({}s remaining)'.format(max_wait))
    time.sleep(1)

if wlan.status() != 3:
    print('Network connection failed')
    print('Connection status:', wlan.status())
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP address:', status[0])
    
    # Set up onboard LED connected to GPIO25 pin
    led = Pin("LED", Pin.OUT)
    led.value(1)  # Turn on the onboard LED

# Set up GPIO17 pin as output
gpio_pin = Pin(17, Pin.OUT)

yellow_thread_running = False


while True:  # Main loop to continuously restart the code
    try:
        setup_socket()

        while True:  # Inner loop to handle socket operations
            data, addr = s.recvfrom(1024)  # Receive data and address from the client
            command = data.decode('utf-8')
            
            if command == "green":
                yellow_thread_running = False
                gpio_pin.value(0)
                
            elif command == "red":
                yellow_thread_running = False
                gpio_pin.value(1)
            elif command == "yellow":
                if not yellow_thread_running:
                    yellow_thread_running = True
                    _thread.start_new_thread(yellow_thread, ())
            else:
                yellow_thread_running = False
                gpio_pin.value(0)
            print("Received command: {}, Free memory is {} Bytes".format(command, gc.mem_free()))
            gc.collect()
    except OSError as e:
        print('Error during data reception:', e)
        s.close()
        print('Socket closed')
        time.sleep(1)  # Wait for a moment before restarting
    except Exception as ex:
        print('An unexpected error occurred:', ex)
        s.close()
        print('Socket closed')
        time.sleep(1)