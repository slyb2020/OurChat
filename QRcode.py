#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from ID_DEFINE import DEFAULT_PATH
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
def generateQRCode(data, imgFn):
    qr = qrcode.QRCode(version=20,
                       error_correction=ERROR_CORRECT_H,
                       box_size=2, border=2)
    # 添加自定义文本信息，
    qr.add_data(data)
    qr.make()
    # 创建二维码图片
    img = qr.make_image()
    imgW, imgH = img.size
    w1, h1 = map(lambda x: x // 4, img.size)
    # 要粘贴的自定义图片，生成缩略图
    im = Image.open(imgFn)
    imW, imH = im.size
    w1 = w1 if w1 < imW else imW
    h1 = h1 if h1 < imH else imH
    im = im.resize((w1, h1))
    # 在二维码上中间位置粘贴自定义图片
    img.paste(im, ((imgW - w1) // 2, (imgH - h1) // 2))
    # 保存二维码图片
    img.save(DEFAULT_PATH+'/qrCode.jpg')  # 自己的存储路径
    # img.save('G:/WangLuoRuanJian/qrCode.jpg')
    # img.show()
if __name__ == "__main__":
    generateQRCode(
        'http://www.tju.edu.cn', DEFAULT_PATH+'/ls.png')
