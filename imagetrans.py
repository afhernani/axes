#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import math
import os
import logging
import PIL.Image
from PIL import Image, ImageOps, ImageDraw

__author__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'imagetrans'
__version__ = '1.0'

__all__ = ('Imagetrans')


class Imagetrans:

    @staticmethod
    def engine(size=None, img=None ) -> Image:
        '''return a scale image contents at size''' 
        # logging.info('#### Engine ###')
        if not size or not img:
            return None
                 
        if size == img.size:
            return img
        tamiz = Image.new('RGBA', size, (0, 0, 0, 255)) # transparente
        # print('size:', size, '\norignal mode:', img.mode, '\ninfo:', img.info)
        r, p = Imagetrans.getScale(size, img.size)
        img_new = ImageOps.scale(img, r, PIL.Image.BOX)
        # return img_new
        tamiz.paste(img_new, p)
        return tamiz

    @staticmethod
    def getScale(marco=None, marco2=None)-> tuple:
        '''return scale and centred possition img
            parammeter:
                marco: size imagen fin
                marco2: size imagen initial '''
        # logging.info('escala -')
        if not marco or not marco2:
            return 1.0
        w, h = marco
        w2, h2 = marco2
        x, y = 0, 0
        # logging.info(f'valores: {w}, {h}, {w2}, {h2}')
        f = w/h
        f2 = w2/h2
        # logging.info(f'relaciones ancho-alto: {f}, {f2}')
        l = math.hypot(w, h)
        l2 = math.hypot(w2, h2)
        # logging.info(f'hipotemas: {l}, {l2}')
        a = math.acos((w/l))
        a2 = math.acos((w2/l2))
        # logging.info(f'angulos: {a}, {a2}')
        if a == a2:
            r = w/w2
            p = (0, 0)
        elif a < a2:
            r =h/h2
            y = 0
            x = int(abs(w - w2*r)/2)
            p = (x, y)
        elif a > a2:
            r =w/w2
            x = 0
            y = int(abs(h - h2*r)/2)
            p = (x, y)
        else:
            r = 1.0
            p = (0, 0)
        # logging.info(f'devuelve: {r}, {p}')
        return (r, p)
