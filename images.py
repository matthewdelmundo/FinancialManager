import re
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image

#Designate our .kv design file
Builder.load_file('images.kv')

class Images(Widget):
	def __init__ (self, percent, **kwargs):
		super(Images, self).__init__(**kwargs)
		Window.size = (338, 600)
		
		self.ids.color_type.allow_stretch = True
		self.ids.color_type.keep_ratio = False

		if percent <= 100 and percent >= 50:
			self.ids.color_type.source = 'images/green.png'
		elif percent < 50 and percent >= 25:
			self.ids.color_type.source = 'images/yellow.png'
		elif percent < 25 and percent >= 0:
			self.ids.color_type.source = 'images/red.jpg'


# App Build
class ScreenApp(App):
    def build(self):
    	percent = 100
    	return Images(percent)


if __name__ == '__main__':
	ScreenApp().run()