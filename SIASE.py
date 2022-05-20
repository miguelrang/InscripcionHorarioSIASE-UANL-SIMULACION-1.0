import pyodbc as SQLServer

from kivymd.app import MDApp

from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'position', 'custom')

from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDRaisedButton

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


	def settings(
					self,
					background=False,
					scroll=False, 
					layout=False,
					cols=1,
					rgb=(1,1,1),
					scroll_y=True,
					row_default_height=0,
					rows=1,
					size_hint_x=1,
					size_hint_y=1,
					pos_hint={},
					padding=0,
					spacing=0
				):
		if background == True:
			background = self.ids.background
			background.padding = padding
			background.cols = cols
			#background.size_hint_x = size_hint_x
			#background.size_hint_y = size_hint_y

			with background.canvas.before:
				Color(rgb=rgb)
				Rectangle(
					size=background.size,
					pos=background.pos
				)
		
		elif scroll == True:
			self.ids.scroll.do_scroll_y = scroll_y
		
		elif layout == True:
			layout = self.ids.layout
			layout.row_default_height = row_default_height
			layout.cols = cols
			layout.rows = rows
			layout.size_hint_x = size_hint_x
			layout.size_hint_y = size_hint_y
			layout.pos_hint = pos_hint
			layout.padding = padding
			layout.spacing = spacing

			with layout.canvas.before:
				Color(rgb=rgb)
				Rectangle(
					size=layout.size,
					pos=layout.pos
				)


	def addSchedule(self, *args):
		subject = self.subject
		get = self.sql.execute(f'EXECUTE getAvailableSchedules [{self.ids.career.text}], [{subject}]')
		options = []
		option = {}
		for g in get:
			name = f'{g[0]} {g[1]} {g[2]}'
			option['name'] = name
			option['group'] = g[3]
			option['op'] = g[4]
			option['schedule'] = g[5]


	def addSubjects(self, *args):
		self.settings(
			background=True,
			padding=(0,0),
			rgb=(100/255, 100/255, 100/255)
		)
		self.settings(
			scroll=True,
			scroll_y=True
		)
		layout = self.ids.layout
		layout.clear_widgets()
		self.settings(
			layout=True,
			rgb=(1,1,1),
			row_default_height=0,
			cols=2,
			rows=len(self.subjects)+1,
			size_hint_x=1,
			size_hint_y=None,
			pos_hint={'center_x': .6, 'center_y': .389},
			padding=10,
			spacing=1
		)
		sem = MDRaisedButton(
			text='    Sem.',
			theme_text_color='Custom',
			text_color=(19/255, 39/255, 77/255, 1),
			md_bg_color=(226/255, 212/255, 171/255, 1),
			size_hint_x=None
		)
		subj = MDRaisedButton(
			text='  Materia' + ' '*225,
			theme_text_color='Custom',
			text_color=(19/255, 39/255, 77/255, 1),
			md_bg_color=(226/255, 212/255, 171/255, 1),
			size_hint_x=None
		)
		layout.add_widget(sem)
		layout.add_widget(subj)

		count = 1
		for subject in self.subjects:
			if count % 2 == 0:
				color = (1, 1, 1, 1)
			else:
				color = (240/255, 240/255, 240/255, 1)
			self.subject = subject
			sem = MDRaisedButton(
				text=self.kardex[subject]['sem'],
				theme_text_color='Custom',
				text_color=(19/255, 39/255, 77/255, 1),
				md_bg_color=color,
				size_hint_x=.04
			)
			subj = MDRaisedButton(
				text=subject + ' '*(240),
				theme_text_color='Custom',
				text_color=(19/255, 39/255, 77/255, 1),
				md_bg_color=color,
				size_hint_x=5,
				on_press=self.addSchedule
			)
			layout.add_widget(sem)
			layout.add_widget(subj)
			count += 1
			

	def updateSubjects(self, *args):
		pass


	def deleteSubjects(self, *args):
		pass


	def onPressInscription(self):
		get = self.sql.execute(f'EXECUTE getStudentStatus {self.ids.enrollment.text}')
		for g in get:
			status = g[0]

		if status == 'ALTA':
			self.subjects = self.getSubjects()
			layout = self.ids.layout
			#print(subjects)
			
			if type(self.subjects) == bool:
				if self.subjects == True:
					self.Dialog('Atención', 'Usted ya ha concluido su carrera.')

				else:
					self.Dialog('Error', 'Usted ha sido dado de baja de la UANL.')
					self.sql.execute(f'EXECUTE updateStudentStatus {self.ids.enrollment.text},{status}')

			else:
				background = self.ids.background
				self.settings(
					background=True,
					padding=(120,0),
					rgb=(100/255, 100/255, 100/255)
				)
				self.settings(
					scroll=True,
					scroll_y=False
				)
				self.settings(
					layout=True,
					rgb=(1,1,1),
					row_default_height=30,
					cols=1,
					rows=4,
					size_hint_x=.9,
					size_hint_y=.6,
					pos_hint={'center_x': .6, 'center_y': .389},
					padding=10,
					spacing=25
				)
				title = MDLabel(
					text='Inscripción de Horario',
					size_hint_y=.01
				)
				period = MDLabel(
					text='Periodo: Agosto - Diciembre 2022',
					size_hint_y=.01
				)
				extra_layout = GridLayout(
					size_hint_y=.1,
					padding=(70,0),
					cols=2,
					rows=1,
				)
				#
				extra_label = MDLabel(
					text='Tipo de Inscripción:'
				)
				extra_button = MDTextField(
					text='Clase Ordinaria',
					icon_right="arrow-down-drop-circle-outline",
					mode='rectangle',
					disabled=True
				)
				extra_layout.add_widget(extra_label)
				extra_layout.add_widget(extra_button)
				#
				layout_buttons = GridLayout(
					padding=(65, 30),
					spacing=10,
					cols=3,
					rows=1
				)
				#
				button_add = MDRectangleFlatButton(
					text='Agregar Materia',
					on_press=self.addSubjects
				)
				button_upd = MDRectangleFlatButton(
					text='Modificar Horario',
					on_press=self.updateSubjects
				)
				button_del = MDRectangleFlatButton(
					text='Eliminar Materia',
					on_press=self.deleteSubjects
				)
				
				layout_buttons.add_widget(button_add)
				layout_buttons.add_widget(button_upd)
				layout_buttons.add_widget(button_del)
				#
				layout.add_widget(title)
				layout.add_widget(period)
				layout.add_widget(extra_layout)
				layout.add_widget(layout_buttons)
		else:
			self.Dialog(title='Error', text='Usted ha sido dado de baja.')

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


