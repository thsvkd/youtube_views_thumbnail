import cv2
import numpy as np
import pyperclip
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image


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


def make_thumbnail_image(text, font_size, color):

    ratio = 0.1
    winname = "BG"
    r, g, b = make_colorcode(color)
    a = 0

    BG_img = cv2.imread(
        "C:/Users/thsxo/Desktop/IMG_2199.JPG")
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


# import matplotlib.pyplot as plt
# import numpy as np
# from PIL import ImageFont, ImageDraw, Image

# image1 = np.zeros((480, 640, 3), np.uint8)
# image2 = Image.fromarray(image1)
# draw = ImageDraw.Draw(image2)
# draw.text((10, 20), "안녕하세요", font=ImageFont.truetype("./batang.ttc", 48), fill=(255,255,255))

# plt.imshow(image2)
# plt.show()

##########################

# import numpy as np
# from PIL import ImageFont, ImageDraw, Image
# import cv2
# import time

# ## Make canvas and set the color
# img = np.zeros((200,400,3),np.uint8)
# b,g,r,a = 0,255,0,0

# ## Use cv2.FONT_HERSHEY_XXX to write English.
# text = time.strftime("%Y/%m/%d %H:%M:%S %Z", time.localtime())
# cv2.putText(img,  text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (b,g,r), 1, cv2.LINE_AA)

# ## Use simsum.ttc to write Chinese.
# fontpath = "./simsun.ttc"
# font = ImageFont.truetype(fontpath, 32)
# img_pil = Image.fromarray(img)
# draw = ImageDraw.Draw(img_pil)
# draw.text((50, 100),  "国庆节/中秋节 快乐!", font = font, fill = (b, g, r, a))
# img = np.array(img_pil)

# ## Display
# cv2.imshow("res", img);cv2.waitKey();cv2.destroyAllWindows()
# cv2.imwrite("res.png", img)
