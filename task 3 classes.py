import turtle as t
from math import sqrt
from turtle import TurtleScreen, onclick, ondrag

class NoasTurtle(t.Turtle):

    def circle(self, radius, center):
        self.penup()
        self.goto(center)
        self.setheading(90)
        self.right(90)
        self.forward(radius)
        self.left(90)
        self.pendown()
        super().circle(radius)  
        self.penup()
        self.left(90)
        self.forward(radius)
        self.right(90)
        self.pendown()

    def square(self, size, center):
        self.penup()
        self.goto(center)
        self.setheading(0)
        self.forward(size/2)
        self.right(90)
        self.pendown()
        self.forward(size/2)
        self.right(90)
        self.forward(size)
        self.right(90)
        self.forward(size)
        self.right(90)
        self.forward(size)
        self.right(90)
        self.forward(size/2)
        self.penup()

    def kmk(self, size, center):
        while size > 10:
            self.square(size, center)
            self.circle(size/2, center)
            size = size/sqrt(2)


santa = NoasTurtle()
santa.speed(0)
t.bgcolor("darkred")
santa.width(3)
santa.color("darkgreen")
#NoasTurtle.register_shape("santa.gif", "santa.gif")
#santa.shape(santa.gif)

santa.kmk(500, (0, 0))
#noa.square(onclick(), ondrag())
#noa.kmk(t.ondrag(None), t.onscreenclick(None))
t.exitonclick()