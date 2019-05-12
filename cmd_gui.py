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
    image_directory = ''
    def __init__(self):
        m = Menu({
            image_directory: lambda input('image dir'): (self.image_directory = input('image dir'))
        })

    def encode(self):
        image_directory = input('image dir')
        message = input('message')
        starting_location = input('loc')
        message_width = int(input('mes wid'))




if __name__ == '__main__':
    m = Menu({
        'encode': 1,
        'decode': 2
    })

    action = m.show()