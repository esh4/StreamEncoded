from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.config import Config

Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '750')


from StartStopBitCodec import *
from PIL import Image
import kivy
kivy.require('1.9.1')

from kivy.config import Config


Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '750')


from StartStopBitCodec import encode_image, decode_image

class Management(ScreenManager):
    pass


class HomeScreen(Screen,GridLayout):
    pass


class Encode(Screen, GridLayout):
    self.ids.dir.text = r'testImg.png'
    self.ids.mes.text

    def update(self):
        self.ids.img.source = self.ids.dir.text

    def switch(self, current, next):
        self.screens = ["width", "directory", "message", "location"]
        self.index = self.screens.index(current)
        if(self.index == 3):
            self.index = 0
        elif(self.index == -1):
            self.index = 3

        if(next == "up"):
            self.index += 1
        elif(next == "down"):
            self.index -= 1

        self.update()
        return self.screens[self.index]

    def firePopup(self):
        pop = encPU()
        pop.open()

    def encodePhoto(self):
        image_directory = self.ids.dir.text
        message = self.ids.mes.text
        starting_location = (self.ids.mes.text.split()[0], self.ids.mes.text.split()[1])
        message_width = self.ids.wid.text
        print(image_directory, message, starting_location, message_width)
        # encoded_image = encode_image(self.ids.dir.text, self.ids.mes.text, self.ids.loc, self.ids.wid.text)
        # encoded_image.save(image_directory[:-4]+'__encoded.png')

class Decode(Screen, GridLayout):
    def firePopup(self):
        pop = decPU()
        pop.open()


class encPU(Popup):
    pass


class decPU(Popup):
    pass

presentation = Builder.load_file("GUI.kv")


class FirstApp(App):
    def build(self):
        return presentation


Simple = FirstApp()
Simple.run()