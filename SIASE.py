import pyodbc as SQLServer

from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'position', 'custom')


class SIASE(Screen):
	def __init__(self, **kwargs):
		super(SIASE, self).__init__(**kwargs)
		
		self.sql = self.sqlCONNECTION()


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


	def resizeWindow(self):
		Window.size = 700, 450
		Window.left = 300
		Window.top = (750 - 650)*2


	def infoStudent(self, user):
		tuplee = self.sql.execute(f'EXECUTE getInfo \'{user}\'')

		for info in tuplee:
			data = info
		enrollment = str(data[0])
		name = f"{data[1]} {data[2]} {data[3]}"
		career = f"{data[4]}"
		career = career.replace('LICENCIADO', 'LIC.')
		career = career.replace('LICENCIATURA', 'LIC.')
		career = career.replace('INGENIERO', 'ING.')
		career = career.replace('INGENIERÍA', 'ING.')
		career = career.replace('INGENIERIA', 'ING.')

		self.ids.enrollment.text = enrollment
		self.ids.name.text = name
		self.ids.career.text = career
		






