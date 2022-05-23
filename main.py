import pyodbc as SQLServer

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'position', 'custom')
#from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
#from kivy.clock import Clock

from Login import Login
from SIASE import SIASE
from Rectoria import Rectoria
from Add import Add
from Mod import Mod
from Delete import Delete 

from nltk.tokenize import word_tokenize

from datetime import datetime
import random
import os
import re

#from PIL import Image
#img = Image.open("images/yellow2.png")
#img = img.resize((25, 25), Image.ANTIALIAS)
#img.save("images/yellow.png")


class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)


class main(MDApp):
	def build(self):
		self.icon = "images/icon.png"

		self.title = "Servicios en Linea"
		Window.size = (700, 450)
		self.theme_cls.theme_style = "Light"
		
		return Builder.load_file("Design.kv")
			
	def on_start(self):
		#Window.size = 500, 700
		#Window.left = (1400 - 1100)*2#1.3
		#Window.top = 200#301

		Window.size = 500, 650
		Window.left = 400
		Window.top = (750 - 650)/2
		self.root.current = "add"
		pass

def sqlCONNECTION():
	try:
		connect = SQLServer.connect('Driver={ODBC Driver 17 for SQL Server};'
									'Server=LAPTOP-CF0NC87S;'
									'Database=UANL;'
									'Trusted_Connection=yes')
		sql = connect.cursor()
		return sql
	except:
		print("Error connection")

if __name__ == "__main__":
	#sql = sqlCONNECTION()
	main().run()
