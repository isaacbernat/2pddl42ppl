import time
import math
import random
import thumby as tb
from thumby import display as dp


class Stats:
    def __init__(self):
        self.wall_bounces = 0
        self.paddle_bounces = 0
        self.start_time = time.ticks_ms()
        self.winner = None


class Paddle:
    WIDTH, HEIGHT, SPEED = 1, dp.height//5, 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = self.HEIGHT
        self.width = self.WIDTH
        self.direction = 0  # -1 up, 0 still, 1 down

    def update(self, menu_selection=None):
        self.y += self.direction * self.SPEED
        self.y = max(self.y, 0)
        self.y = min(self.y, dp.height - self.length)

    def draw(self):
        dp.drawFilledRectangle(self.x, int(self.y), self.width, self.length, 1)


class Ball:
    SIZE, SPEED, AMOUNT, SOUND, BOUNCE_DYNAMIC_ANGLE, SIZE_REDUCTION_RATE = dp.height//5, 1, 1, 100, 1, 0.33

    def __init__(self, direction):
        self.y = dp.height / 2.0
        self.set_random_direction(direction)

    def set_random_direction(self, direction):
        angle = random.uniform(math.pi/8, math.pi/4) * random.choice([-1, 1])  # to debug corner bounce in Solo mode set to math.pi/11.5
        self.x = dp.width - int(self.SIZE) - 2 if direction == -1 else int(self.SIZE) + 1
        self.dx = direction * self.SPEED * math.cos(angle)
        self.dy = self.SPEED * math.sin(angle)

    def update(self, menu_selection, bounce=0):
        def handle_bounce(bounce_type, axis, paddle, pitch=0):
            if axis == 'x':
                if self.BOUNCE_DYNAMIC_ANGLE and paddle:
                    mid_ball, mid_pad = (self.y + self.SIZE/2), (paddle.y + paddle.length/2)
                    relative_position = (mid_pad - mid_ball) / (paddle.length / 2 + self.SIZE / 2)
                    new_angle = max(-1, min(1, relative_position)) * (math.pi / 2.25)
                    self.dx = self.SPEED * abs(math.cos(new_angle)) * (-1 if self.dx > 0 else 1)
                    self.dy = self.SPEED * abs(math.sin(new_angle)) * (-1 if new_angle > 0 else 1)
                else:
                    self.dx = -self.dx
            elif axis == 'y':
                self.dy = -self.dy

            if bounce_type == 1:  # paddle
                self.SIZE = max(1, self.SIZE - self.SIZE_REDUCTION_RATE)
                stats.paddle_bounces += 1
                pitch = 7458
            elif bounce_type == 2:  # wall
                stats.wall_bounces += 1
                pitch = 7902
            else:  # invalid bounce
                return 0
            tb.audio.play(freq=pitch, duration=self.SOUND)
            return bounce_type

        self.x += self.dx
        self.y += self.dy
        if self.dx < 0 and self.x <= Paddle.WIDTH and self.y <= paddle1.y + paddle1.length and paddle1.y <= self.y + self.SIZE:
            bounce = handle_bounce(1, 'x', paddle1)
        elif self.dx < 0 and menu_selection == 0 and (Paddle.WIDTH <= self.x <= Paddle.WIDTH * 2) and self.y <= paddle2.y + paddle2.length and paddle2.y <= self.y + self.SIZE:
            bounce = handle_bounce(1, 'x', paddle2)
        elif self.dx > 0 and menu_selection == 1 and (self.x + self.SIZE >= dp.width - Paddle.WIDTH) and self.y <= paddle2.y + paddle2.length and paddle2.y <= self.y + self.SIZE:
            bounce = handle_bounce(1, 'x', paddle2)
        elif self.dx > 0 and wall.length > 0 and self.x >= dp.width - 1 - self.SIZE:
            bounce = handle_bounce(2, 'x', None)
        if (self.dy < 0 and self.y <= 1) or (self.dy > 0 and self.y >= dp.height - self.SIZE):
            bounce = handle_bounce(2, 'y', None)
        if bounce == 0 and (self.x + self.SIZE <= 0 or self.x >= dp.width):
            stats.winner = "Game over" if self.x <= 0 else "Player1 wins"
            self.dx = 0

    def draw(self):
        dp.drawFilledRectangle(int(self.x), int(self.y), int(self.SIZE), int(self.SIZE), 1)


def handle_ingame_input(paddle1, paddle2):
    if tb.buttonU.pressed():  # paddle1
        paddle1.direction = -1
    elif tb.buttonD.pressed():
        paddle1.direction = 1
    else:
        paddle1.direction = 0
    if tb.buttonA.pressed():  # paddle2
        paddle2.direction = -1
    elif tb.buttonB.pressed():
        paddle2.direction = 1
    else:
        paddle2.direction = 0


def update_and_draw(objects, menu_selection):
    dp.fill(0)
    dp.drawLine(0, 0, dp.width - 1, 0, 1)  # Draw horizontal walls
    dp.drawLine(0, dp.height -1, dp.width - 1, dp.height -1, 1)
    for o in objects:
        o.update(menu_selection)
        o.draw()
    dp.update()


def dp_winner(stats, menu_selection):
    dp.fill(0)
    dp.drawText(f"{stats.winner}!", 0, 0, 1)
    dp.drawText(f"{int((time.ticks_ms() - stats.start_time)/1000)} seconds", 0, 8, 1)
    dp.drawText(f"{stats.wall_bounces} wall bounces", 0, 16, 1)
    dp.drawText(f"{stats.paddle_bounces} paddle bounces", 0, 24, 1)
    dp.drawText("Press Right ->", 0, 32, 1)
    dp.update()

    while True:
        if (tb.buttonR.pressed()):
            return menu_selection
        elif (tb.buttonL.pressed()):
            return -1


