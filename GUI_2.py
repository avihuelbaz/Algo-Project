#!/usr/bin/env python
# coding: utf-8

# In[1]:


#סופי







# Import module
from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox as mb

from robot_stg_1 import *
from stg_2_robot import *
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox as mb
from prepare_data import *

df = pd.read_csv('csv/snp_2009_2020_with_spy_with_tema.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['dt'] = pd.to_datetime(df['Date'])
df = df[df['Name'] != 'MOS']
def sel():
   if (var.get()) == 1:
       selection = "You selected the stg_1 " + " And you buy for $  " + str(var2.get())
       buy_stg_1(var2.get(),df)
       mb.showinfo('my choice', selection)
   if (var.get()) == 2:
       buy_stg_2(var2.get())
       selection = "You selected the stg_2 " + " And you buy for $  " + str(var2.get())
       mb.showinfo('my choice', selection)


root = Tk() 
root.minsize(700,350)
root.title('AlgoTrade_Israel')
  
# Add image file
bg =ImageTk.PhotoImage(Image.open('14.JPG'))
  
# Create Canvas
canvas1 = Canvas( root, width = 400,
                 height = 333)
  
canvas1.pack(fill = "both", expand = True)
  
# Display image
canvas1.create_image( 0, 0, image = bg,anchor = "nw")
  
canvas1.create_text( 500, 30, text = "ברוכים הבאים",fill="white",font=('arial bold',40))
canvas1.create_text( 500, 75, text = ":בחר שיטת השקעה",fill="white",font=('arial bold',16))
canvas1.create_text( 500, 160, text = "($) ?כמה כסף תרצה להשקיע",fill="white",font=('arial bold',16))
var = IntVar()
var2= IntVar()

R1 = Radiobutton(root, text="", variable=var, value=1,bg = "black")
R2 = Radiobutton(root, text="", variable=var, value=2,bg = "black")
L1 = Label(root, text="השקעה לטווח ארוך",bg = "black",fg= "white",font=('arial',12))
L2 = Label(root, text="Swing השקעת  ",bg = "black",fg= "white",font=('arial',12))


button1 = Button( root, text = "       לקנייה        ",command=sel,bg = "white")
my_textbox=Entry(root, textvariable=var2) 
canvas1.create_window( 615, 95, anchor = "nw", window = R1)

canvas1.create_window( 470, 95, anchor = "nw", window = R2)

canvas1.create_window( 495, 95, anchor = "nw", window = L1)

canvas1.create_window( 365, 95, anchor = "nw", window = L2)
  
canvas1.create_window( 440, 180,anchor = "nw",window = my_textbox)
  




canvas1.create_window( 460, 250,   anchor = "nw",  window = button1)
  
# Execute tkinter
root.mainloop()


# In[ ]:




