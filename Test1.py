### TODO:
### * Alles in Arrays packen!
### * Inputvektor mit EINEM Attribut für alle Vektoren
###



from PIL import Image, ImageDraw, ImageDraw2
from bresenham import bresenham
import math
import numpy as np
#import panda as pd


#BILD LADEN UND SCHWARZ WEIß KONVERTIEREN
#im_start = Image.open("Testbild.jpg").convert("L") #MONOCHROME
im_start = Image.open("Testbild.jpg").convert("1") #BINARY
im = im_start.copy()
draw = ImageDraw.Draw(im)

#Grauwerte in Liste schreiben
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



#KREIS MALEN
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



#GENERIERT LISTE MIT N NÄGELN (MITTELPUNKT X/Y)
def naegel_generieren(x, y, radius, n):
    naegel = np.array([[i, x + radius * math.cos(2*np.pi*(i/n)), y + radius * math.sin(2*np.pi*(i/n)) ] for i in range(0,n)])
    naegel = np.around(naegel)
    naegel = naegel.astype(int)
    #print(len(naegel))
    return naegel

naegel = naegel_generieren(mittelpunkt_x, mittelpunkt_y, radius, 200)
print(naegel[:10])

















###                         ###
###                         ###
###ALLE ATTRIBUTE BERECHNEN ###
###                         ###
###                         ###


#Länge siehe oben



#Gibt eine Liste aller Pixelgrauwerte zwischen zwei Pixeln /// 0 = schwarz /// 255 = weiß
#Bsp.: grauwert_liste(0,0,3,3) =>   [5, 36]

def grauwert_liste(x1, y1, x2, y2):
    pixel_liste = list(bresenham(x1, y1, x2, y2))
    #print(pixel_liste)
    # entfernt Start und Endpixel
    pixel_liste.pop(0)
    pixel_liste.pop()
    #print(pixel_liste)
    #print(pixel_liste[0][1])
    grauwert_liste = []
    for k in range(0,len(pixel_liste)):
        #Mögliche Fehlerquelle: hier meckert er er will Integer obwohl er nur Integer bekommt
        x = int(pixel_liste[k][0])
        y = int(pixel_liste[k][1])
        grauwert_liste.append(pixels[(x, y)])
    #print(grauwert_liste)
    return(grauwert_liste)



#Gibt Durchschnitt (float) der Pixelgrauwerte zwischen zweier Pixel

def grauwert_durchschnitt(x1, y1, x2, y2):
    grauwerte = grauwert_liste(x1, y1, x2, y2)
    gesamt = 0
    for x in range(0,len(grauwerte)):
        gesamt = gesamt + grauwerte[x]
    durchschnitt = gesamt / (len(grauwerte))
    return durchschnitt


# Gibt den Unterschied zwischen maximalen Grauwert und minimalem Grauwert auf dem Weg an

def grauwert_varianz(x1, y1, x2, y2):
    grauwerte = grauwert_liste(x1, y1, x2, y2)
    varianz = max(grauwerte) - min(grauwerte)
    return varianz


#Gibt an wie schnell sich hell und dunkel abwechseln, indem es immer den Unterschied zweier benachbarter Pixel berechnet, quadriert(vllt hoch 4 ?)( negatives weg) und alle addiert
#Am Ende durch Anzahl an Pixel auf dem Weg geteilt

def grauwert_square_delta(x1, y1, x2, y2):
    grauwerte = grauwert_liste(x1, y1, x2, y2)
    anzahl = len(grauwerte)
    #print(anzahl)
    delta = []
    for i in range(0,len(grauwerte)-1):
        d = grauwerte[i+1]-grauwerte[i]
        delta.append(d)
    #print(delta)
    square_delta = []
    for j in delta:
        sd = j**2
        square_delta.append(sd)
    #print(square_delta)
    #print(sum(square_delta)/anzahl)
    return (sum(square_delta)/anzahl)


#Gibt an wie sehr sich der Grauwert von der Schwarzen Linie unterscheidet, quadriert(vllt hoch 4 ?)( negatives weg) und alle addiert
#Am Ende durch Anzahl an Pixel auf dem Weg geteilt

