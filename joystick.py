import pygame


def joystick_init():
    # Initialize the joystick module and check number of Joysticks
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print(joysticks)


# Make game
class Player(object):

    def __init__(self):
        self.player = pygame.rect.Rect((300, 400, 50, 50))
        self.color = "white"

    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed, y_speed))

    def change_color(self, color):
        self.color = color

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)


def joystick_check():

    # Import Glabal Variables
    global voltage
    global speed
    # Initialize pygame
    pygame.init()

    player = Player()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    player.change_color("red")
                elif event.button == 1:
                    player.change_color("green")
                elif event.button == 2:
                    player.change_color("blue")
                elif event.button == 3:
                    player.change_color("yellow")
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    voltage = event.value * 10
                    print(voltage)
                elif event.axis == 4:
                    speed = event.value * 140
                    print(speed)

        screen.fill((0, 0, 0))
        player.draw(screen)
        pygame.display.update()

        clock.tick(180)