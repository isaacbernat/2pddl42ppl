import thumby
import time
import math
import random


SCREEN_WIDTH = thumby.display.width
SCREEN_HEIGHT = thumby.display.height
class Stats:
    def __init__(self, menu):
        self.wall_bounces = 0
        self.paddle_bounces = 0
        self.start_time = time.ticks_ms()
        self.winner = None
        self.menu = menu


class Paddle:
    WIDTH = 1
    HEIGHT = 8
    SPEED = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = self.HEIGHT
        self.width = self.WIDTH
        self.direction = 0  # -1 for up, 0 for stationary, 1 for down

    def update(self, menu_selection=None):
        self.y += self.direction * self.SPEED

        # Keep paddle within screen bounds
        if self.y < 0:
            self.y = 0
        elif self.y + self.length > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.length

    def draw(self):
        thumby.display.drawFilledRectangle(self.x, int(self.y), self.width, self.length, 1)


class Wall:
    def __init__(self):
        self.length = 0

    def update(self, menu_selection=None):
        pass

    def draw(self):
        if self.length > 0:
            thumby.display.drawFilledRectangle(SCREEN_WIDTH - 1, 0, 1, self.length, 1)


class Ball:
    SIZE, SPEED, SOUND = 1, 1, 100

    def __init__(self):
        self.x = None
        self.y = SCREEN_HEIGHT / 2.0
        self.speed = self.SPEED
        self.set_random_direction()
        self.last_bounce = 0

    def set_random_direction(self):
        # Random angle between -45 and 45 degrees, avoiding too horizontal angles
        angle = random.uniform(math.pi/8, math.pi/4)
        if random.choice([True, False]):
            angle = -angle
        direction = random.choice([-1, 1])
        
        self.x = SCREEN_WIDTH - self.SIZE - 2 if direction == -1 else self.SIZE + 1
        self.dx = direction * self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)

    def update(self, menu_selection, paddle_bounce=False, wall_bounce=False):
        self.x += self.dx
        self.y += self.dy

        def handle_bounce(bounce_type, pitch):
            current_time = time.ticks_ms()
            if current_time - self.last_bounce > 100:
                if bounce_type == "p":
                    stats.paddle_bounces += 1
                elif bounce_type == "w":
                    stats.wall_bounces += 1
                thumby.audio.play(pitch, self.SOUND)
                self.last_bounce = current_time

        if self.x <= Paddle.WIDTH and self.y <= paddle1.y + paddle1.length and paddle1.y <= self.y + self.SIZE:
            paddle_bounce = True
        elif menu_selection == 0:  # coop
            if (Paddle.WIDTH <= self.x <= Paddle.WIDTH * 2) and self.y <= paddle2.y + paddle2.length and paddle2.y <= self.y + self.SIZE:
                paddle_bounce = True
        elif (self.x + self.SIZE >= SCREEN_WIDTH - Paddle.WIDTH) and self.y <= paddle2.y + paddle2.length and paddle2.y <= self.y + self.SIZE:
            paddle_bounce = True
        if paddle_bounce:
            self.dx = -self.dx
            handle_bounce("p", 7458)
            return
        
        if wall.length > 0 and self.x >= SCREEN_WIDTH - 1 - self.SIZE:
            self.dx = -self.dx
            wall_bounce = True
        elif self.y <= 1 or self.y >= SCREEN_HEIGHT - self.SIZE:
            self.dy = -self.dy
            wall_bounce = True
        if wall_bounce:
            handle_bounce("w", 7902)
            return

        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            stats.winner = "Game over" if self.x <= 0 else "Player1 wins"
            self.dx = 0

    def draw(self):
        thumby.display.drawFilledRectangle(int(self.x), int(self.y), self.SIZE, self.SIZE, 1)


def handle_input(paddle1, paddle2):
    if thumby.buttonU.pressed():
        paddle1.direction = -1
    elif thumby.buttonD.pressed():
        paddle1.direction = 1
    else:
        paddle1.direction = 0

    if thumby.buttonA.pressed():
        paddle2.direction = -1
    elif thumby.buttonB.pressed():
        paddle2.direction = 1
    else:
        paddle2.direction = 0


def update_and_draw(objects, menu_selection):
    thumby.display.fill(0)
    # Draw fixed horizontal walls
    thumby.display.drawLine(0, 0, SCREEN_WIDTH - 1, 0, 1)
    thumby.display.drawLine(0, SCREEN_HEIGHT -1, SCREEN_WIDTH - 1, SCREEN_HEIGHT -1, 1)
    
    for o in objects:
        o.update(menu_selection)
        o.draw()
    thumby.display.update()


def display_winner(stats, menu_selection):
    thumby.display.fill(0)
    thumby.display.drawText(f"{stats.winner}!", 0, 0, 1)
    thumby.display.drawText(f"{int((time.ticks_ms() - stats.start_time)/1000)} seconds", 0, 8, 1)
    thumby.display.drawText(f"{stats.wall_bounces} wall bounces", 0, 16, 1)
    thumby.display.drawText(f"{stats.paddle_bounces} paddle bounces", 0, 24, 1)
    thumby.display.drawText("Press Right ->", 0, 32, 1)
    thumby.display.update()
    time.sleep(1)

    while True:
        if (thumby.buttonR.pressed()):
            return menu_selection
        elif (thumby.buttonL.pressed()):
            return -1
        time.sleep(0.1)


