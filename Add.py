import pyodbc as SQLServer

from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'position', 'custom')

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from nltk.tokenize import word_tokenize
from datetime import datetime

import random
import re

class Add(Screen):
	def __init__(self, **kwargs):
		super(Add, self).__init__(**kwargs)
		self.sql = self.sqlCONNECTION()

		####### S T U D E N T ########
		self.middle_name = False
		self.last_name = False
		self.name_ = False
		self.email = False
		self.date_birth = False
		self.student_faculty = False
		self.student_career = False
		self.valid_kardex = False
		##
		self.actual_kardex = dict()
		self.last_kardex_field = ''
		self.kardex = {}

		self.id_subject = []

		Clock.schedule_interval(self.interval, 1)
		####### T E A C H E R ########
		self.teacher_middle_name = False
		self.teacher_last_name = False
		self.teacher_name_ = False
		self.teacher_email = False
		self.teacher_faculty = False
		self.teacher_career = False
		###### S C H E D U L E #######
		self.id_classroom = 0
		self.classroom = False
		self.banches = False
		self.schedule_id_faculty = ''
		self.schedule_classroom = ''
		self.schedule_banches = ''

		self.schedule_career = False
		self.schedule_teacher = False
		self.schedule_subject = False
		self.group = False
		self.schedule = False


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

	######################################### S T U D E N T ########################################

	def interval(self, dt):
		########################### S T U D E N T #########################
		verifier:bool = False
		verifier2:bool = False
		if self.middle_name == True:
			if self.last_name == True:
				if self.name_ == True:
					if self.email == True:
						if self.date_birth == True:
							#verifier2 = True
							verifier2 = not self.ids.middle_name.disabled
							if self.student_faculty == True:
								if self.student_career == True:
									if self.valid_kardex == True:
										verifier = True
		self.ids.save_student.disabled = not verifier
		self.ids.student_faculty.disabled = not verifier2

		widget = [self.middle_name, self.last_name, self.name_, 
				  self.email, self.date_birth, self.student_faculty]
		verifier = False
		if widget[0] == True:
			verifier = True
		
		if widget[1] == True:
			verifier = True
		
		if widget[2] == True:
			verifier = True
		
		if widget[3] == True:
			verifier = True
		
		if widget[4] == True:
			verifier = True
		
		if widget[5] == True:
			verifier = True
		
		##
		if verifier == True:
			self.ids['teacher'].disabled = True
			self.ids['schedule'].disabled = True
			self.ids['logout'].disabled = True
		else:
			self.ids['logout'].disabled = False
			self.ids['teacher'].disabled = False
			self.ids['schedule'].disabled = False

		########################### T E A C H E R #########################
		verifier:bool = False
		verifier2:bool = False
		if self.teacher_middle_name == True:
			verifier = True
			if self.teacher_last_name == True:
				verifier = True
				if self.teacher_name_ == True:
					verifier = True
					if self.teacher_email == True:
						verifier = True
						verifier2 = not self.ids.teacher_middle_name.disabled
						if self.teacher_faculty == True:
							verifier = True
							if self.teacher_career == True:
								verifier = True
								if self.ids.teacher_career.disabled == False:							
									verifier = False

		self.ids.save_teacher.disabled = not verifier
		self.ids.teacher_faculty.disabled = not verifier2

		widget = [self.teacher_middle_name, self.teacher_last_name, self.teacher_name_, 
				  self.teacher_email, self.teacher_faculty]
		verifier = False
		if widget[0] == True:
			verifier = True
		
		if widget[1] == True:
			verifier = True
		
		if widget[2] == True:
			verifier = True
		
		if widget[3] == True:
			verifier = True
		
		if widget[4] == True:
			verifier = True
		
		##
		if verifier == True:
			self.ids['student'].disabled = True
			self.ids['schedule'].disabled = True
			self.ids['logout'].disabled = True
		else:
			self.ids['logout'].disabled = False
			self.ids['student'].disabled = False
			self.ids['schedule'].disabled = False
		########################## S C H E D U L E ########################
		verifier = False
		if self.schedule_career == True:
			verifier = True
			if self.schedule_teacher == True:
				if self.schedule_subject == True:
					if self.group == True:
						if self.schedule == True:
							verifier = False
						else:
							verifier = True
							#self.ids.schedules.disabled = True

		self.ids.finalize.disabled = verifier

		if verifier == True:
			self.ids['student'].disabled = True
			self.ids['teacher'].disabled = True
			self.ids['logout'].disabled = True
		else:
			self.ids['logout'].disabled = False
			self.ids['student'].disabled = False
			self.ids['teacher'].disabled = False


	def delNumber(self, var):
		numbs = list('0123456789')
		chars = list('|°¬!"#$%&/()=\'?\\¿¡´¨+*~{[^}]`,;.:-_<>')
		for char in range(len(list(var.text).copy())):
			if var.text[char] in numbs or var.text[char] in chars:
				var.text = var.text.replace(var.text[char], "")
				break


	def onTextMiddleName(self):
		middle_name = self.ids.middle_name
		
		middle_name.text = middle_name.text.replace(' ', '')
		middle_name.text = middle_name.text.upper()
		self.delNumber(middle_name)
		if len(middle_name.text) > 2:
			self.middle_name = True
		else:
			self.middle_name = False


	def onTextLastName(self):
		last_name = self.ids.last_name
		last_name.text = last_name.text.replace(' ', '')
		last_name.text = last_name.text.upper()
		self.delNumber(last_name)
		if len(last_name.text) > 2:
			self.last_name = True
		else:
			self.last_name = False


	def onTextName(self):
		name:str = self.ids.name
		name.text = name.text.upper()
		names:list = word_tokenize(name.text)
		self.delNumber(name)
		for x in names:
			if len(x) <= 2:
				self.name_ = False

		self.name_ = True

	def onTextEmail(self):
		email = self.ids.email
	
		name = self.ids.name.text
		middle_name = self.ids.middle_name.text
		last_name = self.ids.last_name.text
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
				
				self.date_birth = True

			else:
				if len(date_birth.text) == 10:
					date_birth.text = ''
				self.date_birth = False
		else:
			date_birth.text = '2005/01/01'

		if len(date_birth.text) < 8 and date_birth.text.count('/') == 2:
			date_birth.text = '2005/01/01'


	def delFaculties(self, faculty:list):
		layout = self.ids.student_button

		layout.clear_widgets()
		
		n = 0
		for facu in faculty:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if n == "student_faculty":
				valid = False
	
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.ids.student_career.text = 'Seleccionar Carrera'

		self.student_faculty = True


	def onPressStudentFaculty(self):
		##
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex, save_student'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		self.student_career = False
		self.valid_kardex = False
		##
		layout = self.ids.student_button
		layout.cols = 1
		layout.row_default_height = 10
		
		faculties = self.sql.execute('EXECUTE dbo.getFaculties')
		faculty = []
		for facu in faculties:
			faculty.append(facu[0])

		n = 0
		for facu in faculty:
			n += 1
			facu = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{facu}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		screen = app.root.get_screen('add')
		screen.ids.student_faculty.text = A{n}.text
		screen.delFaculties({faculty})
			"""
			self.ids[f'A{n}'] = Builder.load_string(facu)
			layout.add_widget(self.ids[f'A{n}'])


	def delCareers(self, career:list):
		layout = self.ids.student_button

		layout.clear_widgets()
		
		n = 0
		for c in career:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if n == "student_faculty":
				valid = False
	
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.student_career = True


	def onPressStudentCareer(self):
		##
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex, save_student'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		self.valid_kardex = False
		##
		layout = self.ids.student_button
		layout.cols = 1
		layout.row_default_height = 10
		
		careers = self.sql.execute(f'EXECUTE dbo.getCareers \'{self.ids.student_faculty.text}\'')
		career = []
		for c in careers:
			career.append(c[0])

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
		screen = app.root.get_screen('add')
		screen.ids.student_career.text = A{n}.text
		screen.delCareers({career})
			"""
			self.ids[f'A{n}'] = Builder.load_string(c)
			layout.add_widget(self.ids[f'A{n}'])
	

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
		layout = self.ids.student_button
		
		layout.clear_widgets()
		for i in range(1, len_kardex):
			del self.ids[f'mdlabel{i}']

			del self.ids[f'textfield{i}{1}']
			del self.ids[f'textfield{i}{2}']
			del self.ids[f'textfield{i}{3}']
			del self.ids[f'textfield{i}{4}']
			del self.ids[f'textfield{i}{5}']
			del self.ids[f'textfield{i}{6}']

		#self.ids.student_show.remove_widget(self.ids.save_kardex)#remove_widget(self.ids.save_kardex)

		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if n == "student_faculty":
				valid = False
	
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
	

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
			if self.ids[f'textfield{i}{1}'].text != '' and self.ids[f'textfield{i}{2}'].text == '':
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
		
		self.ids.save_kardex.disabled = accepter
		if accepter == False:
			faculty = self.ids.student_faculty.text
			career = self.ids.student_career.text
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
			var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex, save_student'
			var:list = var.split(', ')
			valid = True
			for n in var:
				self.ids[n].disabled = False
		else:
			self.ids.save_kardex.disabled = True
			#self.valid_kardex = False


	def onPressKardex(self):
		##
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex, save_student'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True

		##
		layout = self.ids.student_button
		layout.cols = 7
		layout.row_default_height = 50

		self.actual_kardex = {}

		subjects = f'EXECUTE dbo.getSubjects \'{self.ids.student_faculty.text}\','
		subjects += f'\'{self.ids.student_career.text}\''
		subjects = self.sql.execute(subjects)
		subject = []
		for s in subjects:
			subject.append(s[0])

		n = 0
		for s in subject:
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
				y = f"""
TextInput:
	id: textfield{n}{i}
	name: f'textfield{n}{i}'

	size_hint_x: .15
	multiline: False
	#input_filter: 'int'
	on_text: app.root.get_screen('add').validKardex(textfield{n}{i})
	on_focus: app.root.get_screen('add').validKardex(textfield{n}{i})
	"""
				self.ids[f'textfield{n}{i}'] = Builder.load_string(y)
				layout.add_widget(self.ids[f'textfield{n}{i}'])

				if i > 1:
					self.ids[f'textfield{n}{i}'].disabled = True
				
			self.actual_kardex[self.ids[f'mdlabel{n}'].text] = {'OP1':'', 'OP2':'', 'OP3':'', 'OP4':'', 'OP5':'', 'OP6':''}
		
		student_show_layout = self.ids.student_show

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
		app.root.get_screen('add').ids.student_show.remove_widget(save_kardex)
		del save_kardex
		app.root.get_screen('add').saveKardex()
		"""

		self.ids.save_kardex = Builder.load_string(self.ids.save_kardex)
		student_show_layout.add_widget(self.ids.save_kardex)


	def getPassword(self):
		chars = list('ABCDEFGHIHKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz0123456789')
		password = ''
		for i in range(8):
			try:
				password += chars[random.randint(0, len(chars))]
			except:
				password += chars[random.randint(0, len(chars)-1)]

		return password


	def closeStudentExist(self, *args):
		self.student_exist.dismiss()
		self.enableWidgets()


	def studentExist(self):
		self.student_exist = MDDialog(
				title = 'A ocurrido un error.',
				text = 'Este estudiante ya existe.',
				buttons=[
					MDRectangleFlatButton(
						text = 'Aceptar',
						on_press = self.closeStudentExist
					)
				]
			)
		self.student_exist.open()


	def clearShowStudentInfo(self):
		self.ids.student_show.remove_widget(self.ids.clean_student_info)

		self.ids.student_button.clear_widgets()
		self.ids.teacher.disabled = False
		self.ids.schedule.disabled = False
		self.ids.logout.disabled = False
		##
		var = 'middle_name, last_name, name, email, date_birth'.split(', ')
		for v in var:
			self.ids[v].disabled = False
		#for v in var:
			self.ids[v].line_color_focus = .9, .5, 0, 1
			self.ids[v].mode = 'fill'
			self.ids[v].fill_color = .9, .5, 0, .1
		##


	def showStudentInfo(self,faculty,career,enrollment,middle_name,
		last_name,name,date_birth,email,password,student_status):
		layout = self.ids.student_button
		layout.cols = 1

		##
		var = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex, save_student'.split(', ')
		for v in var:
			self.ids[v].disabled = True
		##

		########################################################################################
		self.ids.show_student1 = f"""
