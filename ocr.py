#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <blackhatdwh@gmail.com>
#
# Distributed under terms of the MIT license.

import pytesseract
from PIL import Image, ImageFilter, ImageEnhance

def clean_operator(op):
    clear = ''
    for i in op:
        if i.isdigit():
            clear += i
    return int(clear)

def recognize():
    im = Image.open('login-showPic.jpeg')
    width, height = im.size
    im = im.resize((width*2, height*2))
    im = im.filter(ImageFilter.MinFilter(3))
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(20)
    im = im.convert('1')
    im = im.filter(ImageFilter.MaxFilter(3))
    im.show()
    ocr_result = pytesseract.image_to_string(im, config="-c tessedit_char_whitelist=0123456789+-=?")
    ocr_result = ocr_result.rstrip('-7').rstrip('=?').strip(' ')
    
    print('raw: ', ocr_result)
    
    if ocr_result[0] == '0':
        ocr_result[0] = 9
    
    if ocr_result.find(' ') != -1:
        a = ocr_result.split(' ')[0]
        b = ocr_result.split(' ')[-1]
        if len(b) == 2:
            if b[0] == '7':
                return (clean_operator(a) - clean_operator(b[1]))
            else:
                return (clean_operator(a) + clean_operator(b[1]))
        else:
            return (clean_operator(a) - clean_operator(b))
    if ocr_result.find('-') != -1:
        a = clean_operator(ocr_result.split('-')[0])
        b = clean_operator(ocr_result.split('-')[-1])
        return (a-b)
    if ocr_result.find('+') != -1:
        a = clean_operator(ocr_result.split('+')[0])
        b = clean_operator(ocr_result.split('+')[-1])
        return (a+b)

    return 'wtf' 

if __name__ == '__main__':
    print(recognize())
