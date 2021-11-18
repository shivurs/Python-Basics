from turtle import *
import turtle

def draw_square():
    i = 0
    while i < 4:
        forward(30)
        right(90)
        i +=1

def draw_column(height):
    draw_square()
    i = 1
    while i < height:
        penup()
        right(90)
        forward(30)
        pendown()
        left(90)
        draw_square()
        i += 1

def draw_pyramid_r():
    height = 9
    reposition = 210
    while height > 0:
        draw_column(height)
        penup()
        forward(30)
        left(90)
        forward(reposition)
        right(90)
        pendown()
        height -= 2
        reposition = ((height - 2)*30)


draw_pyramid_r()
input()
