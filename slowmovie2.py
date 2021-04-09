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
from flask import Flask, jsonify, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

from Player import Player
from Files import Files


# Ensure this is the correct import for your particular screen
from waveshare_epd import epd7in5_V2

player = {}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'Videos')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'mp4'}


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


@app.route('/files', methods=['GET'])
def file_list():
    # player = Player(file='.')
    global player

    resp = {}
    resp['files'] = player.movies
    resp['meta'] = {}
    resp['meta']['count'] = len(player.movies)
    return jsonify(resp)


@app.route('/files/list', methods=['PUT'])
def update_list():
    content = request.json
    print(content)
    global player
    player.movies = content['files']
    return jsonify(content), 200


@app.route('/files', methods=['POST'])
def add_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "1", 201

    return "bad request", 400
    # player = Player(file='.')
    # files = Files()
    # return jsonify((files.list()))


@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    files = Files()
    try:
        file = files.getFile(filename)
    except FileNotFoundError:
        # doesn't exist
        return "0", 404
    except:
        return "unkown", 400

    return jsonify(file)


@app.route('/files/<filename>/play', methods=['PUT'])
def play_file(filename):
    files = Files()
    try:
        file = files.getFile(filename)
    except FileNotFoundError:
        # doesn't exist
        return "0", 404
    except:
        return "unkown", 400
    global player
    player.SetFile(filename)
    return "1", 200


@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except FileNotFoundError:
        # doesn't exist
        return "0", 404
    except:
        return "unkown", 400
    return "1", 200


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
    parser.add_argument('-w', '--webserver', default=False, action='store_true',
                        help="Start admin server")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print(args)
    global player
    player = Player(file=args.file, delay=args.delay,
                    frames=args.inc, brighten=args.brighten)
    player.Load()
    player.Dump()
    if args.webserver == True:
        server = FlaskThread()
        server.daemon = True
        server.start()

    # simulate doing something else while flask runs in background

    # slowmovie(args)

    player.Play()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    main()
    exit()
