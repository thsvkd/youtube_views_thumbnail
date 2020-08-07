import cv2
import numpy as np
import pyperclip
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import getpass


def make_colorcode(code):

    if code[0] == '#':
        r = int('0x'+code[1:3], 16)
        g = int('0x'+code[3:5], 16)
        b = int('0x'+code[5:7], 16)
    else:
        r = int('0x'+code[0:2], 16)
        g = int('0x'+code[2:4], 16)
        b = int('0x'+code[4:6], 16)
    print([r, g, b])

    return [r, g, b]


def make_thumbnail_image(text, font_size, font_color):

    ratio = 0.1
    winname = "BG"
    r, g, b = make_colorcode(font_color)
    a = 0

    BG_img = cv2.imread(
        "C:/Users/%s/Desktop/IMG_2199.JPG" % getpass.getuser())
    BG_w, BG_h, BG_c = BG_img.shape
    BG_shape = [BG_w, BG_h, BG_c]
    BG_shape[0] *= ratio
    BG_shape[1] *= ratio

    BG_img = cv2.resize(BG_img, dsize=(
        int(BG_shape[1]), int(BG_shape[0])), interpolation=cv2.INTER_AREA)

    fontpath = "C:/Users/thsxo/AppData/Local/Microsoft/Windows/Fonts/210 콤퓨타세탁R.ttf"
    font = ImageFont.truetype(fontpath, 44)
    img_pil = Image.fromarray(BG_img)
    draw = ImageDraw.Draw(img_pil)
    w, h = font.getsize(text)
    draw.text(((int(BG_shape[1]) - w)/2, ((int(BG_shape[0]) - h)/2)),
              text, font=font, fill=(b, g, r, a))
    BG_img = np.array(img_pil)

    cv2.namedWindow(winname, cv2.WINDOW_AUTOSIZE)
    #cv2.moveWindow(winname, 720, 480)

    cv2.imshow(winname, BG_img)

    cv2.waitKey(0)


if __name__ == "__main__":

    make_thumbnail_image("이 영상의 조회수는 123입니다", 44, "b52b65")