def square_delta_schwarz(x1, y1, x2, y2):
    grauwerte = grauwert_liste(x1, y1, x2, y2)
    anzahl = len(grauwerte)
    #print(anzahl)
    delta = []
    for i in range(0,len(grauwerte)):
        d = 0 - grauwerte[i]
        delta.append(d)
    #print(delta)
    square_delta = []
    for j in delta:
        sd = j**2
        square_delta.append(sd)
    #print(square_delta)
    return (sum(square_delta)/anzahl)



# Gibt mir eine Liste mit allen Attributen aus einer Verbindung (laenge, grauwert_durchschnitt, grauwert_varianz, grauwert_square_delta)

def verbindung_attribute(source, von, bis):
    s = source
    liste = []

    #print(s[von][1], s[von][2], s[bis][1], s[bis][2])

    #Länge
    liste.append(laenge(s[von][1], s[von][2], s[bis][1], s[bis][2]))

    #Grauwert Durchschnitt
    liste.append(grauwert_durchschnitt(s[von][1], s[von][2], s[bis][1], s[bis][2]))

    # Grauwert Varianz
    liste.append(grauwert_varianz(s[von][1], s[von][2], s[bis][1], s[bis][2]))

    # Grauwert Square Delta
    liste.append(grauwert_square_delta(s[von][1], s[von][2], s[bis][1], s[bis][2]))

    # Square Delta zu Schwarz
    liste.append(square_delta_schwarz(s[von][1], s[von][2], s[bis][1], s[bis][2]))

    # Rundet
    liste = np.around(liste, decimals = 3)
    return liste


# Gibt eine Liste aller Verbindungen zurück im Format:
# [[[von_punkt1, bis_punkt2 x1, y1, x2, y2], [p1, p3, x1, y1, x3, y3], ... ],[[p2, p1, x2, y2, x1, y1],...],...]
# "Eigenverbindungen" (von_punkt == bis_punkt) werden nicht in Liste mit aufgenommen
# Liste !!!!!

def alle_verbindungen(source):
    s = source
    alle_verbindungen = []

    for i in s:
        verbindungen = []
        von_punkt = i[0]
        x1 = i[1]
        y1 = i[2]
        for j in s:
            bis_punkt = j[0]
            x2 = j[1]
            y2 = j[2]
            if von_punkt != bis_punkt:
                verbindung = [von_punkt, bis_punkt, x1, y1, x2, y2]
                verbindungen.append(verbindung)

        alle_verbindungen.append(verbindungen)
    return(alle_verbindungen)

#Gibt ein Array aus mit allen Verbindungen (siehe alle_verbindungen) erweitert mit/ angehängt alle Attribute der Verbindung
#Format: [array([0.000000e+00, 1.000000e+00, 2.990000e+02, 2.000000e+02,
#       2.920000e+02, 2.460000e+02, 4.700000e+01, 1.211560e+02,
#       2.550000e+02, 3.428133e+03, 2.178800e+04]), array([...

def alle_verbindungen_attribute(source):
    s = source
    verbindungen = alle_verbindungen(s)
    alle_verbindungen_attribute = []

    for i in range(0,len(verbindungen)):
        verbis = []
        for j in range(0,len(verbindungen[i])):
            v = verbindungen[i][j]
            a = verbindung_attribute(s, v[0], v[1])
            alle_verbindungen_attribute.append(np.concatenate((v, a)))

    return alle_verbindungen_attribute


#print(alle_verbindungen_attribute(naegel)[:2])




#print(verbindung_attribute(naegel, 0, 2))

# VISUELLE KONTROLLE
for nagel in naegel:
    draw.point((nagel[1], nagel[2]), "black")

im.show()


'''
#Linie zeichnen
im = Image.open("lena.pgm")

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128)
draw.line((0, im.size[1], im.size[0], 0), fill=128)
del draw

# write to stdout
im.save(sys.stdout, "PNG")


'''



def vergleich(i1, i2):

    return uebereinstimmung


