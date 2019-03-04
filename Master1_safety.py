#TODO:
#- validate offset weighting


from PIL import Image, ImageDraw, ImageDraw2
from bresenham import bresenham
import math
import numpy as np

### BASIC FUNCTIONS ####################################################################################################

#CALCULATE LENGTH
#Gibt den Abstand zweier Pixel aus: bsp.: laenge(0,0,3,3) =>  4
def length(x1, y1, x2, y2):
    leng = (round(math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)))
    return leng


### PICTURE ############################################################################################################
class Picture:

    def __init__(self, path, binary = True):
        self.picture_path = path
        self.binary = binary

        #open original picture
        if binary == True:
            im_start = Image.open(path).convert("1")  #BINARY (0 = False = black / 255 = White = True )
        else:
            im_start = Image.open(path).convert("L")    #MONOCHROME

        #copy original to not change it
        self.image = im_start.copy()
        self.draw = ImageDraw.Draw(self.image)

        #dimensions
        self.width = self.image.size[0]
        self.height = self.image.size[1]

        #radius/diameter
        self.diameter = 0
        if self.width > self.height:
            self.diameter = self.height - 1

        else:
            self.diameter = self.width - 1
        self.radius = int(self.diameter / 2)

        #center point
        self.center_x = int(self.width / 2)
        self.center_y = int(self.height / 2)

    #gives back an array with all pixel values or for binary of booleans (False = black = 1 / White = True = 0)
    def pixel_array(self):
        pixels = np.array(self.image)
        return pixels

    #gives back an array with 1 for black dot and 0 for none
    def pixel_array_binary(self):
        pixels_bin = self.pixel_array()
        pixels_bin = np.where(pixels_bin == True,0,1)
        return pixels_bin

    #draw center point
    def draw_center(self):
        self.draw.point((self.center_x, self.center_y), 'black')
        #draw circle
        # draw.ellipse((mittelpunkt_x - radius, mittelpunkt_y - radius, mittelpunkt_x + radius,
        # mittelpunkt_y + radius), fill = None, outline = None)

    #paint everything outside of circle white (and crop picture)
    def remove_outter_pic(self, edge = 5):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if length(self.center_x, self.center_y, x, y) >= self.radius:
                    self.draw.point((x, y), "white")
        self.image.save("Picture.png")

        #crop whole box
        #box = [self.center_x-self.radius + edge, self.center_y-self.radius + edge, self.center_x+
        # self.radius + edge, self.center_y+self.radius + edge]
        #self.image = self.image.crop(box)

    def show(self):
        self.image.show()






### ARTWORK ############################################################################################################
class Artwork:

    def __init__(self, width, height, path = "Result.png",):
        self.path = path
        self.width = width
        self.height = height
        self.white = Image.new('1', (self.width, self.height), "white")
        self.artwork = self.white
        self.draw = ImageDraw.Draw(self.artwork)

    #gives back an array with all pixel values or for binary of booleans (False = black = 1 / White = True = 0)
    def pixel_array(self):
        pixels = np.array(self.artwork)
        return pixels

    #gives back an array with 1 for black dot and 0 for none
    def pixel_array_binary(self):
        pixels_bin = self.pixel_array()
        pixels_bin = np.where(pixels_bin == True,0,1)
        return pixels_bin

    # draws one connection on the canvas
    def draw_connection(self, connection, width=1):
        self.draw.line((connection.start_end()), width=width)

    def draw_connections(self):
        pass

    #draws all nails on the canvas
    def draw_nails(self,nails):
        for pos in nails.positions:
            self.draw.point((pos[1], pos[2]), "black")

    def save(self):
        self.artwork.save(self.path)
        print("Artwork saved")

    def show(self):
        self.artwork.show()





### NAILS ##############################################################################################################
class Nails:

    def __init__(self, center_x, center_y, radius, n = 200):

        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.number = n

        self.positions = np.array([[i, self.center_x + self.radius * math.cos(2 * np.pi * (i / self.number)),
                                    self.center_y + self.radius * math.sin(2 * np.pi * (i / self.number))] for i in range(0, n)])
        self.positions = np.around(self.positions)
        self.positions = self.positions.astype(int)


### CONNECTION #########################################################################################################
class Connection:

    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def start_end(self):
        return (self.start_x, self.start_y, self.end_x, self.end_y)

    def pixel_list(self):
        pixel_list = list(bresenham(self.start_x, self.start_y, self.end_x, self.end_y))
        # Ignores first and last pixel
        pixel_list.pop(0)
        pixel_list.pop()
        return pixel_list


c = Connection(1,1,100,100)

### ARTIST #############################################################################################################
class Artist:

    def __init__(self):

        self.pic = Picture("Testbild1.png", binary=True)
        self.aw = Artwork(self.pic.width, self.pic.height)

        self.nails = Nails(self.pic.center_x, self.pic.center_y, self.pic.radius)


    def start(self):
        self.pic.draw_center()
        self.pic.remove_outter_pic()
        #self.pic.show()

    def set_nails(self):
        self.aw.draw_nails(self.nails)

    #computes array with offset (0 = all good, 1 = line still required, -1 = line to much)
    def offset(self,picture, artwork):
        offset_array = picture.pixel_array_binary() - artwork.pixel_array_binary()
        return offset_array

    def offset_weighted(self,picture, artwork, done_weight, under_weight, over_weight):
        offset = offset(picture, artwork)
        offset = np.where(offset == 0, 0+done_weight,offset)
        offset = np.where(offset == 1, 1+under_weight,offset)
        offset = np.where(offset == -1, -1+over_weight,offset)
        return offset


    def show_artwork(self):
        self.aw.show()



artist = Artist()

artist.start()
artist.set_nails()
#artist.aw.save()

#print(artist.pic.pixel_array_binary()[5,:50])
#print(artist.aw.pixel_array_binary()[5,:50])
c = Connection(0,0,200,500)
artist.aw.draw_connection(c, width=10)
#print(artist.aw.pixel_array_binary()[5,:50])
#print(artist.offset(artist.pic,artist.aw)[5,:50])
#print(artist.offset_weighted(artist.pic,artist.aw,0,0,-10)[5,:50])


#Binary(0\1) and TRUE watchout messup in binary



###

###

###

###

###

###

