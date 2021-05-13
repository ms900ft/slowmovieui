import os
import time
import sys
import random
import fnmatch
from PIL import Image, ImageEnhance
import ffmpeg
from waveshare_epd import epd7in5_V2
from Files import Files, fileInfo
import json
from fractions import Fraction


class Player:
    def __init__(self, file, delay=60, frames=10, start_width=0, brighten='2',
                 random=False, frame=0, width=800, height=480, contrast='1.5'):
        self.file = file
        self.delay = delay
        self.frames = frames
        self.start_width = start_width
        self.brighten = brighten
        self.contrast = contrast
        self.random = random
        self.frame = frame
        self.width = width
        self.height = height
        self.viddir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'Videos/')
        self.logdir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'logs/')
        self.spool = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'spool/')
        self.__epaperImage = os.path.join(self.spool, 'paper.jpg')

    def generate(self, filename, time):
        file = os.path.join(self.viddir, filename)
        (
            ffmpeg
            .input(file, ss=time)
            .filter('scale', self.width, self.height, force_original_aspect_ratio=0)
            .filter('pad', self.width, self.height, -1, -1)
            .output(self.__epaperImage, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )


    def movieInfo(self, filename):
        file = os.path.join(self.viddir, filename)
        probe = ffmpeg.probe(file)['streams'][0]
        info = {}
        info['fps'] = float(Fraction(probe['avg_frame_rate']))
        info['frame_count'] = float(probe['nb_frames'])
        # print(info)
        return info

    def initEpaper(self):
        epd = epd7in5_V2.EPD()

        # Initialise and clear the screen
        epd.init()
        epd.Clear()

    def SetFile(self, filename):
        print("playing %s" % filename)
        self.file = filename
        print(self.__dict__)

    def AddFile(self, filename):
        file = fileInfo(self.viddir, filename)
        match = False
        i = 0
        for entry in self.movies:
            if entry['filename'] == file['filename']:
                self.movies[i] = file
                match = True
            i = i + 1
        if match == False:
            info = self.movieInfo(filename)
            file['frame_count'] = info['frame_count']
            file['fps'] = info['fps']
            self.movies.append(file)
        self.Save()

    def DeleteFile(self, filename):
        elm = [filename in item['filename']
               for item in self.movies].index(True)
        x = self.movies
        del x[elm]
        self.movies = x
        print(self.movies)
        self.Save()

    def nextFrame(self):
        for movie in self.movies:
            self.movieInfo(movie['filename'])
            if movie['frame_count'] == 0:
                info = self.movieInfo(movie['filename'])
                movie['frame_count'] = info['frame_count']
                movie['fps'] = info['fps']
                self.Save()
            if movie['position'] + int(self.frames) > int(movie['frame_count']):
                print("next movie")
                old = self.movies.pop(0)
                old['position'] = 0
                self.movies.append(old)
                self.Save()
                break
            frame = float(movie['position'])
            fps = movie.get(
                'fps') != None and movie['fps'] > 0 and movie['fps'] or 25
            frame_time = 1000 / fps
            msTimecode = "%dms" % (frame * frame_time)
            self.generate(movie['filename'], msTimecode)
            print("playing %s von pos %f" %
                  (movie['filename'], frame))
            # print("ssajjsasajk %s %s" % movie['filename'], frame)
            movie['position'] = int(movie['position']) + int(self.frames)
            if 'brightness' in movie:
                self.brighten = movie['brightness']
            if 'contrast' in movie:
                self.contrast = movie['contrast']
            self.Save()
            break
        return True

    def Load(self):
        conf = os.path.join(self.spool, "movielist.json")
        files = Files()
        fileList = files.list()
        if os.path.exists(conf):
            print("reading movielist")
            with open(conf) as fp:
                data = json.load(fp)
            for file in fileList:
                if not find(data, file):
                    data.append(file)
            self.movies = data

        else:
            self.movies = fileList
        self.Save()

    def Save(self):
        conf = os.path.join(self.spool, "movielist.json")
        print("writting movielist")
        with open(conf, 'w') as fp:
            json.dump(self.movies, fp, indent=4)

    def Play(self):
        self.initEpaper()
        self.Load()
        while self.nextFrame():
            # print("next")
            # time.sleep(2)
            epd = epd7in5_V2.EPD()
            pil_im = Image.open(self.__epaperImage)
            enhancer = ImageEnhance.Brightness(pil_im)
            #enhancer = ImageEnhance.Contrast(pil_im)
            # brightens the image
            print(self.brighten)
            enhanced_im = enhancer.enhance(float(self.brighten))
            enhancer = ImageEnhance.Contrast(enhanced_im)
            enhanced_im = enhancer.enhance(float(self.contrast))
            enhanced_im.convert(mode='1', dither=Image.FLOYDSTEINBERG)
            preview = os.path.join(self.spool,"preview.jpg")
            #enhanced_im.save(preview)
            # Dither the image into a 1 bit bitmap (Just zeros and ones)
            # pil_im = pil_im.convert(mode='1',dither=Image.FLOYDSTEINBERG)

            # display the image
            epd.display(epd.getbuffer(enhanced_im))
            enhanced_im.convert('L').save(preview)
            time.sleep(int(self.delay))


def generate_frame(in_filename, out_filename, time, width, height):
    (
        ffmpeg
        .input(in_filename, ss=time)
        .filter('scale', width, height, force_original_aspect_ratio=0)
        .filter('pad', width, height, -1, -1)
        .output(out_filename, vframes=1)
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )


def find(arr, file):
    for x in arr:
        if x["filename"] == file['filename']:
            return True
    return False
