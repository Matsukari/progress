import pyperclip, re

def main():

	link = pyperclip.paste()

	pat = re.compile(r'/[0-9]*[a-zA-Z]+[0-9]+[a-zA-Z0-9]*/')
	gid = pat.search(link)

	try:
		print(gid.group())
	except:
		print('cannot find ID in your clipboard')

if __name__ == '__main__':
	main()