Label:
	text: '[b]DATOS DEL ESTUDIANTE[/b]'
	markup: True
	font_size: 30
	color: 1, 1, 1, 1"""
		self.ids.show_student2 = f"""

Label:
	text: '[b]FACULTAD: [/b] {faculty}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1"""
		self.ids.show_student3 = f"""

Label:
	text: '[b]CARRERA: [/b] {career}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1"""
		self.ids.show_student4 = f"""

Label:
	text: '[b]MATRICULA: [/b]{enrollment}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1"""
		self.ids.show_student5 = f"""

Label:
	text: '[b]ESTUDIANTE: [/b] {name} {middle_name} {last_name}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1"""
		self.ids.show_student6 = f"""

Label:
	text: '[b]ESTADO: [/b] {student_status}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1
		"""

		self.ids.show_student7 = f"""
Label:
	text: '[b]FECHA DE NACIMIENTO: [/b] {date_birth}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1"""

		self.ids.show_student8 = f"""
Label:
	text: '[b]CORREO UNIVERSITARIO: [/b] {email}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1"""

		self.ids.show_student9 = f"""
Label:
	text: '[b]CONTRASEÑA: [/b] {password}'
	markup: True
	font_size: 14
	color: 1, 1, 1, 1"""
		self.ids.clean_student_info = f"""

MDRaisedButton:
	id: clean_student_info
	name: 'clean_student_info'
	
	text: 'Limpiar'
	size_hint_x: 1
	md_bg_color: .6, .6, .6, 1
	on_press: 
		del clean_student_info
		app.root.get_screen('add').clearShowStudentInfo()
		"""
		self.ids.show_student1 = Builder.load_string(self.ids.show_student1)
		self.ids.show_student2 = Builder.load_string(self.ids.show_student2)
		self.ids.show_student3 = Builder.load_string(self.ids.show_student3)
		self.ids.show_student4 = Builder.load_string(self.ids.show_student4)
		self.ids.show_student5 = Builder.load_string(self.ids.show_student5)
		self.ids.show_student6 = Builder.load_string(self.ids.show_student6)
		self.ids.show_student7 = Builder.load_string(self.ids.show_student7)
		self.ids.show_student8 = Builder.load_string(self.ids.show_student8)
		self.ids.show_student9 = Builder.load_string(self.ids.show_student9)
		self.ids.clean_student_info = Builder.load_string(self.ids.clean_student_info)
		layout.add_widget(self.ids.show_student1)
		layout.add_widget(self.ids.show_student2)
		layout.add_widget(self.ids.show_student3)
		layout.add_widget(self.ids.show_student4)
		layout.add_widget(self.ids.show_student5)
		layout.add_widget(self.ids.show_student6)
		layout.add_widget(self.ids.show_student7)
		layout.add_widget(self.ids.show_student8)
		layout.add_widget(self.ids.show_student9)
		self.ids.student_show.add_widget(self.ids.clean_student_info)


	def clearAddStudentInfo(self):
		middle_name = self.ids.middle_name
		last_name = self.ids.last_name
		name = self.ids.name
		email = self.ids.email
		date_birth = self.ids.date_birth
		faculty = self.ids.student_faculty
		career = self.ids.student_career
		kardex = self.ids.kardex
		save = self.ids.save_student

		middle_name.text = ''
		self.middle_name = False
		last_name.text = ''
		self.last_name
		name.text = ''
		self.name_ = False
		email.text = ''
		self.email = False
		date_birth.text = ''
		self.date_birth = False
		faculty.text = 'Seleccionar Facultad'
		faculty.disabled = True
		self.student_faculty = False
		career.text = 'Seleccionar Carrera'
		career.disabled = True
		self.student_career = False
		kardex.disabled = True
		self.valid_kardex = False
		save.disabled = True
		##
		self.actual_kardex = dict()
		self.last_kardex_field = ''
		self.kardex = {}
		self.id_subject = []


	def onPressSaveStudent(self):
		self.onTextEmail()
		existing_student = f"EXECUTE verifyExistingStudent '{self.ids.middle_name.text}',"
		existing_student += f"'{self.ids.last_name.text}', '{self.ids.name.text}', '{self.ids.date_birth.text}'"
		existing_student = self.sql.execute(existing_student)
		for n in existing_student:
			student = n[0]

		if student != '':
			self.studentExist()
		else:
			id_faculty = self.id_faculty
			id_career = self.id_career
			id_subject = self.id_subject
			middle_name = self.ids.middle_name.text
			last_name = self.ids.last_name.text
			name = self.ids.name.text
			date_birth = self.ids.date_birth.text
			##
			email = self.ids.email.text
			num_email = 1
			while True:
				got = ''
				existing_email = self.sql.execute(f"EXECUTE verifYExistingEmail '{email}'")
				for e_m in existing_email:
					got = str(e_m[0])
					break
				
				if got == email:
					if num_email > 1:
						email = got.replace(f'{num_email-1}@', f'{num_email}@')
					else:
						email = got.replace('@', f'{num_email}@')
				else:
					break
				
				num_email += 1
			##
			password = self.getPassword()
			student_status = 'ALTA'
			
			save_student = f"EXECUTE saveStudent {id_faculty},{id_career},'{middle_name}','{last_name}',"
			save_student += f"'{name}','{date_birth}','{email}','{password}','{student_status}'"
			save_student = self.sql.execute(save_student)
			self.sql.commit()
			
			get_student = self.sql.execute(f"EXECUTE getStudent '{middle_name}','{last_name}','{name}'")
			for get in get_student:
				enrollment = get[2] # ID_student
				#password = get[8]

			kard = self.kardex
			for i in range(len(self.kardex)):
				op1 = kard[str(i)][0]
				op2 = kard[str(i)][1]
				op3 = kard[str(i)][2]
				op4 = kard[str(i)][3]
				op5 = kard[str(i)][4]
				op6 = kard[str(i)][5]
				
				save_kardex = f"EXECUTE saveKardex '{id_faculty}', '{id_career}', '{enrollment}', "
				save_kardex += f"'{id_subject[i]}', '{op1}', '{op2}', '{op3}', '{op4}', '{op5}', '{op6}'"
				self.sql.execute(save_kardex)
				self.sql.commit()

			self.showStudentInfo(
				faculty=self.ids.student_faculty.text,
				career=self.ids.student_career.text,
				enrollment=enrollment,
				middle_name=middle_name,
				last_name=last_name,
				name=name,
				date_birth=date_birth,
				email=email,
				password=password,
				student_status=student_status
				)
			self.clearAddStudentInfo()

	def resizeWindowLogin(self):
		Window.size = 700, 450
		Window.left = 300
		Window.top = (750 - 650)*2


	def resizeWindowStudent(self):
		Window.size = 1100, 650
		Window.left = 150
		Window.top = (750 - 650)/2


	def resizeWindowTeacher(self):
		Window.size = 500, 650
		Window.left = 400
		Window.top = (750 - 650)/2


	def resizeWindowSchedule(self):
		Window.size = 500, 690
		Window.left = 400
		Window.top = 35


	def resizeWindowLogout(self):
		self.resizeWindowTeacher()


	def enableWidgets(self):
		################### T E A C H E R ##################
		teacher_middle_name = self.ids.teacher_middle_name
		teacher_last_name = self.ids.teacher_last_name
		teacher_name = self.ids.teacher_name
		teacher_email = self.ids.teacher_email

		teacher_middle_name.disabled = False
		teacher_middle_name.color_mode = 'custom'
		teacher_middle_name.line_color_focus = .9, .5, 0, 1
		teacher_middle_name.mode = 'fill'
		teacher_middle_name.fill_color = .9, .5, 0, .1
		teacher_last_name.disabled = False
		teacher_last_name.color_mode = 'custom'
		teacher_last_name.line_color_focus = .9, .5, 0, 1
		teacher_last_name.mode = 'fill'
		teacher_last_name.fill_color = .9, .5, 0, .1
		teacher_name.disabled = False
		teacher_name.color_mode = 'custom'
		teacher_name.line_color_focus = .9, .5, 0, 1
		teacher_name.mode = 'fill'
		teacher_name.fill_color = .9, .5, 0, .1
		teacher_email.disabled = False
		teacher_email.color_mode = 'custom'
		teacher_email.line_color_focus = .9, .5, 0, 1
		teacher_email.mode = 'fill'
		teacher_email.fill_color = .9, .5, 0, .1
		################## S C H E D U L E #################
		#self.ids.schedule_faculty
		#self.ids.classroom
		#self.ids.banches
		#self.ids.save_classroom
		#self.ids.enable_schedule
		#self.ids.disabled_schedule
		#self.ids.specific_career
		#self.ids.schedule_teacher
		#self.ids.schedule_subject
		#self.ids.schedules
		#self.ids.schedule


	###################################### T E A C H E R ############################################
	def onTextTeacherMiddleName(self):
		middle_name = self.ids.teacher_middle_name
		
		middle_name.text = middle_name.text.replace(' ', '')
		middle_name.text = middle_name.text.upper()
		self.delNumber(middle_name)
		if len(middle_name.text) > 2:
			self.teacher_middle_name = True
		else:
			self.teacher_middle_name = False


	def onTextTeacherLastName(self):
		last_name = self.ids.teacher_last_name
		last_name.text = last_name.text.replace(' ', '')
		last_name.text = last_name.text.upper()
		self.delNumber(last_name)
		if len(last_name.text) > 2:
			self.teacher_last_name = True
		else:
			self.teacher_last_name = False


	def onTextTeacherName(self):
		name:str = self.ids.teacher_name
		name.text = name.text.upper()
		names:list = word_tokenize(name.text)
		self.delNumber(name)
		for x in names:
			if len(x) <= 2:
				self.teacher_name_ = False

		self.teacher_name_ = True

	def onTextTeacherEmail(self):
		email = self.ids.teacher_email
	
		name = self.ids.teacher_name.text
		middle_name = self.ids.teacher_middle_name.text
		last_name = self.ids.teacher_last_name.text
		if len(name) > 2 and len(middle_name) > 2 and len(last_name) > 2:
			name:str = word_tokenize(name)[0]
			middle_name:str = middle_name
			last_name:str = last_name[0] + last_name[len(last_name)-1]

			email.text = f'{name}.{middle_name + last_name}@uanl.edu.mx'.lower()
			email.hint_text = ''
			self.teacher_email = True

		else:
			email.focus = False
			email.hint_text = 'Correo Universitario'
			self.teacher_email = False

	def delFaculties(self, faculty:list):
		layout = self.ids.student_button

		layout.clear_widgets()
		
		n = 0
		for facu in faculty:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if n == "student_faculty":
				valid = False
	
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.ids.student_career.text = 'Seleccionar Carrera'

		self.student_faculty = True


	def delTeacherFaculties(self, faculty:list):
		layout = self.ids.teacher_info

		layout.clear_widgets()
		
		n = 0
		for facu in faculty:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'teacher_middle_name, teacher_last_name, teacher_name, email, teacher_faculty, teacher_career'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if n == "teacher_faculty":
				valid = False
	
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.ids.teacher_career.text = 'Seleccionar Carrera'

		self.teacher_faculty = True


	def onPressTeacherFaculty(self):
		##
		var:str = 'teacher_middle_name, teacher_last_name, teacher_name, teacher_email, teacher_faculty, teacher_career, save_teacher'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		self.teacher_career = False
		##
		layout = self.ids.teacher_info
		layout.cols = 1
		layout.row_default_height = 10
		
		faculties = self.sql.execute('EXECUTE dbo.getFaculties')
		faculty = []
		for facu in faculties:
			faculty.append(facu[0])

		n = 0
		for facu in faculty:
			n += 1
			f = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{facu}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		screen = app.root.get_screen('add')
		screen.ids.teacher_faculty.text = A{n}.text
		screen.delTeacherFaculties({faculty})
			"""
			self.ids[f'A{n}'] = Builder.load_string(f)
			layout.add_widget(self.ids[f'A{n}'])

			print(layout)
			print(self.ids[f'A{n}'])
			print(facu)


	def delTeacherCareers(self, career:list):
		layout = self.ids.teacher_info

		layout.clear_widgets()
		
		n = 0
		for c in career:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'teacher_middle_name, teacher_last_name, teacher_name, teacher_email, teacher_faculty, teacher_career'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if n == "teacher_faculty":
				valid = False
	
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.teacher_career = True


	def onPressTeacherCareer(self):
		##
		var:str = 'teacher_middle_name, teacher_last_name, teacher_name, teacher_email, teacher_faculty, teacher_career, save_teacher'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.teacher_info
		layout.cols = 1
		#layout.row_default_height = 10
		
		careers = self.sql.execute(f'EXECUTE dbo.getCareers \'{self.ids.teacher_faculty.text}\'')
		career = []
		for c in careers:
			career.append(c[0])

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
		screen = app.root.get_screen('add')
		screen.ids.teacher_career.text = A{n}.text
		screen.delTeacherCareers({career})
			"""
			self.ids[f'A{n}'] = Builder.load_string(c)
			layout.add_widget(self.ids[f'A{n}'])


	def closeTeacherExist(self, *args):
		self.teacher_exist.dismiss()


	def teacherExist(self, n:int):
		if n == 1:
			self.teacher_exist = MDDialog(
					title='A ocurrido un error.',
					text='Este profesor ya imparte clases en esta facultad y carrera.',
					buttons=[
						MDRectangleFlatButton(
							text='Aceptar',
							on_press=self.closeTeacherExist
						)
					]
			)

		else:
			button = MDRectangleFlatButton(
						text='Agregar',
						on_press=self.closeTeacherExist
					)
			button.bind(on_press=self.saveTeacher)
			self.teacher_exist = MDDialog(
					title='Atención.',
					text='''Este profesor ya imparte clases en otra facultad/carrera.
¿Agregar de todos modos?''',
					buttons=[
						button,
						MDRectangleFlatButton(
							text='Cancelar',
							on_press=self.closeTeacherExist,
						)
					]
			)

		self.teacher_exist.open()


	def clearShowTeacherInfo(self):
		layout = self.ids.show_teacher
		layout.clear_widgets()

		teacher_scrolling = """
ScrollView:
	do_scroll_y: True
"""
		teacher_info = """
GridLayout:
	id: teacher_info
	name: 'teacher_info'

	cols: 1
	size_hint_y: None
	row_default_height: 50
	height: self.minimum_height
"""
		teacher_scrolling = Builder.load_string(teacher_scrolling)
		layout.add_widget(teacher_scrolling)
		self.ids.teacher_info = Builder.load_string(teacher_info)
		teacher_scrolling.add_widget(self.ids.teacher_info)
		
		self.ids.student.disabled = False
		self.ids.schedule.disabled = False
		self.ids.logout.disabled = False
		##
		var = 'teacher_middle_name, teacher_last_name, teacher_name, teacher_email'.split(', ')
		for v in var:
			self.ids[v].disabled = False
			self.ids[v].line_color_focus = .9, .5, 0, 1
			self.ids[v].mode = 'fill'
			self.ids[v].fill_color = .9, .5, 0, .1
		##


	def showTeacherInfo(self,faculty,career,enrollment,middle_name,
		last_name,name,email,password,teacher_status):
		layout = self.ids.show_teacher
		layout.cols = 1

		##t
		var = 'teacher_middle_name, teacher_last_name, teacher_name, teacher_email, teacher_faculty, teacher_career, save_teacher'.split(', ')
		for v in var:
			self.ids[v].disabled = True
		##

		########################################################################################
		self.ids.show_teacher1 = f"""
Label:
	text: '[b]DATOS DEL PROFESOR[/b]'
	markup: True
	font_size: 24
	color: 1, 1, 1, 1"""
		self.ids.show_teacher2 = f"""

Label:
	text: '[b]FACULTAD: [/b] {faculty}'
	markup: True
	font_size: 9
	color: 1, 1, 1, 1"""
		self.ids.show_teacher3 = f"""

Label:
	text: '[b]CARRERA: [/b] {career}'
	markup: True
	font_size: 9
	color: 1, 1, 1, 1"""
		self.ids.show_teacher4 = f"""

Label:
	text: '[b]MATRICULA: [/b]{enrollment}'
	markup: True
	font_size: 9
	color: 1, 1, 1, 1"""
		self.ids.show_teacher5 = f"""

Label:
	text: '[b]PROFESOR: [/b] {name} {middle_name} {last_name}'
	markup: True
	font_size: 9
	color: 1, 1, 1, 1"""
		self.ids.show_teacher6 = f"""

Label:
	text: '[b]ESTADO: [/b] {teacher_status}'
	markup: True
	font_size: 9
	color: 1, 1, 1, 1
		"""

		self.ids.show_teacher7 = f"""
Label:
	text: '[b]CORREO UNIVERSITARIO: [/b] {email}'
	markup: True
	font_size: 9
	color: 1, 1, 1, 1"""

		self.ids.show_teacher8 = f"""
Label:
	text: '[b]CONTRASEÑA: [/b] {password}'
	markup: True
	font_size: 9
	color: 1, 1, 1, 1"""
		self.ids.clean_teacher_info = f"""

MDRaisedButton:
	id: clean_teacher_info
	name: 'clean_teacher_info'
	
	text: 'Limpiar'
	size_hint_x: 1
	md_bg_color: 0, 0, 0, 1#.24, .74, .53, 1
	on_press:
		app.root.get_screen('add').clearShowTeacherInfo()
		"""
		self.ids.show_teacher1 = Builder.load_string(self.ids.show_teacher1)
		self.ids.show_teacher2 = Builder.load_string(self.ids.show_teacher2)
		self.ids.show_teacher3 = Builder.load_string(self.ids.show_teacher3)
		self.ids.show_teacher4 = Builder.load_string(self.ids.show_teacher4)
		self.ids.show_teacher5 = Builder.load_string(self.ids.show_teacher5)
		self.ids.show_teacher6 = Builder.load_string(self.ids.show_teacher6)
		self.ids.show_teacher7 = Builder.load_string(self.ids.show_teacher7)
		self.ids.show_teacher8 = Builder.load_string(self.ids.show_teacher8)
		self.ids.clean_teacher_info = Builder.load_string(self.ids.clean_teacher_info)
		layout.add_widget(self.ids.show_teacher1)
		layout.add_widget(self.ids.show_teacher2)
		layout.add_widget(self.ids.show_teacher3)
		layout.add_widget(self.ids.show_teacher4)
		layout.add_widget(self.ids.show_teacher5)
		layout.add_widget(self.ids.show_teacher6)
		layout.add_widget(self.ids.show_teacher7)
		layout.add_widget(self.ids.show_teacher8)
		layout.add_widget(self.ids.clean_teacher_info)


	def clearAddTeacherInfo(self):
		middle_name = self.ids.teacher_middle_name
		last_name = self.ids.teacher_last_name
		name = self.ids.teacher_name
		email = self.ids.teacher_email
		faculty = self.ids.teacher_faculty
		career = self.ids.teacher_career
		save = self.ids.save_teacher

		middle_name.text = ''
		self.teacher_middle_name = False
		last_name.text = ''
		self.teacher_last_name
		name.text = ''
		self.teacher_name_ = False
		email.text = ''
		self.teacher_email = False
		faculty.text = 'Seleccionar Facultad'
		faculty.disabled = True
		self.teacher_faculty = False
		career.text = 'Seleccionar Carrera'
		career.disabled = True
		self.teacher_career = False
		save.disabled = True
		##
		self.id_subject = []

		self.enableWidgets()


	def saveTeacher(self, *args):
		exist = False
		for i in args:
			if i.text == 'Agregar':
				exist = True

		id_faculty = self.t_id_faculty
		id_career = self.t_id_career
		middle_name = self.ids.teacher_middle_name.text
		last_name = self.ids.teacher_last_name.text
		name = self.ids.teacher_name.text
		if exist == True:
			enrollment = self.t_enrollment
			email = self.t_email
			password = self.t_password

		else:
			get = self.sql.execute(f"EXECUTE getTeacherEnrollment")
			for g in get:
				enrollment = g[0]
			enrollment = int(enrollment)+1
			email = self.ids.teacher_email.text
			password = self.getPassword()
		teacher_status = 'ALTA'

		print(id_faculty)
		print(id_career)
		print(enrollment)
		print(middle_name)
		print(last_name)
		print(name)
		print(email)
		print(password)
		print(teacher_status)
		save_teacher = f"EXECUTE saveTeacher {id_faculty},{id_career},{enrollment},'{middle_name}',"
		save_teacher += f"'{last_name}','{name}','{email}','{password}','{teacher_status}'"
		self.sql.execute(save_teacher)
		self.sql.commit()
		
		self.showTeacherInfo(
			faculty=self.ids.teacher_faculty.text,
			career=self.ids.teacher_career.text,
			enrollment=enrollment,
			middle_name=middle_name,
			last_name=last_name,
			name=name,
			email=email,
			password=password,
			teacher_status=teacher_status
		)
		self.clearAddTeacherInfo()


	def onPressSaveTeacher(self):
		self.onTextTeacherEmail()
		existing_teacher = f"EXECUTE verifyExistingTeacher '{self.ids.teacher_middle_name.text}', "
		existing_teacher += f"'{self.ids.teacher_last_name.text}', '{self.ids.teacher_name.text}', "
		existing_teacher += f"'{self.ids.teacher_email.text}'"
		existing_teacher = self.sql.execute(existing_teacher)
		ids_faculty = []
		ids_career = []
		for n in existing_teacher:
			ids_faculty.append(n[0])
			ids_career.append(n[1])
			id_teacher = n[2]
			self.t_enrollment = n[3]
			self.t_middle_name = n[4]
			self.t_last_name = n[5]
			self.t_name = n[6]
			self.t_email = n[7]
			self.t_password = n[8]

		data = self.sql.execute(f'EXECUTE getTeacherIds [{self.ids.teacher_faculty.text}],[{self.ids.teacher_career.text}]')
		for d in data:
			self.t_id_faculty = d[0]
			self.t_id_career = d[1]
			
		#valid = False
		exist = False
		if self.t_id_faculty in ids_faculty:
			exist = True
			if self.t_id_career in ids_career:
				self.teacherExist(1)
			else:
				self.teacherExist(2)
		elif ids_faculty != [0]:
			valid = True
			self.teacherExist(2)
		else:
			self.saveTeacher()
	##################################### S C H E D U L E ###########################################

	def delScheduleFaculties(self, faculty:list):
		layout = self.ids.schedule_data

		layout.clear_widgets()
		
		n = 0
		for facu in ['CIENCIAS FISICO-MATEMATICAS']:#faculty:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'schedule_faculty, classroom, banches'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.schedule_faculty = True


	def onPressScheduleFaculty(self):
		##
		var:str = 'schedule_faculty, classroom, banches, save_classroom, available_schedule, '
		var += 'unavailable_schedule, schedule_career, schedule_teacher, schedule_subject, schedules, save_schedule, finalize'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		self.classroom = False
		self.banches = False
		##
		layout = self.ids.schedule_data
		layout.cols = 1
		layout.row_default_height = 10
		
		faculties = self.sql.execute('EXECUTE dbo.getFaculties')
		faculty = []
		for facu in faculties:
			faculty.append(facu[0])

		n = 0
		for facu in ['CIENCIAS FISICO-MATEMATICAS']:#faculty:
			n += 1
			facu = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{facu}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		screen = app.root.get_screen('add')
		screen.ids.schedule_faculty.text = A{n}.text
		screen.delScheduleFaculties({faculty})
			"""
			self.ids[f'A{n}'] = Builder.load_string(facu)
			layout.add_widget(self.ids[f'A{n}'])

		self.schedule_faculty = False


	def validClassroomBanches(self):
		if self.classroom == True and self.banches == True:
			self.ids.save_classroom.disabled = False

		else:
			self.ids.save_classroom.disabled = True


	def onTextClassroom(self):
		classroom = self.ids.classroom

		classroom.text = classroom.text.upper()

		chars = list('°¬|!"#$%&/()=\'?\\¿¡´¨+*~{[}]~^`,;.:_')
		if set(chars) & set(classroom.text):
			for char in chars:
				classroom.text = classroom.text.replace(char, '')

		if len(classroom.text) > 0:
			self.classroom = True
		else:
			self.classroom = False

		self.validClassroomBanches()


	def onTextBanches(self):
		banches = self.ids.banches

		if banches.text != '':
			if int(banches.text) < 10 and banches.focus == False:
				banches.text = '10'

			if int(banches.text) > 65 and banches.focus == False:
				banches.text = '65'

			self.banches = True
		else:
			self.banches = False
		self.validClassroomBanches()


	def closeDialogNameClassroom(self):
		self.dialog_name_classroom.dismiss()


	def saveClassroom(self):
		id_faculty = self.schedule_id_faculty
		classroom = self.schedule_classroom
		banches = self.schedule_banches

		self.sql.execute(f'EXECUTE saveClassroom {id_faculty},\'{classroom}\',{banches}')
		self.sql.commit()
		data = self.sql.execute(f'EXECUTE getClassroomData \'{self.ids.schedule_faculty.text}\',\'{self.ids.classroom.text}\'')
		for found in data:
			id_faculty = found[0]
			id_classroom = found[1]
			banches = found[2]
		
		self.ids.banches.text = str(banches)
		self.schedule_id_faculty = id_faculty
		self.id_classroom = id_classroom

		self.ids.schedule_faculty.disabled = True
		self.ids.classroom.disabled = True
		self.ids.banches.disabled = True

		widgets = 'schedule_career, schedule_teacher, schedule_subject, group, schedules, finalize'
		widgets = widgets.split(', ')

		for widget in widgets:
			self.ids[widget].disabled = False

		self.onTextAvailableSchedule()
		self.onTextUnavailableSchedule()


	def saveClassroomDisabled(self):
		self.ids.save_classroom.disabled = True


	def closeDialogAddClassroom(self, *args):
		for i in args:
			if i.text == 'Aceptar':
				self.saveClassroom()

		self.dialog_add_classroom.dismiss()


	def dialogAddClassroom(self):
		self.dialog_add_classroom = MDDialog(
			title='Este salon de clases no existe.',
			text='¿Desea agregar el aula?',
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=self.closeDialogAddClassroom
				),
				MDRectangleFlatButton(
					text='Cancelar',
					on_press=self.closeDialogAddClassroom
				)
			]
		)
		self.dialog_add_classroom.open()


	def onPressSaveClassroom(self):
		if self.classroom == True and self.banches == True:
			data = self.sql.execute(f'EXECUTE getClassroomData \'{self.ids.schedule_faculty.text}\',\'{self.ids.classroom.text}\'')
			for found in data:
				id_faculty = found[0]
				id_classroom = found[1]
				banches = found[2]

			if id_faculty == 0 and id_classroom == 0 and banches == 0:
				data = self.sql.execute(f"EXECUTE getIDFaculty [{self.ids.schedule_faculty.text}]")
				for d in data:
					self.schedule_id_faculty=d[0]
				self.schedule_classroom=self.ids.classroom.text
				self.schedule_banches=self.ids.banches.text
				self.dialogAddClassroom()
			else:
				self.ids.banches.text = str(banches)
				self.schedule_id_faculty = id_faculty
				self.id_classroom = id_classroom

				self.ids.schedule_faculty.disabled = True
				self.ids.classroom.disabled = True
				self.ids.banches.disabled = True
				self.ids.save_classroom.disabled = True

				self.ids.schedule_career.disabled = False

				self.onTextAvailableSchedule()
				self.onTextUnavailableSchedule()
		else:
			self.ids.save_classroom.disabled = True


	def onTextAvailableSchedule(self):
		available_schedule = self.ids.available_schedule
		
		got = '''07:00-07:30;07:30-08:00;
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
		got = got.replace('\n', '')
		got = got.replace(' ', '')
		got = got.replace('\t', '')
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		print(got)
		available_schedule.text = got


	def onTextUnavailableSchedule(self):
		unavailable_schedule = self.ids.unavailable_schedule
		
		available_schedule = self.ids.available_schedule
		listed = available_schedule.text
		listed = listed.split(';')

		getting = self.sql.execute(f"EXECUTE getUnavailableSchedule '{self.schedule_id_faculty}','{self.id_classroom}'")
		ids_career = []
		ids_teacher = []
		ids_subject = []
		ids_schedule = []
		ids_group = []
		unavailables = []
		for g in getting:
			ids_career.append(g[0])
			ids_teacher.append(g[1])
			ids_subject.append(g[2])
			ids_schedule.append(g[3])
			ids_group.append(g[4])
			unavailables.append(g[5])

		full_separate = []
		for unavailable in unavailables:
			separate = unavailable.split(';')
			for i in separate:
				full_separate.append(i)
		full_separate.sort()
		while True:
			if full_separate != []:
				if full_separate[0] == '':
					full_separate = full_separate[1:]
				else:
					break
			else:
				break
		for unavailable in full_separate:
			try:
				listed.remove(unavailable)
			except:
				pass

		available_schedule = ''
		for i in listed:
			available_schedule += f'{i};'
		self.ids.available_schedule.text = available_schedule
		unavailable_schedule = ''
		for j in full_separate:
			unavailable_schedule += f'{j};'
		self.ids.unavailable_schedule.text = unavailable_schedule

		return [ids_career, ids_teacher, ids_subject, ids_schedule, ids_group, full_separate] 


	def delScheduleCareers(self, career):
		layout = self.ids.schedule_data

		layout.clear_widgets()
		
		n = 0
		for c in ['LICENCIADO EN SEGURIDAD EN TECNOLOGIAS DE INFORMACION']:#career:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'schedule_career, schedule_teacher'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.schedule_career = True


	def onPressScheduleCareer(self):
		##
		var:str = 'schedule_career, schedule_teacher, schedule_subject, group, schedules, save_schedule, finalize'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.schedule_data
		layout.cols = 1
		layout.row_default_height = 10
		
		careers = self.sql.execute(f'EXECUTE dbo.getCareers \'{self.ids.schedule_faculty.text}\'')
		career = []
		for c in careers:
			career.append(c[0])

		n = 0
		for c in ['LICENCIADO EN SEGURIDAD EN TECNOLOGIAS DE INFORMACION']:#career:
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
		screen = app.root.get_screen('add')
		screen.ids.schedule_career.text = A{n}.text
		screen.delScheduleCareers({career})
			"""
			self.ids[f'A{n}'] = Builder.load_string(c)
			layout.add_widget(self.ids[f'A{n}'])


	def delScheduleTeachers(self, teacher):
		layout = self.ids.schedule_data

		layout.clear_widgets()
		
		n = 0
		for t in ['GONZALEZ GONZALEZ OSVALDO HABIB']:#teacher:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'schedule_teacher, schedule_subject'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.schedule_teacher = True


	def closeTeachersDialog(self, *args):
		self.teachers_dialog.dismiss()


	def onPressScheduleTeacher(self):
		##
		var:str = 'schedule_teacher, schedule_subject, group, schedules, save_schedule, finalize'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.schedule_data
		layout.cols = 1
		
		teachers = self.sql.execute(f'EXECUTE dbo.getTeachers \'{self.ids.schedule_faculty.text}\',\'{self.ids.schedule_career.text}\'')
		teacher = []
		for t in teachers:
			teacher.append(f'{t[0]} {t[1]} {t[2]}')

		n = 0
		for t in ['GONZALEZ GONZALEZ OSVALDO HABIB']:#teacher:
			n += 1
			t = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{t}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		screen = app.root.get_screen('add')
		screen.ids.schedule_teacher.text = A{n}.text
		screen.delScheduleTeachers({teacher})
			"""
			self.ids[f'A{n}'] = Builder.load_string(t)
			layout.add_widget(self.ids[f'A{n}'])

		if teacher == []:
			self.teachers_dialog = MDDialog(
				title='Atención.',
				text='No hay profesores disponibles en esta carrera.',
				buttons=[
					MDRectangleFlatButton(
						text='Aceptar',
						on_press=self.closeTeachersDialog
					)
				]
			)
			self.teachers_dialog.open()

		self.schedule_teacher = False


	def delScheduleSubjects(self, subject):
		layout = self.ids.schedule_data

		layout.clear_widgets()
		
		n = 0
		for s in ['PROGRAMA DE SEGURIDAD']:#subject:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'schedule_subject, group'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.schedule_subject = True


	def onPressScheduleSubject(self):
		##
		var:str = 'schedule_subject, group, schedules, save_schedule, finalize'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.schedule_data
		layout.cols = 1
		layout.row_default_height = 10
		
		subjects = self.sql.execute(f'EXECUTE dbo.getSubjects \'{self.ids.schedule_faculty.text}\',\'{self.ids.schedule_career.text}\'')
		subject = []
		for s in subjects:
			subject.append(s[0])

		n = 0
		for s in ['PROGRAMA DE SEGURIDAD']:#subject:
			n += 1
			s = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{s}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		screen = app.root.get_screen('add')
		screen.ids.schedule_subject.text = A{n}.text
		screen.delScheduleSubjects({subject})
			"""
			self.ids[f'A{n}'] = Builder.load_string(s)
			layout.add_widget(self.ids[f'A{n}'])

		self.schedule_subject = False


	def closeGroupDialog(self, *args):
		self.group_dialog.dismiss()


	def onTextGroup(self):
		g = self.ids.group
		if g.text != '':
			try:
				group = int(g.text)
				self.ids.schedules.disabled = False
				self.group = True
			except:
				self.ids.schedules.disabled = True
				self.group_dialog = MDDialog(
					title='Error',
					text='El grupo no acepta ni letras ni caracteres.',
					buttons=[
						MDRectangleFlatButton(
							text='Aceptar',
							on_press=self.closeGroupDialog
						)
					]
				)
				chars = g.text
				for char in chars:
					if char not in '0123456789':
						g.text = g.text.replace(char, '')
				self.group_dialog.open()
				self.group = False

		if g.text == '' and g.focus == False:
			self.ids.schedules.disabled = True
			self.group_dialog = MDDialog(
				title='Atención.',
				text='Es obligatorio agregar el grupo.',
				buttons=[
					MDRectangleFlatButton(
						text='Aceptar',
						on_press=self.closeGroupDialog
					)
				]
			)
			self.group_dialog.open()
			self.group = False


	def closeOutTimeDialog(self, *args):
		self.out_time_dialog.dismiss()


	def delSchedules(self, schedule):
		layout = self.ids.schedule_data

		layout.clear_widgets()
		
		n = 0
		for s in schedule:
			n += 1
			del self.ids[f'A{n}']

		var:str = 'schedules, add_schedule'
		var:list = var.split(', ')
		valid = True
		for n in var:
			self.ids[n].disabled = False
			
			if valid:
				self.ids[n].color_mode = 'custom'
				self.ids[n].line_color_focus = .9, .5, 0, 1
				self.ids[n].multiline = False
				self.ids[n].mode = 'fill'
				self.ids[n].fill_color = .9, .5, 0, .1
				self.ids[n].size_hint_x = .9
		
		self.schedules = True


	def onPressSchedules(self):
		##
		var:str = 'schedules, add_schedule, save_schedule, finalize'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.schedule_data
		layout.cols = 1
		layout.row_default_height = 10
		
		schedule = self.ids.available_schedule
		to_add = self.ids.to_add.text.split(';')
		for to in to_add:
			if to != '':
				schedule.text = schedule.text.replace(f'{to};', '')

		n = 0
		for s in schedule.text.split(';'):
			n += 1
			s = f"""
MDRaisedButton:
	id: A{n}
	name: 'A{n}'

	text: '{s}'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: 
		screen = app.root.get_screen('add')
		screen.ids.schedules.text = A{n}.text
		screen.delSchedules({schedule.text.split(';')})
			"""
			self.ids[f'A{n}'] = Builder.load_string(s)
			layout.add_widget(self.ids[f'A{n}'])

		self.schedules = False


	def sortSchedules(self):
		sort = self.ids.to_add.text.split(';')
		sort.sort()
		self.ids.to_add.text = ''
		
		for s in sort:
			if s != '':
				self.ids.to_add.text += s + ';'


	def closeScheduleExist(self, *args):
		self.schedule_exist.dismiss()


	def closeDialogGroupExist(self, *args):
		self.dialog_group_exist.dismiss()


	def closeBusySchedule(self, *args):
		self.busy_schedule.dismiss()


	def existingSchedules(self, command:str, schedule:str) -> bool and str:
		valid = False
		existing = ''
		getting = self.sql.execute(command)
		existing_schedules = []
		for g in getting:
			existing_schedules.append(g[0])
		
		if existing_schedules != []:
			existing_schedules = existing_schedules[0]
			existing_schedule = []
			existing_sch = existing_schedules.split(';')
			for x in existing_sch:
				existing_schedule.append(f'{x};')

			try:
				existing_schedule.remove(';')
				existing_schedule.remove('')
			except:
				pass
			for i in existing_schedule:
				if i in schedule:
					existing = i
					valid = True
					break
		return [valid, existing]


	def clearScheduleFields(self):
		career = self.ids.schedule_career
		career.text = 'Seleccionar Carrera'
		career.disabled = True
		self.schedule_career = False
		teacher = self.ids.schedule_teacher
		teacher.text = 'Seleccionar Profesor'
		teacher.disabled = True
		self.schedule_teacher = False
		subject = self.ids.schedule_subject
		subject.text = 'Seleccionar Materia'
		subject.disabled = True
		self.schedule_subject = False
		group = self.ids.group
		group.text = ''
		group.disabled = True
		self.group = False
		to_add = self.ids.to_add
		to_add.text = ''
		schedules = self.ids.schedules
		schedules.text = 'Seleccionar Horario'
		schedules.disabled = True
		self.schedule = False
		self.ids.save_schedule.disabled = True


	def onPressSaveSchedule(self):
		#self.schedule_id_faculty
		to_add = self.ids.schedules.text
		
		full_data = self.onTextUnavailableSchedule()
		
		ids_career = full_data[0]
		ids_teacher = full_data[1]
		ids_subject = full_data[2]
		ids_schedule = full_data[3]
		ids_group = full_data[4]
		unavailables = full_data[5]

		schedules_app = to_add.split(';')
		valid = False
		for schedule in schedules_app:
			if schedule in unavailables:
				self.schedule_exist = MDDialog(
					title='Aviso.',
					text=f'\'{schedule}\' ya esta ocupado.',
					buttons=[
						MDRectangleFlatButton(
							text='Aceptar',
							on_press=self.closeScheduleExist
						)
					]
				)
				self.schedule_exist.open()
				valid = True
				break

		id_faculty = self.schedule_id_faculty # ID
		id_classroom = self.id_classroom # ID
		getting = self.sql.execute(f"EXECUTE getIds [{self.ids.schedule_faculty.text}],[{self.ids.schedule_career.text}],[{self.ids.schedule_subject.text}]")
		for g in getting:
			id_career = g[1] # ID
			id_subject = g[2] # ID

		full_name = self.ids.schedule_teacher.text.split(' ')
		middle_name = full_name[0]
		last_name = full_name[1]
		name_list = full_name[2:]
		name = ''
		for i in name_list:
			name += f'{i} '
		name = name[:len(name)-1]
		getting = self.sql.execute(f"EXECUTE getIdTeacher [{id_faculty}],[{id_career}],[{middle_name}],[{last_name}],[{name}]")
		for g in getting:
			id_teacher = g[0] # ID
		id_group = self.ids.group.text # ID
		schedule = self.ids.to_add.text
		valid2 = False
		if id_career in ids_career:
			if id_teacher in ids_teacher:
				if id_subject in ids_subject:
					if id_group in ids_group:
						self.dialog_group_exist = MDDialog(
							title='Atención.',
							text=''''Esta clase ya fue agregada.
Si desea modificar el horario, acceda a la opción 'Modificar'.''',
							buttons=[
								MDRectangleFlatButton(
									text='Aceptar',
									on_press=self.closeDialogGroupExist
								)
							]
						)
						self.dialog_group_exist.open()
						valid = True
						valid2 = True
		if valid == False:
			get = self.existingSchedules(
				command=f'EXECUTE getAllClassroomsGroup [{self.schedule_id_faculty}],[{id_group}]',
				schedule=schedule
			)
			valid = get[0]
			if valid == True:
				self.busy_schedule = MDDialog(
					title='Error.',
					text=f'Este grupo({id_group}) ya tiene clases en este horario({get[1]})',
					buttons=[
						MDRectangleFlatButton(
							text='Aceptar',
							on_press=self.closeBusySchedule
						)
					]
				)
				self.busy_schedule.open()

		if valid == False:
			get = self.existingSchedules(
				command=f"EXECUTE getAllClassroomsTeacher {self.schedule_id_faculty},{id_teacher}",
				schedule=schedule
			)
			valid = get[0]
			if valid == True:
				self.busy_schedule = MDDialog(
					title='Error.',
					text=f'El profesor({self.ids.schedule_teacher.text}) ya imparte clases en este horario({get[1]})',
					buttons=[
						MDRectangleFlatButton(
							text='Aceptar',
							on_press=self.closeBusySchedule
						)
					]
				)
				self.busy_schedule.open()

		if valid == False:
			self.sql.execute(f"EXECUTE saveSchedule [{id_faculty}],[{id_classroom}],[{id_career}],[{id_teacher}],[{id_subject}],[{id_group}],[{schedule}]")
			self.sql.commit()
			self.clearScheduleFields()
		else:
			if valid2 == True:
				self.clearScheduleFields()
				self.clearClassroomFields()
				self.ids.finalize.disabled = True
			else:
				self.ids.save_schedule.disabled = True
				self.ids.add_schedule.disabled = True
				self.ids.schedules.disabled = False
				self.ids.to_add.text = self.ids.to_add.text.replace(get[1], '')


	def clearClassroomFields(self):
		classroom = self.ids.classroom
		classroom.text = ''
		classroom.disabled = True
		self.classroom = False
		banches = self.ids.banches
		banches.text = ''
		banches.disabled = True
		self.banches = False
		faculty = self.ids.schedule_faculty
		faculty.text = 'Seleccionar Facultad'
		faculty.disabled = False


	def onPressFinalize(self):
		self.clearScheduleFields()
		self.clearClassroomFields()
		self.ids.finalize.disabled = True
