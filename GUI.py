
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.config import Config
import re


# sets the window to a static unchangable size
Config.set('graphics', 'resizable', False)

from StartStopBitCodec import *
from SendReceiveImage import  *

from PIL import Image
import kivy
import _thread
import time
kivy.require('1.9.1')

# object that handles the screen switching
class Management(ScreenManager):
    pass

# home screen object
class HomeScreen(Screen,GridLayout):
    pass

# encode screen object
class Encode(Screen, GridLayout):
    # function to check whether the user has inputted a valid directory, so the image can be displayed
    # in case the directory is invalid, image source defaults to the value of None, and displays nothing
    def update(self):
        self.ids.img.source = self.ids.dir.text

    # function that encodes the photo, based off of user inputted data in the GUI
    def encode_image(self):
        #  defaults
        #  self.ids.dir.text = r'testImg.png'
        #  self.ids.mes.text = open('testMsg.txt', 'r').read()
        #  self.ids.loc.text = '700 1500'
        #  self.ids.wid.text = '200'

        image_directory = self.ids.dir.text
        image = Image.open(image_directory)
        message = self.ids.mes.text
        starting_location = re.sub('\s', '', self.ids.loc.text).split(',')
        starting_location = (int(starting_location[0]), int(starting_location[1]))
        message_width = int(self.ids.wid.text)
        print(image_directory, message, starting_location, message_width)
        encoded_image = encode_image(image, message, starting_location, message_width)

        encoded_image_dir = image_directory[:-4]+'__encoded.png'

        encoded_image.save(encoded_image_dir)



        popup = encPU()
        popup.ids.answer.text = send_image(encoded_image_dir, self.ids.ip.text)
        popup.open()


# decode screen object
class Decode(Screen, GridLayout):
    decoded_msg = ''
    # function that decodes the image
    def decode_image(self):
        #  self.ids.dir2.text = 'testImg__encoded.png'

        image_directory = self.ids.dir2.text

        self.decoded_msg = decode_image(Image.open(image_directory))
        print(self.decoded_msg)
    # function that opens up the popup
    def firePopup(self):
        PU = decPU()
        PU.open()
        PU.ids.decodedLabel.text = self.decoded_msg.strip()

    #  function to check whether the user has inputted a valid directory, so the image can be displayed
    def update(self):
        self.ids.img2.source = self.ids.dir2.text

# decode popup object
class decPU(Popup):
    pass

# received image popup object
class ReceivedPopup(Popup):
    receive = None
    pu = None
    image_dir = ''

    @staticmethod
    def update():
        pass
    #      ReceivedPopup.pu.ids.received_image.source = '280px-PNG_transparency_demonstration_1.png'
    #      print(ReceivedPopup.pu.ids.received_image.source)

    @staticmethod
    def acceptIMG(accept):
        ReceivedPopup.pu.receive = accept

    @staticmethod
    def show_popup():
        ReceivedPopup.pu = ReceivedPopup()
        ReceivedPopup.pu.open()
        while ReceivedPopup.pu.receive is None:
            print(ReceivedPopup.pu.receive)
            time.sleep(0.5)
        return ReceivedPopup.pu.receive

    @staticmethod
    def display_image(dir):
        ReceivedPopup.pu.image_dir = dir
        print(ReceivedPopup.pu.image_dir)
        ReceivedPopup.pu.update()

class encPU(Popup):
    pass


# translates the .kv file and links it to the .py file
presentation = Builder.load_file("GUI.kv")


# runs the GUI as an application
class Pencode(App):
    def build(self):
        return presentation


    def wait_for_image(self):
        _thread.start_new_thread(recv_image, (ReceivedPopup.show_popup, ReceivedPopup.display_image))

