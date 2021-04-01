#!/usr/bin/python
# -*- coding:utf-8 -*-

# *************************
# ** Before running this **
# ** code ensure you've  **
# ** turned on SPI on    **
# ** your Raspberry Pi   **
# ** & installed the     **
# ** Waveshare library   **
# *************************

import os
import time
import sys
import random
from PIL import Image, ImageEnhance
import ffmpeg
import argparse
from threading import Thread
from flask import Flask, jsonify, request, send_from_directory
from Player import Player


# Ensure this is the correct import for your particular screen
from waveshare_epd import epd7in5_V2


app = Flask(__name__)

i = "hallo"


# @app.errorhandler(Exception)
# def error_handler(e):
#     return "Unknown Error", 500


@app.route('/test', methods=['GET'])
def test():
    """
    Test endpoint to show breakage
    """
    AAAAAA
    return jsonify(True)


@app.route('/')
def hello_world():
    return 'Hello, World!xx %s' % app.static_folder


@app.route('/img/grap.jpg')
def send_js():
    return send_from_directory('.', 'grab.jpg')
    # x = send_static_file('grap.jpg')
    # return send_static_file('grap.jpg')


@app.route('/post/<string:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    global i
    i = post_id
    return 'Post %s ' % post_id


class FlaskThread(Thread):
    def run(self):
        app.run(
            host='0.0.0.0', port=8888, debug=True, use_debugger=True,
            use_reloader=False)


def check_mp4(value):
    if not value.endswith('.mp4'):
        raise argparse.ArgumentTypeError("%s should be an .mp4 file" % value)
    return value


def parse_args():
    parser = argparse.ArgumentParser(description='SlowMovie Settings')
    parser.add_argument('-r', '--random', action='store_true',
                        help="Random mode: chooses a random frame every refresh")
    parser.add_argument('-f', '--file', type=check_mp4,
                        help="Add a filename to start playing a specific film. Otherwise will pick a random file, and will move to another film randomly afterwards.")
    parser.add_argument('-d', '--delay',  default=10,
                        help="Delay between screen updates, in seconds")
    parser.add_argument('-i', '--inc',  default=4,
                        help="Number of frames skipped between screen updates")
    parser.add_argument('-b', '--brighten',  default=1.0,
                        help="brighten factor")
    parser.add_argument('-s', '--start',
                        help="Start at a specific frame")
    parser.add_argument('-w', '--webserver',
                        help="Start admin server")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print(args)
    player = Player(file=args.file, delay=args.delay,
                    frames=args.inc, brighten=args.brighten)
    player.Dump()
    if args.webserver == True:
        server = FlaskThread()
        server.daemon = True
        server.start()

    # simulate doing something else while flask runs in background

    # slowmovie(args)

    player.play()


if __name__ == '__main__':
    main()
    exit()
