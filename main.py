import pyodbc as SQLServer

from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'position', 'custom')
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock

from nltk.tokenize import word_tokenize

from datetime import datetime
import os
import re

#from PIL import Image
#img = Image.open("images/wallpaper2.png")
#img = img.resize((1210, 655), Image.ANTIALIAS)
#img.save("images/wallpaper3.png")


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
		if self.ids.account_text.text == "Estudiante:":
			# A UANL student account is always an 'int'
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
		else: # it means that it is a rectoria account, so...
			# we accept different chars because it is an email
			account.input_filter = None
			expression = re.compile(r"\w+\.\w+@uanl\.edu\.mx")
			# if the input not satisfy the expression...
			if not expression.fullmatch(account.text):
				# invalid input
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


	def signIn(self):
		####### HERE WE HAVE TO VALID IF THE USER IS
		######  IN THE DATABASE
		######
		app = MDApp.get_running_app()
		if self.ids.account_text.text == "Estudiante:":
			window = "student"
		else:
			window = "rectoria"
		app.root.current = window
		

		Window.size = 1100, 650
		Window.left = (1400 - 1100)/2
		Window.top = ( 750 - 650)/2


class Rectoria(Screen):
	def __init__(self, **kwargs):
		super(Rectoria, self).__init__(**kwargs)


class Student(Screen):
	def __init__(self, **kwargs):
		super(Student, self).__init__(**kwargs)


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
		self.revalidate = False
		##
		self.actual_kardex = dict()


		Clock.schedule_interval(self.interval, 1)


	def interval(self, dt):
		verifier:bool = False
		verifier2:bool = False
		if self.middle_name == True:
			if self.last_name == True:
				if self.name_ == True:
					if self.email == True:
						if self.date_birth == True:
							verifier2 = True
							verifier2 = not self.ids.middle_name.disabled
							if self.student_faculty == True:
								if self.student_career == True:
									verifier = True
		self.ids.save_student.disabled = not verifier
		self.ids.student_faculty.disabled = not verifier2

		enabled_widgets = [self.middle_name, self.last_name, self.name_, 
						 self.email, self.date_birth, self.student_faculty]
		verifier = False
		for widget in enabled_widgets:
			if widget == True:
				verifier = True
				break
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
				print(var.text)
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
		
		print(actual_year)
		print(year_birth)
		if valid.fullmatch(year_birth) and (int(actual_year) - int(year_birth)) > 16:
			year = year_birth

		else:
			year = int(actual_year) - 17

		print(year)
		return year


	def onTextDateBirth(self):
		date_birth:str = self.ids.date_birth

		actual_date:str = self.getDate()
		actual_date:list = actual_date.split('/')
		year = actual_date[0]
		month = actual_date[1]
		day = actual_date[2]

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
		self.ids.revalidate.text = 'Revalidación'

		self.student_faculty = True


	def onPressStudentFaculty(self):
		##
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, revalidate'
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

		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, revalidate'
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
		
		self.ids.revalidate.text = 'Revalidación'

		self.student_career = True


	def onPressStudentCareer(self):
		##
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, revalidate'
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


	def validRevalidate(self, revalidated):
		oportunity = self.ids[revalidated.name]
		try:
			actual = int(oportunity.name[len(oportunity.name)-1]) # '#' of oportunity
			neutral = oportunity.name[:len(oportunity.name)-1] # textfield
			grade_op = int(oportunity.text)
			if grade_op > -1 and grade_op < 70:
				self.ids[f'{neutral + str(actual + 1)}'].disabled = False
				for i in range(1, 7, 1):
					if i > actual:
						self.ids[f'{neutral}{i}'].disabled = False
						break
			
			elif grade_op < 0 or grade_op > 100:
				oportunity.text = ''
				for i in range(1, 7, 1):
					if i > actual:
						self.ids[f'{neutral}{i}'].text = ''
						self.ids[f'{neutral}{i}'].disabled = True

			else:
				for i in range(1, 7, 1):
					if i > actual:
						self.ids[f'{neutral}{i}'].text = ''
						self.ids[f'{neutral}{i}'].disabled = True

		except:
			for i in range(1, 7, 1):
				if i > actual:
					self.ids[f'{neutral}{i}'].text = ''
					self.ids[f'{neutral}{i}'].disabled = True
	

	def saveKardex(self):
		self.revalidate = True
		#########
		#########
		#########
		#########


	def onPressRevalidate(self):
		##
		var:str = 'middle_name, last_name, name, email, date_birth, student_faculty, student_career, revalidate'
		var:list = var.split(', ')
		for n in var:
			self.ids[n].disabled = True
		##
		layout = self.ids.student_button
		layout.cols = 7
		layout.row_default_height = 50

		careers = sql.execute(f'EXECUTE dbo.getSubjects \'{self.ids.student_faculty.text}\', \'{self.ids.student_career.text}\'')
		career = []
		for c in careers:
			career.append(c[0])

		n = 0
		for c in career:
			n += 1

			x = f"""
MDLabel:
	id: mdlabel{n}
	name: 'mdlabel{n}'

	text: f'{c}'
	#size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
			"""
			self.ids[f'mdlabel{n}'] = Builder.load_string(x)
			layout.add_widget(self.ids[f'mdlabel{n}'])
			self.actual_kardex[f'mdlabel{n}'] = ''

			i = 1
			while i < 7:
				y = f"""
TextInput:
	id: textfield{n}{i}
	name: f'textfield{n}{i}'

	size_hint_x: .15
	multiline: False
	input_filter: 'int'
	on_text: app.root.get_screen('add').validRevalidate(textfield{n}{i})
	on_focus: app.root.get_screen('add').validRevalidate(textfield{n}{i})
	"""
				self.ids[f'textfield{n}{i}'] = Builder.load_string(y)
				layout.add_widget(self.ids[f'textfield{n}{i}'])

				if i > 1:
					self.ids[f'textfield{n}{i}'].disabled = True
				i += 1
		student_show_layout = self.ids.student_show

		saver_layout = """
BoxLayout:
	id: saver_layout
	name: 'saver_ layout'
	
	orientation: 'horizontal'
	padding: 7.5
	size_hint_y: .1
	cols: 2
	rows: 1
		"""
		self.ids.saver_layout = Builder.load_string(saver_layout)
		student_show_layout.add_widget(self.ids.saver_layout)
		saver_layout = self.ids.saver_layout

		save_kardex = """
MDRaisedButton:
	id: save_kardex
	name: 'save_kardex'

	text: 'Guardar Kardex'
	size_hint_x: .9
	text_color: .9, .5, 0, 1
	md_bg_color: 1, 1, 1, 1
	line_color: 0, 0, 1, 1
	on_press: app.root.get_screen('add').saveKardex()
		"""
		self.ids.save_kardex = Builder.load_string(save_kardex)
		saver_layout.add_widget(self.ids.save_kardex)


	def onPressSaveStudent(self):
		pass


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

	#def on_start(self):
	#	Window.size = 1100, 650
	#	Window.left = (1400 - 1100)/2
	#	Window.top = ( 750 - 650)/2
	#	self.root.current = "add"

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
