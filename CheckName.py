import re


name_re='^[a-zA-Z_]\w*$'


while True :
	s=raw_input()

	if(s=='exit'):
		break 
		
	result=re.match(name_re,s)

	if result:
		print 'Ok'
	else: 
		print 'No'
