#!/usr/bin/env python3

from lib.GoogleDriveInterface import *
from lib.String import *
from lib.Event import KeyPoller
from lib.std import Timer
from lib import std
import curses, os, sys, json
import curses.textpad


class Curses():
    def __init__(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()

        self.screen.keypad(True)
        self.screen.nodelay(True)

    def __del__(self):
        self.screen.nodelay(False)
        self.screen.keypad(False)

        curses.echo()
        curses.nocbreak()
        curses.curs_set(False)

        curses.endwin()


IS_ACTIVE = 0
class GoogleDriveCLI(Curses, GoogleDriveInterface):
    def __init__(self):
        Curses.__init__(self)

        #self.w, self.h = os.get_terminal_size()
        self.w = 70
        self.h = 20
        self.pace = None
        with open('gui_pacing.json', 'rt') as file:
            self.pace = json.loads(file.read())

        # TODO: startup menu, specify creds

        GoogleDriveInterface.__init__(self, 'credentials.json', 'client_secrets.json')

        self.poller = KeyPoller()
        self.key = None

        # this corresponds to the index for files list
        self.cursorimg = '->'
        # Load Files in root
        self.querybody = {
            'q': "'root' in parents",
            'pageSize': 1000,#self.h - self.pace['first_item'][0], 
            'fields': "nextPageToken, files(id, name, mimeType, size, parents)"
        }
        self.LoadFiles(self.querybody, walk=False)

        self.selection = {'files': 0, 'Moptions': 0, 'Foptions': 0}
        self.minselection = 0
        self.selected = None
        self.path = ['root']
        self.pathstr = 'root'

        self.insideof = 'files'

        self.is_action3 = False # Back, Return
        self.is_action1 = False # Selecting, Opening file option
        self.is_action2 = False # Go to folder
        self.prevfiles = []
        self.maxfiles = self.h - self.pace['first_item'][0]

        # Below options will be rendered as ordered here
        self.mainoptions = [
            '[Upload]',
            '[New Folder]',
            '[Help]'
        ]
        self.fileoptions = [
            'Rename',
            'Copy Link',
            'Download',
            'Delete',
            'Move',
            'Copy',
            'Details',
            'To Trash',
            'Share'
        ]
        self.fileoptionstate = curses.A_DIM

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.SELECT_COLOR = 1
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.NORMAL_COLOR = 2
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
        self.NOTICE_COLOR = 3

        self.divideborder = int((self.w//2) + self.pace['divide_offset'])


    def HandleEvents(self):
        self.key = self.poller.Poll()
        self.has_entered = False

        if self.key != None:
            self.key = self.key.lower()
            # FIRST: get minimum(if exceeds) SECOND: get maximum(if minimum bankrupt)
            if   self.key == 'w' or self.key == 'a': 
                self.selection[self.insideof] = max(min(self.selection[self.insideof] - 1, len(self.files)-1), 0)
                if self.selection['files'] < self.minselection:
                    self.minselection = max(self.minselection - 1, 0)
            elif self.key == 's' or self.key == 'd': 
                self.selection[self.insideof] = max(min(self.selection[self.insideof] + 1, len(self.files)-1), 0)
                if self.selection['files'] >= self.minselection + self.maxfiles:
                    self.minselection = min(self.minselection + 1, len(self.files)-1)
            elif self.key == 'j': self.is_action1 = True
            elif self.key == 'k': self.is_action2 = True
            elif self.key == 'p': 
                self.is_action1 = False
                self.is_action3 = True


    def GotoFolder(self, dst):

        if dst == 'prev' and len(self.prevfiles) > 0:
            self.files = self.prevfiles[-1]
            self.path.pop()
            self.prevfiles.pop()

        elif dst == 'next' and self.selected['mimeType'] == 'application/vnd.google-apps.folder':
            self.path.append(self.selected['name'])
            self.prevfiles.append(self.files)

            self.querybody['q'] = f"'{self.selected['id']}' in parents"
            self.LoadFiles(self.querybody, walk=False)

        self.pathstr = std.ListToString(self.path, '/')
        self.selection['files'] = 0
        self.minselection = 0

    def Update(self):
        self.screen.refresh()

        if not self.files:
            self.files.append('No files found')

        if self.is_action1:
            if self.insideof == 'files':
                self.selection['Foptions'] = 0
                self.insideof = 'Foptions'
                self.fileoptionstate = IS_ACTIVE
            elif self.insideof == 'Foptions':
                pass
            elif self.insideof == 'Moptions':
                pass

        elif self.is_action2 and self.insideof == 'files':
            self.selected = self.files[self.selection['files']]
            self.GotoFolder('next')
            self.is_action2 = False
        elif self.is_action3:
            if self.insideof == 'files':
                self.GotoFolder('prev')
            self.fileoptionstate = curses.A_DIM
            self.is_action1 = False
            self.is_action3 = False
            self.insideof = 'files'
            self.selection['Foptions'] = 0

            


    def ClearScreen(self):
        for row in range(self.h):
            self.screen.addstr(row, 0, ' ' * self.w)

    def DrawHeaders(self):
        # Draw Title
        self.screen.addstr(*self.pace['title'], 'GoogleDrive'.center(self.w, '-'))

        # Show Current Directory
        self.screen.addstr(*self.pace['path_notif'], f'Current Directory: {self.pathstr}')

    def DrawMainOptions(self):
        # Draw Top Menu [Horizontally]
        prevoption = ''
        for col, option in enumerate(self.mainoptions):
            self.screen.addstr(self.pace['first_Moption'][0],
                               self.pace['first_Moption'][1] + ((len(prevoption)  + self.pace['Moption_distance'])),
                               option)
            # Compensate distance
            prevoption += option + (' ' * self.pace['Moption_distance'])
    def DrawFileListing(self):
        # Draw File Listing [Vertically] (first box)
        for row in range(self.minselection, min(self.minselection + min(self.maxfiles, len(self.files)), len(self.files))):
            name = self.files[row]['name']
            color = self.NORMAL_COLOR
            if len(name) >= self.divideborder: name = name[:self.divideborder]
            if self.selection['files'] == row: color = self.SELECT_COLOR

            '''with open('/home/amon/dump', 'a') as f:
                f.write(str(self.pace['first_item'][0] + (row - self.selection['files'])) + 'y ')
                f.write(str(self.pace['first_item'][1]) + 'x = ')
                f.write(name + '\n\n')'''

            # From current file to what row
            self.screen.addstr(self.pace['first_item'][0] + (row - self.minselection), 
                               self.pace['first_item'][1], name, curses.color_pair(color))

        #  Erase the additional text in file's name; exceeding border
        for row in range(self.maxfiles):
            self.screen.addstr(self.pace['first_item'][0] + row,
                               self.divideborder, ' ' * (self.w - self.divideborder))
        curses.textpad.rectangle(self.screen, *self.pace['item_box'], 1+self.h+1, 1+self.divideborder+1)
    def DrawFileOptions(self):
        # Draw File options [vertically] (second box)
        # X position is used as distance from border
        for row, option in enumerate(self.fileoptions):
            color = self.NORMAL_COLOR
            if self.is_action1 and self.selection['Foptions'] == row: color = self.SELECT_COLOR

            self.screen.addstr(self.pace['first_Foption'][0] + row,
                               self.divideborder + self.pace['first_Foption'][1],
                               option, self.fileoptionstate | curses.color_pair(color))
        curses.textpad.rectangle(self.screen, self.pace['Foption_box'][0], self.divideborder+3, 1+self.h+1, 1+self.w-1+1)

    def DrawCursor(self):
        # Draw Cursor
        y = self.pace['first_item'][0] + self.selection[self.insideof]
        x = self.pace['first_item'][1] + self.pace['cursor_offset'] - len(self.cursorimg)
        self.screen.addstr(y, x, self.cursorimg)


    def Draw(self):
        self.ClearScreen()

        self.DrawHeaders()
        self.DrawMainOptions()
        self.DrawFileListing()
        self.DrawFileOptions()

    def Run(self):
        while(True):
            self.HandleEvents()
            self.Update()
            self.Draw()


if __name__ == '__main__':
    drive = GoogleDriveCLI()
    def main(*args, **kwargs):
        drive.Run()
    curses.wrapper(main)
    '''
    for row in range(drive.selection['files'], drive.maxfiles):
        name = drive.files[row]['name']

        if len(name) >= drive.divideborder: name = name[:drive.divideborder]
        if drive.selection['files'] == row: color = drive.SELECT_COLOR

        print(f"{drive.pace['first_item'][0] + (row - drive.selection['files'])}y, {drive.pace['first_item'][1]}x {name}")

'''