def dp_menu(selected=0, options=["Coop", "Versus", "Solo", "Settings"]):
    while True:
        dp.fill(0)
        dp.drawText("2pddl 4 2ppl", 0, 0, 1)
        for i, option in enumerate(options):
            if i == selected:
                dp.drawFilledRectangle(0, 8 + i * 8, len(option) * 6, 8, 1)
            dp.drawText(option, 0, 8 + i * 8, int(i != selected))
        dp.update()
        
        if tb.buttonU.justPressed():
            selected = (selected - 1) % len(options)
        elif tb.buttonD.justPressed():
            selected = (selected + 1) % len(options)
        elif tb.buttonA.justPressed() or tb.buttonR.justPressed():
            return selected


def restart_game(menu_selection, start_direction_choices=[1]):
    paddle1 = Paddle(0, dp.height // 2 - Paddle.HEIGHT // 2)
    paddle2 = Paddle(dp.width - Paddle.WIDTH, dp.height // 2 - Paddle.HEIGHT // 2)
    wall = Paddle(dp.width - Paddle.WIDTH, 0)
    if menu_selection == 0:  # Coop
        paddle2.x = paddle1.x + 1
        paddle1.y = 0
        paddle2.y = dp.height - paddle2.length
        wall.length = dp.height
    elif menu_selection == 1:  # Versus
        wall.length = 0
        start_direction_choices = [-1, 1]
    elif menu_selection == 2:  # Solo
        paddle2.length = 0
        wall.length = dp.height
    balls = [Ball(direction=random.choice(start_direction_choices)) for _ in range(Ball.AMOUNT)]
    return paddle1, paddle2, balls, wall, Stats()


def dp_settings(selected=0, start_index=0):
    settings = [  # name, value, min_val, max_val, step
        ["Ball Speed", Ball.SPEED, 0.2, 5.0, 0.2],
        ["Ball Size", Ball.SIZE, 1, 50, 1],
        ["Paddle Height", Paddle.HEIGHT, 2, 40, 2],
        ["Paddle Speed", Paddle.SPEED, 0.2, 2.0, 0.2],
        ["Sound Duration", Ball.SOUND, int(0), 500, 50],
        ["Ball Amount", Ball.AMOUNT, 1, 20, 1],
        ["Bounce Angle", Ball.BOUNCE_DYNAMIC_ANGLE, 0, 1, 1],
        ["Ball reduction rate", Ball.SIZE_REDUCTION_RATE, 0, 2, 0.1],
    ]
    while True:
        dp.fill(0)
        dp.drawText("Settings", 0, 0, 1)
        for i in range(3):  # screen can show max 5 lines of text
            index = start_index + i
            if index < len(settings):
                name, value, _, _, _ = settings[index]
                if index == selected:
                    dp.drawFilledRectangle(0, 8 + i * 8, len(name) * 6 + 24, 8, 1)
                dp.drawText(f"{name}: {value:.1f}", 0, 8 + i * 8, int(index != selected))
        if selected == len(settings):
            dp.drawFilledRectangle(0, 32, 24, 8, 1)
        dp.drawText("Back = Left", 0, 32, selected != len(settings))
        dp.update()
        
        if tb.buttonU.justPressed():
            if selected > 0:
                selected -= 1
                if selected < start_index:
                    start_index = selected
            else:
                selected = len(settings)
                start_index = max(0, len(settings) - 3)
        elif tb.buttonD.justPressed():
            if selected < len(settings):
                selected += 1
                if selected >= start_index + 3:
                    start_index = selected - 2
            else:
                selected = 0
                start_index = 0
        elif selected != len(settings) and (tb.buttonA.justPressed() or tb.buttonR.justPressed()):
            adjust_setting(settings[selected])
        elif tb.buttonL.justPressed() or tb.buttonA.justPressed() or tb.buttonR.justPressed():
            return settings


def adjust_setting(setting):
    name, value, min_val, max_val, step = setting
    while True:
        dp.fill(0)
        dp.drawText(name, 0, 0, 1)
        dp.drawText(f"Value: {value:.1f}", 0, 16, 1)
        dp.drawText("Left = Back", 0, 32, 1)
        dp.update()
        
        if tb.buttonD.justPressed():
            value = max(min_val, value - step)
        elif tb.buttonU.justPressed():
            value = min(max_val, value + step)
        elif tb.buttonA.justPressed() or tb.buttonR.justPressed() or tb.buttonL.justPressed():
            setting[1] = value
            return


dp.setFPS(60)
menu_selection = -1

while True:
    if menu_selection == -1:
        menu_selection = dp_menu()
        paddle1, paddle2, balls, wall, stats = restart_game(menu_selection)
        stats.winner = "Good luck!    "
    elif stats.winner:
        if menu_selection == 3:  # Settings
            new_settings = dp_settings()
            Ball.SPEED = new_settings[0][1]
            Ball.SIZE = new_settings[1][1]
            Paddle.HEIGHT = int(new_settings[2][1])
            Paddle.SPEED = new_settings[3][1]
            Ball.SOUND = new_settings[4][1]
            Ball.AMOUNT = new_settings[5][1]
            Ball.BOUNCE_DYNAMIC_ANGLE = new_settings[6][1]
            Ball.SIZE_REDUCTION_RATE = new_settings[7][1]
            menu_selection = -1
        menu_selection = dp_winner(stats, menu_selection)
        paddle1, paddle2, balls, wall, stats = restart_game(menu_selection)
    else:
        handle_ingame_input(paddle1, paddle2)
        update_and_draw([paddle1, paddle2, wall] + balls, menu_selection)

# TODO balls accelerate on X bounces
