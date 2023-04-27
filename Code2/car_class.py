# Create the Car class
# Import Packages
import pygame
import numpy as np
# Import Functions
from Code2.game_class import Game
from Code2.Functions import GearFunctions, ImportFunctions


# Define the Car class
class Car:
    # Define Car Variables
    MASS = 1275.0  # vehicle mass kg
    DRAGCOEFF = 0.45
    FRONTAREA = 0.1257 * 0.1613  # ms^2

    # Initialise at Idle - Gear = 1

    # Define Sound File where sounds are found
    s = 'sound_files'

    # Graph Data
    velocity_history = []
    velocity_time = []
    throttle_history = []

    def __init__(self, x, y, width, height):
        # Physics
        self.x = x
        self.y = y
        self.displacement = 0.0  # m
        self.velocity = 0.0  # m/s
        self.acceleration = 0.0  # m/s^2
        self.throttle = 0.0  # between 0 = 0%, 1 = 100%
        self.force_thrust = 0.0  # N
        self.force_drag = 0.0  # N
        self.force_net = 0.0  # N
        self.rpm = 1000 # rpm
        self.gear = 1

        # Visualisation
        self.width = width
        self.height = height
        self.color = (255, 255, 255)

    def update(self, graphdata):
        # Store previous throttle and velocity
        lastthrottle = self.throttle
        lastvelocity = self.velocity

        # Calculate thrust Force
        self.force_thrust = self.throttle * ImportFunctions.import_p_curve(self.velocity, Car.MASS)

        # Calculate drag force
        rolling_resistance = 0.27 * self.velocity  # estimate
        self.force_drag = rolling_resistance + 0.5 * Game.AIRDENSITY * Car.DRAGCOEFF * Car.FRONTAREA * self.velocity ** 2

        # Calculate acceleration
        self.force_net = self.force_thrust - self.force_drag
        self.acceleration = self.force_net / Car.MASS

        # Update velocity
        self.velocity += self.acceleration / Game.FPS
        if self.velocity < 0:
            self.velocity = 0

        # Store the current velocity
        Car.velocity_history.append(self.velocity * 2.23694)
        Car.velocity_time.append(pygame.time.get_ticks() / 1000)
        Car.throttle_history.append(self.throttle)

        # Send to gear comparison
        positions = np.array([[lastthrottle * 100, lastvelocity * 1.6], [self.throttle * 100, self.velocity * 1.6]])

        self.gear = GearFunctions.gear_change_check(positions, graphdata, self.gear)

        # Update position
        self.x += self.velocity * Game.FPS / 100
        self.displacement += self.velocity * Game.FPS

        # Check for boundary collision
        if self.x < 0:
            self.x = Game.WIDTH - self.width
        elif self.x > Game.WIDTH - self.width:
            self.x = 0

        # Update cube colour if constant velocity
        if self.force_drag + 0.01 >= abs(self.force_thrust):
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)
        if self.velocity < 0:
            self.force_drag *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        # Write Speed on cube
        # text = font.render(str(round(self.velocity, 2)), 1, (255, 255, 255))
        # screen.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))

        # Counter Row 1
        Row1 = 10
        # Add Throttle Counter
        text_throttle = font.render('Throttle: ' + str(round(self.throttle, 3)), 1, (255, 255, 255))
        screen.blit(text_throttle, (10, Row1))

        # Add Velocity Counter
        text_vel = font.render('Velocity (MPH): ' + str(round(self.velocity * 2.23694, 3)), 1, (255, 255, 255))
        screen.blit(text_vel, (Game.WIDTH / 3 + 10, Row1))

        # Add Acceleration Counter
        text_acc = font.render('Acceleration (m/s^2): ' + str(round(self.acceleration, 3)), 1, (255, 255, 255))
        screen.blit(text_acc, (2 * Game.WIDTH / 3 + 10, Row1))

        # Counter Row 2
        Row2 = 50
        # Add Thrust Counter
        text_thrust = font.render('Thrust (N): ' + str(round(self.force_thrust, 2)), 1, (255, 255, 255))
        screen.blit(text_thrust, (10, Row2))

        # Add Drag Counter
        text_drag = font.render('Drag (N): ' + str(round(self.force_drag, 2)), 1, (255, 255, 255))
        screen.blit(text_drag, (Game.WIDTH / 3 + 10, Row2))

        # Add Net Force Counter
        text_net = font.render('Net (N): ' + str(round(self.force_net, 2)), 1, (255, 255, 255))
        screen.blit(text_net, (2 * Game.WIDTH / 3 + 10, Row2))

        # Counter Row 3
        Row3 = 90
        # Add a Displacement Counter
        text_displacement = font.render('Distance (m): ' + str(round(self.displacement, 2)), 1, (255, 255, 255))
        screen.blit(text_displacement, (10, Row3))

        # Add a Time Counter
        text_time = font.render('Time (s): ' + str(round(pygame.time.get_ticks() / 1000, 2)), 1, (255, 255, 255))
        screen.blit(text_time, (Game.WIDTH / 3 + 10, Row3))

        # Add a Gear Counter
        text_gear = font.render('Gear: ' + str(self.gear), 1, (255, 255, 255))
        screen.blit(text_gear, (2 * Game.WIDTH / 3 + 10, Row3))
