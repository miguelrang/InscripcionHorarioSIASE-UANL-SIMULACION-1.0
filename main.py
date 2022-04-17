import pyodbc as SQLServer

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'position', 'custom')
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock

from nltk.tokenize import word_tokenize

from datetime import datetime
import random
import os
import re

#from PIL import Image
#img = Image.open("images/yellow2.png")
#img = img.resize((25, 25), Image.ANTIALIAS)
#img.save("images/yellow.png")


class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)


class Login(Screen):
	type_ids = ('touch',)
	def __init__(self, **kwargs):
		super(Login, self).__init__(**kwargs)
		# 'Clock.schedule_interval' function calls the
		# function 'interval' (automatically add the var 'dt').
		# The second parameter says each seconds call the function. 
		Clock.schedule_interval(self.interval, 1)


	def interval(self, dt):
		# 'datetime.now()' literaly returns the date and
		# the time.
		info = str(datetime.now())
		# We save the date as str (it is desordered(year-month-day))
		date:str = info[:10]
		# We save the time
		time:str = info[11:16]
		# The disordered date is converted as list
		date_disordered:list = info[:10].split("-")
		# We reverse the list to get the ordered date
		date:list = list(reversed(date_disordered))
		# We convert the date list to str
		date:str = ''.join(date)
		# We separate the date (day-month-year)
		ordered_date:str = f"{date[0:2]}-{date[2:4]}-{date[4:8]}"

		# We update the Labels
		self.ids.calendar_text.text = ordered_date
		self.ids.clock_text.text = time


	def onPressType_(self):
		# We get the id of the type account
		type_ = self.ids.type_
		# We get the id of the label
		account_text = self.ids.account_text
		# If the account is in 'Alumno' mode...
		if type_.text == "Alumno                         ":
			# we change to 'Rectoria'...
			type_.text = "Rectoría                         "
			# and the label too is changed
			account_text.text = "Cuenta:"
			account_text.pos_hint = {"center_x": .112, "center_y": .33}
		else: # If the account is 'Rectoria' mode...
			type_.text = "Alumno                         "
			account_text.text = "Estudiante:"
			account_text.pos_hint = {"center_x": .095, "center_y": .33}

		return type_.text


	def onTextAccount(self):
		# We get the text input ID of 'account'
		account = self.ids.account
		# If the disabled var cuntinues being False it means
		# all is ok
		disabled = False
		# Account is always an 'int'
		account.input_filter = "int"
		# This conditional is necesary because if we
		# valid 'int(account.text)' first and the 
		# textinput is empty, the program brakes
		if account.text != "":
			# The student account can not be less than 1000
			# nor greater 2000000, if it happens, invalid input,
			# so, disabled = True
			if int(account.text) < 1000 or int(account.text) >= 2000000:
				disabled = True
		else: # It means the textinput is empty
			# so, it is invalid
			disabled = True
		

		# if diabled = True, password continues disabled
		# else it would be enable
		self.ids.password.disabled = disabled
		if disabled == True:
			# We disable the login button if password or
			# account are not valid
			self.ids.login.disabled = True
			account.background_color = 255/255, 255/255, 255/255, 1
		else:
			# if disabled = False
			# we valid if the password is correct
			self.onTextPassword()
			account.background_color = 168/255, 214/255, 172/255, 1

		return disabled


	def onTextPassword(self):
		disabled = False
		# We get the ID of text input password
		password = self.ids.password
		# The password can not be less than 7 nor greater than 16
		# so, we valid that
		if len(password.text) > 7 and len(password.text) < 17:
			disabled = False
		else:
			disabled = True

		# we set the enable or disable of login button
		self.ids.login.disabled = disabled
		if disabled == True:
			password.background_color = 255/255, 255/255, 255/255, 1
		else:
			password.background_color = 168/255, 214/255, 172/255, 1

		return disabled


	def onPressHiddenEye(self):
		icon = self.ids.hidden_eye
		password = self.ids.password
		if icon.icon == "eye":
			icon.icon = 'eye-off'
			password.password = True

		else:
			icon.icon = 'eye'
			password.password = False


	def signIn(self):
		####### HERE WE HAVE TO VALID IF THE USER IS
		######  IN THE DATABASE
		######
		app = MDApp.get_running_app()
		if self.ids.account_text.text == "Estudiante:":
			window = "siase"
		else:
			window = "rectoria"
		app.root.current = window
		

		Window.size = 1100, 650
		Window.left = (1400 - 1100)/2
		Window.top = ( 750 - 650)/2


class SIASE(Screen):
	def __init__(self, **kwargs):
		super(SIASE, self).__init__(**kwargs)


class Rectoria(Screen):
	def __init__(self, **kwargs):
		super(Rectoria, self).__init__(**kwargs)


