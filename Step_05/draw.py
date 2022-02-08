import turtle


def draw(new_matrix: list, window: tuple, drawing_speed: int) -> None:
    screen = turtle.Screen()
    screen.title("monetmaker")
    screen.screensize(window[0], window[1])
    screen.colormode(255)
    pen = turtle.Turtle()
    pen.ht()
    screen.tracer(drawing_speed)
    image_width = new_matrix.shape[1]
    image_height = new_matrix.shape[0]
    for y in range(int(image_height/2), int(image_height/-2),  -1):
        pen.penup()
        pen.goto(-(image_width / 2), y)
        pen.pendown()
        for x in range(-int(image_width/2), int(image_width/2), 1):
            pix_width = int(x + (image_width/2))
            pix_height = int(image_height/2 - y)
            pen.color(new_matrix[pix_height, pix_width])
            pen.forward(1)
        screen.update()
    turtle.done()
    return