def display_menu(selected=0):
    options = ["Coop", "Versus", "Solo", "Settings"]

    while True:
        thumby.display.fill(0)
        thumby.display.drawText("2pddl 4 2ppl", 0, 0, 1)
        for i, option in enumerate(options):
            if i == selected:
                thumby.display.drawFilledRectangle(0, 8 + i * 8, len(option) * 6, 8, 1)
                thumby.display.drawText(option, 0, 8 + i * 8, 0)
            else:
                thumby.display.drawText(option, 0, 8 + i * 8, 1)
        thumby.display.update()
        
        if thumby.buttonU.justPressed():
            selected = (selected - 1) % len(options)
        elif thumby.buttonD.justPressed():
            selected = (selected + 1) % len(options)
        elif thumby.buttonA.justPressed() or thumby.buttonR.justPressed():
            return selected
        time.sleep(0.1)


def restart_game(menu_selection):
    paddle1 = Paddle(0, SCREEN_HEIGHT // 2 - Paddle.HEIGHT // 2)
    paddle2 = Paddle(SCREEN_WIDTH - Paddle.WIDTH - 1, SCREEN_HEIGHT // 2 - Paddle.HEIGHT // 2)
    wall = Wall()
    if menu_selection == 0:  # Coop
        paddle2.x = paddle1.x + 1
        paddle1.y = 0
        paddle2.y = SCREEN_HEIGHT - paddle2.length
        wall.length = SCREEN_HEIGHT
    elif menu_selection == 1:  # Versus
        wall.length = 0
    elif menu_selection == 2:  # Solo
        paddle2.length = 0
        wall.length = SCREEN_HEIGHT
    return paddle1, paddle2, Ball(), wall, Stats(menu_selection)


def display_settings(selected=0, start_index=0):
    settings = [
        ["Ball Speed", Ball.SPEED, 0.2, 3.0, 0.2],
        ["Ball Size", Ball.SIZE, 1, 10, 1],
        ["Paddle Height", Paddle.HEIGHT, 2, 40, 2],
        ["Paddle Speed", Paddle.SPEED, 0.2, 2.0, 0.2],
        ["Sound Duration", Ball.SOUND, 0, 500, 50],
    ]
    while True:
        thumby.display.fill(0)
        thumby.display.drawText("Settings", 0, 0, 1)
        for i in range(3):  # screen can display max 5 lines of text
            index = start_index + i
            if index < len(settings):
                name, value, _, _, _ = settings[index]
                if index == selected:
                    thumby.display.drawFilledRectangle(0, 8 + i * 8, len(name) * 6 + 24, 8, 1)
                    thumby.display.drawText(f"{name}: {value:.1f}", 0, 8 + i * 8, 0)
                else:
                    thumby.display.drawText(f"{name}: {value:.1f}", 0, 8 + i * 8, 1)
        if selected == len(settings):
            thumby.display.drawFilledRectangle(0, 32, 24, 8, 1)
            thumby.display.drawText("Back", 0, 32, 0)
        else:
            thumby.display.drawText("Back", 0, 32, 1)
        thumby.display.update()
        
        if thumby.buttonU.justPressed():
            if selected > 0:
                selected -= 1
                if selected < start_index:
                    start_index = selected
            else:
                selected = len(settings)
                start_index = max(0, len(settings) - 3)
        elif thumby.buttonD.justPressed():
            if selected < len(settings):
                selected += 1
                if selected >= start_index + 3:
                    start_index = selected - 2
            else:
                selected = 0
                start_index = 0
        elif selected != len(settings) and (thumby.buttonA.justPressed() or thumby.buttonR.justPressed()):
            adjust_setting(settings[selected])
        elif thumby.buttonL.justPressed() or thumby.buttonA.justPressed() or thumby.buttonR.justPressed():
            return settings
        time.sleep(0.1)


def adjust_setting(setting):
    name, value, min_val, max_val, step = setting
    
    while True:
        thumby.display.fill(0)
        thumby.display.drawText(name, 0, 0, 1)
        thumby.display.drawText(f"Value: {value:.1f}", 0, 16, 1)
        thumby.display.drawText("Back", 0, 32, 1)
        thumby.display.update()
        
        if thumby.buttonD.justPressed():
            value = max(min_val, value - step)
        elif thumby.buttonU.justPressed():
            value = min(max_val, value + step)
        elif thumby.buttonA.justPressed() or thumby.buttonR.justPressed() or thumby.buttonL.justPressed():
            setting[1] = value
            return
        time.sleep(0.05)


thumby.display.setFPS(60)
menu_selection = -1

while True:
    if menu_selection == -1:
        menu_selection = display_menu()
        paddle1, paddle2, ball, wall, stats = restart_game(menu_selection)
        stats.winner = "Good luck!    "
    elif stats.winner:
        if menu_selection == 3:  # Settings
            new_settings = display_settings()
            Ball.SPEED = new_settings[0][1]
            Ball.SIZE = new_settings[1][1]
            Paddle.HEIGHT = int(new_settings[2][1])
            Paddle.SPEED = new_settings[3][1]
            Ball.SOUND = new_settings[4][1]
            menu_selection = -1
        menu_selection = display_winner(stats, menu_selection)
        paddle1, paddle2, ball, wall, stats = restart_game(menu_selection)
    else:
        handle_input(paddle1, paddle2)
        update_and_draw({paddle1, paddle2, ball, wall}, menu_selection)

# TODO more complex settings (e.g. more balls)
# TODO change angle based on paddle bounce position (also on settings)