class Add(Screen):
	def __init__(self, **kwargs):
		super(Add, self).__init__(**kwargs)
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
		##

		Clock.schedule_interval(self.interval, 1)


	def interval(self, dt):
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
		else:
			self.ids['teacher'].disabled = False
			self.ids['schedule'].disabled = False


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
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.student_button
		layout.cols = 1
		layout.row_default_height = 10
		
		faculties = sql.execute('EXECUTE dbo.getFaculties')
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
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, kardex'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.student_button
		layout.cols = 1
		layout.row_default_height = 10
		
		careers = sql.execute(f'EXECUTE dbo.getCareers \'{self.ids.student_faculty.text}\'')
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

		self.ids.saver_layout.clear_widgets()#remove_widget(self.ids.save_kardex)

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
		print(accepter)# 1
		print(accepter)# 2
		print(accepter)# 3
		print(accepter)# 4
		print(accepter)# 5
		print(accepter)# 6
		print(accepter)# 7
		print(accepter)# 8
		print(accepter)# 9
		print(accepter)# 10
		print(accepter)# 11
		print(accepter)# 12
		print(accepter)# 13
		
		self.ids.save_kardex.disabled = accepter
		if accepter == False:
			faculty = self.ids.student_faculty.text
			career = self.ids.student_career.text
			i = 0
			self.kardex = {}
			for subject in self.actual_kardex:
				ids = sql.execute(f'EXECUTE getIds \'{faculty}\', \'{career}\', \'{subject}\'')
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
				#sql.execute('EXECUTE getIDSubject')
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

		try:
			self.ids.student_show.remove_widget(self.ids.saver_layout)
			del self.ids.saver_layout
		except:
			pass

		self.actual_kardex = {}

		subjects = f'EXECUTE dbo.getSubjects \'{self.ids.student_faculty.text}\','
		subjects += f'\'{self.ids.student_career.text}\''
		subjects = sql.execute(subjects)
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

		saver_layout = """
BoxLayout:
	id: saver_layout
	name: 'saver_layout'
	
	orientation: 'horizontal'
	padding: 7.5
	size_hint_y: .1
	cols: 2
	rows: 1
		"""

		self.ids.saver_layout = Builder.load_string(saver_layout)
		student_show_layout.add_widget(self.ids.saver_layout)
		saver_layout = self.ids.saver_layout

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
		del save_kardex
		app.root.get_screen('add').saveKardex()
		"""

		self.ids.save_kardex = Builder.load_string(self.ids.save_kardex)
		saver_layout.add_widget(self.ids.save_kardex)


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

		self.ids.show_student1 = f"""
Label:
	text: '[b]DATOS DEL ESTUDIANTE[/b]'
	markup: True
	font_size: 30
	color: 1, 1, 1, 1"""
		extra = f"""
Label:
	text: ''
		"""
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

MDRectangleFlatButton:
	id: clean_student_info
	name: 'clean_student_info'
	
	text: 'Limpiar'
	size_hint_x: 1
	md_bg_color: 1, 1, 1, 1
	on_press: 
		del clean_student_info
		app.root.get_screen('add').clearShowStudentInfo()
		"""
		self.ids.show_student1 = Builder.load_string(self.ids.show_student1)
		self.ids.extra = Builder.load_string(extra)
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
		layout.add_widget(self.ids.extra)
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
		existing_student = sql.execute(existing_student)
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
				existing_email = sql.execute(f"EXECUTE verifYExistingEmail '{email}'")
				for e_m in existing_email:
					got = str(e_m[0])
					break
				
				print(got, email)
				print(got, email)
				print(got, email)
				print(got, email)
				print(got, email)
				print(got, email)
				print(got, email)
				
				if got == email:
					if num_email > 1:
						email = got.replace(f'{num_email-1}@', f'{num_email}@')
					else:
						email = got.replace('@', f'{num_email}@')
				else:
					break
				
				num_email += 1
				print(num_email)
			##
			password = self.getPassword()
			student_status = 'ALTA'
			
			save_student = f"EXECUTE saveStudent {id_faculty},{id_career},'{middle_name}','{last_name}',"
			save_student += f"'{name}','{date_birth}','{email}','{password}','{student_status}'"
			save_student = sql.execute(save_student)
			sql.commit()
			
			get_student = sql.execute(f"EXECUTE getStudent '{middle_name}','{last_name}','{name}'")
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
				sql.execute(save_kardex)
				sql.commit()

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

			
class Mod(Screen):
	def __init__(self, **kwargs):
		super(Mod, self).__init__(**kwargs)


class Delete(Screen):
	def __init__(self, **kwargs):
		super(Delete, self).__init__(**kwargs)


class main(MDApp):
	def build(self):
		self.icon = "images/icon.png"

		self.title = "Servicios en Linea"
		Window.size = (700, 450)
		self.theme_cls.theme_style = "Light"
		
		return Builder.load_file("Design.kv")
		
	def on_start(self):
		Window.size = 1100, 650
		Window.left = (1400 - 1100)/2
		Window.top = ( 750 - 650)/2
		self.root.current = "add"

def sqlCONNECTION():
	try:
		connect = SQLServer.connect('Driver={ODBC Driver 17 for SQL Server};'
									'Server=LAPTOP-CF0NC87S;'
									'Database=UANL;'
									'Trusted_Connection=yes')
		sql = connect.cursor()
		return sql
	except:
		print("Error connection")

if __name__ == "__main__":
	sql = sqlCONNECTION()
	
	main().run()
