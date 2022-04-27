from pictureApi import Loadout
from util import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import shutil


class FighRenderer():

    def __init__(self, killer, victim):
        self.__killer = killer
        self.__victim = victim
        pass

    def addText(self, pos, text, pic):
        img = Image.open(pic)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("AGENCYB.TTF", size=52)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text(pos, text, (255, 255, 255), font=font)
        img.save(pic)

    def generate(self):
        killerLoadout = Loadout(self.__killer)
        victimLoadout = Loadout(self.__victim)

        basePicPath = Util.generateRandomPngTempPath()
        shutil.copyfile("template.png", basePicPath)

        base = Image.open(basePicPath)

        killerItems = [
            {'item': killerLoadout.bag,       'pos': (100, 250)},
            {'item': killerLoadout.head,      'pos': (350, 215)},
            {'item': killerLoadout.cape,      'pos': (600, 250)},
            {'item': killerLoadout.weapon,    'pos': (100, 470)},
            {'item': killerLoadout.armour,    'pos': (350, 440)},
            {'item': killerLoadout.offWeapon, 'pos': (600, 470)},
            {'item': killerLoadout.potion,    'pos': (100, 700)},
            {'item': killerLoadout.boots,     'pos': (350, 665)},
            {'item': killerLoadout.food,      'pos': (600, 700)},
            {'item': killerLoadout.mount,     'pos': (350, 895)}
        ]
        killerText = [
            {'text': self.__killer['Name'],             'pos': (280, 80)},
            {'text': self.__killer['AverageItemPower'], 'pos': (280, 130)}
        ]

        victimItems = [
            {'item': killerLoadout.bag,       'pos': (0, 0)},
            {'item': killerLoadout.head,      'pos': (0, 0)},
            {'item': killerLoadout.cape,      'pos': (0, 0)},
            {'item': killerLoadout.weapon,    'pos': (0, 0)},
            {'item': killerLoadout.armour,    'pos': (0, 0)},
            {'item': killerLoadout.offWeapon, 'pos': (0, 0)},
            {'item': killerLoadout.potion,    'pos': (0, 0)},
            {'item': killerLoadout.boots,     'pos': (0, 0)},
            {'item': killerLoadout.food,      'pos': (0, 0)},
            {'item': killerLoadout.mount,     'pos': (0, 0)}
        ]
        victimText = [
            {'text': self.__killer['Name'],             'pos': (0, 0)},
            {'text': self.__killer['AverageItemPower'], 'pos': (0, 0)}
        ]

        items = killerItems + victimItems
        texts = killerText + victimText

        for entry in items:
            image = Util.fetchIcon(entry['item'])
            base.paste(image, entry['pos'])

        base.save(basePicPath, quality=95)

        for textObj in texts:
            text = str(textObj['text'])
            self.addText(textObj['pos'], text, basePicPath)

        return basePicPath
