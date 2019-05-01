import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class Management(ScreenManager):
    pass


class HomeScreen(Screen,GridLayout):
    pass


class Encode(Screen, GridLayout):


    def update(self):
        self.ids.img.source = self.ids.dir.text





class Decode(Screen, GridLayout):
    pass

'''
class SimplePopUp(Popup):
    def displayImage(self, selection):
        return selection
'''


presentation = Builder.load_file("GUI.kv")


class FirstApp(App):
    def build(self):
        return presentation


Simple = FirstApp()
Simple.run()