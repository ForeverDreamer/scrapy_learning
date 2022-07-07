#!/usr/bin/python
from PIL import Image
import pytesseract
import sys
# 添加系统变量之后cmd和ide都需要重启才能生效
# sys.path.append('C:\\Program Files\\Tesseract-OCR\\tesseract.EXE')


def recognize_captcha(img_path):
    im = Image.open(img_path).convert("L")
    # 1. threshold the image
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    out = im.point(table, '1')
    # out.show()
    # 2. recognize with tesseract
    num = pytesseract.image_to_string(out)
    return num


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python recognize.py <image_filename>")
    res = recognize_captcha(sys.argv[1])
    strs = res.split("\n")
    if len(strs) >=1:
        print(strs[0])
