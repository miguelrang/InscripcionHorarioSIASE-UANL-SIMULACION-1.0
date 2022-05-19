import pyodbc as SQLServer

from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'position', 'custom')

#from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from kivy.lang import Builder


class SIASE(Screen):
	def __init__(self, **kwargs):
		super(SIASE, self).__init__(**kwargs)
		
		self.sql = self.sqlCONNECTION()

		self.kardex = {}


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
		

	def closeDialog(self, *args):
		self.dialog.dismiss()


	def Dialog(self, title, text):
		self.dialog = MDDialog(
			title=title,
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=self.closeDialog
				)
			]
		)
		self.dialog.open()
		if text == 'Servicio no Disponible':
			self.kardex = {}


	def validOP(self, subject, op):
		k_op = self.kardex[subject][f'op{op}']
		next_k_op = self.kardex[subject][f'op{op+1}']
		if k_op != '':
			if set(k_op) & set('ACNP'):
				if k_op == 'AC':
					return False

				else:
					if set(next_k_op) & set('ACNP'):
						if next_k_op == 'AC':
							return False

						else:
							return True

					else:
						if int(next_k_op) > 69 and int(next_k_op) < 101:
							return False

						else:
							return True

			else:
				if int(k_op) > 69 and int(k_op) < 101:
					return False

				else:
					if set(next_k_op) & set('ACNP'):
						if next_k_op == 'AC':
							return False

						else:
							return True

					else:
						if int(next_k_op) > 69 and int(next_k_op) < 101:
							return False

						else:
							return True
		
		else:
			return True

	def getSubjects(self):
		get = self.sql.execute(f'EXECUTE getKardex {self.ids.enrollment.text}')
		for g in get:
			self.kardex[g[1]] = {'sem':f'{g[0]}', 'op1':f'{g[2]}', 'op2':f'{g[3]}', 'op3':f'{g[4]}', 'op4':f'{g[5]}', 'op5':f'{g[6]}', 'op6':f'{g[7]}'}
		
		end = 0
		subjects = []
		for subject in self.kardex.keys():
			for op in range(1, 7, 2):
				if op == 5 and self.validOP(subject, op) == False: # DADO DE BAJA
					return False
					break

				if self.validOP(subject, op) == True:
					if subject not in subjects:
						subjects.append(subject)
				else:
					break

			if self.kardex[subject]['op1'] != '':
				end = int(self.kardex[subject]['sem'])

			last = int(self.kardex[subject]['sem'])

		if subjects == [] and end == 0:
			return True

		else:
			end += 2
			if end <= last:
				pass

			elif end-1 <= last:
				end -= 1

			else:
				end -= 2

			for subject in subjects.copy():
				if end >= int(self.kardex[subject]['sem']):
					pass
				else:
					subjects.remove(subject)

		return subjects


	def onPressInscription(self):
		subjects = self.getSubjects()
		print(subjects)
		
		if type(subjects) == bool:
			if subjects == True:
				self.Dialog('Atención', 'Usted ya ha concluido su carrera.')

			else:
				self.Dialog('Error', 'Usted ha sido dado de baja de la UANL.')

		else:
			for subject in subjects:
				pass


	def onPressSchedule(self):
		get = self.sql.execute(f'EXECUTE getStudentSchedule {self.ids.enrollment.text}')


	def onPressKardex(self):
		if self.kardex == {}:
			get = self.sql.execute(f'EXECUTE getKardex {self.ids.enrollment.text}')
			for g in get:
				self.kardex[g[1]] = {'sem':f'{g[0]}', 'op1':f'{g[2]}', 'op2':f'{g[3]}', 'op3':f'{g[4]}', 'op4':f'{g[5]}', 'op5':f'{g[6]}', 'op6':f'{g[7]}'}

		scroll = self.ids.scroll
		scroll.do_scroll_y = True

		layout = self.ids.layout
		layout.clear_widgets()
		layout.size_hint_x = .9
		layout.row_default_height = 38
		layout.padding = 20
		layout.spacing = 1
		layout.cols = 8

		for i in range(0, 8):
			if i == 0:
				text = 'Sem.'
			if i == 1:
				text = '  Materia'
			if i > 1:
				text = f'  OP{i-1}'
			titles = f"""
MDLabel:
	text: '{text}'
	theme_text_color: 'Custom'
	text_color: 19/255, 39/255, 77/255, 1
	md_bg_color: 226/255, 212/255, 171/255, 1
	size_hint_x: .04
			"""
			titles = Builder.load_string(titles)
			layout.add_widget(titles)

		n = 1
		for subject in self.kardex.keys():
			print('bunchausen')
			if (n%2 == 0):
				color = 1, 1, 1, 1
			else:
				color = '240/255, 240/255, 240/255, 1'
			
			sem = f"""
MDLabel:
	text: '{self.kardex[subject]['sem']}'
	theme_text_color: 'Custom'
	text_color: 19/255, 39/255, 77/255, 1
	md_bg_color: {color}
	size_hint_x: .04
			"""
			sem = Builder.load_string(sem)
			layout.add_widget(sem)
			s = f"""
MDLabel:
	text: '{subject}'
	theme_text_color: 'Custom'
	text_color: 19/255, 39/255, 77/255, 1
	md_bg_color: {color}
	size_hint_x: .45
			"""
			s = Builder.load_string(s)
			layout.add_widget(s)
			for i in range(1, 7, 1):
				op = f"""
MDLabel:
	text: '{self.kardex[subject][f'op{i}']}'
	theme_text_color: 'Custom'
	text_color: .1, .29, .54, 1
	md_bg_color: {color}
	size_hint_x: .05
				"""
				op = Builder.load_string(op)
				layout.add_widget(op)
			n += 1


