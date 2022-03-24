import curses, random, time, os, sys
from lib import keypoller
from datetime import datetime
from datetime import timedelta



start_time = datetime.now()

# returns the elapsed seconds since the start of the program
def GetTicks():
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms
def Gotoxy(x,y):
	print ("%c[%d;%df" % (0x1B, y, x), end='')
    # or print("\033[6;3HHello")
def IntList(plist):
    for i in range(len(plist)): 
        plist[i] = int(plist[i])

    return plist
def StrClear(screen, text, bg, y, x):
	
	screen.addstr(y, x, bg * len(text))


# justified text
class JText():
    """docstring for Text"""
    def __init__(self, text, y, x):

        self.text = tuple(text.split('\n'))

        self.x = x
        self.y = y


    def Draw(self, screen, attr=0):

        for i in range(len(self.text)):
            screen.addstr(self.y + i, self.x, self.text[i], attr)

    def Cover(self, screen, bg, attr=0):

        for i in range(len(self.text)):
            screen.addstr(self.y + i, self.x, bg * len(self.text[i]), attr)

# group of blocks
class GBlock():

	"""docstring for GBlock"""
	def __init__(self, pattern, by, bx):
		self.pattern = pattern.split('\n')
		self.x = []
		self.y = by

		x = bx
		newline = False

		# found once NOT a mole, proceeding characters are treated as part of result SINCE TETRIS BLOCKS ARE CLOSELY CLUSTERED
		for c in pattern:

			if c == '\n':
				x = bx - 1 # roll back to first x position
				newline = True

			elif c != ' ' and (newline or len(self.x) == 0):
				self.x.append(x)

			x += 1

		#eliminate the moles
		for row in range(len(self.pattern)):
			self.pattern[row] = self.pattern[row].strip(' ')


	def Draw(self, screen, vely=0, velx=0, attr=0):
		self.y += vely

		for row in range(len(self.pattern)):
 			self.x[row] += velx
 			screen.addstr(self.y + row, self.x[row], self.pattern[row], attr)

	def Cover(self, screen, bg=' ', attr=0):

		for row in range(len(self.pattern)):
			screen.addstr(self.y + row, self.x[row], bg * len(self.pattern[row]), attr)

	def HasCollided(self, B, vely=0, velx=0):

		for A_row in range(len(self.pattern)):
			for A_col in range(len(self.pattern[A_row])):

				for B_row in range(len(B.pattern)):
					for B_col in range(len(B.pattern[B_row])):

						if (self.x[A_row] + A_col + velx == B.x[B_row] + B_col) and \
						   (self.y        + A_row + vely == B.y        + B_row):
						   return True

		return False

	def GetLeftmost(self):
		return min(self.x)

	def GetRightmost(self):

		# find the row of blocks which has the most length plus its initial x; rightmost x
		rightmost = 0
		for i, row in enumerate(self.pattern):
			rightmost = max(len(row) + self.x[i], rightmost)

		return rightmost
       
	def GetBottommost(self):
		return self.y + len(self.pattern)


PAT_L = 0
PAT_Z = 1
PAT_O = 2
PAT_I = 3
PAT_T = 4
# left, bottom, right, top as index respectively; Starting from 1-bottom
PAT = \
{
	PAT_L: ['  █\n███',   '█\n█\n██',	'███\n█',	 '██\n █\n █'	],
	PAT_Z: [' █\n██\n█',  '██\n ██',	' █\n██\n█', '██\n ██'      ],
	PAT_O: ['██\n██',     '██\n██',		'██\n██', 	 '██\n██'		],
	PAT_I: ['██', 		  '█\n█',		'██', 		 '█\n█'			],
	PAT_T: [' █\n██\n █', ' █ \n███',	'█\n███\n█', '███\n █'		]
}

