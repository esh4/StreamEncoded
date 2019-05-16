from Constants import CommunicationConstants
import socket
from datetime import datetime


def send_image(image_dir, ip='localhost'):
    try:
        # Connect to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 5990))

        # send AWAIT_IMAGE command
        s.send(CommunicationConstants.commands['INCOMING_IMAGE'])

        # send image
        data = open(r'' + image_dir, 'rb').read()
        for i in range(0, len(data), 1024):
            s.send(data[i:i + 1024])
        s.send(CommunicationConstants.commands['END_TX'])

        print('sent!')
        return 'Image send to {}'.format(ip)
    except Exception as e:
        return str(e)
    finally:
        s.close()


def recv_image(accept_image=lambda: False, directory_callback=lambda: False, directory='Downloads'):
    # configure server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5990))
    server_socket.listen(1)
    try:
        while True:
            (client_socket, client_address) = server_socket.accept()
            print('connected to {}'.format(client_address))

            command = client_socket.recv(1024)

            if command == CommunicationConstants.commands['INCOMING_IMAGE'] and accept_image():
                print('receiving img')
                image_data = b''
                data = b''
                while data != CommunicationConstants.commands['END_TX']:
                    data = client_socket.recv(1024)
                    # last chunk will be smaller than 1kB
                    if len(data) < 1024:
                        data = data[:-2]
                        image_data += data
                        break
                    image_data += data

                image_dir = '{}/recv {}.png'.format(directory, datetime.now())
                with open(image_dir, 'wb') as f:
                    f.write(image_data)
                directory_callback(image_dir)
    finally:
        server_socket.close()
        client_socket.close()

if __name__ == '__main__':
    recv_image()
