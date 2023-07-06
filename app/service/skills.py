# def isskill(lines):
# 	skills=["python","customer support","sales","c++","programming","android","css","python","adobe","google","processing","sql","django","cloud","drawing","painting","html","algorithms","excel","analytics","data structures","dbms","php","R","science","machine","tally","accountancy","chemistry","physics"]
# 	#print(skills)
# 	line = lines.lower()
# 	for s in skills:
# 		if line.find(s)!=-1:
# 			#print(s)
# 			return True
# 	return False


def isskill(line):
    
    skills = ["python", "java", "c","html","bootstrap","javascript","react js", "reactjs", 'typescirpt', 'angular', "aws",  "c++", "android", "css", "adobe", "google", "flask", "sql", "django", "cloud", "painting", "html", "algorithms", "excel", "analytics", "data structures", "dbms", "php", "ruby", "chemistry", "physics"]
    line = line.lower()
    for s in skills:
        if s.lower() in line:
            return s
    return ""
