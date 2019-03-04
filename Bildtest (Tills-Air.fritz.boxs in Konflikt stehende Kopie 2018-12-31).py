from PIL import Image, ImageDraw, ImageDraw2
from bresenham import bresenham
import math
import numpy as np
#import panda as pd


###
###
### BILD VORBEREITEN
###
###

#BILD LADEN UND SCHWARZ WEIß KONVERTIEREN
#im_start = Image.open("Testbild2.jpeg").convert("L") #MONOCHROME
im_start = Image.open("Testbild4.jpg").convert("1") #BINARY
im = im_start.copy()


########

nx, ny = im.size
im = im.resize((int(nx*(260/im.size[0])), int(ny*(260/im.size[1]))), Image.BICUBIC)

nx, ny = im.size
print(nx, ny)

draw = ImageDraw.Draw(im)


#######


# KREISDATEN BERECHNEN (GRÖßT MÖGLICHEN KREIS)
im_breite = im.size[0]
im_hoehe = im.size[1]


durchmesser = 0

# minus 1 dass später kein Pixel 1 über dem Bildrand rauskommt
if im_breite > im_hoehe:
    durchmesser = im_hoehe-1

else:
    durchmesser = im_breite-1
radius = int(durchmesser/2)


mittelpunkt_x = int(im_breite/2)
mittelpunkt_y = int(im_hoehe/2)

#Bildgröße auf Durchmesser X Durchmesser anpassen + kleiner weißer Rand
#rand = 5
#box = [mittelpunkt_x-radius + rand, mittelpunkt_y-radius + rand, mittelpunkt_x+radius + rand, mittelpunkt_y+radius + rand]
#im = im.crop(box)


#KREIS UND MITTELPUNKT MALEN
#draw.ellipse((mittelpunkt_x - radius, mittelpunkt_y - radius, mittelpunkt_x + radius, mittelpunkt_y + radius), fill = None, outline = None)
draw.point((mittelpunkt_x, mittelpunkt_y), 'black')
#print(im.format, im.size, im.mode)

#Gibt Länge eines Fadens aus: bsp.: laenge(0,0,3,3) =>  4
def laenge(x1, y1, x2, y2):
    laenge = (round(math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)))
    return (laenge)

#BILD AUßERHALB KREIS ENTFERNEN / WEIß MACHEN
for x in range(0,im_breite):
    for y in range (0, im_hoehe):
        if laenge(mittelpunkt_x, mittelpunkt_y, x, y) >= radius:
            draw.point((x, y), "white")


im.show()