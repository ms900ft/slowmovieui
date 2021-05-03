import os
import fnmatch


class Files:

    def __init__(self):
        self.viddir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'Videos/')
        self.logdir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'logs/')
        self.fileTypes = [".mp4", ".m4v", ".mkv", ".mov"]

    def list(self):
        listOfFiles = os.listdir(self.viddir)
        pattern = "*.mov"
        files = []
        for entry in listOfFiles:
            if self.supported_filetype(entry):
                # if fnmatch.fnmatch(entry, pattern):
                file = fileInfo(self.viddir, entry)
                files.append(file)
        return files

    def getFile(self, filename):
        return fileInfo(self.viddir, filename)

    def supported_filetype(self, file):
        _, ext = os.path.splitext(file)
        return ext.lower() in self.fileTypes


def fileInfo(path, filename):
    file = {}
    file['filename'] = filename
    statinfo = os.stat(os.path.join(path, filename))
    file['size'] = statinfo.st_size
    file['mod'] = statinfo.st_mtime
    file['frame_count'] = 0
    file['position'] = 0
    file['brightness'] = 1
    file['contrast'] = 1
    file['frames_per_delay'] = 10
    file['delay'] = 60
    file['fps'] = 0
    return file
