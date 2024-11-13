import turtle
import math

start_coordinates=[(0,0),(-200,0),(-200,200),(0,200)]
turtle.colormode(255)
turtle.pencolor(75,20,150)
turtle.speed(0)
i = 1

for step in start_coordinates:
    turtle.penup()
    turtle.setpos((0,0))
    if i == 2:
       turtle.pencolor(20,72,130)
    elif i == 3:
       turtle.pencolor(55,20,110)
    elif i == 4:
       turtle.pencolor(20,55,90)
    turtle.setpos(step)
    turtle.setheading(0)
    size = 200
    counter = 0.2
    while (size > 20):
        for step in range(4):
            turtle.pendown()
            turtle.forward(size)
            turtle.right(90)
        turtle.forward(counter*size)
        turtle.right(counter*90)
        size = size-counter*size
    i = i+1

turtle.penup()    
turtle.setpos((0,0))
turtle.exitonclick()


#question: can i tell the turtle to continue drawing until she meets a line?