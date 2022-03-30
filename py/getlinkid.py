import pyperclip, re, sys

def main():

	link = ''
	if len(sys.argv) == 2:
		link = sys.argv[1]
	else:
		link = pyperclip.paste()

	pat = re.compile(r'/[0-9]*[_\-]*[a-zA-Z]+[_\-]*[0-9]+[a-zA-Z0-9_\-]*/*')
	gid = pat.search(link)

	try:
		print(f'got, {gid.group()[1:]}')
		pyperclip.copy(gid.group(1:)) # without '/'
	except:
		print('no id found')


if __name__ == '__main__':
	main()

