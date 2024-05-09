import socket
import time

def connect():
    pico_ip = '192.168.0.12'
    pico_port = 80

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    while not connected:
        try:
            print('Connecting to the Raspberry Pi Pico W...')
            sock.connect((pico_ip, pico_port))
            print('Connected to the Raspberry Pi Pico W.')
            connected = True
        except ConnectionError:
            print('Failed to connect to the Raspberry Pi Pico W. Retrying in 1 second...')
            time.sleep(1)
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            break
    return sock

def send_command(sock, command):
    try:
        # Send the command
        sock.sendall(command.encode())
        print(f'Command "{command}" sent successfully.')
    except Exception as e:
        print(f'An error occurred while sending the command: {str(e)}')
        # Attempt to reconnect
        return None
    return sock

def main():
    sock = None
    try:
        while True:
            if sock is None:
                sock = connect()
                if sock is None:
                    continue  # Retry connection
            # Get the command from the user
            command = input('Enter a command (green, yellow, red, or quit): ')
            if command.lower() == 'quit':
                print('Exiting the program.')
                break
            if command.lower() in ['green', 'yellow', 'red']:
                sock = send_command(sock, command.lower())
                print('this is the command: ' + command.lower())
                if sock is None:
                    continue  # Retry connection
            else:
                print('Invalid command. Please enter green, yellow, red, or quit.')

    except Exception as e:
        print(f'An error occurred: {str(e)}')
    finally:
        if sock is not None:
            sock.close()
            print('Disconnected from the Raspberry Pi Pico W.')

if __name__ == '__main__':
    main()
