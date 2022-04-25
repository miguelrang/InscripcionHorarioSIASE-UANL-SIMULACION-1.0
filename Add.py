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
			if self.teacher_last_name == True:
				if self.teacher_name_ == True:
					if self.teacher_email == True:
						verifier2 = not self.ids.teacher_middle_name.disabled
						if self.teacher_faculty == True:
							if self.teacher_career == True:
								verifier = True
						
							
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
						if int(self.ids[f'textfield{i}{1}'].text) > -1 and int(self.ids[f'textfield{i}{3}'].text) < 70:
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


	def studentExist(self):
		self.student_exist = MDDialog(
				title = 'A ocurrido un error.',
				text = 'Este estudiante ya existe.',
				buttons = [
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
		#self.ids.fullname_teacher
		#self.ids.name_subject
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
		screen.ids.teacher_faculty.text = A{n}.text
		screen.delTeacherFaculties({faculty})
			"""
			self.ids[f'A{n}'] = Builder.load_string(facu)
			layout.add_widget(self.ids[f'A{n}'])


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
		layout.row_default_height = 10
		
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


	def teacherExist(self):
		self.teacher_exist = MDDialog(
				title = 'A ocurrido un error.',
				text = 'Este profesor ya existe.',
				buttons = [
					MDRectangleFlatButton(
							text = 'Aceptar',
							on_press = self.closeTeacherExist
						)
				]
			)
		self.teacher_exist.open()


	def clearShowTeacherInfo(self):
		#self.ids.teacher_show.remove_widget(self.ids.clean_student_info)

		self.ids.show_teacher.clear_widgets()
		self.ids.student.disabled = False
		self.ids.schedule.disabled = False
		self.ids.logout.disabled = False
		##
		var = 'teacher_middle_name, teacher_last_name, teacher_name, teacher_email'.split(', ')
		for v in var:
			self.ids[v].disabled = False
		#for v in var:
			self.ids[v].line_color_focus = .9, .5, 0, 1
			self.ids[v].mode = 'fill'
			self.ids[v].fill_color = .9, .5, 0, .1
		##


	def showTeacherInfo(self,faculty,career,enrollment,middle_name,
		last_name,name,email,password,teacher_status):
		layout = self.ids.show_teacher
		layout.cols = 1

		##
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
		del clean_teacher_info
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


	def onPressSaveTeacher(self):
		self.onTextTeacherEmail()
		existing_teacher = f"EXECUTE verifyExistingTeacher '{self.ids.teacher_middle_name.text}',"
		existing_teacher += f"'{self.ids.teacher_last_name.text}', '{self.ids.teacher_name.text}'"
		existing_teacher = self.sql.execute(existing_teacher)
		for n in existing_teacher:
			teacher = n[0]

		if teacher != '':
			self.teacherExist()
		else:
			ids = self.sql.execute(f'EXECUTE getTeacherIds \'{self.ids.teacher_faculty.text}\', \'{self.ids.teacher_career.text}\'')
			n_id: int = 0

			for id_ in ids:
				id_faculty = id_[0]
				id_career = id_[1]
			
			middle_name = self.ids.teacher_middle_name.text
			last_name = self.ids.teacher_last_name.text
			name = self.ids.teacher_name.text
			##
			email = self.ids.teacher_email.text
			num_email = 1
			while True:
				got = ''
				existing_email = self.sql.execute(f"EXECUTE verifYExistingTeacherEmail '{email}'")
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
			teacher_status = 'ALTA'
			
			save_teacher = f"EXECUTE saveTeacher {id_faculty},{id_career},'{middle_name}','{last_name}',"
			save_teacher += f"'{name}','{email}','{password}','{teacher_status}'"
			save_teacher = self.sql.execute(save_teacher)
			self.sql.commit()
			
			get_teacher = self.sql.execute(f"EXECUTE getTeacher '{middle_name}','{last_name}','{name}'")
			for get in get_teacher:
				enrollment = get[2] # ID_teacher
				#password = get[8]

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
	##################################### S C H E D U L E ###########################################