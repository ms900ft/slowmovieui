import os
import fnmatch


class Files:

    def __init__(self):
        self.viddir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'Videos/')
        self.logdir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'logs/')

    def list(self):
        listOfFiles = os.listdir(self.viddir)
        pattern = "*.mp4"
        files = []
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                file = fileInfo(self.viddir, entry)
                files.append(file)
        return files

    def getFile(self, filename):
        return fileInfo(self.viddir, filename)


def fileInfo(path, filename):
    file = {}
    file['filename'] = filename
    statinfo = os.stat(os.path.join(path, filename))
    file['size'] = statinfo.st_size
    file['mod'] = statinfo.st_mtime
    return file
