import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


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
        pass


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