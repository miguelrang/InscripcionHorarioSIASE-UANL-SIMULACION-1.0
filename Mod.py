import pyodbc as SQLServer

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
		
		if self.ids.student_faculty.text != 'Facultad' and self.ids.student_faculty.text != info['student_faculty']:
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
			if self.ids.student_career.text != 'Carrera' and self.ids.student_career.text != info['student_career']:
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
				if self.student_faculty in info['student_faculty'] and self.student_career in info['student_career']:
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
		numbs = list('0123456789')
		chars = list('|°¬!"#$%&/()=\'?\\¿¡´¨+*~{[^}]`,;.:-_<>')
		for char in range(len(list(var.text).copy())):
			if var.text[char] in numbs or var.text[char] in chars:
				var.text = var.text.replace(var.text[char], "")
				break


	def validName(self, name):
		name = self.ids[name]
		if name == 'middle_name' or name == 'last_name':
			name.text = name.text.replace(' ', '')
		name.text = name.text.upper()
		self.delNumber(name)
		if len(name.text) > 2:
			if name.focus == False:
				pass
		else:
			if name.focus == False:
				self.studentDialog('Debe contener almenos 3 letras.')

		self.studentEquals()


	def onTextMiddleName(self):
		self.validName('middle_name')
		self.setEmail(
			email='email',
			name='name',
			middle_name='middle_name',
			last_name='last_name'
		)


	def onTextLastName(self):
		self.validName('last_name')
		self.setEmail(
			email='email',
			name='name',
			middle_name='middle_name',
			last_name='last_name'
		)


	def onTextName(self):
		self.validName('name')
		self.setEmail(
			email='email',
			name='name',
			middle_name='middle_name',
			last_name='last_name'
		)


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

		self.studentEquals()


	def onTextPassword(self, password):
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
					self.studentDialog('La longitud de la contraseña debe ser mayor a 7 y menor a 17.')
					

		else:
			if password.focus == False:
				self.studentDialog('La contraseña debe contener al menos una letra mayuscula, una minuscula y un número.')
				
		self.studentEquals()


	def onPressStatus(self, status):
		status = self.ids[status]
		if status.text == 'ALTA':
			status.text = 'BAJA'

		else:
			status.text = 'ALTA'

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
				self.ids[f].text = 'Facultad'

			elif 'career' in f:
				self.ids[f].text = 'Carrera'

		for f in field2:
			if 'status' in f:
				self.ids[f].text = 'Status'

			else:
				self.ids[f].text = ''

		self.ids.cancel_student.disabled = True

	
	def onPressUpdateStudent(self):
		field = [
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
		for f in field:
			if self.ids[f].text != self.actual_student_info[f]:
				valid = True
					
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
			self.studentDialog('Se ha actualizado la información correctamente.')
		
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
			self.sql.commit()
			if (valid == True and equals == False) == False:
				self.studentDialog('Se ha actualizado la información correctamente.')
		self.ids.update_student.disabled = True





