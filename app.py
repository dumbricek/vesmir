import json
from tkinter import *
from PIL import ImageTk, Image
from grafika import *
import threading
from tkinter.filedialog import askopenfile, asksaveasfile
from datetime import datetime

root =  Tk()
class MyApp:
    #Inicializování hodnot
    def __init__(self, parent):
            self.color_fg = 'black'
            self.speed=8
            self.width=800
            self.height=600
            self.action = "Hra"
            self.up = False
            self.right = False
            self.down = False
            self.left = False
            self.shot = Shot(1000,1000,"red")
            self.sdirection = ""
            self.up1 = False
            self.right1 = False
            self.down1 = False
            self.left1 = False
            self.shot1 = self.shot1=Shot(1000,1000,"blue")
            self.parent = parent
            self.sdirection1 = ""
            self.path = "img/space1.jpg"
            self.img = ImageTk.PhotoImage(Image.open(self.path))
            self.ship = Ship(725,525,"left",0,"")
            self.ship1 = Ship(0,0,"right",0,"1")
            self.drawWidgets()

    #Vykreslení widgetů
    def drawWidgets(self):
        self.canvas = Canvas(root,width=self.width, height=self.height, bg="White")
        self.canvas.create_image(0, 0, image=self.img, anchor='nw')
        self.ship.draw(self.canvas)
        self.ship1.draw(self.canvas)
        self.canvas.pack(fill=BOTH,expand=True)
        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        self.move()
        menu.add_cascade(label='Hra',menu=filemenu)
        root.bind("<KeyPress>", self.on_key_press)
        root.bind("<KeyRelease>", self.on_key_release)
        filemenu.add_command(label='Konec',command=self.parent.destroy)
        filemenu.add_command(label='Uložit...',command=self.save_file)
        filemenu.add_command(label='Restart',command=self.restart)
        
    #Detekce střely s lodí
    def detect(self, mX, mY, x, y):
        if((mX>=x-50)and(mX<=x)and(mY<=y)and(mY>=y-50)):
            return True
        else:
            return False


    def save_file(self):
        print("Ulozeni souboru")
        file = open("skore.txt","a")
        user_input = str(datetime.now()) + " Červený hráč: " + str(self.ship.points) + " Modrý hráč: " + str(self.ship1.points) + "\n"
        file.write(user_input)
        file.close



    #Vyčištění plátna
    def clear_canvas(self):
        self.canvas.delete("all")
    
    #Restartování hodnot
    def konec(self):
        self.shot=Shot(1000,1000,"red")
        self.shot1=Shot(1000,1000,"blue")
        self.ship.x = 725
        self.ship1.x = 0
        self.ship1.y = 0
        self.ship.y = 525
        self.ship.direction = "left"
        self.ship1.direction = "right"
        self.action = "Hra"
        self.up = False
        self.right = False
        self.down = False
        self.left = False
        self.sdirection = ""
        self.up1 = False
        self.right1 = False
        self.down1 = False
        self.left1 = False
        self.sdirection1 = ""
        self.redraw_canvas()

    #Překreslení plátna
    def redraw_canvas(self):
        self.clear_canvas()
        if (self.detect(self.ship.x,self.ship.y,self.shot1.x,self.shot1.y)):
            self.canvas.configure(background="Black")
            self.action = "konec"
            self.ship1.points += 1
            self.canvas.create_text(200,200,fill="Blue",font=("Helvetica", 30),
                        text=self.ship1.points)
            self.canvas.create_text(600,200,fill="Red",font=("Helvetica", 30),
                        text=self.ship.points)  
            self.canvas.create_text(400,300,fill="blue",font=("Helvetica", 20),
                        text="Modrý hráč vyhrál")
            self.canvas.create_text(400,400,fill="white",font=("Helvetica", 20),
                        text="Pro restartování hry zmáčkni R")
        elif (self.detect(self.ship1.x,self.ship1.y,self.shot.x,self.shot.y)):
            self.canvas.configure(background="Black")
            self.action = "konec"
            self.ship.points += 1
            self.canvas.create_text(200,200,fill="Blue",font=("Helvetica", 30),
                        text=self.ship1.points)
            self.canvas.create_text(600,200,fill="Red",font=("Helvetica", 30),
                        text=self.ship.points)                        
            self.canvas.create_text(400,300,fill="red",font=("Helvetica", 20),
                        text="Červený hráč vyhrál")
            self.canvas.create_text(400,400,fill="white",font=("Helvetica", 20),
                        text="Pro restartování hry zmáčkni R")
        else:
            self.canvas.create_image(0, 0, image=self.img, anchor='nw')
            self.ship.draw(self.canvas)
            self.ship1.draw(self.canvas)
            if(self.shot1):
                self.shot1.draw(self.canvas)   
            if(self.shot):
                self.shot.draw(self.canvas)
            root.after(40,self.move)
              
        

    #Zjišťování zmáčknutého tlačítka
    def on_key_press(self, event):
        if(event.keysym == "Up"):
            self.up = True
            self.ship.direction = "up"
        if(event.keysym == "Right"):
            self.right = True
            self.ship.direction = "right"
        if(event.keysym == "Down"):
            self.down = True
            self.ship.direction = "down"
        if(event.keysym == "Left"):
            self.left = True
            self.ship.direction = "left"
        if(event.keysym == "w"):
            self.up1 = True
            self.ship1.direction = "up"
        if(event.keysym == "d"):
            self.right1 = True
            self.ship1.direction = "right"
        if(event.keysym == "s"):
            self.down1 = True
            self.ship1.direction = "down"
        if(event.keysym == "a"):
            self.left1 = True
            self.ship1.direction = "left"
        if(event.keysym == "m") and (not(self.shot) or (self.shot.x<0 or self.shot.x>self.width or self.shot.y<0 or self.shot.y>self.height)):
            self.shot = Shot(self.ship.x + 75/2 -5,self.ship.y + 75/2 - 5,"red")
            self.sdirection = self.ship.direction
            self.shot.draw(self.canvas)            
        if(event.keysym == "q") and (not(self.shot1) or (self.shot1.x<0 or self.shot1.x>self.width or self.shot1.y<0 or self.shot1.y>self.height)):
            self.shot1 = Shot(self.ship1.x + 75/2 - 5,self.ship1.y + 75/2 - 5,"blue")
            self.sdirection1 = self.ship1.direction
            self.shot1.draw(self.canvas)
        if(event.keysym == "r") and (self.action == "konec"):            
            self.konec()

    #Restartování skóre 
    def restart(self):
        self.clear_canvas()
        self.konec()
        self.ship.points=0
        self.ship1.points=0
        self.redraw_canvas


    #Zjišťováni puštěného tlačítka
    def on_key_release(self, event):
        if(event.keysym == "Up"):
            self.up = False
        if(event.keysym == "Right"):
            self.right = False
        if(event.keysym == "Down"):
            self.down = False
        if(event.keysym == "Left"):
            self.left = False
        if(event.keysym == "w"):
            self.up1 = False
        if(event.keysym == "d"):
            self.right1 = False
        if(event.keysym == "s"):
            self.down1 = False
        if(event.keysym == "a"):
            self.left1 = False

    #Pohyb objektů
    def move(self):
        if(self.up):
            if(self.ship.y + self.ship.width < 0):
                self.ship.y = self.height
            self.ship.y -=self.speed
        if(self.down):
            if(self.ship.y > self.height):
                self.ship.y = -self.ship.height
            self.ship.y +=self.speed
        if(self.left):
            if(self.ship.x + self.ship.width < 0):
                self.ship.x = self.width
            self.ship.x -=self.speed
        if(self.right):
            if(self.ship.x >self.width):
                self.ship.x = -self.ship.width
            self.ship.x +=self.speed
        if(self.up1):
            if(self.ship1.y + self.ship.height < 0):
                self.ship1.y = self.height
            self.ship1.y -=self.speed
        if(self.down1):
            if(self.ship1.y > self.height):
                self.ship1.y = -self.ship.height
            self.ship1.y +=self.speed
        if(self.left1):
            if(self.ship1.x + self.ship.width < 0):
                self.ship1.x = self.width
            self.ship1.x -=self.speed
        if(self.right1):
            if(self.ship1.x >self.width):
                self.ship1.x = -self.ship.width
            self.ship1.x +=self.speed
        if(self.shot):
            if(self.sdirection=="up"):
                self.shot.y -= self.speed*3
            if(self.sdirection=="down"):
                self.shot.y += self.speed*3
            if(self.sdirection=="left"):
                self.shot.x -= self.speed*3
            if(self.sdirection=="right"):
                self.shot.x += self.speed*3
        if(self.shot1):
            if(self.sdirection1=="up"):
                self.shot1.y -= self.speed*3
            if(self.sdirection1=="down"):
                self.shot1.y += self.speed*3
            if(self.sdirection1=="left"):
                self.shot1.x -= self.speed*3
            if(self.sdirection1=="right"):
                self.shot1.x += self.speed*3
        self.redraw_canvas()
        
        

myapp = MyApp(root)
root.mainloop()