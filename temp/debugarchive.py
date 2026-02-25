import turtle as t
import random

t.title("Snake Game Classic: HNTech")
t.bgcolor("green")

#Variables
length = 3

coin = t.Turtle()
coin.shape("circle")
coin.penup()
coin.color("yellow")
coin.shapesize(2,2,2)

xpos = random.randint(-200,200)
ypos = random.randint(-200,200)

coin.setx(xpos)
coin.sety(ypos)

snake = t.Turtle()
snake.shape("square")
snake.color("blue")
snake.speed(1)
snake.penup()
snake.shapesize(1,length,1)


def right():
    orient = snake.heading()
    snake.hideturtle()
    if orient == 270:
        snake.right(270)
        snake.showturtle()
    elif orient == 180:
        snake.right(180)
        snake.showturtle()
    elif orient == 90:
        snake.right(90)
        snake.showturtle()

def left():
    orient = snake.heading()
    snake.hideturtle()
    if orient == 270:
        snake.right(90)
        snake.showturtle()
    elif orient == 0:
        snake.left(180)
        snake.showturtle()
    elif orient == 90:
        snake.left(90)
        snake.showturtle()

def up():
    orient = snake.heading()
    snake.hideturtle()
    if orient == 270:
        snake.right(180)
        snake.showturtle()
    elif orient == 0:
        snake.left(90)
        snake.showturtle()
    elif orient == 180:
        snake.right(90)
        snake.showturtle()

def down():
    orient = snake.heading()
    snake.hideturtle()
    if orient == 180:
        snake.left(90)
        snake.showturtle()
    elif orient == 0:
        snake.right(90)
        snake.showturtle()
    elif orient == 90:
        snake.left(180)
        snake.showturtle()
    
t.onkey(left,"Left")
t.onkey(right, "Right")
t.onkey(up, "Up")
t.onkey(down, "Down")

t.listen()

def randomcoin():
    coin.hideturtle()
    coin.setx(random.randint(-200,200))
    coin.sety(random.randint(-200,200))
    coin.showturtle()


while True:
    snake.forward(50)
    if snake.distance(coin)<40:
        randomcoin()
        length = length + 1
        snake.shapesize(1,length,1)




