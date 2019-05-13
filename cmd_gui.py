from .StartStopBitCodec import *

class Menu:
    menu_options = {}

    def __init__(self, options):
        self.menu_options = options

    def show(self):
        i = 0
        for k in self.menu_options:
            print(i, k)
            i += 1

        choice = input()
        return self.menu_options[choice]

class encode_gui:

    def __init__(self):
        # m = Menu({
        #     image_directory:
        # }

        encoding_option = {
            'image_directory': '',
            'message': '',
            'starting_location': (),
            'message_width': 200
        }

    def encode(self):
        image_directory = input('image dir')
        self.message = input('message')
        self.starting_location = input('loc')
        self.message_width = int(input('mes wid'))






if __name__ == '__main__':
    m = Menu({
        'encode': 1,
        'decode': 2
    })

    action = m.show()