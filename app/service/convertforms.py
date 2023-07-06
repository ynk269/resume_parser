import nltk
import spacy
from spacy.matcher import Matcher


def basicdetails(lines,text):
    

    # load pre-trained model
    nlp = spacy.load('en_core_web_sm')

    # # initialize matcher with a vocab
    matcher = Matcher(nlp.vocab)
 
    dictionary={}
   
    def extract_name(resume_text, lines):
        # def extract_name(resume_text):
        nlp_text = nlp(resume_text)
        
        # Pattern for full name with optional middle name
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN', 'OP': '?'}]
        
        matcher.add('NAME', [pattern])
        matches = matcher(nlp_text)
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text

    print('Name --')
    name=extract_name(text,lines)
    print(name)
    dictionary["Name"]=name
    
    
   
    import re
    """extarcting phone number"""

    def extract_mobile_number(text):
        phone = re.findall(re.compile(r'[0-9]{0,2}\s*[0-9]{10}'), text)
        
        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
                # return number
            else:
                return number

        

    print('Phone')
    phone=(extract_mobile_number(text))
    print(phone)
    dictionary['Phone']=phone

   
    def extract_email(email):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None

    # print('email')
    email=(extract_email(text))
    # print(email)
    dictionary["Email"]=email
    
    


    word_tokens = nltk.word_tokenize(text) 
    

    def extract_degrees(lines):
        degrees=['b.tech', 'b.e','ba','ma','xii','b.sc','m.sc','m.tech','high school','senior','x','bachelor','bachelors','master','masters','specialization','mba','msc','10+2', 'intermediate', 'ssc']
        in_degrees=[]
        for w in lines:
            w=w.lower()
            if w in degrees:
                if w=='senior' and 'xii' and 'intermediate' in in_degrees or w=='junior' and 'x' and 'ssc' in in_degrees or w=='bachelor' and 'b.tech' and 'b.e' in in_degrees or w=='b.tech' and 'bachelor' in in_degrees or w=='masters' and 'm.tech' in in_degrees or w=='msc' and 'm.sc' in in_degrees or w=='m.sc' and 'msc' in in_degrees :
                    continue
                in_degrees.append(w)
                
        return in_degrees

    degrees=[]
    for w in word_tokens:
        if w.lower()=="education":
            degrees=extract_degrees(word_tokens)
            count_edu=len(degrees)
            #finddates=extract_dates(text,count_edu)
            print(degrees, '---degrees---')

    def extract_gender(word_tokens):
        gender=" "
        for w in word_tokens:
            if w.lower() == "male" or w.lower() == "m":
                gender = "Male"
            elif w.lower() == "female" or w.lower() == "f":
                gender = "Female"
        return gender

    gender=extract_gender(word_tokens)
    dictionary['gender']=gender
    dictionary['degrees']=degrees
    # print('dictionary--> ', dictionary)
    return dictionary

    


fields_of_study=['computer','science','buisness','art','commerce','economics']

def find_fields(check_line):
    words=nltk.word_tokenize(check_line)
    for w in words:
        if w in fields_of_study:
            return w
    return None

emptypes=['internship','part-time','full-time','self_employed','freelance','contract']

def find_emp_type(check_line):
    words=nltk.word_tokenize(check_line)
    for w in words:
        if w in emptypes:
            return w
    return None
