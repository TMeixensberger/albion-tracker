from pictureApi import LoadoutGenerator
from util import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

class FighRenderer():
    
    def __init__(self, killer, victim):
        self.__killer = killer
        self.__victim = victim
        pass

    def addText(self, x, y, text, pic):
        img = Image.open(pic)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("", 50)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((x, y),text,(255,255,255), font=font)
        img.save(pic)

    def generate(self):
        killerLoadout = LoadoutGenerator(self.__killer)
        victimLoadout = LoadoutGenerator(self.__victim)
        killerPath = killerLoadout.generate()
        victimPath = victimLoadout.generate()

        spacerBetweenLoadouts = 50
        totalHeight = killerLoadout.height() 
        totalWidth = killerLoadout.width() + victimLoadout.width() + spacerBetweenLoadouts

        basePicPath = Util.generateBasePic(totalHeight, totalWidth)

        base = Image.open(basePicPath)
        base.paste(Image.open(killerPath), (0, 0))
        base.paste(Image.open(victimPath), (killerLoadout.width(), 0))
        base.save(basePicPath, quality=95)


        self.addText(0, 0, self.__killer["Name"], basePicPath)
        self.addText(victimLoadout.width() + spacerBetweenLoadouts, 0, self.__victim["Name"], basePicPath)
        return basePicPath