import re
def parse_syllabus(text:str)->list[str]:
 lines=[re.sub(r'^[\s•\-\d.)]+','',x).strip() for x in text.splitlines()]
 return [x for x in lines if len(x)>2 and not re.match(r'^(unit|module)\s*\d+',x,re.I)]
