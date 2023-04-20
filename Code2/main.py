# Main file for the engine simulation
# Import packages
import pandas as pd
import pygame
import matplotlib.pyplot as plt
import sounddevice as sd
# Import Classes
from Code2.checkfiles  import check_files
from Code2.game_class import Game
from Code2.car_class import Car
from Code2.Functions import ImportFunctions, GearFunctions


# Define the input files and the gear change data
input_files = ('sound_files/front_1000.wav',
               'sound_files/front_1500.wav',
               'sound_files/front_2000.wav',
               'sound_files/front_2500.wav',
               'sound_files/front_3000.wav'
               )

# Import Gear Change Data
gear_change_data = '2D_gear_change_profile.xlsx'

# Set the number of rpm sections
min_rpm = 1000
max_rpm = 10000
rpm_sectioning = 5

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
clock = pygame.time.Clock()

# Initialise Joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# Initialise the Pygame Audio Module
pygame.mixer.init()

# Block Write Method
# Check if the files exist for engine running
file_checkers = check_files(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning)

# Set Up the engine
print('\nSet Up Engine')

ulines_dir, dlines_dir = ImportFunctions.import_gear_change(gear_change_data)
graphdata = GearFunctions.gear_change_graph(ulines_dir, dlines_dir)

# Run the engine
print('\nRunning Engine')

# Create a Car object
car = Car(100, Game.HEIGHT - 100, 50, 50)

print('Playing')

prev_rpm = 0

# Define the main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                car.throttle = event.value
        # elif event.type == pygame.KEYUP:
        #   if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
        #       cube.acceleration = 0.0

    # Update the Car
    car.update(graphdata)

    # Draw the Car
    screen.fill((0, 0, 0))
    car.draw(screen)

    # Play the sounds
    if car.rpm != prev_rpm:
        pygame.mixer.music.load('sound_files/' + str(car.rpm) + '_sound.wav')
        pygame.mixer.music.play(-1)
    print(car.rpm)

    # Update the screen
    pygame.display.flip()
    clock.tick(Game.FPS)
    prev_rpm = car.rpm

# Plot the velocity over time
plt.plot(Car.velocity_time, Car.throttle_history)
plt.xlabel('Time (s)')
plt.ylabel('Throttle (%)')
plt.title('Velocity of the cube over time')
plt.savefig('velocity_plot.png')

# Quit pygame
pygame.quit()

plt.show()

# output vehicle velocity and throttle to other programs
