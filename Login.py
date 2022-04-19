import pyodbc as SQLServer

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'position', 'custom')

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from datetime import datetime

import random
import re

class Login(Screen):
	#type_ids = ('touch',)
	def __init__(self, **kwargs):
		super(Login, self).__init__(**kwargs)
		self.sql = self.sqlCONNECTION()

		# 'Clock.schedule_interval' function calls the
		# function 'interval' (automatically add the var 'dt').
		# The second parameter says each seconds call the function. 
		Clock.schedule_interval(self.interval, 1)


	def sqlCONNECTION(self):
		try:
			connect = SQLServer.connect('Driver={ODBC Driver 17 for SQL Server};'
										'Server=LAPTOP-CF0NC87S;'
										'Database=UANL;'
										'Trusted_Connection=yes')
			sql = connect.cursor()
			return sql
		except:
			print("Error connection")


	def interval(self, dt):
		# 'datetime.now()' literaly returns the date and
		# the time.
		info = str(datetime.now())
		# We save the date as str (it is desordered(year-month-day))
		date:str = info[:10]
		# We save the time
		time:str = info[11:16]
		# The disordered date is converted as list
		date_disordered:list = info[:10].split("-")
		# We reverse the list to get the ordered date
		date:list = list(reversed(date_disordered))
		# We convert the date list to str
		date:str = ''.join(date)
		# We separate the date (day-month-year)
		ordered_date:str = f"{date[0:2]}-{date[2:4]}-{date[4:8]}"

		# We update the Labels
		self.ids.calendar_text.text = ordered_date
		self.ids.clock_text.text = time


	def onPressType_(self):
		# We get the id of the type account
		type_ = self.ids.type_
		# We get the id of the label
		account_text = self.ids.account_text
		# If the account is in 'Alumno' mode...
		if type_.text == "Alumno                         ":
			# we change to 'Rectoria'...
			type_.text = "Rectoría                         "
			# and the label too is changed
			account_text.text = "Cuenta:"
			account_text.pos_hint = {"center_x": .112, "center_y": .33}
		else: # If the account is 'Rectoria' mode...
			type_.text = "Alumno                         "
			account_text.text = "Estudiante:"
			account_text.pos_hint = {"center_x": .095, "center_y": .33}

		return type_.text


	def onTextAccount(self):
		# We get the text input ID of 'account'
		account = self.ids.account
		# If the disabled var cuntinues being False it means
		# all is ok
		disabled = False
		# Account is always an 'int'
		account.input_filter = "int"
		# This conditional is necesary because if we
		# valid 'int(account.text)' first and the 
		# textinput is empty, the program brakes
		if account.text != "":
			# The student account can not be less than 1000
			# nor greater 2000000, if it happens, invalid input,
			# so, disabled = True
			if int(account.text) < 1000 or int(account.text) >= 2000000:
				disabled = True
		else: # It means the textinput is empty
			# so, it is invalid
			disabled = True
		

		# if diabled = True, password continues disabled
		# else it would be enable
		self.ids.password.disabled = disabled
		if disabled == True:
			# We disable the login button if password or
			# account are not valid
			self.ids.login.disabled = True
			account.background_color = 255/255, 255/255, 255/255, 1
		else:
			# if disabled = False
			# we valid if the password is correct
			self.onTextPassword()
			account.background_color = 168/255, 214/255, 172/255, 1

		return disabled


	def onTextPassword(self):
		disabled = False
		# We get the ID of text input password
		password = self.ids.password
		# The password can not be less than 7 nor greater than 16
		# so, we valid that
		if len(password.text) > 7 and len(password.text) < 17:
			disabled = False
		else:
			if len(password.text) > 20:
				password.text = password.text[:16]
				disabled = False
			else:
				disabled = True

		# we set the enable or disable of login button
		self.ids.login.disabled = disabled
		if disabled == True:
			password.background_color = 255/255, 255/255, 255/255, 1
		else:
			password.background_color = 168/255, 214/255, 172/255, 1

		return disabled


	def onPressHiddenEye(self):
		icon = self.ids.hidden_eye
		password = self.ids.password
		if icon.icon == "eye":
			icon.icon = 'eye-off'
			password.password = True

		else:
			icon.icon = 'eye'
			password.password = False


	def closeAlert(self, *args):
		self.student_exist.dismiss()


	def alert(self):
		self.student_exist = MDDialog(
				title = 'A ocurrido un error.',
				text = 'Usuario o contraseña incorrectos.',
				buttons = [
					MDRectangleFlatButton(
							text = 'Aceptar',
							on_press = self.closeAlert
						)
				]
			)
		self.student_exist.open() 


	def signIn(self):
		if self.ids.account_text.text == "Estudiante:":
			getting = self.sql.execute(f'EXECUTE verifyLoginStudent \'{self.ids.account.text}\', \'{self.ids.password.text}\'')
			for x in getting:
				got = x[0]
			window = "siase"
		else:
			getting = self.sql.execute(f'EXECUTE verifyLoginRector \'{self.ids.account.text}\', \'{self.ids.password.text}\'')
			for x in getting:
				got = x[0]
			window = "rectoria"

		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		print('got', got)
		
		if got != 0:
			app = MDApp.get_running_app()
			app.root.current = window

			if window == 'siase':
				app.root.get_screen(window).infoStudent(self.ids.account.text)
			
			Window.size = 1100, 650
			Window.left = (1400 - 1100)/2
			Window.top = ( 750 - 650)/2
		else:
			self.alert()
