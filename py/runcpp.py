


def main():
	import sys, os
	from pathlib import Path
	from importlib.machinery import SourceFileLoader

	auto = SourceFileLoader("auto", "/home/amon/programming/auto").load_module()

	try:
		# get the command
		links = {'sdl': '-lSDL2 -lSDL2_image -lSDL2_ttf -lSDL2_mixer'}
		configs = {'--link': '', '--lib': '', '--incl': ''}

		for i, arg in enumerate(sys.argv):
			if arg in configs.keys():

				nextarg = sys.argv[i+1]

				# check every space delimited; next argument should be enclosed with quotes ("")
				for val in nextarg.split():
					new = ''
					if val in links.keys():
						new = links[nextarg] + ' '
					else:
						new = val

					configs[arg] += new

		os.system(f'g++')



	except IndexError:
		print('runcpp: invalid argument')

	print(sys.argv)


if __name__ == '__main__':
	main()

"""

	$ runcpp --link "sdl gl" --lib "lib/fiengine" --modified --compileall -o sample
	--objs ""

"""