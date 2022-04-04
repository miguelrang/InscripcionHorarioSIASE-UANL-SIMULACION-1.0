from bs4 import BeautifulSoup
import PyPDF2
from nltk.tokenize import word_tokenize
import requests
import re
import os


with requests.Session() as session:
	response = session.get("https://www.uanl.mx/escuelas-y-facultades/")
	html = response.text
	finder_faculties = re.compile(r"https://www.uanl.mx/wp-content/uploads/2018/10/(.*).png")
	
	faculty = finder_faculties.findall(html)
	faculty = faculty[58:]

try:
	for i in range(len(faculty.copy())-1):
		faculty.remove(faculty[i+1])
except:
	pass

count = 0
for facu in faculty.copy():
	faculty[count] = faculty[count].replace("-1", "")
	faculty[count] = faculty[count].replace("_", " ")
	
	count += 1

faculties = {}
for i in range(len(faculty)):
	faculties[f"{i+1}"] = faculty[i]
	
for i in range(len(faculties)):
	faculties[str(i+1)] = faculties[str(i+1)].upper()
	print(f"INSERT INTO faculty(faculty_name) VALUES('{faculties[str(i+1)]}');")

html = BeautifulSoup(response.text, 'html.parser')
links = html.find_all('a')
n_faculty = 1
data = []
url = []
careers:dict = {}
semesters:list = []
urls_career:dict = {}
boolean = False

for link in links:
	info = link.get('href')
	
	if info != None:
		if str(info) == "#facultad-1":
			boolean = True

		if boolean == True:
			if "http://posgrado.uanl.mx/posgrados-por-facultad/" not in info and info != "\n":

				if "#facultad-" in info:
					info = info.replace("#facultad-", "")
					if int(info) != n_faculty:
						careers[str(n_faculty)] = data
						urls_career[str(n_faculty)] = url
						data = []
						url = []

					n_faculty = int(info)
				
				if "https://www.uanl.mx/content/" in info or "https://www.uanl.mx/oferta/" in info:
					#######
					response = requests.get(info)
					html = BeautifulSoup(response.text, 'html.parser')
					rectangle = html.find('div', class_='sidebar-pagina')
					duration = False
					for h3 in rectangle:
						if duration == True:
							semesters.append(str(h3))
							break

						if str(h3) == '<h3>Duración</h3>':
							duration = True
					#######
					url.append(info)

					info = info.replace("https://www.uanl.mx/content/", "")
					info = info.replace("https://www.uanl.mx/oferta/", "")
					info = info.replace("/", "")
					info = info.replace("-", " ")
					
					data.append(info)

		if info == "https://www.uanl.mx/contraloria-social/":
			break
careers[str(26)] = data
urls_career[str(n_faculty)] = url
#print(urls_career)

print("\n\n\n\n")
count = 1
for i in range(len(careers)):
	for j in range(len(careers[str(i+1)])):
		career = careers[str(i+1)]
		print(f"INSERT INTO Career(ID_faculty, ID_career, name_career, n_semester) VALUES({i+1},{count},'{career[j].upper()}',{semesters[count-1].replace(' semestres', '')});")
		count += 1

#print("\n\n\n\n")
def getContent(url):
	request = requests.get(url)
	content = request.text
	html = BeautifulSoup(content, "html.parser")

	tags = html.find_all("a")
	for tag in tags:
		url_pdf = tag.get("href")
		verify = re.compile(r"https://www.uanl.mx/wp-content/uploads/[1-9][0-9]+/\d*/.*plan.*estudio.*\.pdf")
		if url_pdf != None:
			if verify.fullmatch(url_pdf.lower()):
				return url_pdf


def getPDF(url_pdf):
	page = requests.get(url_pdf)
	with open("AAA.pdf", "wb") as f:
		f.write(page.content)

	with open("AAA.pdf", "rb") as f:
		content = PyPDF2.PdfFileReader(f)
		
		pdf = []
		try:
			pdf.append(content.getPage(0).extractText())
			pdf.append(content.getPage(1).extractText())
			pdf.append(content.getPage(2).extractText())
			pdf.append(content.getPage(3).extractText())
		except:
			pass

	#with open("AAA.txt", "w") as f:
	#	f.write((''.join(pdf)).upper())

	#with open("AAA.txt", "r") as f:
	#	pdf = f.readlines()

	os.system("del /f AAA.pdf")

	pdf = (''.join(pdf)).upper()
	pdf = pdf.replace("\n", "")
	#os.system("del /f AAA.txt")

	return word_tokenize(pdf)


