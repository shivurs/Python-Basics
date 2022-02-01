from turtle import *

colormode(255)
delay(0)
right(90)

def draw_picture(filename, size = 10):
    pensize(size)
    file = open(filename, 'r')

    for line in file:
        line = line.strip('\n')
        line = line.replace(')', ',').replace('(', ',').replace(' ', '')
        color_vals = line.split(',')
        reposition_next(size)
        for idx in range(len(color_vals)):
            if color_vals[idx] == '' and idx < (len(color_vals) - 1):
                r = int(color_vals[idx + 1])
                g = int(color_vals[idx + 2])
                b = int(color_vals[idx + 3])
                pencolor(r, g, b)
                forward(size)
    file.close()   

def reposition_next(size):
    penup()
    sety(size)
    left(180)
    forward(size)
    right(90)
    forward(size)
    right(90)
    pendown()

#filename = 'C:/Users/siobh/Desktop/Coding Practice/PCL-Stutt/rainbow.txt'
#draw_picture(filename, 15)