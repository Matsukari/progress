from apiclient import discovery, errors
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from lib.std import Timer
import io, os


DFLT_FIELDS = ['nexPageToken, files(id, mimeType, size, name, parents)']
class GoogleDriveInterface():
    def __init__(self, creds, secret, scopes='https://www.googleapis.com/auth/drive'):

        timer = Timer()
        #print(f'finished imports in {timer.Now()} ms')

        # define path variables
        self.creds_path = creds
        self.secret_path = secret

        # define API scope
        self.scopes = scopes
        # returned by ListFiles
        self.files = []
        self.downloader = None


        # define store
        self.store = file.Storage(self.creds_path)
        self.credentials = self.store.get()# get access token

        if not self.credentials or self.credentials.invalid:
            flow = client.flow_from_clientsecrets(self.secret_path, self.scopes)

            self.credentials = tools.run_flow(flow, self.store)


        #print(f'finished loading credentials under {timer.SinceLastPeek()} ms')

        # define API service
        self.http = self.credentials.authorize(Http())
        self.drive = discovery.build('drive', 'v3', http=self.http)

        #print(f'finished building drive api service under {timer.SinceLastPeek()} ms')

    def Download(self, item, format='', dst='/home/amon/Downloads/' + os.popen('date', 'r').read().split('\n')[0], wait=True):
        request = None
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            querybody = {
                'q': f"'{item['id']}' in parents",
                'pageSize': 100,
                'fields': "files(id, name, mimeType, size, parents)"
            }
            self.LoadFiles(querybody)

        else:
            pass


        for file in self.files:
            request = self.drive.files().get_media(fileId=item['id'])
            fh = io.FileIO(dst + format, mode='wb')
            self.downloader = MediaIoBaseDownload(fh, request)

    def Rename(self, item, newtitle):
        try:
            file = {'title': newtitle}

            # Rename the file.
            updated_file = self.drive.files().patch(
                fileId=item['id'],
                body=file,
                fields='title').execute()

            return updated_file
        except (errors.HttpError, error):
            print('An error occurred: %s' % error)
            return None

    def Send2Trash(self):
        pass

    def Share(self):
        pass

    def CreateShortcut(self):
        pass

    def CreateFolder(self):
        pass

    def Move(self):
        pass

    def Delete(self):
        pass

    def Upload(self):
        pass


    # Note that even though functions below are named partly with *File* this includes folder, shortcut or any metadata 
    # walk as in, os.walk(); go skim through every folder inside the given folder and collect whatever you walked in
    def LoadFiles(self, param ,walk=False):
        results = self.drive.files().list(**param).execute()
        self.files = results.get('files', [])

        if walk:
            foldersid = []
            for file in self.files:
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    foldersid.append(file['id'])
                    print('folder')

            for fold in foldersid:
                results = self.drive.files().list(q=f"'{fold}' in parents", fields=param['fields']).execute()
                self.files.extend(results.get('files', []))


    # if folder; return by list
    def GetFileBy(self, field):
        if not self.files:
            self.LoadFiles({'fields': 'files(name, mimeType, id)'})

        for file in self.files:
            if field[0] in file.keys() and field[1] in file.values():
                return file

        print(f"{field[0]}: '{field[1]}' not found!")
        return None
