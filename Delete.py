import pyodbc as SQLServer

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton


class Delete(Screen):
	def __init__(self, **kwargs):
		super(Delete, self).__init__(**kwargs)
		self.sql = self.sqlCONNECTION()

		self.teacher_career = ''


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


	def closeStudentDoesntExist(self, *args):
		self.student_doesnt_exist.dismiss()


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
			self.student_doesnt_exist = MDDialog(
				title='Atención',
				text='Este estudiante no existe o fue eliminado.',
				buttons=[
					MDRectangleFlatButton(
						text='Aceptar',
						on_press=self.closeStudentDoesntExist
					)
				]
			)
			self.student_doesnt_exist.open()
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


	def onPressDelStudent(self):
		self.sql.execute(f'EXECUTE deleteStudent \'{self.ids.student_enrollment.text}\'')
		self.sql.commit()
		self.onPressCancelStudent()


	def onPressCancelStudent(self):
		fields = [
			'student_enrollment',
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
		self.ids.student_enrollment.disabled = False
		self.ids.search_student.disabled = False
		for field in fields:
			self.ids[field].text = ''
		self.ids.del_student.disabled = True
		self.ids.cancel_student.disabled = True

	###################################### T E A C H E R #############################################
	def closeNoExistingTeacher(self, *args):
		self.no_existing_teacher.dismiss()


	def noExistingTeacher(self):
		self.no_existing_teacher = MDDialog(
			title='Atención.',
			text='El profesor no existe.',
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=self.closeNoExistingTeacher
				)
			]
		)
		self.no_existing_teacher.open()


	def delCareers(self, career:list):
		self.ids.teacher_no_scroll.pos_hint = {'center_x': -1}

		layout = self.ids.show_teacher_careers

		layout.clear_widgets()
		
		n = 0
		for c in career:
			n += 1
			del self.ids[f'A{n}']


	def onPressTeacherCareer(self):
		layout = self.ids.show_teacher_careers
		#layout.cols = 1
		#layout.row_default_height = 10
		
		if self.ids.teacher_enrollment.text != '':

			careers = self.sql.execute(f'EXECUTE dbo.getTeacherCareers \'{self.ids.teacher_enrollment.text}\'')
			career = []
			for c in careers:
				career.append(c[0])

			if career != []:
				self.ids.teacher_no_scroll.pos_hint = {'center_x': .5}
				n = 0
				for c in career:
					n += 1
					c = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{c}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		screen = app.root.get_screen('del')
		screen.ids.teacher_careers.text = A{n}.text[:3] + '...'
		screen.teacher_career = A{n}.text
		screen.delCareers({career})
					"""
					self.ids[f'A{n}'] = Builder.load_string(c)
					layout.add_widget(self.ids[f'A{n}'])

			else:
				self.noExistingTeacher()
		else:
			self.noExistingTeacher()


	def getTeacher(self):
		if self.ids.teacher_careers.text == 'Carrera':
			self.noExistingTeacher()
		
		else:
			getting = self.sql.execute(f'EXECUTE getTeacherInfo {self.ids.teacher_enrollment.text}, \'{self.teacher_career}\'')
			for got in getting:
				data = [
					got[0], got[1], got[2], got[3],
					got[4], got[5], got[6], got[7]
				]
			
			fields = [
				'teacher_faculty',
				'teacher_career',
				'teacher_middle_name',
				'teacher_last_name',
				'teacher_name',
				'teacher_email',
				'teacher_password',
				'teacher_status'
			]

			n = 0
			for field in fields:
				self.ids[field].text = data[n]
				n += 1

			self.ids.cancel_teacher.disabled = False
			self.ids.del_teacher.disabled = False
			self.ids.teacher_enrollment.disabled = True
			self.ids.teacher_careers.disabled = True
			self.ids.search_teacher.disabled = True


	def onPressDelTeacher(self):
		self.sql.execute(f'EXECUTE deleteTeacher \'{self.ids.teacher_enrollment.text}\', \'{self.teacher_career}\'')
		self.sql.commit()
		self.onPressCancelTeacher()


	def onPressCancelTeacher(self):
		fields = [
			'teacher_faculty',
			'teacher_career',
			'teacher_middle_name',
			'teacher_last_name',
			'teacher_name',
			'teacher_email',
			'teacher_password',
			'teacher_status'
		]
		self.teacher_career = ''
		self.ids.teacher_enrollment.disabled = False
		self.ids.teacher_careers.disabled = False
		self.ids.teacher_careers.text = 'Carrera'
		self.ids.search_teacher.disabled = False
		for field in fields:
			self.ids[field].text = ''
		self.ids.del_teacher.disabled = True
		self.ids.cancel_teacher.disabled = True



