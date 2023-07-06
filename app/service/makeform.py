import re

import nltk
from nltk.tokenize import word_tokenize

from .convertforms import *
from .skills import *


def remove_symbols(text):
    # Remove special symbols
    text = re.sub(r'•', '', text)
    text = re.sub(r'', '', text)
    # Add more symbols to remove if needed
    
    return text

def inpositions(text):
	positions=["Representative","Designer","Engineer","Technician","Developer","Mentor","Assistant","Counselor","Secretary","Manager","Leader"]
	for p in positions:
		if text.find(p)!=-1:
			return True
	return False

def populate_skills(lines):
   
    skills = []
    skillmode = False

    for line in lines:
		
        check_line = line.lower()
        line = re.sub(r"[^a-zA-Z0-9%-.@:\'\"$+/]", " ", line)

        if skillmode:
            skill = isskill(check_line)
            if skill and skill not in skills:
                skills.append(skill)
                
        elif check_line.startswith("skills") or check_line.startswith("technical skills"):
            skillmode = True

    return skills


def MakeForm(text):
	length=len(text)
	dictionary={}
	flag=0
	count=0
	text = remove_symbols(text)
	# print(text)
	lines=text.splitlines()
	lines = [x for x in lines if x != '' and x != ' ' and x not in ['• ', '•']] 
	
	text=text.replace(',','\n')

	#print(lines)
	dictionary=basicdetails(lines,text)
	dictionary['Address']=" "
	# email=dictionary['Email']
	if dictionary['Phone']==None:
		dictionary['Phone']=""
	if dictionary['Email']==None:
		dictionary['Email']=""
	if dictionary['Name']==None:
		dictionary['Name']=""
	# dictionary['marital']="unmarried"
	edu={}
	education=[]
	inter={}
	internship=[]
	pro={}
	project=[]
	skills=[]
	trainings=0
	trainings=[]
	train={}
	skillmode=0
	no=0
	no_edu=0

	skills = populate_skills(lines)
	dictionary['Skills'] = skills

	for line in lines:
		check_line=line.lower()
		line=re.sub(r"[^a-zA-Z0-9%-.@:\'\"$+/]"," ",line)
		
		if check_line.find("github")!=-1:
			dictionary["github"]=line
			continue
		if check_line.find("linkedin")!=-1:
			dictionary["linkedin"]=line
			continue

		if  bool(re.search(r'\s{0,2}skills\s{0,2}$', check_line)) ==True or line.find("Skills")!=-1 or line.find("SKILLS")!=-1:
			skillmode=1
			flag=0
			count=0
			continue

		if 'responsibility' in check_line or 'education' in check_line  or dictionary['Name'] in line or dictionary['Phone'] in line or dictionary['Email'] in line:
			continue
		
		if line =="  ":
			flag=0
			count=0
		if(check_line.find('internships')!=-1) or bool(re.search(r'\s{0,2}experience\s{0,2}$', check_line)) ==True or (check_line.find('employment history')!=-1):
			#print(line)
			flag=2
			count=0
			skillmode=0
			continue
		if (check_line.find('projects')!=-1) or  bool(re.search(r'\s{0,2}project\s{0,2}$', check_line)) ==True or bool(re.search(r'\s{0,2}projects\s{0,2}$', check_line)) ==True:
			flag=3
			count=0
			skillmode=0
			continue

		if(check_line.find('trainings')!=-1)  or (check_line.find('certifications')!=-1):
			#print(line)
			flag=4
			count=0
			skillmode=0
			continue

		if flag==2:
				#print('intern',count)
				if bool(re.search(r'[0-9]{4}', check_line))==True and count==0:
						inter['Date']=line
						count=0
						continue

				#print(line)
				employment_type=find_emp_type(check_line)
				if employment_type !=None:
					inter['EmpType']=employment_type
				if count==3 :
					
					if len(line)>=20:
						if bool(re.search(r'.\s*$', check_line)) ==True:
							if no==0:
								inter['Description']=line
								#print('final')
								#print(line)
							else:
								des+=line
								inter['Description']=des

							no=0
						else:
							if no==0:
								des=""
							no=no+1
							des+=line+" "
							#print(des)
							#inter['Description']=des
							continue
					else:
						inter['Description']=" "

					if 'EmpType' not in inter.keys():
						inter['EmpType']="Internship"
					if 'Date' not in inter.keys():
						inter['Date']="2000-01-01"
					if 'EndDate' not in inter.keys():
						inter['EndDate']="2000-01-01"
					internship.append(inter)
					#obj=Internship(email=email,position=inter['Position'],company=inter['Company'],date=inter['Date'],desc=inter['Description'])
					#obj.save()
					inter={}
					count=0
				elif count==2 :
					if 'Date' not in inter.keys():
						if bool(re.search(r'[0-9]{4}', check_line))==True :
							l=re.findall(r'[0-9]{4}', check_line)
							if len(l)==1:
								start_date=l[0]+"-01-01"
								edu['Date']=start_date
								end_date="2000-01-01"
								edu['EndDate']=end_date
							if len(l)==2:
								start_date=l[0]+"-01-01"
								edu['Date']=start_date
								end_date=l[1]+"-01-01"
								edu['EndDate']=end_date
							count=3
							continue
						else:
							inter['Date']="2000-01-01"
					else:
						count=3
				elif count==1 :
					if bool(re.search(r'\d', check_line)) ==False :
						line=re.sub(r"[^a-zA-Z0-9]"," ",line)
						inter['Company']=line
						count=2
						continue
					else:
						inter['Company']=" "
				elif count==0 :
					if bool(re.search(r'\d', check_line)) ==False and inpositions(line):
						line=re.sub(r"[^a-zA-Z]"," ",line)
						inter['Position']=line
						count=1
						continue

		if flag==3:
				#print('project',count)
				#print(line)
				if count==3 :
					#if bool(re.search(r'\d', check_line)) ==False :
					if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date="2000-01-01"
							pro['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date=l[1]+"-01-01"
							pro['EndDate']=end_date
						#print(line)
					else:
						newname=line

					pro['Description']=" "
					if 'Link' not in pro.keys():
						pro['Link']="https://"
					if 'Date' not in pro.keys():
						pro['Date']="2000-01-01"
					if 'EndDate' not in pro.keys():
						pro['EndDate']="2000-01-01"
					project.append(pro)
					pro={}
					pro['Name']=newname
					count=1

					
					#obj=Project(email=email,name=pro['Name'],date=pro['Date'],link=pro['Link'],desc=pro['Description'])
					#obj.save()
					#pro={}
					
				elif count==2 :
					if(line.find("https://")!=-1):
						pro['Link']=line
					else:
						pro['Link']=line
					pro['Description']=""
					project.append(pro)
					pro={}
					count=0
					
				elif count==1 :
					if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date="2000-01-01"
							pro['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date=l[1]+"-01-01"
							pro['EndDate']=end_date
						#print(line)
						count=2
					else:
						if(line.find("https://")!=-1):
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=line
							count=3
						else:
							print("here")
							print(line)
							print(pro['Name'])
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=""
							project.append(pro)
							pro={}
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=""
							pro['Name']=line
							project.append(pro)
							pro={}
							count=0

				elif count==0 :
					if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date="2000-01-01"
							pro['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							pro['Date']=start_date
							end_date=l[1]+"-01-01"
							pro['EndDate']=end_date
						#print(line)
						count=2
					else:
						if(line.find("https://")!=-1):
							pro['Date']="2000-01-01"
							pro['EndDate']="2000-01-01"
							pro['Link']=line
							count=3
						else:
							print(line)
							pro['Name']=line
							count=1
		if flag==4:
			if count==0:
				if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['Title']=line
					count=1

			elif count==1:
				if bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['organization']=line
					count=2
				elif bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1:
					l=re.findall(r'[0-9]{4}', check_line)
					#print(l)
					if len(l)==1:
						start_date=l[0]+"-01-01"
						train['Date']=start_date
						#print(line)
					count=1

			elif count==2:
				if bool(re.search(r'[0-9]{4}', check_line))==True and  line.find("https://")==-1 and 'Date' not in train.keys():
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							train['Date']=start_date
						#print(line)
						count=3
				if 'Date' in train.keys():
					count=3
					continue

			elif count==3:
				if len(line)<=50 and bool(re.search(r'\d', check_line)) ==True or  line.find("https://")==-1:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['credentials']=line
					if 'Date' not in train.keys():
						train['Date']="2000-01-01"
					trainings.append(train)
					train={}
					count=0
				elif bool(re.search(r'\d', check_line)) ==False and len(line)<=70:
					line=re.sub(r"[^a-zA-Z0-9]"," ",line)
					train['Title']=line
					train['credentials']="undefined"
					if 'Date' not in train.keys():
						train['Date']="2000-01-01"
					trainings.append(train)
					train={}
					count=0


	if 'degrees' in dictionary.keys():
		degrees=dictionary['degrees']	
	else:
		no_edu=1	
	
	word_tokens = nltk.word_tokenize(text) 
	
	if no_edu ==0:
		for deg in degrees:
			flag=0
			if deg=="x":
				deg+=" "
			edu={}
			for line in lines:
				check_line=line.lower()
				if check_line.find(deg)!=-1 :
					line=re.sub(r"[^a-zA-Z]"," ",line)
					edu['Degree']=line
					field_of_study=find_fields(check_line)
					if field_of_study!=None and 'field_of_study' not in edu:
						edu['field_of_study']=field_of_study
					flag=1
				elif flag==1:
				#print(line)
					if bool(re.search(r'\d', check_line)) ==False and 'Institution' not in edu:
						edu['Institution']=line
					if  bool(re.search(r'[0-9]{4}', check_line))==True and 'Date' not in edu:
						l=re.findall(r'[0-9]{4}', check_line)
						#print(l)
						if len(l)==1:
							start_date=l[0]+"-01-01"
							edu['Date']=start_date
							end_date="2000-01-01"
							edu['EndDate']=end_date
						if len(l)==2:
							start_date=l[0]+"-01-01"
							edu['Date']=start_date
							end_date=l[1]+"-01-01"
							edu['EndDate']=end_date
						#edu['Date']=line

					if check_line.find("grade")!=-1 or check_line.find("gpa")!=-1 or check_line.find("cgpa")!=-1 or check_line.find("%")!=-1 and 'Grade' not in edu:
						line=re.sub(r"[^0-9.%]"," ",line)
						edu['Grade']=line
					field_of_study=find_fields(check_line)
					if field_of_study!=None and 'field_of_study' not in edu:
						edu['field_of_study']=field_of_study
			education.append(edu)

	dictionary['Trainings']=trainings
	dictionary["Education"]=education
	dictionary["Internships"]=internship
	dictionary['Projects']=project
	dictionary['Skills']=skills
	#print(skills)
	
	return dictionary
























