import pyodbc as SQLServer
from kivy.uix.screenmanager import Screen

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton


class Delete(Screen):
	def __init__(self, **kwargs):
		super(Delete, self).__init__(**kwargs)
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


	def closeStudentDoesntExist(self, *args):
		self.student_doesnt_exist.dismiss()


	def getStudent(self):
		getting = self.sql.execute(f'EXECUTE getStudentInfo {self.ids.student_enrollment.text}')
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
				data[n] = str(data[n]).replace('-', '/')
				self.ids[field].text = data[n]
				n += 1

			self.ids.cancel_student.disabled = False
			self.ids.del_student.disabled = False
			self.ids.student_enrollment.disabled = True
			self.ids.search_student.disabled = True


	def onPressDelStudent(self):
		self.sql.execute(f'EXECUTE deleteStudent \'{self.ids.student_enrollment.text}\'')


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



















