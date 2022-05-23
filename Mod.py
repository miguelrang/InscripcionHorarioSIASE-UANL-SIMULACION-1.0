import pyodbc as SQLServer

from kivy.core.window import Window

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from nltk.tokenize import word_tokenize
from datetime import datetime

import re

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

		self.actual_student_info = {}

		self.id_faculty = ''
		self.id_career = ''
		self.id_subject = []
		self.old_kardex = {}
		self.actual_kardex = {}
		self.kardex = {}


		self.actual_teacher_info = {}
		self.teacher_faculty = ''
		self.teacher_career = ''

		self.classroom = ''
		self.banches = 0
		self.choose_schedule = ''
		self.new_schedule = ''
		self.schedule_faculty = ''
		self.schedule_classroom = ''


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
		for i in range(2):
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
			self.actual_student_info = {}
			self.student_faculty = data[0]
			self.student_career = data[1]
			self.actual_student_info['student_faculty'] = data[0]
			self.actual_student_info['student_career'] = data[1]
			self.actual_student_info['middle_name'] = data[2]
			self.actual_student_info['last_name'] = data[3]
			self.actual_student_info['name'] = data[4]
			self.actual_student_info['date_birth'] = str(data[5]).replace('-', '/')
			self.actual_student_info['email'] = data[6]
			self.actual_student_info['password'] = data[7]
			self.actual_student_info['student_status'] = data[8]
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
				self.ids[f'{field}'].text = data[n]
				
				n += 1

			self.ids.cancel_student.disabled = False
			self.ids.update_student.disabled = True
			self.ids.editable_student.disabled = False
			self.ids.student_enrollment.disabled = True
			self.ids.search_student.disabled = True


	def studentEquals(self):
		equal = True
		to_continue = True
		info = self.actual_student_info
		
		if self.ids.student_faculty.text != 'Facultad' and self.student_faculty != info['student_faculty']:
			print(1)
			print(1)
			print(1)
			print(1)
			print(1)
			print(1)
			print(1)
			
			if self.kardex != {}:
				print(1.1)
				equal = False
				to_comtinue = False


		if to_continue == True:
			if self.ids.student_career.text != 'Carrera' and self.student_career != info['student_career']:
				print(2)
				print(2)
				print(2)
				print(2)
				print(2)
				print(2)
				print(2)
				print(2)
				
				if self.kardex != {}:
					print(2.1)
					equal = False
					to_continue = False

			if self.kardex != {}:
				old_kardex = self.old_kardex.copy()
				try:
					for subject in old_kardex:
						del old_kardex[subject]['sem']
				except:
					pass

				if old_kardex != self.actual_kardex:
					equal = False

			elif self.kardex == {} and to_continue == True:
				if self.student_faculty == info['student_faculty'] and self.student_career == info['student_career']:
					print(3)
					print(3)
					print(3)
					print(3)
					print(3)
					print(3)
					print(3)
					print(3)
					
					if self.ids.middle_name.text != info['middle_name']:
						equal = False
						print(3.1)

					elif self.ids.last_name.text != info['last_name']:
						equal = False
						print(3.2)

					elif self.ids.name.text != info['name']:
						equal = False
						print(3.3)

					elif self.ids.date_birth.text != info['date_birth']:
						equal = False
						print(3.4)

					elif self.ids.email.text != info['email']:
						equal = False
						print(3.5)

					elif self.ids.password.text != info['password']:
						equal = False
						print(3.6)

					elif self.ids.student_status.text != info['student_status']:
						equal = False
						print(3.7)

		self.ids.update_student.disabled = equal

		return equal


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
			complete_layout='student_data',
			layout='show_student',
			layout_no_scroll='student_no_scroll', # no scroll layout
			execute='getFaculties',
			max_len=35,
			widget='student_faculty'
		)
		self.ids.student_career.text = 'Carrera'
		self.kardex = {}
		
		

	def onPressStudentCareer(self):
		if self.ids.student_faculty.text == 'Facultad':
			self.studentDialog('No ha Seleccionado ninguna facultad.')

		else:
			self.Showing(
				complete_layout='student_data',
				layout='show_student',
				layout_no_scroll='student_no_scroll',
				execute=f'getCareers [{self.student_faculty}]',
				max_len=35,
				widget='student_career'
			)
		self.kardex = {}


	def validKardex(self, oportunity):
		self.last_kardex_field = oportunity.name

		oportunity.text = oportunity.text.replace(' ', '')
		oportunity.text = oportunity.text.upper()
		chars = list('abcdefghijklmnñopqrstuvwxyz|°¬!"#$%&/()=\'?\\¿¡´¨+~*{[^}]`,;.:-_<>'.upper())		
		try:
			if oportunity.text == '':
				actual_oportunity:int = int(oportunity.name[len(oportunity.name)-1])
				next_oportunity1:str = oportunity.name[:len(oportunity.name)-1] + str(actual_oportunity+1)
				self.ids[next_oportunity1].disabled = True
				if actual_oportunity == 1 or actual_oportunity == 3 or actual_oportunity == 5:
					self.ids.save_kardex.disabled = False
				else:
					self.ids.save_kardex.disabled = True
			elif (oportunity.text == 'N' or oportunity.text == 'NP' or 
				oportunity.text == 'NA' or oportunity.text == 'A' or oportunity.text == 'AC'):
				if oportunity.text == 'N' and oportunity.focus == False:
					oportunity.text = 'NP'
				elif oportunity.text == 'A' and oportunity.focus == False:
					oportunity.text = 'AC'
				grade = oportunity.text
				
				if grade == 'NP' or grade == 'NA':
					next_oportunity1:int = int(oportunity.name[len(oportunity.name)-1]) + 1
					if (next_oportunity1-1) == 6:
						self.ids.save_kardex.disabled = True
					else:
						next_oportunity:str = oportunity.name[:len(oportunity.name)-1] + str(next_oportunity1)
						self.ids[next_oportunity].disabled = False
						if next_oportunity1 == 3 or next_oportunity1 == 5:
							self.ids.save_kardex.disabled = False
						else:
							self.ids.save_kardex.disabled = True
				elif grade == 'AC':
					next_oportunity1:int = int(oportunity.name[len(oportunity.name)-1]) + 1
					if (next_oportunity1-1) == 6:
						pass
					else:
						next_oportunity:str = oportunity.name[:len(oportunity.name)-1] + str(next_oportunity1)
					self.ids[next_oportunity].disabled = True
					self.ids.save_kardex.disabled = False
			elif set(oportunity.text) & set(chars):
				oportunity.text = 'NP'
			else:
				grade = int(oportunity.text)

				if grade > 100:
					oportunity.text = '100'
				if grade >= 0 and grade < 70:
					next_oportunity1:int = int(oportunity.name[len(oportunity.name)-1]) + 1
					if grade < 0 or grade > 100 and (next_oportunity1-1) == 6:
						self.ids.save_kardex.disabled = True
					else:
						next_oportunity:str = oportunity.name[:len(oportunity.name)-1] + str(next_oportunity1)
						if (next_oportunity1-1 == 6):
							pass
						else:
							self.ids[next_oportunity].disabled = False
						if next_oportunity1 == 3 or next_oportunity1 == 5:
							self.ids.save_kardex.disabled = False
						else:
							self.ids.save_kardex.disabled = True
				elif grade > 69 and grade < 101:
					next_oportunity1:int = int(oportunity.name[len(oportunity.name)-1]) + 1
					next_oportunity:str = oportunity.name[:len(oportunity.name)-1] + str(next_oportunity1)
					self.ids[next_oportunity].disabled = True
					self.ids.save_kardex.disabled = False
		except Exception as e:
			print(e)
			print(e)
			print(e)
			print(e)
			print(e)
			print(e)
			print(e)
			print(e)
			print(e)
			print(e)

			exp = re.compile(r'textfield[0-9][0-9]*6')
			if exp.fullmatch(oportunity.name):
				num = 0
				try:
					num = int(oportunity.text)
				except:
					pass
				if oportunity.text == 'AC' or (num > 69 and num < 101):
					self.ids.save_kardex.disabled = False
				else:
					self.ids.save_kardex.disabled = True
			
		return self.ids.save_kardex.disabled


	def delKardex(self, len_kardex):
		layout = self.ids.show_student
		layout.cols = 1
		layout.row_default_height = 0
		self.ids.student_no_scroll.pos_hint = {'center_x': .5}
		layout.clear_widgets()
		for i in range(1, len_kardex):
			del self.ids[f'mdlabel{i}']

			del self.ids[f'textfield{i}{1}']
			del self.ids[f'textfield{i}{2}']
			del self.ids[f'textfield{i}{3}']
			del self.ids[f'textfield{i}{4}']
			del self.ids[f'textfield{i}{5}']
			del self.ids[f'textfield{i}{6}']

		self.ids.editable_student.disabled = False


	def saveKardex(self):
		#self.ids[self.last_kardex_field].focus = False
		# We get the kardex data
		self.valid_kardex = True
		n = 0
		for subject in self.actual_kardex:
			n += 1
			textfield = f'textfield{n}'
			try:
				for i in range(1, 7, 1):
					self.actual_kardex[subject][f'OP{i}'] = self.ids[f'{textfield}{i}'].text
			except Exception as e:
				print(e)
				print(e)
				print(e)
				print(e)
				print(e)
				print(e)
				print(e)
				print(e)
				print(e)
				print(e)

		nums = list('0123456789')
		for i in range(1, len(self.actual_kardex)):
			accepter = False # VALID
			if self.ids[f'textfield{i}{1}'].text != '':
				if self.ids[f'textfield{i}{2}'].text == '':
					if set(self.ids[f'textfield{i}{1}'].text) & set(nums):
						if int(self.ids[f'textfield{i}{1}'].text) > -1 and int(self.ids[f'textfield{i}{1}'].text) < 70:
							accepter = True
							break

					else:
						if self.ids[f'textfield{i}{1}'].text == 'NP' or self.ids[f'textfield{i}{1}'].text == 'NA':
							accepter = True
							break
					
			else:
				if self.ids[f'textfield{i}{3}'].text != '' and self.ids[f'textfield{i}{4}'].text == '':
					if set(self.ids[f'textfield{i}{3}'].text) & set(nums):
						if int(self.ids[f'textfield{i}{3}'].text) > -1 and int(self.ids[f'textfield{i}{3}'].text) < 70:
							accepter = True
							break
					else:
						if self.ids[f'textfield{i}{3}'].text == 'NP' or self.ids[f'textfield{i}{3}'].text == 'NA':
							accepter = True
							break
				else:
					if self.ids[f'textfield{i}{5}'].text != '' and self.ids[f'textfield{i}{6}'].text == '':
						if set(self.ids[f'textfield{i}{5}'].text) & set(nums):
							if int(self.ids[f'textfield{i}{5}'].text) > -1 and int(self.ids[f'textfield{i}{5}'].text) < 70:
								accepter = True
								break
						else:
							if self.ids[f'textfield{i}{5}'].text == 'NP' or self.ids[f'textfield{i}{5}'].text == 'NA':
								accepter = True
								break
		
		print(self.actual_kardex)
		print(len(self.actual_kardex))
		# Example [83, NP, '', '', '', ''] --> [83, '', '', '', '', '']
		i = 1
		for subject in self.actual_kardex.keys():
			clear = False
			for j in range(1, 7):
				if self.ids[f'textfield{i}{j}'].text == '':
					clear = True
					
				elif set(self.ids[f'textfield{i}{j}'].text) & set(nums):
					if int(self.ids[f'textfield{i}{j}'].text) > 69 and int(self.ids[f'textfield{i}{j}'].text) < 101:
						clear = True

				else:
					if self.ids[f'textfield{i}{j}'].text == 'AC':
						clear = True

				if clear == True:
					for k in range(j+1, 7):
						print(clear, f'textfield{i}{k}')
						self.actual_kardex[subject][f'OP{k}'] = ''
					break
			i += 1


		self.ids.save_kardex.disabled = accepter
		if accepter == False:
			faculty = self.student_faculty
			career = self.student_career
			i = 0
			self.kardex = {}
			for subject in self.actual_kardex:
				ids = self.sql.execute(f'EXECUTE getIds \'{faculty}\', \'{career}\', \'{subject}\'')
				n_id: int = 0
				for id_ in ids:
					id_faculty = id_[0]
					id_career = id_[1]
					id_subject = id_[2]
				self.id_faculty = id_faculty
				self.id_career = id_career
				self.id_subject.append(id_subject)

				op1 = self.actual_kardex[subject]['OP1']
				op2 = self.actual_kardex[subject]['OP2']
				op3 = self.actual_kardex[subject]['OP3']
				op4 = self.actual_kardex[subject]['OP4']
				op5 = self.actual_kardex[subject]['OP5']
				op6 = self.actual_kardex[subject]['OP6']
				#self.sql.execute('EXECUTE getIDSubject')
				self.kardex[str(i)] = [op1, op2, op3, op4, op5, op6]
				i += 1

			self.delKardex(len(self.actual_kardex))
			self.ids.student_no_scroll.pos_hint = {'center_x': -1}
			
		else:
			self.ids.save_kardex.disabled = True
			#self.valid_kardex = False


	def onPressKardex(self):
		self.ids.editable_student.disabled = True
		layout = self.ids.show_student
		layout.cols = 7
		layout.padding = 2
		layout.row_default_height = 50

		self.actual_kardex = {}

		subjects = []
		if self.student_faculty != '' and self.student_career != '':
			subjects = self.sql.execute(f'EXECUTE dbo.getSubjects [{self.student_faculty}], [{self.student_career}]')
		subject = []
		for s in subjects:
			subject.append(s[0])

		get = self.sql.execute(f'EXECUTE getKardex {self.ids.student_enrollment.text}')
		self.old_kardex = {}
		for g in get:
			self.old_kardex[g[1]] = {'sem':f'{g[0]}', 'op1':f'{g[2]}', 'op2':f'{g[3]}', 'op3':f'{g[4]}', 'op4':f'{g[5]}', 'op5':f'{g[6]}', 'op6':f'{g[7]}'}

		if subject != []:
			self.ids.student_no_scroll.pos_hint = {'center_x': .5}
			n = 0
			for s in subject:
				print(s)
				n += 1

				x = f"""
MDLabel:
	id: mdlabel{n}
	name: 'mdlabel{n}'

	text: f'{s}'
	#size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
				"""
				self.ids[f'mdlabel{n}'] = Builder.load_string(x)
				layout.add_widget(self.ids[f'mdlabel{n}'])

				i = 1
				for i in range(1, 7, 1):
					try:
						text = self.old_kardex[s][f'op{i}']
					except:
						text = ''
					y = f"""
TextInput:
	id: textfield{n}{i}
	name: f'textfield{n}{i}'

	text: '{text}'
	size_hint_x: .15
	multiline: False
	#input_filter: 'int'
	on_text: app.root.get_screen('mod').validKardex(textfield{n}{i})
	on_focus: app.root.get_screen('mod').validKardex(textfield{n}{i})
		"""
					self.ids[f'textfield{n}{i}'] = Builder.load_string(y)
					layout.add_widget(self.ids[f'textfield{n}{i}'])

					if i > 1:
						self.ids[f'textfield{n}{i}'].disabled = True
					
				self.actual_kardex[self.ids[f'mdlabel{n}'].text] = {'OP1':'', 'OP2':'', 'OP3':'', 'OP4':'', 'OP5':'', 'OP6':''}
			
			student_show_layout = self.ids.student_no_scroll

			self.ids.save_kardex = """
MDRaisedButton:
	id: save_kardex
	name: 'save_kardex'

	text: 'Guardar Kardex'
	size_hint_x: 1
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		#del saver_layout
		app.root.get_screen('mod').ids.student_no_scroll.remove_widget(save_kardex)
		del save_kardex
		app.root.get_screen('mod').ids.update_student.disabled = False
		app.root.get_screen('mod').saveKardex()
			"""

			self.ids.save_kardex = Builder.load_string(self.ids.save_kardex)
			student_show_layout.add_widget(self.ids.save_kardex)
			
		else:
			layout.cols = 1
			self.studentDialog('No ha Seleccionado una Facultad o Carrera.')
			

	def delNumber(self, var):
		numbs = '0123456789'
		char = '|°¬!"#$%&/()=\'?\\¿¡´¨+*~{[^}]`,;.:-_<>'
		chars = list(numbs + char)
		for char in chars:
			var.text = var.text.replace(char, "")


	def validName(self, name, type_=''):
		if 'middle_name' in name or 'last_name' in name:
			name = self.ids[name]
			name.text = name.text.replace(' ', '')
		
		if type(name) == str:
			name = self.ids[name]
		
		name.text = name.text.upper()
		
		self.delNumber(name)
		if len(name.text) > 2:
			if name.focus == False:
				pass
		else:
			if name.focus == False:
				if type_ == 'Teacher':
					self.dialogTeacher('Atención', 'Debe contener al menos 3 letras')
				else:
					self.studentDialog('Debe contener almenos 3 letras.')


	def onTextMiddleName(self):
		self.validName('middle_name')
		self.setEmail(
			email='email',
			name='name',
			middle_name='middle_name',
			last_name='last_name'
		)
		self.studentEquals()
		

	def onTextLastName(self):
		self.validName('last_name')
		self.setEmail(
			email='email',
			name='name',
			middle_name='middle_name',
			last_name='last_name'
		)
		self.studentEquals()


	def onTextName(self):
		self.validName('name')
		self.setEmail(
			email='email',
			name='name',
			middle_name='middle_name',
			last_name='last_name'
		)
		self.studentEquals()


	def getDate(self):
		# 'datetime.now()' literaly returns the date and
		# the time.
		info = str(datetime.now())
		# We save the date as str (it is desordered(year-month-day))
		date:str = info[:10]
		# The disordered date is converted as list
		date_disordered:list = info[:10].split("-")
		# We reverse the list to get the ordered date
		date:list = list(reversed(date_disordered))
		# We convert the date list to str
		date:str = ''.join(date)
		# We separate the date (day-month-year)
		ordered_date:str = f"{date[4:8]}/{date[2:4]}/{date[0:2]}"

		# We update the Labels
		actual_date = ordered_date

		return actual_date


	def validDay(self, date_birth):
		date_birth:list = date_birth.text.split('/')
		year = date_birth[0]
		month = date_birth[1]
		day = date_birth[2]

		month_thirty_one:list = ['01', '03', '05', '07', '08', '10', '12']
		month_thirty:list = ['04', '06', '09', '11']

		valid:bool = False
		if month in month_thirty_one:
			valid = int(day) > 0 and int(day) < 32

			if valid == False and int(day) > 31:
				day = 31
			elif valid == False: # and int(day) < 0
				day = 1

		elif month in month_thirty:
			valid = int(day) > 0 and int(day) < 31
			
			if valid == False and int(day) > 30:
				day = 30
			elif valid == False: # and int(day) < 0
				day = 1

		else:
			if int(year) % 4 == 0 and int(year) % 100 != 0:
				valid = int(day) > 0 and int(day) < 30

				if valid == False and int(day) > 29:
					day = 29
				elif valid == False: # and int(day) < 0
					day = 1
			else:
				valid = int(day) > 0 and int(day) < 29

				if valid == False and int(day) > 28:
					day = 28
				elif valid == False: # and int(day) < 0
					day = 1

		return day


	def validMonth(self, month):
		valid = re.compile(r'(\d\d|\d)')
		
		if valid.fullmatch(month):
			if int(month) > 0 and int(month) < 13:
				month = month

			elif int(month) > 12:
				month = '12'
			else:
				month = '01'
		else:
			month = '01'

		return month


	def validYear(self, actual_year, year_birth):
		valid = re.compile(fr"(19[6-9][0-9]|20[0-{actual_year[2]}][0-9])")
		
		if valid.fullmatch(year_birth) and (int(actual_year) - int(year_birth)) > 16:
			year = year_birth

		else:
			year = int(actual_year) - 17

		return year


	def onTextDateBirth(self):
		date_birth:str = self.ids.date_birth

		actual_date:str = self.getDate()
		actual_date:list = actual_date.split('/')
		year = actual_date[0]
		month = actual_date[1]
		day = actual_date[2]

		invalid_chars:list = list('|°¬!"#$%&()=?\'\\¡¿¨´+*~{[^}]`}-_.:,;abcdefghijklmnñopqrstuvwxyz'.upper())
		if not set(date_birth.text.upper()) & set(invalid_chars):
			valid_date_birth = re.compile(fr"(19[6-9][0-9]|20[0-{year[2]}][0-{year[3]}])/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|31)")
			if valid_date_birth.fullmatch(date_birth.text):
				year_birth = date_birth.text.split('/')[0]
				if (int(year) - int(year_birth)) > 16 :
					date_birth.text = date_birth.text[:len(date_birth.text)-2] + str(self.validDay(date_birth))
					
				else:
					year_birth = self.validYear(year, date_birth.text.split('/')[0])
					month_birth = self.validMonth(date_birth.text.split('/')[1])
					day_birth = self.validDay(date_birth)

					date_birth.text = f'{year_birth}/{month_birth}/{day_birth}'
					
				
			else:
				if len(date_birth.text) == 10:
					date_birth.text = ''
					self.studentDialog('Fecha de Nacimiento Incorrecta.')
					

		else:
			date_birth.text = '2005/01/01'

		if len(date_birth.text) < 8 and date_birth.text.count('/') == 2:
			date_birth.text = '2005/01/01'

		self.studentEquals()


	def setEmail(self, email, name, middle_name, last_name):
		email = self.ids[email]
	
		name = self.ids[name].text
		middle_name = self.ids[middle_name].text
		last_name = self.ids[last_name].text
		if len(name) > 2 and len(middle_name) > 2 and len(last_name) > 2:
			name:str = word_tokenize(name)[0]
			middle_name:str = middle_name
			last_name:str = last_name[0] + last_name[len(last_name)-1]

			email.text = f'{name}.{middle_name + last_name}@uanl.edu.mx'.lower()
			email.hint_text = ''
			self.email = True

		else:
			email.focus = False
			email.hint_text = 'Correo Universitario'
			self.email = False


	def onTextPassword(self, password, type_=''):
		password = self.ids[password]
		lower_case = 'abcdefghijklmnñopqrstuvwxyz'
		upper = lower_case.upper()
		nums = '0123456789'
		if set(password.text) & set(lower_case) and set(password.text) & set(upper) and set(password.text) & set(nums):
			if len(password.text) > 7 and len(password.text) < 17:
				if password.focus == False:
					pass

			else:
				if password.focus == False:
					if type_=='Teacher':
						self.dialogTeacher('Atención', 'La longitud de la contraseña debe ser mayor a 7 y menor a 17.')
					else:
						self.studentDialog('La longitud de la contraseña debe ser mayor a 7 y menor a 17.')
					

		else:
			if password.focus == False:
				if type_ == 'Teacher':
					self.dialogTeacher('Atención', 'La contraseña debe contener una letra mayuscula, una minuscula y un número.')
				else:
					self.studentDialog('La contraseña debe contener al menos una letra mayuscula, una minuscula y un número.')
				
		if type_ == 'Teacher':
			self.teacherEquals()
		else:
			self.studentEquals()


	def onPressStatus(self, status, type_=''):
		status = self.ids[status]
		if status.text == 'ALTA':
			status.text = 'BAJA'

		else:
			status.text = 'ALTA'

		if type_=='Teacher':
			self.teacherEquals()
		else:
			self.studentEquals()


	def onPressCancelStudent(self):
		self.ids.student_enrollment.text = ''
		self.ids.student_enrollment.disabled = False
		self.ids.search_student.disabled = False
		self.ids.editable_student.disabled = True
		field1 = [
			'student_faculty',
			'student_career',
		]
		field2 = [
			'middle_name',
			'last_name',
			'name',
			'date_birth',
			'email',
			'password',
			'student_status'
		]
		for f in field1:
			if 'faculty' in f:
				self.ids[f].text = 'Seleccionar Facultad'

			elif 'career' in f:
				self.ids[f].text = 'Seleccionar Carrera'

		for f in field2:
			if 'status' in f:
				self.ids[f].text = 'Status'

			else:
				self.ids[f].text = ''

		self.ids.cancel_student.disabled = True

	
	def onPressUpdateStudent(self):
		field = [
			'middle_name',
			'last_name',
			'name',
			'date_birth',
			'email',
			'password',
			'student_status'
		]
		to = [
			self.student_faculty,
			self.student_career,
			self.ids.middle_name.text,
			self.ids.last_name.text,
			self.ids.name.text,
			self.ids.date_birth.text,
			self.ids.email.text,
			self.ids.password.text,
			self.ids.student_status.text
		]
		valid = False
		check = False
		for f in field:
			if self.ids[f].text != self.actual_student_info[f]:
				print(self.ids[f].text)
				print(self.actual_student_info[f])
				valid = True
		
		if self.student_faculty != self.actual_student_info['student_faculty']:
			valid = True
		
		if self.student_career != self.actual_student_info['student_career']:
			valid = True

		if self.kardex != {}:
			valid = True

		if self.actual_student_info['name'] != self.ids.name.text:
			check = True

		elif self.actual_student_info['middle_name'] != self.ids.middle_name.text:
			check = True

		elif self.actual_student_info['last_name'] != self.ids.last_name.text:
			check = True

		if check == True:
			get = self.sql.execute(f"EXECUTE getStudent '{self.ids.middle_name.text}', '{self.ids.last_name.text}', '{self.ids.name.text}'")
			aux = ''
			for g in get:
				aux = g[0]
				
			if aux != '':
				valid = False
				self.studentDialog('Este estudiante ya existe.')
					
		equals = self.studentEquals()
		if equals == True:
			self.studentDialog('No se ha hecho ninguna modificación o faltan datos por agregar.')

		if valid == True and equals == False:
			self.actual_student_info['student_faculty'] = to[0]
			self.actual_student_info['student_career'] = to[1]
			self.actual_student_info['middle_name'] = to[2]
			self.actual_student_info['last_name'] = to[3]
			self.actual_student_info['name'] = to[4]
			self.actual_student_info['date_birth'] = to[5]
			self.actual_student_info['email'] = to[6]
			self.actual_student_info['password'] = to[7]
			self.actual_student_info['student_status'] = to[8]
			self.sql.execute(
				f'EXECUTE updateStudent [{self.ids.student_enrollment.text}], [{to[0]}], [{to[1]}], [{to[2]}], [{to[3]}], [{to[4]}], [{to[5]}], [{to[6]}], [{to[7]}], [{to[8]}]'
			)
		
			if self.kardex != {}:
				self.sql.execute(
					f'EXECUTE deleteKardex [{self.ids.student_enrollment.text}]'
				)
				id_faculty = self.id_faculty
				id_career = self.id_career
				id_subject = self.id_subject

				kard = self.kardex
				for i in range(len(self.kardex)):
					op1 = kard[str(i)][0]
					op2 = kard[str(i)][1]
					op3 = kard[str(i)][2]
					op4 = kard[str(i)][3]
					op5 = kard[str(i)][4]
					op6 = kard[str(i)][5]
					
					save_kardex = f"EXECUTE saveKardex '{id_faculty}', '{id_career}', '{self.ids.student_enrollment.text}',"
					save_kardex += f" '{id_subject[i]}', '{op1}', '{op2}', '{op3}', '{op4}', '{op5}', '{op6}'"
					self.sql.execute(save_kardex)
			self.sql.commit()
			self.studentDialog('Se ha actualizado la información correctamente.')
		self.ids.update_student.disabled = True


	#################################### T E A C H E R ###########################################
	def teacherEquals(self):
		equal = True
		#to_continue = True
		info = self.actual_teacher_info
		
		if self.ids.teacher_faculty.text != 'Facultad' and self.teacher_faculty != info['teacher_faculty']:
			equal = False
			#to_comtinue = False


		#if to_continue == True:
		elif self.ids.teacher_career.text != 'Carrera' and self.teacher_career != info['teacher_career']:
			print(2)
			print(2)
			print(2)
			print(2)
			print(2)
			print(2)
			print(2)
			print(2)
			
			equal = False
			#to_continue = False

			#if to_continue == True:
		if self.teacher_faculty == info['teacher_faculty'] and self.teacher_career == info['teacher_career']:
			print(3)
			print(3)
			print(3)
			print(3)
			print(3)
			print(3)
			print(3)
			print(3)
			
			if self.ids.teacher_middle_name.text != info['teacher_middle_name']:
				equal = False
				print(3.1)

			elif self.ids.teacher_last_name.text != info['teacher_last_name']:
				equal = False
				print(3.2)

			elif self.ids.teacher_name.text != info['teacher_name']:
				equal = False
				print(3.3)

			elif self.ids.teacher_email.text != info['teacher_email']:
				equal = False
				print(3.5)

			elif self.ids.teacher_password.text != info['teacher_password']:
				equal = False
				print(3.6)

			elif self.ids.teacher_status.text != info['teacher_status']:
				equal = False
				print(3.7)

		self.ids.update_teacher.disabled = equal

		return equal


	def closeDialogTeacher(self, *args):
		self.dialog_teacher.dismiss()


	def dialogTeacher(self, title, text):
		self.dialog_teacher = MDDialog(
			title=title,
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=self.closeDialogTeacher
				)
			]
		)
		self.dialog_teacher.open()


	def delTeacherCareers(self, career:list):
		self.ids.teacher_no_scroll.pos_hint = {'center_x': -1}

		layout = self.ids.show_teacher

		layout.clear_widgets()
		
		n = 0
		for c in career:
			n += 1
			del self.ids[f'A{n}']


	def onPressTeacherCareer(self):
		layout = self.ids.show_teacher
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
		screen = app.root.get_screen('mod')
		screen.ids.teacher_careers.text = A{n}.text[:3] + '...'
		screen.teacher_career = A{n}.text
		screen.delTeacherCareers({career})
					"""
					self.ids[f'A{n}'] = Builder.load_string(c)
					layout.add_widget(self.ids[f'A{n}'])

			else:
				self.dialogTeacher('Error', 'Este profesor o matricula no existen.')
		else:
			self.dialogTeacher('Error.', 'No has agregado ninguna matricula')


	def getTeacher(self):
		if self.ids.teacher_careers.text == 'Carrera':
			self.dialogTeacher('Error.', 'Aún no especificas la carrera.')
		
		else:
			getting = self.sql.execute(f'EXECUTE getTeacherInfo {self.ids.teacher_enrollment.text}, \'{self.teacher_career}\'')
			for got in getting:
				data = [
					got[0], got[1], got[2], got[3],
					got[4], got[5], got[6], got[7]
				]

			self.actual_teacher_info = {}
			self.teacher_faculty = data[0]
			self.teacher_career = data[1]
			self.actual_teacher_info['teacher_faculty'] = data[0]
			self.actual_teacher_info['teacher_career'] = data[1]
			self.actual_teacher_info['teacher_middle_name'] = data[2]
			self.actual_teacher_info['teacher_last_name'] = data[3]
			self.actual_teacher_info['teacher_name'] = data[4]
			self.actual_teacher_info['teacher_email'] = data[5]
			self.actual_teacher_info['teacher_password'] = data[6]
			self.actual_teacher_info['teacher_status'] = data[7]
			
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
				self.ids[field].diabled = False
				n += 1

			self.ids['teacher_faculty'].disabled = False
			self.ids['teacher_career'].disabled = False
			self.ids['teacher_middle_name'].disabled = False
			self.ids['teacher_last_name'].disabled = False
			self.ids['teacher_name'].disabled = False
			self.ids['teacher_email'].disabled = False
			self.ids['teacher_password'].disabled = False
			self.ids['teacher_status'].disabled = False

			self.ids.cancel_teacher.disabled = False
			#self.ids.update_teacher.disabled = False
			self.ids.teacher_enrollment.disabled = True
			self.ids.teacher_careers.disabled = True
			self.ids.search_teacher.disabled = True


	def onPressTeacherFaculty(self):
		self.Showing(
			complete_layout='teacher_data',
			layout='show_teacher',
			layout_no_scroll='teacher_no_scroll', # no scroll layout
			execute='getFaculties',
			max_len=35,
			widget='teacher_faculty'
		)
		self.ids.teacher_career.text = 'Carrera'
		self.teacherEquals()


	def onPressTeachCareer(self):
		if self.ids.teacher_faculty.text == 'Facultad':
				self.dialogTeacher('Error.','No ha Seleccionado ninguna facultad.')

		else:
			self.Showing(
				complete_layout='teacher_data',
				layout='show_teacher',
				layout_no_scroll='teacher_no_scroll',
				execute=f'getCareers [{self.teacher_faculty}]',
				max_len=35,
				widget='teacher_career'
			)
			self.teacherEquals()


	def onTextTeacherMiddleName(self):
		self.validName('teacher_middle_name')
		self.setEmail(
			email='teacher_email',
			name='teacher_name',
			middle_name='teacher_middle_name',
			last_name='teacher_last_name'
		)
		self.teacherEquals()


	def onTextTeacherLastName(self):
		self.validName('teacher_last_name')
		self.setEmail(
			email='teacher_email',
			name='teacher_name',
			middle_name='teacher_middle_name',
			last_name='teacher_last_name'
		)
		self.teacherEquals()


	def onTextTeacherName(self):
		self.validName('teacher_name')
		self.setEmail(
			email='teacher_email',
			name='teacher_name',
			middle_name='teacher_middle_name',
			last_name='teacher_last_name'
		)
		self.teacherEquals()


	def onTextTeacherPassword(self):
		self.onTextPassword(password='teacher_password', type_='Teacher')


	def onPressTeacherStatus(self):
		self.onPressStatus(status='teacher_status', type_='Teacher')


	def onPressUpdateTeacher(self):
		field = [
			'teacher_middle_name',
			'teacher_last_name',
			'teacher_name',
			'teacher_email',
			'teacher_password',
			'teacher_status'
		]
		to = [
			self.teacher_faculty,
			self.teacher_career,
			self.ids.teacher_middle_name.text,
			self.ids.teacher_last_name.text,
			self.ids.teacher_name.text,
			self.ids.teacher_email.text,
			self.ids.teacher_password.text,
			self.ids.teacher_status.text
		]
		valid = False
		check = False
		for f in field:
			if self.ids[f].text != self.actual_teacher_info[f]:
				print(self.ids[f].text)
				print(self.actual_teacher_info[f])
				valid = True
		valid2 = False
		if self.teacher_faculty != self.actual_teacher_info['teacher_faculty']:
			valid2 = True
		if self.teacher_career != self.actual_teacher_info['teacher_career']:
			valid2 = True

		if self.actual_teacher_info['teacher_name'] != self.ids.teacher_name.text:
			check = True

		elif self.actual_teacher_info['teacher_middle_name'] != self.ids.teacher_middle_name.text:
			check = True

		elif self.actual_teacher_info['teacher_last_name'] != self.ids.teacher_last_name.text:
			check = True

		if valid2 == True:
			get = self.sql.execute(f"EXECUTE getTeacher '{self.actual_teacher_info['teacher_middle_name']}', '{self.actual_teacher_info['teacher_last_name']}', '{self.actual_teacher_info['teacher_name']}', '{self.teacher_career}'")
			aux = ''
			for g in get:
				aux = g[0]
				
			if aux != '':
				valid = False
				self.dialogTeacher('Error.', f'Este Profesor ya imparte clases en la carrera {self.teacher_career}.')
		
		elif check == True:
			get = self.sql.execute(f"EXECUTE getTeacher '{self.ids.teacher_middle_name.text}', '{self.ids.teacher_last_name}', '{self.ids.teacher_name}', '{self.teacher_career}'")
			aux = ''
			for g in get:
				aux = g[0]
				
			if aux != '':
				valid = False
				self.dialogTeacher('Error.', f'Este Profesor ya existe.')
					
		equals = self.teacherEquals()
		if equals == True:
			self.dialogTeacher('Atención', 'No se ha hecho ninguna modificación o faltan datos por agregar.')

		if valid == True and equals == False:
			get = self.sql.execute(f"EXECUTE getIDFac_CarTeacher [{self.actual_teacher_info['teacher_faculty']}], [{self.actual_teacher_info['teacher_career']}]")
			for g in get:
				id_faculty = g[0]
				id_career = g[1]

			self.actual_teacher_info['teacher_faculty'] = to[0]
			self.actual_teacher_info['teacher_career'] = to[1]
			self.actual_teacher_info['teacher_middle_name'] = to[2]
			self.actual_teacher_info['teacher_last_name'] = to[3]
			self.actual_teacher_info['teacher_name'] = to[4]
			self.actual_teacher_info['teacher_email'] = to[5]
			self.actual_teacher_info['teacher_password'] = to[6]
			self.actual_teacher_info['teacher_status'] = to[7]
			
			self.sql.execute(
				f'EXECUTE updateTeacher [{id_faculty}], [{id_career}], [{self.ids.teacher_enrollment.text}], [{to[0]}], [{to[1]}], [{to[2]}], [{to[3]}], [{to[4]}], [{to[5]}], [{to[6]}], [{to[7]}]'
			)
		
			self.sql.commit()
			self.dialogTeacher('Atención', 'Se ha actualizado la información correctamente.')
		self.ids.update_teacher.disabled = True
	

	def onPressCancelTeacher(self):
		self.ids.teacher_enrollment.text = ''
		self.ids.teacher_enrollment.disabled = False
		self.ids.teacher_careers.text = 'Carrera'
		self.ids.teacher_careers.disabled = False
		self.ids.search_teacher.disabled = False
		self.ids.cancel_teacher.disabled = True
		field1 = [
			'teacher_faculty',
			'teacher_career',
		]
		field2 = [
			'teacher_middle_name',
			'teacher_last_name',
			'teacher_name',
			'teacher_email',
			'teacher_password',
			'teacher_status'
		]
		for f in field1:
			self.ids[f].disabled = True
			if 'faculty' in f:
				self.ids[f].text = 'Seleccionar Facultad'

			elif 'career' in f:
				self.ids[f].text = 'Seleccionar Carrera'

		for f in field2:
			self.ids[f].disabled = True
			if 'status' in f:
				self.ids[f].text = 'Status'

			else:
				self.ids[f].text = ''

		self.ids.cancel_student.disabled = True


	################################# S C H E D U L E #############################
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
		screen = app.root.get_screen('mod')
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
		screen = app.root.get_screen('mod')
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
					'classroom',
					'banches',
					'cancel_classroom',
					'update_classroom',
					'continue_classroom'
				]
				for widget in classroom:
					if widget == 'banches':
						get = self.sql.execute(f'EXECUTE getBanches [{self.schedule_faculty}], [{self.schedule_classroom}]')
						for g in get:
							self.ids[widget].text = str(g[0])
							self.banches = str(g[0])
						self.ids.banches.disabled = False

					elif widget == 'classroom':
						self.ids[widget].text = self.ids.schedule_classroom.text
						self.classroom = self.ids[widget].text
						self.ids[widget].disabled = False

					else:
						self.ids[widget].disabled = not self.ids[widget].disabled
				
				#self.ids.cancel_all_schedule.disabled = True
				#self.ids.update_schedule.disabled = True
				

	def restartClassroom_Schedule(self):
		first_part = [
			'schedule_faculty',
			'schedule_classroom',
			'classroom',
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

			if count == 3:
				self.ids[widget].text = ''
				self.ids[widget].disabled = True

			if count == 5:
				#self.ids[widget].text = ''
				self.ids[widget].disabled = True
			
			if count == 6:
				#self.ids[widget].text = ''
				self.ids[widget].disabled = True
			
			if count == 7:
				#self.ids[widget].text = ''
				self.ids[widget].disabled = True
				
			count += 1

		second_part = [
			'available_schedule', ############## 0
			'unavailable_schedule', ############# 1
			'choose_schedule', # 2
			'new_schedule', #################### 2
			'edit_schedule', # 4
			'clear_new_schedule', # 5
			'schedule_career', ################### 6
			'schedule_teacher', ################## 7
			'cancel_all_schedule', # 8
			'update_schedule' # 9
		]
		count = 0
		for widget in second_part:
			self.ids[widget].disabled = True
			self.ids[widget].text = ''
			if count == 2:
				self.ids[widget].text = 'Seleccionar Horario'

			if count == 4:
				self.ids[widget].text = 'Agregar Nuevo Horario'

			if count == 5:
				self.ids[widget].text = 'Limpiar Nuevo Horario'

			if count == 8:
				self.ids[widget].text = 'Cancelar Todo'

			if count == 9:
				self.ids[widget].text = 'Actualizar Horario'

			count += 1


	def onPressUpdateClassroom(self):
		if self.classroom == self.ids.schedule_classroom.text and self.banches == self.ids.banches.text:
			self.dialogSchedule('No se ha hecho ninguna modificación.')
		
		else:
			get = self.sql.execute(f'EXECUTE getClassrooms [{self.schedule_faculty}]')
			classroom = []
			for g in get:
				classroom.append(f'{g[0]}')
			if self.ids.classroom.text not in classroom:
				self.sql.execute(f'EXECUTE updateClassroom [{self.schedule_faculty}],[{self.classroom}],[{self.ids.classroom.text}],[{self.banches}], [{self.ids.banches.text}]')
				self.sql.commit()
				self.dialogSchedule('Se han guardado las modificaciones satisfactoriamente.')
				self.classroom = self.ids.schedule_classroom.text
				self.banches = self.ids.banches.text
			else:
				self.dialogSchedule('Esta Aula  ya existe.')


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
				'update_classroom',
				'continue_classroom'
			]
			for widget in classroom:
				self.ids[widget].disabled = True

			self.ids.choose_schedule.disabled = False
			self.ids.cancel_all_schedule.disabled = False


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

		self.ids.available_schedule.text = ''
		aux = ''
		for i in range(len(text)):
			#self.ids.available_schedule.text += text[i]
			aux = aux + text[i]
			exp = re.compile(r"[0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9]")
			if exp.fullmatch(aux):
				self.ids.available_schedule.text += f'{aux};'
				aux = ''
		

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
		self.ids.edit_schedule.disabled = False
		self.ids.clear_new_schedule.disabled = False


	def onPressChooseSchedule(self):
		layout = self.ids.show_schedule
		layout.clear_widgets()
		#layout.cols = 1
		#layout.row_default_height = 10

		self.ids.schedule_career.text = ''
		self.ids.schedule_teacher.text = ''
		self.ids.update_schedule.disabled = True
		schedules = self.sql.execute(f'EXECUTE dbo.getSchedules [{self.schedule_faculty}], [{self.schedule_classroom}]')
		schedule = []
		for s in schedules:
			schedule.append(s[0])

		if schedule == []:
			self.dialogSchedule('No hay horarios agregados.')
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
		screen = app.root.get_screen('mod')
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


	def delEditSchedule(self, schedule):
		self.ids.schedule_no_scroll.pos_hint = {'center_x': -1}

		layout = self.ids.show_schedule
		self.ids.classroom_and_schedule.disabled = False

		layout.clear_widgets()
		
		n = 0
		for s in schedule:
			if s != '' and s != ' ':
				n += 1
				del self.ids[f'A{n}']

		#get = self.sql.execute(f'EXECUTE getC_T [{self.schedule_faculty}], [{self.schedule_classroom}], [{self.choose_schedule}]')
		#for g in get:
		#	self.ids.schedule_career.text = g[0]
		#	self.ids.schedule_teacher.text = f'{g[1]} {g[2]} {g[3]}'
		
		self.ids.update_schedule.disabled = False


	def onPressEditSchedule(self):
		layout = self.ids.show_schedule
		layout.clear_widgets()
		#layout.cols = 1
		#layout.row_default_height = 10

		self.ids.update_schedule.disabled = True
		schedule = (self.ids.available_schedule.text + self.ids.choose_schedule.text).split(';')
		schedule.sort()
		new_schedule = self.ids.new_schedule.text.split(';')
		for new in new_schedule:#[:len(new_schedule)-1]:
			try:
				schedule.remove(new)
				schedule.remove('')
			except:
				pass
		
		#schedule = schedule[:len(schedule)-1]

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
			
			if s != '' and s != ' ':
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
		screen = app.root.get_screen('mod')
		if len(A{n}.text) > 50: \
			c_s = A{n}.text[:50] + '...'
		else: \
			c_s = A{n}.text
		screen.ids.new_schedule.text += c_s + ';'
		screen.new_schedule = A{n}.text
		screen.delEditSchedule({schedule})
				"""
				self.ids[f'A{n}'] = Builder.load_string(s)
				layout.add_widget(self.ids[f'A{n}'])


	def onPressUpdateSchedule(self):
		new_schedule = self.ids.new_schedule.text.split(';')
		new_schedule = new_schedule[:len(new_schedule)-1]
		if new_schedule != []:
			self.sql.execute(f'EXECUTE updateSchedule [{self.schedule_faculty}], [{self.ids.schedule_career.text}], [{self.ids.classroom.text}], [{self.ids.choose_schedule.text}], [{self.ids.new_schedule.text}]')
			self.sql.commit()


			self.ids.cancel_classroom.disabled = False
			self.ids.update_classroom.disabled = False
			self.ids.continue_classroom.disabled = False
			self.ids.new_schedule.text = ''
			self.ids.choose_schedule.disabled = True
			self.ids.edit_schedule.disabled = True
			self.ids.clear_new_schedule.disabled = True
			self.ids.cancel_all_schedule.disabled = True
			self.ids.update_schedule.disabled = True
			self.ids.schedule_career.text = ''
			self.ids.schedule_career.disabled = True
			self.ids.schedule_teacher.text = ''
			self.ids.schedule_teacher.disabled = True
			
			get = self.sql.execute(f'EXECUTE getSchedules [{self.schedule_faculty}], [{self.schedule_classroom}]')
			got = []
			for g in get:
				got.append(g[0])

			if got == []:
				self.dialogSchedule('No hay horarios agregados para esta aula.')

			else:
				self.setAvailableSchedules(got)
			
			self.dialogSchedule('Se ha realizado la actualización satisfactoriamente.')

		else:
			self.dialogSchedule('No ha seleccionado el nuevo horario.')


	###
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


