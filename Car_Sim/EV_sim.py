import pygame
import math
import numpy as np
import matplotlib.pyplot as plt

# Define constants
WIDTH = 1000
HEIGHT = 500
FPS = 60
GRAVITY = 9.81
MASS = 1275.0 # vehicle mass kg
PI = 3.14159

# Define Functions
def P_curve(input_value): # EV Performance Curve
    
    input_value_mph = input_value*2.23694/1.000001658
    # This is a curve of x-axis speed in mph and y-axis max acceleration available in Gs
    # Performance curve with reduction gear:
    points = [(0, 0.53), (32.68, 0.513), (33.27, 0.5), (41, 0.4), (52.68, 0.3), (71.71, 0.2), (101, 0.1), (137, 0.0)]

    # Performance curve without reduction gear:
    #points = [(0, 0.247), (71.71, 0.2), (101, 0.1), (137, 0.0)]

    # Split the points into separate lists for x and y values
    x, y = zip(*points)

    # Fit a curve to the data
    coefficients = np.polyfit(x, y, 3)
    polynomial = np.poly1d(coefficients)

    # Check if the intercept is within the range of the x values
    if min(x) <= input_value_mph <= max(x):
        # Find the y-intercept and convert to thrust in N
        thrust = polynomial(input_value_mph)*9.81*MASS
        return thrust
    else:
        return None

# Initialise Joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define the cube class
class Cube:
    def __init__(self, x, y, width, height):
        # Physics
        self.x = x
        self.y = y
        self.displacement = 0.0 # m
        self.velocity = 0.0     # m/s
        self.acceleration = 0.0 # m/s^2
        self.throttle = 0.0     # between 0 = 0%, 1 = 100%
        self.force_thrust = 0.0 # N
        self.force_drag = 0.0   # N
        self.force_net = 0.0    # N

        # Graph Data
        self.velocity_history = []
        self.velocity_time = []

        # Visualisation
        self.width = width
        self.height = height
        self.color = (255, 255, 255)

    def update(self):

        # Calculate thrust Force
        self.force_thrust = self.throttle*P_curve(self.velocity)

        # Calculate drag force
        drag_coof = 0.45
        front_area = 0.1257*0.1613 # m^2
        air_density = 1.293 # kg/m^3
        rolling_resistance = 0.27*self.velocity # estimate
        self.force_drag = rolling_resistance + 0.5*air_density*drag_coof*front_area*self.velocity**2

        # Calculate acceleration
        self.force_net = self.force_thrust - self.force_drag
        self.acceleration = self.force_net/MASS

        # Update velocity
        self.velocity += self.acceleration/FPS

        # Store the current velocity
        self.velocity_history.append(self.velocity*2.23694)
        self.velocity_time.append(pygame.time.get_ticks()/1000)

        # Update position
        self.x += self.velocity*FPS/100
        self.displacement += self.velocity*FPS

        # Check for boundary collision
        if self.x < 0:
            self.x = WIDTH - self.width
        elif self.x > WIDTH - self.width:
            self.x = 0

        # Update cube colour if constant velocity
        if self.force_drag + 0.01 >= abs(self.force_thrust):
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)
        if self.velocity < 0:
            self.force_drag *= -1

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        # Write Speed on cube
        # text = font.render(str(round(self.velocity, 2)), 1, (255, 255, 255))
        # screen.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))

        #Counter Row 1
        Row1 = 10
        # Add Throttle Counter
        text_throttle = font.render('Throttle: ' + str(round(self.throttle, 3)), 1, (255, 255, 255))
        screen.blit(text_throttle, (10, Row1))

        # Add Velocity Counter
        text_vel = font.render('Velocity (MPH): ' + str(round(self.velocity*2.23694, 3)), 1, (255, 255, 255))
        screen.blit(text_vel, (WIDTH/2 - text_vel.get_width()/2, Row1))

        # Add Acceleration Counter
        text_acc = font.render('Acceleration (m/s^2): ' + str(round(self.acceleration, 3)), 1, (255, 255, 255))
        screen.blit(text_acc, (WIDTH - text_acc.get_width() - 10, Row1))
        

        #Counter Row 2
        Row2 = 50
        # Add Thrust Counter
        text_thrust = font.render('Thrust (N): ' + str(round(self.force_thrust, 2)), 1, (255, 255, 255))
        screen.blit(text_thrust, (10, Row2))

        # Add Drag Counter
        text_drag = font.render('Drag (N): ' + str(round(self.force_drag, 2)), 1, (255, 255, 255))
        screen.blit(text_drag, (WIDTH/2 - text_drag.get_width()/2, Row2))

        # Add Net Force Counter
        text_net = font.render('Net (N): ' + str(round(self.force_net, 2)), 1, (255, 255, 255))
        screen.blit(text_net, (WIDTH - text_net.get_width() - 10, Row2))

        #Counter Row 2
        Row3 = 90
        # Add a Displacement Counter
        text_displacement = font.render('Distance (m): ' + str(round(self.displacement, 2)), 1, (255, 255, 255))
        screen.blit(text_displacement, (10, Row3))

        # Add a Time Counter
        text_time = font.render('Time (s): ' + str(round(pygame.time.get_ticks()/1000, 2)), 1, (255, 255, 255))
        screen.blit(text_time, (WIDTH/2 - text_time.get_width()/2, Row3))


# Create a cube object
cube = Cube(100, HEIGHT - 100, 50, 50)

# Define the main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                cube.throttle = event.value
        # elif event.type == pygame.KEYUP:
        #     if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
        #         cube.acceleration = 0.0

    # Update the cube
    cube.update()

    # Draw the cube
    screen.fill((0, 0, 0))
    cube.draw()

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Plot the velocity over time
plt.plot(cube.velocity_time, cube.velocity_history)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (MPH)')
plt.title('Velocity of the cube over time')
plt.savefig('velocity_plot.png')


# Quit pygame
pygame.quit()

plt.show()

# output vehicle velocity and throttle to other programs