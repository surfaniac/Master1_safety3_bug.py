### TODO:
### - sortieren
### - zeichnen
### - Testbild anpassen (Kontraste erhöhen)



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
#im_start_monochrome = Image.open("Testbild1.png").convert("L") #MONOCHROME
im_start = Image.open("Testbild2.jpeg").convert("1") #BINARY
im = im_start.copy()
draw = ImageDraw.Draw(im)

#"Bildwerte" in Liste schreiben
pixels = np.array([])
pixels = im.load()
#print(pixels[0,0])


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




###
###
###
### LISTE MIT NÄGELN GENERIEREN
###
###
###



#GENERIERT LISTE MIT NÄGELN (MITTELPUNKT X/Y, RADIUS, N = ANZAHL)
def naegel_generieren(x, y, radius, n):
    naegel = np.array([[i, x + radius * math.cos(2*np.pi*(i/n)), y + radius * math.sin(2*np.pi*(i/n)) ] for i in range(0,n)])
    naegel = np.around(naegel)
    naegel = naegel.astype(int)
    #print(len(naegel))
    return naegel



###
###
###
### SCORE LISTE GENERIEREN
###
###
###



#w = Anzahl Weißpunkte
#l = Länge der Verbindung
#r = Weiße Punkte in einer Row
#ra = Anzahl der Weißen Punkte in einer Row die in den r-Count mit aufgenommen werden

#Je kleiner Score desto besser (desto eher sollte die Verbindung gezogen werden)

def score_verbindung(x1, y1, x2, y2, w_faktor = 2, l_faktor = -1, r_faktor = 10, ra_faktor = 3):
    # here the magic is happening ;)

    pixel_liste = list(bresenham(x1, y1, x2, y2))
    # entfernt Start und Endpixel
    pixel_liste.pop(0)
    pixel_liste.pop()
    # Macht aus meiner Pixelliste eine Liste mit 0 = weiß und 1 = schwarz
    binary_liste = []
    for k in range(0, len(pixel_liste)):
        p = 2
        kx = int(pixel_liste[k][0])
        ky = int(pixel_liste[k][1])
        if pixels[(kx, ky)] == 255:  # weiß
            p = 0
        elif pixels[(kx, ky)] == 0:  # schwarz
            p = 1
        else:
            print("Bild nicht BINARY !!!")
        binary_liste.append(p)

    w = binary_liste.count(0)
    l = len(binary_liste)

    r = 0
    c = 0
    for k in range(0,len(binary_liste)):
        if binary_liste[k] == 0:
            c = c + 1
            if c == ra_faktor: # zählt einmal wenn länge über ra_faktor egal wie lange weißstück ist /// wenn andersgewünscht nach zweiter if c = 0 setzen
                r = r + 1
                c = 0
        else:
            c = 0

    score = w*w_faktor + r*r_faktor + l*l_faktor
    return score


# Gibt eine Liste aller Verbindungen plus Score zurück im Format:
# [[[von_punkt1, bis_punkt2 x1, y1, x2, y2, score1], [p1, p3, x1, y1, x3, y3, score2], ... ],[[p2, p1, x2, y2, x1, y1, score_i],...],...]
# "Eigenverbindungen" (von_punkt == bis_punkt) werden nicht in Liste mit aufgenommen
# Verbindungsdopplungen wie 1,2 und 2,1 werden nicht mit aufgenommen
# Liste !!!!! concatenate


def alle_verbindungen_score(source, w_faktor = 2, l_faktor = -1, r_faktor = 10, ra_faktor = 3):
    s = source
    alle_verbindungen = []

    for i in s:
        verbindungen = []
        von_punkt = i[0]
        x1 = i[1]
        y1 = i[2]
        for j in range(1 ,len(s)):
            bis_punkt = s[j][0]
            x2 = s[j][1]
            y2 = s[j][2]

            if von_punkt != bis_punkt:
                score = score_verbindung(x1, y1, x2, y2, w_faktor, l_faktor, r_faktor, ra_faktor)
                verbindung = [von_punkt, bis_punkt, x1, y1, x2, y2, score]
                alle_verbindungen.append(verbindung)

       # alle_verbindungen = np.concatenate((alle_verbindungen, verbindungen))
    return (alle_verbindungen)


def sortieren(liste):

    liste.sort(key=lambda l: l[6], reverse = False)
    return liste










def bild_score(input, output):
    pixels_input = np.array(input)
    pixels_output = np.array(output)

    bild_score_liste = pixels_input - pixels_output
    bild_score_liste = sum(bild_score_liste**2)
    return(sum(bild_score_liste))



def zeichnen\
                (anzahl_verbindungen, auslasser, w_faktor, l_faktor, r_faktor, ra_faktor):

    naegel = naegel_generieren(mittelpunkt_x, mittelpunkt_y, radius, 200)
    x = alle_verbindungen_score(naegel, w_faktor, l_faktor, r_faktor, ra_faktor)
    s = sortieren(x)

    # VISUELLE KONTROLLE TESTBILD
    im.show()

    im_end = Image.new('L', (im_breite, im_hoehe), "white")
    draw_end = ImageDraw.Draw(im_end)

    # VISUELLE KONTROLLE AUSGABEBILD
    for nagel in naegel:
        draw_end.point((nagel[1], nagel[2]), "black")

    for i in range(1,anzahl_verbindungen):
        x1 = s[i][2]
        y1 = s[i][3]
        x2 = s[i][4]
        y2 = s[i][5]
        if i % auslasser != 0:
            draw_end.line((x1, y1, x2, y2), width = 1)

    im_end.save("Ausgabe.jpg", "JPEG")
    im_end.show()