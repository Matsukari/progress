#import os, subprocess
#
#def Gotoxy(x,y):
#    print ("%c[%d;%df" % (0x1B, y, x), end='')
    # or print("\033[6;3HHello")


#col, line = os.get_terminal_size()
#line = os.popen('echo $LINENO', 'r').read().split()
#line = subprocess.Popen('echo ${LINENO}', shell=True)
#
#print(line.communicate())
#print(os.getenv('LINENO'))

#os.system('clear')
#
#print('hello\nhello\nhello')
#gotoxy(1, 1)
#print('Shot')
#gotoxy(1, 4)


"""print('hello')
os.system('bash /home/amon/programming/bashdoc.sh')
data = open('ex.data', 'r').read().split()[0]
print('readed data: %s' % data)
print('done')"""

import curses, time, os


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



def IntList(plist):
    for i in range(len(plist)): 
        plist[i] = int(plist[i])

    return plist

def StrClear(screen, text, bg, y, x):
    screen.addstr(y, x, bg * len(text))



class GBlock():
    """docstring for GBlock"""
    def __init__(self, pattern, by, bx, mole=' '):
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

            elif c != mole and (newline or len(self.x) == 0):
                self.x.append(x)

            x += 1

        #eliminate the moles
        for row in range(len(self.pattern)):
            self.pattern[row] = self.pattern[row].strip(mole)


    def Draw(self, screen, vely=0, velx=0, attr=0):
        self.y += vely

        for row in range(len(self.pattern)):
            self.x[row] += velx
            screen.addstr(self.y + row, self.x[row], self.pattern[row], attr)

    def Cover(self, screen, bg=' ', attr=0):

        for row in range(len(self.pattern)):
            screen.addstr(self.y + row, self.x[row], bg * len(self.pattern[row]), attr)

        

import time
from datetime import datetime
from datetime import timedelta

start_time = datetime.now()

# returns the elapsed seconds since the start of the program
def GetTicks():
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms


from lib import keypoller

def main(*args, **kwds):
    print('Start!')
    screen = curses.initscr()

    curses.start_color()
    curses.curs_set(False)
    curses.noecho()
    curses.cbreak()

    screen.keypad(True)
    screen.nodelay(True)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    screen.addstr(10, 10, 'hello', curses.color_pair(1))


    """key = screen.getkey()
    while key != 'q':

        text = JText('-jtext\nexample-', 5, 5)

        if key == 'j':
            text.Draw(screen, curses.color_pair(1))
        else:
            text.Cover(screen, '-')

        screen.addstr(7, 5, '-new\nline-')
        screen.refresh()

        key = screen.getkey()"""

    block = GBlock(' O \nOOO\n0', 1, 15)
    vely = 1
    velx = 0
    lasttime = 0
    event = keypoller.KeyPoller()
    while True:

        vely = 0
        velx = 0
        if GetTicks() - lasttime >= 300:
            lasttime = GetTicks()

            vely = 1

        block.Cover(screen, '-')

        try:
            curses.halfdelay()
            key = screen.getkey()#event.poll()
            if key == 'j':
                block.Cover(screen, '*')
            elif key == 'a':
                velx = -1


            elif key == 'd':
                velx = 1


        except:
            pass

        block.Draw(screen, vely, velx)


        screen.refresh()



    screen.keypad(False)

    curses.nocbreak()
    curses.echo()
    curses.endwin()

    


if __name__ == '__main__':
    #curses.wrapper(main)
    from lib import std
    
    s = '/home/amon/programming/x.txt'
    print(std.RStringBetween(s, '/', '/', 1))

    with open('items', 'r') as f:
        print(f.read())

    import os
    print(os.getcwd())
