from PIL import ImageTk, Image


#Třída Shot
class Shot():
    #Inicializování třídy Shot
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.fill_color = color
        self.outline_color = "black"


    #Vykreslení třídy Shot
    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.fill_color, outline=self.outline_color)


#Třída Ship
class Ship():
    #Inicializování třídy Ship
    def __init__(self, x, y, direction, points, lod):
        self.x = x
        self.y = y
        self.direction = direction
        self.points = points
        self.width = 75
        self.height = 75
        self.lod = lod


    #Vykreslení třídy Ship
    def draw(self, canvas):
        self.imglod = Image.open('img\lod'+ self.lod +'-' + self.direction + '.png')
        self.imglod = self.imglod.resize((self.width,self.height), Image.ANTIALIAS)
        self.imglod = ImageTk.PhotoImage(self.imglod)
        canvas.create_image(self.x, self.y, image=self.imglod, anchor='nw')
