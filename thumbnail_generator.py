#!/usr/bin/python

import platform
import numpy as np
from datetime import datetime
from enum import Enum
import httplib2
import getpass
import os
import sys
import cv2
from PIL import ImageFont, ImageDraw, Image
import youtube_API_test

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser, run_flow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

user_name = getpass.getuser()
platform_name = platform.system()

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

CLIENT_SECRETS_FILE = "client_secrets_thsvkd.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

%s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(
    os.path.join(os.path.dirname(__file__), youtube_API_test.CLIENT_SECRETS_FILE)
)
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"

#
###
#
#
#


def make_colorcode(code):
    # This func replaces the color code with an RGB value.
    # #FFFFFF -> 255, 255, 255 or
    # FFFFFF -> 255, 255, 255

    a = 0
    if code[0] == "#":
        r = int("0x" + code[1:3], 16)
        g = int("0x" + code[3:5], 16)
        b = int("0x" + code[5:7], 16)
    else:
        r = int("0x" + code[0:2], 16)
        g = int("0x" + code[2:4], 16)
        b = int("0x" + code[4:6], 16)
    print([r, g, b, a])

    return [r, g, b, a]


def fint_font_file(root, font_style):
    for (path, dir, files) in os.walk(root):
        for filename in files:
            ext = filename.split(".")
            if ext[0] == font_style:
                fontpath = "%s/%s" % (path, filename)
    return fontpath


def get_font_truetype(font_size, font_style):
    # This function returns the font that corresponds to that font when you enter a font name.
    # (The path only applies to Windows!)

    fontpath = fint_font_file("fonts", font_style)
    if len(fontpath) == 0:
        if platform_name == "Windows":
            fontpath = "C:/Users/%s/AppData/Local/Microsoft/Windows/Fonts/%s.ttf" % (
                user_name,
                font_style,
            )
        elif platform_name == "Linux":
            fontpath = fint_font_file("/usr/share/fonts", font_style)

        # ttf_fontpath = "/usr/share/fonts/truetype/%s.ttf" % (font_style,)
        # otf_fontpath = "/usr/share/fonts/truetype/%s.otf" % (font_style,)

    if os.path.isfile(fontpath):
        return ImageFont.truetype(fontpath, font_size)
    else:
        print("can't load font. plz check font name")
        exit()


def drawtext(BG_img, text, rgba):
    # This function returns a image of text on the background image

    font = text[1]
    text = text[0]
    text = text.split("\n")
    r = rgba[0]
    g = rgba[1]
    b = rgba[2]
    a = rgba[3]

    BG_w, BG_h, BG_c = BG_img.shape
    BG_shape = [BG_w, BG_h, BG_c]
    img_pil = Image.fromarray(BG_img)
    draw = ImageDraw.Draw(img_pil)

    for i, text_line in enumerate(text):
        w, h = font.getsize(text_line)
        draw.text(
            ((int(BG_shape[1]) - w) / 2, ((int(BG_shape[0]) - h * len(text)) / 2) + h * i),
            text_line,
            font=font,
            fill=(b, g, r, a),
        )

    return np.array(img_pil)


def show_preview_image(BG_img):
    # Preview completed thumbnail images

    winname = "thumbnail image"
    cv2.namedWindow(winname, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(winname, BG_img)
    cv2.waitKey(0)


def image_resize(BG_img, size):
    # Change the background image size
    # ifyouspecifyanimagesize, such as 1920x1080,
    # it changes to that size, and if you specify a ratio,
    # the image size changes to that ratio.

    BG_w, BG_h, BG_c = BG_img.shape
    BG_shape = [BG_w, BG_h, BG_c]

    if not isinstance(size, list):
        ratio = size
        BG_shape[0] *= ratio
        BG_shape[1] *= ratio
    else:
        BG_shape[0] = size[1]
        BG_shape[1] = size[0]

    BG_img = cv2.resize(
        BG_img, dsize=(int(BG_shape[1]), int(BG_shape[0])), interpolation=cv2.INTER_AREA
    )

    print("img resize to %d x %d" % (int(BG_shape[1]), int(BG_shape[0])))

    return BG_img


def make_thumbnail_image(contents):

    text, font_size, font_color, font_style, img_name, img_size = contents
    r, g, b, a = make_colorcode(font_color)  # a is always zero.

    if len(img_name) != 0:
        BG_img = cv2.imread(img_name)
    else:
        BG_img = cv2.imread("BG_sample.png")

    BG_img = image_resize(BG_img, img_size)
    font = get_font_truetype(font_size=font_size, font_style=font_style)
    thumbnail = drawtext(BG_img=BG_img, text=[text, font], rgba=[r, g, b, a])

    return thumbnail


def get_authenticated_service(args):
    flow = flow_from_clientsecrets(
        CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE
    )

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http())
    )