class Tetris():
	"""docstring for Tetris"""
	def __init__(self, scrw, scrh):

		self.w = scrw
		self.h = scrh

		self.drawicon = '0'
		self.bgicons = ['-', '|']
		self.boardfill = {}

		self.gblocks = []
		self.curgb = None
		self.currot = 1 # bottom
		self.curpat = None

		self.movedelay = 300 # ms
		self.lastmove = 0
		self.lastkey = 0
		self.keytickhist = []

		self.velx = 0
		self.vely = 0
		self.event = keypoller.Event()
		self.keyhist = []
		self.reckey = ''

		self.screen = curses.initscr()
		curses.start_color()
		curses.curs_set(False)
		curses.noecho()
		curses.cbreak()

		self.screen.keypad(True)
		self.screen.nodelay(True)

		#print('loaded')

	def __del__(self):

		self.screen.nodelay(False)
		self.screen.keypad(False)

		curses.echo()
		curses.nocbreak()
		curses.curs_set(False)

		curses.endwin()


	def CreateGBlock(self, pattern, y, x):
		# default 1-bottom
		self.curpat = pattern
		self.gblocks.append(GBlock(PAT[pattern][1], y, x, ' '))
		self.curgb = self.gblocks[-1]

	def CreateRandomGBlock(self):
		#-debug
		self.curpat = random.randint(0, len(PAT)-1)
		self.CreateGBlock(self.curpat, 1, random.randint(1, self.w-2))


	def HandleEvents(self):

		key = self.event.Poll()

		if not key is None:
			key = key.lower()
			self.reckey = key
			self.keyhist.append(key)
			self.keytickhist.append(GetTicks())

			if   key == 'a': self.velx = -1
			elif key == 'd': self.velx =  1
			elif key == 'w': self.velx = -1
			elif key == 's': self.velx =  1
			elif key == 'j': self.movedelay = 10
			#elif len(self.keyhist) >= 2 and (self.keyhist[-2] == 'h') and GetTicks() - self.keytickhist[-2] <= 600:
			#	if   key == 'a': self.currot -= 1
			#	elif key == 'd': self.currot += 1
			
			#	self.currot = self.currot % len(PAT) # wrap-around
			
			#	self.curgb = GBlock(PAT[pattern][self.currot], y, x, ' ')
		else:
			self.reckey = None


	def DrawBG(self):

		#print('starting bg')
		self.screen.addstr(0, 0, self.bgicons[0] * self.w)

		for row in range(self.h-3):
			self.screen.addstr(row+1, 0, self.bgicons[1].ljust(self.w - 1) + self.bgicons[1])

		self.screen.addstr(self.h-2, 0, self.bgicons[0] * self.w)
		#print('endgin bg')


	def HandleCollision(self):

		# bounds

		if self.curgb.GetLeftmost() < 1: # left-most block 
			self.velx += 1
		elif self.curgb.GetRightmost() > self.w-1: # right-most block
			self.velx -= 1

		bottommost = self.curgb.GetBottommost()
		if bottommost >= self.h-2:

			#for i, s in enumerate(self.curgb.pattern):
			#	row = self.curgb.y + i
			#	if row not in self.boardfill:
			#		self.boardfill[row] = 0

			#	self.boardfill[row] += len(s)
			#	if self.boardfill[row] >= self.w:


			self.CreateRandomGBlock()

		# per gblocks

		if len(self.gblocks) > 1:
			for i in range(len(self.gblocks)-1):

				hascollided = self.curgb.HasCollided(self.gblocks[i], self.vely, self.velx)

				if hascollided and self.reckey == 'a': 
					self.velx += 1
				elif hascollided and self.reckey == 'd': 
					self.velx -= 1
				elif hascollided and self.vely > 0:
					self.CreateRandomGBlock()




	def Run(self):
		self.CreateRandomGBlock()

		try:
			while True:
				self.movedelay = 300
				self.velx = 0
				self.vely = 0
				self.HandleEvents()

				if GetTicks() - self.lastmove >= self.movedelay:
					self.lastmove = GetTicks()
					self.vely = 1

				self.HandleCollision()


				#self.gblocks[-1].Cover(self.screen, ' ')
				self.DrawBG()

				if len(self.gblocks) > 1:
					for i in range(len(self.gblocks) - 1):
						self.gblocks[i].Draw(self.screen)

				self.curgb.Draw(self.screen, self.vely, self.velx)

				#-debug
				self.screen.addstr(1, 2, str(self.curpat))

				self.screen.refresh()


		except KeyboardInterrupt:
			self.screen.addstr(1, 1, 'Interrupted')


def main():

	h = 20
	w = 20

	tetris = Tetris(w, h)
	#print('after load')
	tetris.Run()


if __name__ == '__main__':
	main()

