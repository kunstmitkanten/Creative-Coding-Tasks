import turtle
from math import sqrt

stack = []
 
def square(size):
    turtle.pendown()
    for _ in range(4):
     turtle.forward(size)
     turtle.right(90)


def recursion(startsize):
    square(startsize)                           #draw square
    stack.append(startsize)
    turtle.forward(startsize/2)
    turtle.right(45)                            #next starting position
    if startsize <= 10:
        circle()
        return
    else:
        smallersize = startsize /sqrt(2)        #calculate half of the diameter
        recursion(smallersize)

def circle():
   for i in range(len(stack)):
      turtle.penup()
      turtle.setpos(0,0)
      turtle.setheading(270)
      turtle.forward(stack[i]/2)
      turtle.pendown()
      turtle.circle(stack[i]/2)                 

# after a loot of trying now i need to stop because it is late :D
# but originally i wanted the circles to layer over the squares
# i tried long to let the circles liek bounce back when the turtle reaches the middle,
# but it was not that easy because the circle always starts in a certian corner and the
# squares are twisting all the time...
# with more time i gues i could have come to a solution but for now these recursions
# and patterns need to be enough :)

turtle.speed(6)
recursion(300)

turtle.exitonclick()