def upload_thumbnail(youtube, video_id, file):
    youtube.thumbnails().set(videoId=video_id, media_body=file).execute()


def get_view_count(youtube, video_id):

    stats = youtube.videos().list(part="statistics, snippet", id=video_id).execute()
    viewCount = stats["items"][0]["statistics"]["viewCount"]

    print("video view count : %s" % viewCount)

    return viewCount


def search_args_parse():
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    return args


def thumbnail_args_parse():
    argparser.add_argument(
        "--video-id", required=True, help="ID of video whose thumbnail you're updating."
    )
    argparser.add_argument("--file", required=True, help="Path to thumbnail image file.")
    args = argparser.parse_args()

    return args


class DEBUG(Enum):
    LOAD_VIDEO_LIST = 1
    SEARCH = 2
    UPDATE_THUMBNAIL = 3
    PREVIEW_THUNBNAIL = 4


debug = DEBUG.UPDATE_THUMBNAIL
if user_name == "thsxo":
    youtube_API_test.DEVELOPER_KEY = open("api_key_thsvkd.txt", "r").readline()
    youtube_API_test.CLIENT_SECRETS_FILE = "client_secrets_thsvkd.json"
else:
    youtube_API_test.DEVELOPER_KEY = open("api_key.txt", "r").readline()
    youtube_API_test.CLIENT_SECRETS_FILE = "client_secrets.json"

if __name__ == "__main__":

    thumbnail_args = thumbnail_args_parse()
    youtube = get_authenticated_service(thumbnail_args)
    viewCount = get_view_count(youtube, thumbnail_args.video_id)

    text = "이 영상의 조회수는\n%s 입니다!" % viewCount
    font_size = 300
    font_color = "ff847c"
    font_style = "BlackHanSans"
    img_name = ""
    img_size = 1

    contents = [text, font_size, font_color, font_style, img_name, img_size]

    # youtube = get_authenticated_service(args)
    # upload_thumbnail(youtube, args.video_id, args.file)

    if debug == DEBUG.PREVIEW_THUNBNAIL:
        final_thumbnail = make_thumbnail_image(contents=contents)
        show_preview_image(final_thumbnail)
    elif debug == DEBUG.LOAD_VIDEO_LIST:
        youtube_API_test.get_video_list(youtube_API_test.CLIENT_SECRETS_FILE)
    elif debug == DEBUG.SEARCH:
        args = search_args_parse()
        try:
            youtube_API_test.youtube_search(args)
        except HttpError as e:
            print("An HTTP error {} occurred:\n{}".format(e.resp.status, e.content))
    elif debug == DEBUG.UPDATE_THUMBNAIL:
        while True:
            today = datetime.today()
            if today.second % 2 == 0:
                final_thumbnail = make_thumbnail_image(contents=contents)
                try:
                    dir_name = "thumbnail_images"

                    if not (os.path.isdir(dir_name)):
                        os.makedirs(os.path.join(dir_name))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        print("Failed to create directory!!!!!")
                        raise

                image_path = dir_name + "/%04d%02d%02d_%02d%02d%02d.jpg" % (
                    today.year,
                    today.month,
                    today.day,
                    today.hour,
                    today.minute,
                    today.second,
                )

                cv2.imwrite(
                    image_path, final_thumbnail,
                )

                if not os.path.exists(image_path):
                    exit("Please specify a valid file using the --file= parameter.")

                try:
                    upload_thumbnail(youtube, thumbnail_args.video_id, image_path)
                except HttpError as e:
                    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
                else:
                    print("The custom thumbnail was successfully set.")

                # if not os.path.exists(args.file):
                #     exit("Please specify a valid file using the --file= parameter.")

                # youtube = get_authenticated_service(args)
                # try:
                #     upload_thumbnail(youtube, args.video_id, args.file)
                # except HttpError as e:
                #     print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
                # else:
                #     print("The custom thumbnail was successfully set.")
