import os
import hashlib
from random import random
from PIL import Image, ImageDraw, ImageFilter
from matplotlib import pyplot as plt
import numpy as np
import random
import tempfile
import requests


spacer = 10
imageSize = 217

image_height = 5 * spacer + 4 * imageSize
image_width = 4 * spacer + 3 * imageSize


class LoadoutGenerator():
    def __init__(self, bag, head, cape, armour, weapon, offWeapon, food, potion, boots, mount):
        self.__bag = bag
        self.__head = head
        self.__cape = cape
        self.__armour = armour
        self.__weapon = weapon
        self.__offWeapon = offWeapon
        self.__food = food
        self.__potion = potion
        self.__boots = boots
        self.__mount = mount
        self.__picPaths = []

    def cleanupCache(self):
        for path in self.__picPaths:
            if os.path.exists(path):
                os.remove(path)

    def generateRandomPngTempPath(self):
        seed = random.randint(0, 187187)
        hash_object = hashlib.md5(str(seed).encode('utf-8'))
        name = hash_object.hexdigest()
        fileName = "{0}/{1}.png".format(tempfile.gettempdir(), str(name))
        self.__picPaths.append(fileName)
        return fileName

    def generateBasePic(self):
        fileName = self.generateRandomPngTempPath()
        canvas = 1 * np.ones((image_height, image_width, 3), np.uint8)
        plt.imshow(canvas, interpolation='nearest')
        plt.imsave(fileName, canvas)
        img = Image.open(fileName)
        rgba = img.convert("RGBA")
        datas = rgba.getdata()
        newData = []
        for item in datas:
            newData.append((255, 255, 255, 0))
        rgba.putdata(newData)
        rgba.save(fileName, "PNG")
        return fileName

    def generateEmptyItem(self):
        fileName = self.generateRandomPngTempPath()
        canvas = 1 * np.ones((imageSize, imageSize, 3), np.uint8)
        plt.imshow(canvas, interpolation='nearest')
        plt.imsave(fileName, canvas)
        img = Image.open(fileName)
        rgba = img.convert("RGBA")
        datas = rgba.getdata()
        newData = []
        for item in datas:
            newData.append((255, 255, 255, 0))
        rgba.putdata(newData)
        rgba.save(fileName, "PNG")
        return fileName

    def fetchIcon(self, id) -> Image:
        imagePath = self.generateRandomPngTempPath()
        if id is not None:
            endpoint = "https://render.albiononline.com/v1/item/{0}.png".format(
                str(id["Type"]))
            request = requests.get(endpoint)
            if request.status_code == 200:
                file = open(imagePath, "wb")
                file.write(request.content)
                file.close()
        else:
            imagePath = self.generateEmptyItem()
        img = Image.open(imagePath)
        return img

    def generate(self):
        basePath = self.generateBasePic()
        base = Image.open(basePath)
        base.paste(self.fetchIcon(self.__bag), (spacer, spacer))
        base.paste(self.fetchIcon(self.__head),
                   (spacer + imageSize + spacer, spacer))
        base.paste(self.fetchIcon(self.__cape), (spacer + imageSize +
                                                 spacer + imageSize + spacer, spacer))
        base.paste(self.fetchIcon(self.__weapon),
                   (spacer, spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__armour), (spacer + imageSize +
                                                   spacer, spacer + imageSize + spacer))
        if self.__offWeapon is not None:
            base.paste(self.fetchIcon(self.__offWeapon), (spacer + imageSize +
                                                          spacer + imageSize + spacer, spacer + imageSize + spacer))
        else:
            base.paste(self.fetchIcon(self.__weapon), (spacer + imageSize +
                                                       spacer + imageSize + spacer, spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__food), (spacer, spacer + imageSize +
                                                 spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__boots), (spacer + imageSize + spacer, spacer +
                                                  imageSize + spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__potion), (spacer + imageSize +
                                                   spacer + imageSize + spacer, spacer + imageSize + spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__mount), (spacer + imageSize + spacer, spacer +
                                                  imageSize + spacer + imageSize + spacer + imageSize + spacer))
        base.save(basePath, quality=95)
        return basePath

# o = LoadoutGenerator("", "", "", "", "", "", "", "", "", "")
# o.generate()
# o.fetchIcon("T4_OFF_HORN_KEEPER")
