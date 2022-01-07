import turtle

WIDTH, HEIGHT = 800, 600
SPEED = 10
screen = turtle.getscreen()
screen.title("monetmaker")
screen.setup(WIDTH, HEIGHT)

screen.addshape("images/lion_edge.png")
turtle.pen({"pensize":5,"fillcolor":"red","speed":100,"shown":False})


turtle.penup()
turtle.goto(-WIDTH/2,0)
turtle.pendown()
for a in range(WIDTH):
    turtle.forward(SPEED)
turtle.mainloop()
