import socket
from PIL import ImageGrab
from glob import glob
import shutil
import os
import subprocess


def directory(path):
    dirs = glob(path)
    ret = '\nDirectory of' + path + '\n\n'
    for d in dirs:
        ret += '\t\t' + d.split('\\')[-1] + '\n'
    return ret


def serve_data():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5990))
    server_socket.listen(1)

    (client_socket, client_address) = server_socket.accept()
    print('connected to client')

    try:
        command = ''
        while command != 'exit':
            print('waiting for a command')
            command = client_socket.recv(1024)
            print(command)

            data = ''
            command_list = command.split()
            if command_list[0] == 'send_file':
                try:
                    data = open(r''+command_list[1], 'rb').read()
                except IOError:
                    data = 'No such file'

            elif command_list[0] == 'take_screenshot':
                if len(command_list) > 1:
                    file_name = command[1]
                else:
                    file_name = 'screen.jpg'
                im = ImageGrab.grab()
                im.save(file_name)
                data = 'Screenshot captured'
                
            elif command_list[0] == 'dir':
                data = directory(command_list[1])

            elif command_list[0] == 'delete':
                os.remove(command_list[1])
                data = command_list[1] + ' deleted'

            elif command_list[0] == 'copy':
                shutil.copy(command_list[1], command_list[2])
                data = command_list[1] + ' has been copied to ' + command_list[2]

            elif command_list[0] == 'execute':
                subprocess.call(command_list[1])
                data = 'Executing ' + command_list[1]

            # send length of response
            client_socket.send(str(len(data)))

            # send the response 1Mb at a time
            responseString = ''

            # Socket.send only sends strings
            data = str(data)
            for i in range(0, len(data), 1024):
                responseString += data[i:i + 1024]
                client_socket.send(data[i:i + 1024])



    finally:
        client_socket.close()
        server_socket.close()
        print 'Disconnected from client :('


if __name__ == '__main__':
    serve_data()
