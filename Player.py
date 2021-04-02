import os
import time
import sys
import random
import fnmatch
from PIL import Image, ImageEnhance
import ffmpeg
from waveshare_epd import epd7in5_V2


class Player:
    def __init__(self, file, delay=60, frames=10, start_width=0, brighten=1, random=False, frame=0):
        self.file = file
        self.delay = delay
        self.frames = frames
        self.start_width = start_width
        self.brighten = brighten
        self.random = random
        self.frame = frame
        self.viddir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'Videos/')
        self.logdir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'logs/')

    def Dump(self):
        print(self.__dict__)

    def Dump2(self):
        print(self.__dict__)

    def files(self):
        listOfFiles = os.listdir(self.viddir)
        pattern = "*.mp4"
        files = []
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                file = {}
                file['filename'] = entry
                files.append(file)
                print(entry)
                return files

    def play(self):
        frameDelay = float(self.delay)
        print("Frame Delay = %f" % frameDelay)

        increment = float(self.frames)
        print("Increment = %f" % increment)

        if self.random:
            print("In random mode")
        else:
            print("In play-through mode")

        if self.file:
            print('Try to start playing %s' % self.file)
        else:
            print("Continue playing existing file")

        # Scan through video folder until you find an .mp4 file
        currentVideo = ""
        videoTry = 0
        while not (currentVideo.endswith('.mp4')):
            currentVideo = os.listdir(self.viddir)[videoTry]
            videoTry = videoTry + 1

        # the nowPlaying file stores the current video file
        # if it exists and has a valid video, switch to that
        try:
            f = open('nowPlaying')
            for line in f:
                currentVideo = line.strip()
            f.close()
        except:
            f = open('nowPlaying', 'w')
            f.write(currentVideo)
            f.close()

        videoExists = 0
        for file in os.listdir(self.viddir):
            if file == currentVideo:
                videoExists = 1

        if videoExists > 0:
            print("The current video is %s" % currentVideo)
        elif videoExists == 0:
            print('error')
            currentVideo = os.listdir(self.viddir)[0]
            f = open('nowPlaying', 'w')
            f.write(currentVideo)
            f.close()
            print("The current video is %s" % currentVideo)

        movieList = []

        # log files store the current progress for all the videos available

        for file in os.listdir(self.viddir):
            if not file.startswith('.'):
                movieList.append(file)
                try:
                    log = open(self.logdir + '%s<progress' % file)
                    log.close()
                except:
                    log = open(self.logdir + '%s<progress' % file, "w")
                    log.write("0")
                    log.close()

        print(movieList)

        if self.file:
            if self.file in movieList:
                currentVideo = self.file
        else:
            print('%s not found' % self.file)

        print("The current video is %s" % currentVideo)

        # Ensure this is the correct driver for your particular screen
        epd = epd7in5_V2.EPD()

        # Initialise and clear the screen
        epd.init()
        epd.Clear()

        currentPosition = 0

        # Open the log file and update the current position

        log = open(self.logdir + '%s<progress' % currentVideo)
        for line in log:
            currentPosition = float(line)

        if self.frame:
            print('Start at frame %f' % float(self.frame))
            currentPosition = float(self.frame)

        # Ensure this matches your particular screen
        width = 800
        height = 480

        inputVid = self.viddir + currentVideo

        # Check how many frames are in the movie
        frameCount = int(ffmpeg.probe(inputVid)['streams'][0]['nb_frames'])
        print("there are %d frames in this video" % frameCount)

        while 1:

            if self.random:
                frame = random.randint(0, frameCount)
            else:
                frame = currentPosition

            msTimecode = "%dms" % (frame*41.666666)

            # Use ffmpeg to extract a frame from the movie, crop it, letterbox it and save it as grab.jpg
            generate_frame(inputVid, 'grab.jpg', msTimecode, width, height)

            # Open grab.jpg in PIL
            pil_im = Image.open("grab.jpg")
            enhancer = ImageEnhance.Brightness(pil_im)
            # brightens the image
            enhanced_im = enhancer.enhance(float(self.brighten))
            enhanced_im.convert(mode='1', dither=Image.FLOYDSTEINBERG)

            # Dither the image into a 1 bit bitmap (Just zeros and ones)
            # pil_im = pil_im.convert(mode='1',dither=Image.FLOYDSTEINBERG)

            # display the image
            epd.display(epd.getbuffer(enhanced_im))
            # time.sleep(10)
            # epd.display(epd.getbuffer(pil_im))
            print('Diplaying frame %d of %s' % (frame, currentVideo))

            currentPosition = currentPosition + increment
            if currentPosition >= frameCount:
                currentPosition = 0
                log = open(self.logdir + '%s<progress' % currentVideo, 'w')
                log.write(str(currentPosition))
                log.close()

                thisVideo = movieList.index(currentVideo)
                if thisVideo < len(movieList)-1:
                    currentVideo = movieList[thisVideo+1]
                else:
                    currentVideo = movieList[0]

            log = open(self.logdir + '%s<progress' % currentVideo, 'w')
            log.write(str(currentPosition))
            log.close()

            f = open('nowPlaying', 'w')
            f.write(currentVideo)
            f.close()

        #     epd.sleep()
            time.sleep(frameDelay)
            epd.init()

        epd.sleep()

        epd7in5.epdconfig.module_exit()


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
