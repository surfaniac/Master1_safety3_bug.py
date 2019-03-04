#TODO:
#- sort connections by score

# DIFFERENT MINDSETS:
#### TRUE IS: X-AXIS IS VERTICAL AND Y_AXIS HORIZONTAL

#Twist x and y axis / array is x vertical y horizontal / picture understanding normally different
#

#1. Offset (set connection and then compare if it was a good decision)
#2. Final picture (plus for black / minus for white)

from PIL import Image, ImageDraw, ImageDraw2
from bresenham import bresenham
import math
import numpy as np
from itertools import cycle

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
        self.center_x = int(self.height / 2)
        self.center_y = int(self.width / 2)

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

        self.number_of_connections = 12000

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

        # Format as integer [index, x_coordinate(vertical), y_coordinate(horizontal)] [ 50, 150, 349]
        self.positions = np.array([[i, self.center_x + self.radius * math.cos(2 * np.pi * (i / self.number)),
                                   self.center_y + self.radius * math.sin(2 * np.pi * (i / self.number))] for i in range(0, n)])
        #self.positions = np.array([[i, self.center_y + self.radius * math.sin(2 * np.pi * (i / self.number)),
        #                self.center_x + self.radius * math.cos(2 * np.pi * (i / self.number))] for i in range(0, n)])
        self.positions = np.around(self.positions)
        self.positions = self.positions.astype(int)
        print(self.positions)

#nails = Nails(110,110,100)

### CONNECTION #########################################################################################################
class Connection:

    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        # For the connection from (0,0) to (3,3) the output is [(1, 1), (2, 2)]
        self.pixel_list = list(bresenham(self.start_x, self.start_y, self.end_x, self.end_y))
        self.pixel_list = self.pixel_list[1:-1]


    def start_end(self):
        return (self.start_x, self.start_y, self.end_x, self.end_y)


    def judgment_score(self, judgment_array):
        print(judgment_array.shape)
        print(self.pixel_list)
        judgment = [judgment_array[pixel[0],pixel[1]] for pixel in self.pixel_list]
        judgment_score = sum(judgment)
        return judgment_score

c = Connection(0,0,4,4)
print(c.pixel_list)


### CONNECTIONS #########################################################################################################
class Connections:

    def __init__(self, nails_position):
        #connect nails list to a circle
        self.nails_position = nails_position
        self.number_nails = len(self.nails_position)

    # Format of all connections: List of all nails with format [idx,idx,idx,...]
    def possible_connection_indices(self, nail_index, space):
        #space = space to one side
        if space*2 >= self.number_nails:
            print("Space to big")
        idx_list = [x[0] for x in self.nails_position]
        idx_list = idx_list[nail_index+1:] + idx_list[:nail_index]
        idx_list = idx_list[space:-(space)]
        return idx_list

    # Format of all connections: List of all nails with format [[idx,pos_x,pos_y],[idx,pos_x,pos_y],[...],...]
    def possible_connection_nails(self, nail_index, space):
        #space = space to one side
        if space*2 >= self.number_nails:
            print("Space to big")
        idx_list = (self.nails_position).tolist()
        idx_list = idx_list[nail_index + 1:] + idx_list[:nail_index]
        idx_list = idx_list[space:-(space)]
        return idx_list

    #Format of all connections: [Connection-object, Connection-object, ...]
    def possible_connections(self, nail_index, space):
        connections_list = []
        indices = self.possible_connection_indices(nail_index, space)
        for idx in indices:
            if self.nails_position[idx][0] != idx:
                print("Index error in Connection list!")
            else:
                start_x = self.nails_position[nail_index][1]
                start_y = self.nails_position[nail_index][2]
                end_x = self.nails_position[idx][1]
                end_y = self.nails_position[idx][2]
                c = Connection(start_x, start_y, end_x, end_y)
                connections_list.append(c)

        return connections_list



#connections = Connections(nails.positions)
#print(nails.positions[100])
#print(connections.possible_connection_indices(100,98))
#print(connections.possible_connection_nails(100,98))
#print(connections.possible_connections(100,99))





### ARTIST #############################################################################################################
class Artist:

    def __init__(self):

        self.pic = Picture("Testbild1.png", binary=True)
        self.aw = Artwork(self.pic.width, self.pic.height)
        #self.aw = Artwork(self.pic.height, self.pic.width)

        self.nails = Nails(self.pic.center_x, self.pic.center_y, self.pic.radius)


    def start(self):
        self.pic.draw_center()
        self.pic.remove_outter_pic()
        self.pic.show()

    def set_nails(self):
        self.aw.draw_nails(self.nails)

    #JUDGMENT MATRIX:
    #name_v1:       done    under   over    done
    #name_v2:       dont    under   over    done
    #picture:       0       1       0       1
    #artwork:       0       0       1       1
    #weight:        -5      1       -1?     0.2

    # updates judgment array has shape ((400, 300, 2)) (x,y,[pic_binary_value,aw_binary_value])
    def update_judgment_array(self, dont_weight = -5, under_weight=1, over_weight=-1, done_weight = 0.2):

        #get pixel rom picture and artwork
        p = self.pic.pixel_array_binary()
        a = self.aw.pixel_array_binary()

        #generate empty array same shape
        ja = np.zeros(p.shape)
        #apply rules from judgment matrix
        ja = np.where(p == 0, np.where(a==0,dont_weight,ja),ja)
        ja = np.where(p == 1, np.where(a == 0, under_weight, ja), ja)
        ja = np.where(p == 0, np.where(a == 1, over_weight, ja), ja)
        ja = np.where(p == 1, np.where(a == 1, done_weight, ja), ja)
        #generate/update judgment array
        self.judgment_array = ja



    def offset_connections(self):
        pass


    def show_artwork(self):
        self.aw.show()


artist = Artist()

artist.start()
artist.set_nails()
artist.show_artwork()

number_of_connections = 12000
jarn_position = [100]
space = 20

for n in range(0,number_of_connections):

    if n % 1 == 0:
        artist.update_judgment_array()



    connections = Connections(artist.nails.positions).possible_connections(jarn_position[-1],space)
    connections_scores = [c.judgment_score(artist.judgment_array) for c in connections]

    connections_sorted = [x for _, x in sorted(zip(connections_scores,connections), key=lambda pair: pair[0])]
    selected_connection = connections_sorted[0]

    jarn_position.append(selected_connection.)
    artist.aw.draw_connection(selected_connection)


    if n % 30 == 0:
        artist.show_artwork()



print("judgment")
artist.update_judgment_array()
#print(artist.nails.positions[50])

c_one = Connection(0,0,3,3)
print("pixel_list")
print(c_one.pixel_list)
print(c_one.judgment_score(artist.judgment_array))



###

###

###

###

###

###

