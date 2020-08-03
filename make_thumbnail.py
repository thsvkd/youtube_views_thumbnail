import cv2
import numpy as np
import pyperclip
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image

video_size_ratio = [16, 9]


def make_font_img(text):
    ratio = 40
    W, H = video_size_ratio[0] * ratio, video_size_ratio[1] * ratio
    img = np.zeros((H, W, 3), np.uint8)
    b, g, r, a = 255, 255, 255, 0

    fontpath = "C:/Users/thsxo/AppData/Local/Microsoft/Windows/Fonts/210 콤퓨타세탁R.ttf"
    font = ImageFont.truetype(fontpath, 20)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    w, h = font.getsize(text)
    draw.text((0, 0), text, font=font, fill=(b, g, r, a))
    #draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=(b, g, r, a))
    img = np.array(img_pil)
    img = img[:h, :w]
    cv2.imshow("res", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img


def main(title_img):

    ratio = 0.1
    winname = "BG"

    BG_img = cv2.imread(
        "C:/Users/thsxo/Desktop/IMG_2199.JPG")
    BG_w, BG_h, BG_c = BG_img.shape
    BG_shape = [BG_w, BG_h, BG_c]
    BG_shape[0] *= ratio
    BG_shape[1] *= ratio

    title_w, title_h, title_c = title_img.shape
    title_shape = [title_w, title_h, title_c]

    BG_img = cv2.resize(BG_img, dsize=(
        int(BG_shape[1]), int(BG_shape[0])), interpolation=cv2.INTER_AREA)

    BG_img[(int(BG_shape[0]) - title_shape[0])//2:(int(BG_shape[0]) + title_shape[0])//2,
           (int(BG_shape[1]) - title_shape[1])//2:(int(BG_shape[1]) + title_shape[1])//2] = title_img

    cv2.namedWindow(winname, cv2.WINDOW_AUTOSIZE)
    #cv2.moveWindow(winname, 720, 480)
    cv2.imshow(winname, BG_img)

    cv2.waitKey(0)


if __name__ == "__main__":
    # main()
    title = make_font_img("0123456789")
    main(title)


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
