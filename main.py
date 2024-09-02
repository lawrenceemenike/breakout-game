import turtle
import random

# Set up the screen
screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Paddle movement functions
def paddle_left():
    x = paddle.xcor()
    if x > -350:
        x -= 20
        paddle.setx(x)

def paddle_right():
    x = paddle.xcor()
    if x < 350:
        paddle.setx(x + 20)

# Keyboard bindings
screen.listen()
screen.onkeypress(paddle_left, "Left")
screen.onkeypress(paddle_right, "Right")

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1  # Start with a slower speed
ball.dy = -1

# Brick wall
bricks = []
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

for i in range(len(colors)):  # Adjusted loop to match the length of colors
    for j in range(5):
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.color(colors[i])
        brick.shapesize(stretch_wid=1, stretch_len=2)
        brick.penup()
        brick.goto(-350 + (i * 70), 250 - (j * 30))
        bricks.append(brick)

# Score
score = 0
misses = 0

# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Score: 0  Misses: 0", align="center", font=("Courier", 24, "normal"))

def update_score():
    global score
    score += 1
    score_display.clear()
    score_display.write(f"Score: {score}  Misses: {misses}", align="center", font=("Courier", 24, "normal"))

def update_misses():
    global misses
    misses += 1
    score_display.clear()
    score_display.write(f"Score: {score}  Misses: {misses}", align="center", font=("Courier", 24, "normal"))
    if misses >= 3:
        end_game()

def end_game():
    global score, misses
    ball.goto(0, 0)
    ball.dx = 0
    ball.dy = 0
    score_display.goto(0, 0)
    score_display.write("Game Over", align="center", font=("Courier", 36, "normal"))
    screen.update()
    turtle.ontimer(restart_game, 3000)

def restart_game():
    global score, misses
    score = 0
    misses = 0
    ball.goto(0, 0)
    ball.dx = 1  # Reset to initial slower speed
    ball.dy = -1
    score_display.goto(0, 260)
    score_display.clear()
    score_display.write(f"Score: {score}  Misses: {misses}", align="center", font=("Courier", 24, "normal"))
    for brick in bricks:
        brick.showturtle()

def increase_ball_speed():
    ball.dx *= 1.1
    ball.dy *= 1.1

# Increase ball speed every 10 seconds
turtle.ontimer(increase_ball_speed, 10000)

# Game loop
while True:
    screen.update()
    
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    
    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    
    if ball.ycor() < -290:
        ball.goto(0, 0)
        ball.dy *= -1
        update_misses()
    
    if ball.xcor() > 390:
        ball.setx(390)
        ball.dx *= -1
    
    if ball.xcor() < -390:
        ball.setx(-390)
        ball.dx *= -1
    
    # Paddle and ball collision
    if ball.ycor() < -240 and ball.ycor() > -250 and ball.xcor() < paddle.xcor() + 40 and ball.xcor() > paddle.xcor() - 40:
        ball.sety(-240)
        ball.dy *= -1

    # Check for collisions with bricks
    for brick in bricks:
        if brick.isvisible():
            if ball.xcor() > brick.xcor() - 40 and ball.xcor() < brick.xcor() + 40 and ball.ycor() > brick.ycor() - 20 and ball.ycor() < brick.ycor() + 20:
                ball.dy *= -1
                brick.hideturtle()
                update_score()

    # Check if all bricks are hit
    if all(not brick.isvisible() for brick in bricks):
        ball.goto(0, 0)
        ball.dx = 0
        ball.dy = 0
        score_display.goto(0, 0)
        score_display.write("You Win!", align="center", font=("Courier", 36, "normal"))
        screen.update()
        turtle.ontimer(restart_game, 3000)