def getPDFCleansed(pdf):
	from_ = pdf.index("PRIMER")
	simbology = False
	try:
		to = pdf.index("SIGLAS")
		simbology = True
	except:
		try:
			to = pdf.index("SIMBOLOGÍA")
			simbology = True
		except:
			to = len(pdf)
			simbology = False
	pdf = pdf[from_:to]

	#n:int = pdf.count("SEMESTRE")
	i = 1
	sem:bool = False
	subj:bool = False
	char = False
	subject = ""
	semester:list = []
	semesters:dict = {}
	
	# CLEANING TRASH
	acfs = []
	simb = []
	acs = []
	h_s = []
	t_s = []
	for j in range(len(pdf)):
		if 'ACF' in pdf[j]:
			acfs.append(pdf[j])
		if '*' in pdf[j] or '**' in pdf[j]:
			simb.append(pdf[j])
		if 'AC' == pdf[j]:
			acs.append(pdf[j])
		if 'H/S' == pdf[j]:
			h_s.append(pdf[j])
		if 'T/S' == pdf[j]:
			t_s.append(pdf[j])
		
	for acf in acfs:
		x = pdf.index(acf)
		if pdf[x-1] != 'OPTATIVA':
			pdf.pop(x)

	for sim in simb:
		b = pdf.index(sim)
		pdf.pop(b)
	
	for ac in acs:
		y = pdf.index(ac)
		pdf.pop(y)

	for hs in h_s:
		z = pdf.index(hs)
		pdf.pop(z)

	for ts in t_s:
		a = pdf.index(ts)
		pdf.pop(a)

	while 'CICLO' in pdf:
		c = pdf.index('CICLO')
		pdf.pop(c)
		pdf.pop(c-1)
	#

	for n in range(len(pdf)):
		if pdf[n] == "SEMESTRE":
			sem = True

		if sem == True and pdf[n] != "SEMESTRE":
			try:
				if pdf[n+1] == "SEMESTRE":
					semesters[str(i)] = semester
					semester = []
					sem = False
					i += 1
				#elif acf == True:
				#	if "ACF" in pdf[n]:
				#		subj = True
				#	
				#	numbs:str = "0123456789"
				#	chars:str = "_\\/|°!\"#$%&()='?¿¡´¨+*~{[^}]`,;.:_"
				#	if subj == True and "ACF" not in pdf[n]:
				#		subject += pdf[n] + " "
				#		if "ACF" not in pdf[n+1]:
				#			for x in pdf[n+1]:
				#				try:
				#					integer = int(x)
				#					subj = False
				#					break
				#				except:
				#					if x in numbs or x in chars:
				#						subj = False
				#						break
				#		if subj == False:
				#			#print(subject[:len(subject)-1])
				#			semester.append(subject[:len(subject)-1])
				#			subject = ""
			
				else:
					subj = True
					try:
						num = int(pdf[n])
						subj = True #
					except:
						numbs:str = "0123456789"
						chars:str = "_\\/|°!\"#$%&()='?¿¡´¨+*~{[^}]`,;._"
						for m in pdf[n]:
							try:
								integer = int(m)
								subj = False
								break
							except:
								if m in numbs or m in chars:
									subj = False
									break

						if subj == True:
							if pdf[n] != "C" and pdf[n] != "TOTAL":
								subject += pdf[n] + " "

						try:
							if (subject != "" and subject != "DEL PE " and 
								subject != "DEL PLAN DE ESTUDIOS " and subject != "DEL PLAN DE ESTUDIO "):
								num = int(pdf[n+1])
								semester.append(subject[:len(subject)-1])
								subject = ""
								subj = False
						except:
							pass

			except:
				pass

	semesters[str(i)] = semester

	return semesters


def getStudyPlan(url_pdf):
	url_pdf = getContent(url_pdf)
	pdf:list = getPDF(url_pdf)
	study_plan:list = getPDFCleansed(pdf)
	return study_plan

faculty_career_study_plan:dict = {}
for i in range(26):
	career_study_plan:dict = {}
	for j in range(len(urls_career[str(i+1)])):
		url_pdf = urls_career[str(i+1)][j]
		print(url_pdf)
		study_plan = getStudyPlan(url_pdf)
		#print(study_plan)
			
		career_study_plan[str(j+1)] = study_plan
	faculty_career_study_plan[str(i+1)] = career_study_plan

#print(faculty_career_study_plan)
print("\n\n")
count = 0
c = 0
for faculty in range(len(faculty_career_study_plan)):
	for career in range(len(faculty_career_study_plan[str(faculty+1)])):
		c += 1
		for semester in range(len(faculty_career_study_plan[str(faculty+1)][str(career+1)])):
			for subject in range(len(faculty_career_study_plan[str(faculty+1)][str(career+1)][str(semester+1)])):
				name_subject = faculty_career_study_plan[str(faculty+1)][str(career+1)][str(semester+1)][subject]
				print(f"INSERT INTO SemesterSubject(ID_faculty,ID_career,ID_semester,name_subject) VALUES({faculty+1},{c},{semester+1},'{name_subject}');")
				count += 1
