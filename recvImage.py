import socket
import os


def request_data():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket object created'

        s.connect((raw_input('Enter server\'s ip address'), 5990))
        print 'connected to server'

        command = ''
        while command != 'exit':
            command = raw_input('Enter Command:\n')
            s.send(command)

            responseLen = int(s.recv(1024))
            print 'Expected response length: ', responseLen

            # receive the response in chunks
            counter = 0
            response_data = ''
            for i in range(0, responseLen, 1024):
                response_data += s.recv(1024)
                counter += 1
            print 'num of receives: ', counter

            print 'Actual response length: ', len(response_data)

            # sometimes there is overflow, this patches that issue.
            # admittedly not the most elegant of solution, but for now it works so -\_/-
            if len(response_data) < int(responseLen):
                print 'waiting for overflow'
                response_data += s.recv(1024)

            commandList = command.split()

            '''
                Example command:
                    send_file C:\Users\Eshel\pic.jpg
            '''
            if commandList[0] == 'send_file':
                filename = commandList[1].split('\\')[-1]
                with open(filename, 'wb') as f:
                    f.write(response_data)

                # just for test purposes, definitely a bad idea to run any random file that gets sent to us.
                os.system(filename)
            else:
                print 'Response: ', response_data


    finally:
        s.close()

if __name__ == '__main__':
    request_data()
