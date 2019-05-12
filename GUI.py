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


class Management(ScreenManager):
    pass


class HomeScreen(Screen,GridLayout):
    pass


class Encode(Screen, GridLayout):

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
        pop = PopUps()
        pop.open()

    def encodePhoto(self):
        # defaults
        self.ids.dir.text = r'testImg.png'
        self.ids.mes.text = open('testMsg.txt', 'r').read()
        self.ids.loc.text = '700 1500'
        self.ids.wid.text = '200'

        image_directory = self.ids.dir.text
        image = Image.open(image_directory)
        message = self.ids.mes.text
        starting_location = (int(self.ids.loc.text.split()[0]), int(self.ids.loc.text.split()[1]))
        message_width = int(self.ids.wid.text)
        print(image_directory, message, starting_location, message_width)
        encoded_image = encode_image(image, message, starting_location, message_width)
        encoded_image.save(image_directory[:-4]+'__encoded.png')

class Decode(Screen, GridLayout):
    pass


class PopUps(Popup):
    pass



presentation = Builder.load_file("GUI.kv")


class FirstApp(App):
    def build(self):
        return presentation


Simple = FirstApp()
Simple.run()