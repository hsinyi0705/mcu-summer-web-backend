import json

def pp(content):
	for i in range(len(str(content))+4):
		print("#",end="")
	print('\n# ',end="")
	print(content,end='')
	print(' #')
	for i in range(len(str(content))+4):
		print("#",end="")
	print()