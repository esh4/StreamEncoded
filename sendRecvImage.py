from Constants import CommunicationConstants
import socket


def send_image(image_dir):
    try:
        # Connect to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 5990))

        # send AWAIT_IMAGE command
        s.send(CommunicationConstants.commands['INCOMING_IMAGE'])

        # send image
        data = open(r'' + image_dir, 'rb').read()

        for i in range(0, len(data), 1024):
            s.send(data[i:i + 1024])

        s.send(CommunicationConstants.commands['END_TX'])
        print('sent!')
    finally:
        s.close()


def recv_image(callback=lambda: x):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5990))
    server_socket.listen(1)
    try:
        (client_socket, client_address) = server_socket.accept()
        print('connected to {}'.format(client_address))

        command = client_socket.recv(1024)
        print(command == CommunicationConstants.commands['INCOMING_IMAGE'])

        if command == CommunicationConstants.commands['INCOMING_IMAGE']:
            print('recving img')
            image_data = b''
            data = b''
            while data != CommunicationConstants.commands['END_TX']:
                print(data)
                data = client_socket.recv(1024)
                if len(data) < 1024:
                    data = data[:-2]
                    print(data[-2:])
                    image_data += data
                    break
                image_data += data

            with open('recv.png', 'wb') as f:
                f.write(image_data)
            callback()
    finally:
        server_socket.close()
        client_socket.close()

if __name__ == '__main__':
    recv_image()
