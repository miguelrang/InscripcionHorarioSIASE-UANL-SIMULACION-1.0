import pyodbc as SQLServer

from kivy.core.window import Window

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton


class Delete(Screen):
	def __init__(self, **kwargs):
		super(Delete, self).__init__(**kwargs)
		self.sql = self.sqlCONNECTION()

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
	line_color: .9, .5, 0, 1
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


	################################### S C H E D U L E #######################################
	def closeDialogSchedule(self, *args):
		self.dialog_schedule.dismiss()


	def dialogSchedule(self, text):
		self.dialog_schedule = MDDialog(
			title='Atención.',
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=self.closeDialogSchedule
				)
			]
		)
		self.dialog_schedule.open()


	def delScheduleFaculties(self, faculty:list):
		self.ids.schedule_no_scroll.pos_hint = {'center_x': -1}

		layout = self.ids.show_schedule
		self.ids.classroom_and_schedule.disabled = False
		layout.clear_widgets()
		
		n = 0
		for f in faculty:
			n += 1
			del self.ids[f'A{n}']


	def onPressScheduleFaculty(self):
		layout = self.ids.show_schedule
		layout.clear_widgets()
		self.ids.classroom_and_schedule.disabled = True
		#layout.cols = 1
		#layout.row_default_height = 10
		
		faculties = self.sql.execute(f'EXECUTE dbo.getFaculties')
		faculty = []
		for f in faculties:
			faculty.append(f[0])

		self.ids.schedule_no_scroll.pos_hint = {'center_x': .5}
		n = 0
		for f in faculty:
			n += 1
			f = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{f}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: .9, .5, 0, 1
	on_press: 
		screen = app.root.get_screen('del')
		if len(A{n}.text) >= 23: \
			len_faculty = A{n}.text[:23] + '...'
		else: \
			len_faculty = A{n}.text
		screen.ids.schedule_faculty.text = len_faculty
		screen.schedule_faculty = A{n}.text
		screen.delScheduleFaculties({faculty})
					"""
			self.ids[f'A{n}'] = Builder.load_string(f)
			layout.add_widget(self.ids[f'A{n}'])


	def delScheduleClassrooms(self, classroom):
		self.ids.schedule_no_scroll.pos_hint = {'center_x': -1}

		layout = self.ids.show_schedule

		self.ids.classroom_and_schedule.disabled = False
		layout.clear_widgets()
		
		n = 0
		for c in classroom:
			n += 1
			del self.ids[f'A{n}']


	def onPressScheduleClassroom(self):
		layout = self.ids.show_schedule
		layout.clear_widgets()
		#layout.cols = 1
		#layout.row_default_height = 10
		
		if self.ids.schedule_faculty.text == 'Seleccionar Facultad':
			self.dialogSchedule('No has seleccionado una facultad.')

		else:
			classrooms = self.sql.execute(f'EXECUTE dbo.getClassrooms \'{self.schedule_faculty}\'')
			classroom = []
			for c in classrooms:
				classroom.append(c[0])

			if classroom == []:
				self.dialogSchedule('Esta facultad no cuenta con aulas.')
			
			else:
				self.ids.classroom_and_schedule.disabled = True
				self.ids.schedule_no_scroll.pos_hint = {'center_x': .5}
				n = 0
				for c in classroom:
					n += 1
					c = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{c}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: .9, .5, 0, 1
	on_press: 
		screen = app.root.get_screen('del')
		if len(A{n}.text) >= 23: \
			clsroom = A{n}.text[:23] + '...'
		else: \
			clsroom = A{n}.text
		screen.ids.schedule_classroom.text = clsroom
		screen.schedule_classroom = A{n}.text
		screen.delScheduleClassrooms({classroom})
						"""
					self.ids[f'A{n}'] = Builder.load_string(c)
					layout.add_widget(self.ids[f'A{n}'])


	def setAvailableSchedules(self, got:list):
		got.sort()
		self.ids.unavailable_schedule.text = ''
		for g in got:
			self.ids.unavailable_schedule.text += g

		text = '''07:00-07:30;07:30-08:00;
				  08:00-08:30;08:30-09:00;
				  09:00-09:30;09:30-10:00;
				  10:00-10:30;10:30-11:00;
				  11:00-11:30;11:30-12:00;
				  12:00-12:30;12:30-13:00;
				  13:00-13:30;13:30-14:00;
				  14:00-14:30;14:30-15:00;
				  15:00-15:30;15:30-16:00;
				  16:00-16:30;16:30-17:00;
				  17:00-17:30;17:30-18:00;
				  18:00-18:30;18:30-19:00;
				  19:00-19:30;19:30-20:00;
				  20:00-20:30;20:30-21:00;
				  21:00-21:30;21:30-22:00;'''
		text = text.replace('\n', '')
		text = text.replace(' ', '')
		text = text.replace('\t', '')
		for m in self.ids.unavailable_schedule.text.split(';'):
			text = text.replace(f'{m};', '')

		self.ids.available_schedule.text = text


	def onPressScheduleAccept(self):
		if self.ids.schedule_faculty.text == 'Seleccionar Facultad':
			self.dialogSchedule('No has seleccionado ninguna facultad.')

		elif self.ids.schedule_classroom.text == 'Seleccionar Carrera':
			self.dialogSchedule('No has seleccionado ningun aula')

		else:
			get = self.sql.execute(f'EXECUTE getSchedules [{self.schedule_faculty}], [{self.schedule_classroom}]')
			got = []
			for g in get:
				got.append(g[0])

			if got == []:
				self.dialogSchedule('No hay horarios agregados para esta aula.')

			else:
				self.setAvailableSchedules(got)

				classroom = [
					'schedule_faculty',
					'schedule_classroom',
					'schedule_accept',
					'banches',
					'cancel_classroom',
					'del_classroom',
					'continue_classroom'
				]
				for widget in classroom:
					if widget == 'banches':
						get = self.sql.execute(f'EXECUTE getBanches [{self.schedule_faculty}], [{self.schedule_classroom}]')
						for g in get:
							self.ids[widget].text = str(g[0])

					else:
						self.ids[widget].disabled = not self.ids[widget].disabled


	def restartClassroom_Schedule(self):
		first_part = [
			'schedule_faculty',
			'schedule_classroom',
			'banches',
			'schedule_accept',
			'cancel_classroom',
			'update_classroom',
			'continue_classroom'
		]
		count = 0
		for widget in first_part:
			self.ids[widget].disabled = False

			if count == 0:
				self.ids[widget].text = ''
				self.ids[widget].text = 'Seleccionar Facultad'
				
			if count == 1:
				self.ids[widget].text = ''
				self.ids[widget].text = 'Seleccionar Aula'

			if count == 2:
				self.ids[widget].text = ''
				self.ids[widget].disabled = True

			if count == 4:
				#self.ids[widget].text = ''
				self.ids[widget].disabled = True
			
			if count == 5:
				#self.ids[widget].text = ''
				self.ids[widget].disabled = True
			
			if count == 6:
				#self.ids[widget].text = ''
				self.ids[widget].disabled = True
				
			count += 1

		second_part = [
			'available_schedule',
			'unavailable_schedule',
			'choose_schedule',
			'schedule_career',
			'schedule_teacher',
			'cancel_all_schedule',
			'del_all_schedule',
			'del_schedule',
		]
		count = 0
		for widget in second_part:
			self.ids[widget].disabled = True
			self.ids[widget].text = ''
			if count == 2:
				self.ids[widget].text = 'Seleccionar Horario'

			if count == 5:
				self.ids[widget].text = 'Cancelar Todo'

			if count == 6:
				self.ids[widget].text = 'Eliminar Horarios'

			if count == 7:
				self.ids[widget].text = 'Eliminar Horario'

			count += 1


	def onPressDelClassroom(self):
		self.sql.execute(f'EXECUTE deleteClassroom [{self.schedule_faculty}], [{self.schedule_classroom}]')
		self.sql.commit()
		self.restartClassroom_Schedule()
		self.schedule_faculty = ''
		self.schedule_classroom = ''
		self.choose_schedule = ''


	def onPressContinueClassroom(self):
		schedules = self.sql.execute(f'EXECUTE dbo.getSchedules [{self.schedule_faculty}], [{self.schedule_classroom}]')
		schedule = []
		for s in schedules:
			schedule.append(s[0])

		if schedule == []:
			self.dialogSchedule('No hay horario disponibles.')
			self.restartClassroom_Schedule()
			self.schedule_faculty = ''
			self.schedule_classroom = ''
			self.choose_schedule = ''
		
		else:
			classroom = [
				'schedule_faculty',
				'schedule_classroom',
				'continue_classroom',
				'banches',
				'cancel_classroom',
				'del_classroom',
				'continue_classroom'
			]
			for widget in classroom:
				self.ids[widget].disabled = True

			self.ids.choose_schedule.disabled = False
			self.ids.del_all_schedule.disabled = False
			self.ids.cancel_all_schedule.disabled = False


	def delChooseSchedule(self, schedule):
		self.ids.schedule_no_scroll.pos_hint = {'center_x': -1}

		layout = self.ids.show_schedule
		self.ids.classroom_and_schedule.disabled = False

		layout.clear_widgets()
		
		n = 0
		for s in schedule:
			n += 1
			del self.ids[f'A{n}']

		get = self.sql.execute(f'EXECUTE getC_T [{self.schedule_faculty}], [{self.schedule_classroom}], [{self.choose_schedule}]')
		for g in get:
			self.ids.schedule_career.text = g[0]
			self.ids.schedule_teacher.text = f'{g[1]} {g[2]} {g[3]}'
		self.ids.del_schedule.disabled = False


	def onPressChooseSchedule(self):
		layout = self.ids.show_schedule
		layout.clear_widgets()
		#layout.cols = 1
		#layout.row_default_height = 10

		self.ids.schedule_career.text = ''
		self.ids.schedule_teacher.text = ''
		self.ids.del_schedule.disabled = True
		schedules = self.sql.execute(f'EXECUTE dbo.getSchedules [{self.schedule_faculty}], [{self.schedule_classroom}]')
		schedule = []
		for s in schedules:
			schedule.append(s[0])

		if schedule == []:
			self.dialogSchedule('No hay mas horarios por eliminar.')
			self.restartClassroom_Schedule()
			self.schedule_faculty = ''
			self.schedule_classroom = ''
			self.choose_schedule = ''
		
		else:
			self.ids.classroom_and_schedule.disabled = True
			self.ids.schedule_no_scroll.pos_hint = {'center_x': .5}
			n = 0
			for s in schedule:
				print(s)
				print(s)
				print(s)
				print(s)
				print(s)
				print(s)
				print(s)
				
				n += 1
				s = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{s}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: .9, .5, 0, 1
	on_press: 
		screen = app.root.get_screen('del')
		if len(A{n}.text) > 50: \
			c_s = A{n}.text[:50] + '...'
		else: \
			c_s = A{n}.text
		screen.ids.choose_schedule.text = c_s
		screen.choose_schedule = A{n}.text
		screen.delChooseSchedule({schedule})
					"""
				self.ids[f'A{n}'] = Builder.load_string(s)
				layout.add_widget(self.ids[f'A{n}'])


	def onPressDelAllSchedule(self):
		self.sql.execute(f'EXECUTE restartClassroom [{self.schedule_faculty}], [{self.schedule_classroom}]')
		self.sql.commit()
		self.restartClassroom_Schedule()
		self.schedule_faculty = ''
		self.schedule_classroom = ''
		self.choose_schedule = ''
		self.dialogSchedule('Se han eliminado todos los horarios satisfactoriamente.')


	def onPressDelSchedule(self):
		self.sql.execute(f'EXECUTE deleteSchedule [{self.schedule_faculty}], [{self.schedule_classroom}], [{self.choose_schedule}]')
		self.sql.commit()
		self.ids.choose_schedule.text = 'Seleccionar Horario'
		self.ids.schedule_career.text = ''
		self.ids.schedule_teacher.text = ''
		
		get = self.sql.execute(f'EXECUTE getSchedules [{self.schedule_faculty}], [{self.schedule_classroom}]')
		got = []
		for g in get:
			got.append(g[0])	
		self.setAvailableSchedules(got)
		
		if got == []:
			self.dialogSchedule('No hay mas horarios por eliminar de esta Aula')
			self.restartClassroom_Schedule()
			self.schedule_faculty = ''
			self.schedule_classroom = ''
			self.choose_schedule = ''


	def resizeWindow(self):
		Window.size = 1100, 650
		Window.left = (1400 - 1100)/2
		Window.top = ( 750 - 650)/2


	def resizeWindowAdd(self):
		Window.size = 1100, 650
		Window.left = 150
		Window.top = (750 - 650)/2


	def resizeWindowDel(self):
		Window.size = 500, 650
		Window.left = 400
		Window.top = (750 - 650)/2


	def resizeWindowLogin(self):
		Window.size = 700, 450
		Window.left = 300
		Window.top = (750 - 650)*2


	def resizeWindowLogout(self):
		self.resizeWindowDel()

