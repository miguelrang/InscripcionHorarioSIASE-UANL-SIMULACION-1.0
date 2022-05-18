import pyodbc as SQLServer

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

class Mod(Screen):
	def __init__(self, **kwargs):
		super(Mod, self).__init__(**kwargs)
		self.sql = self.sqlCONNECTION()

		self.student_faculty = ''
		self.student_career = ''

		self.teacher_career = ''

		self.schedule_faculty = ''
		self.schedule_classroom = ''
		self.choose_schedule = ''


	def sqlCONNECTION(self):
		try:
			connect = SQLServer.connect('Driver={ODBC Driver 17 for SQL Server};'
										'Server=LAPTOP-CF0NC87S;'
										'Database=UANL;'
										'Trusted_Connection=yes')
			sql = connect.cursor()
			return sql
		except:
			print("Error Connection")


	def closeStudentDialog(self, *args):
		self.student_dialog.dismiss()


	def studentDialog(self, text):
		self.student_dialog = MDDialog(
			title='Atención',
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=self.closeStudentDialog
				)
			]
		)
		self.student_dialog.open()


	def getStudent(self):
		enrollment = self.ids.student_enrollment.text
		if enrollment == '':
			enrollment = '0'

		getting = self.sql.execute(f'EXECUTE getStudentInfo {enrollment}')
		faculty = ''
		for got in getting:
			faculty = got[0]
			data = [
				got[0], got[1], got[2], got[3],
				got[4], got[5], got[6], got[7],
				got[8]
			]

		if faculty == '':
			self.studentDialog('Este estudiante no existe o fue eliminado.')
		else:
			fields = [
				'student_faculty',
				'student_career',
				'middle_name',
				'last_name',
				'name',
				'date_birth',
				'email',
				'password',
				'student_status'
			]
			n = 0
			for field in fields:
				if field == 'date_birth':
					data[n] = str(data[n]).replace('-', '/')
				self.ids[field].text = data[n]
				n += 1

			self.ids.cancel_student.disabled = False
			self.ids.del_student.disabled = False
			self.ids.student_enrollment.disabled = True
			self.ids.search_student.disabled = True


	def delShowing(self, complete_layout, layout, layout_no_scroll, data:list):
		
		self.ids[complete_layout].disabled = False

		self.ids[layout_no_scroll].pos_hint = {'center_x': -1}

		self.ids[layout].clear_widgets()
		
		n = 0
		for d in data:
			n += 1
			del self.ids[f'A{n}']


	def Showing(self, complete_layout, layout, layout_no_scroll, execute, max_len, widget):
		layout=self.ids[layout]
		layout.clear_widgets()
		complete_layout=self.ids[complete_layout]
		complete_layout.disabled = True
		#layout.cols = 1
		#layout.row_default_height = 10
		
		content = self.sql.execute(f'EXECUTE {execute}')
		data = []
		for d in content:
			data.append(d[0])

		layout_no_scroll = self.ids[layout_no_scroll]
		layout_no_scroll.pos_hint = {'center_x': .5}
		n = 0
		for d in data:
			print(d)
			n += 1
			d = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{d}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: .9, .5, 0, 1
	on_press: 
		screen = app.root.get_screen('mod')
		if len(A{n}.text) >= {max_len}: \
			len_d = A{n}.text[:{max_len}] + '...'
		else: \
			len_d = A{n}.text
		screen.ids['{widget}'].text = len_d
		screen.{widget} = A{n}.text
		screen.delShowing('{complete_layout.name}', '{layout.name}', '{layout_no_scroll.name}', {data})
					"""
			self.ids[f'A{n}'] = Builder.load_string(d)
			layout.add_widget(self.ids[f'A{n}'])


	def onPressStudentFaculty(self):
		self.Showing(
			'student_data', # complete layout
			'show_student', # layout
			'student_no_scroll', # no scroll layout
			'getFaculties', # execute
			35, # max len
			'student_faculty' # name var
		)


	def onPressStudentCareer(self):
		if self.ids.student_faculty.text == 'Facultad':
			self.studentDialog('No ha Seleccionado ninguna facultad.')

		else:
			self.Showing(
				'student_data', # complete layout
				'show_student', # layout
				'student_no_scroll', # no scroll layout
				f'getCareers {self.student_faculty}', # execute
				35, # max len
				'student_career' # name var
			)



