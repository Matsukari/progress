import sys, os, re, copy
from pathlib import Path
from lib import std

"""
	g++ compiler wrapper
"""

EXCLUDE_MARK = '$EXCLUDE'
EXCLUDE_ALL_MARK = '$EXCLUDE_ALL'


def main():

	try:
		is_assemble = False
		is_regex = False
		is_verbose = False

		# get the command
		flags = {'sdl': '-lSDL2 -lSDL2_image -lSDL2_ttf -lSDL2_mixer'}
		# those optionz who have next value dedicated
		configs = {'--objs': '', 	# single file or whole folder
				   '--sources': '', # by default: same as --objs; all given should be directory
				   '--flags': '',	# compiler or linker flags 
				   '--incls': '',
				   '--libs': '', 
				   '--objformats': '.o ', # target format in compilation
				   '--srcformats': '.h .cpp ',
				   '--output': '',	# compiling to obj or an executable
				   '--import': ''
		}
		switches = {
			'-c': False,
			'--regex': False,
			'--verbose': False,
			'--run': False,
			'--lasttime': False
		}
		objfiles = []
		srcfiles = []

		# get the values next to given option(argument)
		for i, arg in enumerate(sys.argv):
			if arg in configs.keys():

				nextarg = sys.argv[i+1]

				# check every space delimited; asumming this argument is enclosed with quotes("")
				for val in nextarg.split():
					new = val

					if arg == '--flags' and val in flags.keys():
						new = flags[val] + ' '
					# if argument is in default of configs, empty it
					for default in configs.values(): 
						if val in default.split(): configs[arg] = ''

					configs[arg] += new + ' '

			elif arg in switches.keys():
				switches[arg] = True

		if configs['--sources'] == '':
			configs['--sources'] = configs['--objs']


		objfiles += std.GetFiles(configs['--objs'].split(), configs['--objformats'].split())
		srcfiles += std.GetFiles(configs['--sources'].split(), configs['--srcformats'].split())


		# Check and eliminate if object file's name is similar to that of <src> file' name
		def ExcludeObj(src):
			for i, obj in enumerate(objfiles):
				if Path(obj).stem == Path(src).stem:
					objfiles.pop(i)
					print(f'{Path(src).stem}, excluded')


		# check if files are MARKED as said above
		for src in srcfiles:
			with open(src, 'r') as file:
				# find exlcude mark in either first or second line of the file
				line1 = file.readline()
				line2 = file.readline()

				# exclude all files in the directory of the file with mark of exclusion
				if EXCLUDE_ALL_MARK in line1 or EXCLUDE_ALL_MARK in line2:

					# iterate again and check if the file with MARK-OF-EXCLUSION's directory matches with other ones
					for src2 in srcfiles:
						if Path(src).parent == Path(src2).parent:
							# then find this source file in object files, and check if they have similar filename
							ExcludeObj(src2)

				elif EXCLUDE_MARK in line1 or EXCLUDE_MARK in line2:
					ExcludeObj(src)


		# compile
		print()
		print('runcpp: Ready, ', end='')

		print(f"g++ {std.ArgToString(objfiles)}\n{configs['--incls']}\n{configs['--libs']}\n{configs['--flags']}\n-o {configs['--output']}")
		#os.system(f"g++ {std.ArgToString(objfiles)}\n{configs['--incls']}\n{configs['--libs']}\n{configs['--flags']}\n-o {configs['--output']}")
		#if switches['--run']:
		#	os.system(f'./{configs['--output']}')

	except IndexError:
		print('runcpp: invalid argument')


if __name__ == '__main__':
	main()

"""

	$ auto runcpp --flags "sdl gl" --libs "lib/fiengine" -o sample
	--objs ""

"""