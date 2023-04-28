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
from Code2.gear_contour_plot import find_rpm


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
max_rpm = 3500
rpm_sectioning = 5
maxspeed = 200 # kmph

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
rpm_planes, gear_planes = find_rpm(min_rpm, max_rpm, maxspeed, dlines_dir, ulines_dir)
graphdata = GearFunctions.gear_change_graph(ulines_dir, dlines_dir)


# Run the engine
print('\nRunning Engine')

# Create a Car object
car = Car(100, Game.HEIGHT - 100, 50, 50)

print('Playing')

prev_rpm = min_rpm - 5

# Define the main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                car.throttle = (event.value + 1) / 2
        # elif event.type == pygame.KEYUP:
        #   if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
        #       cube.acceleration = 0.0

    # Update the Car

    car.update(graphdata)

    # Draw the Car
    screen.fill((0, 0, 0))
    car.draw(screen)

    # Find car gear
    gear_total = 0
    for gear_plane in gear_planes:
        gear_total += gear_planes[gear_plane][round(car.throttle * 100), round(car.velocity)]
    if gear_total == car.gear + 1:
        car.gear += 1
    if gear_total == car.gear - 1:
        car.gear -= 1

    # Find car rpm and round to nearest 5
    car.rpm = rpm_planes[str(int(car.gear)) + ' gear'][round(car.throttle * 100), round(car.velocity)]
    car.rpm = round(car.rpm / 5) * 5

    # Play the sounds
    print('sound_files/' + str(int(car.rpm)) + '_sound.wav')
    pygame.mixer.music.load('sound_files/' + str(int(car.rpm)) + '_sound.wav')
    pygame.mixer.music.play(-1)

    # Update the screen
    pygame.display.flip()
    Game.FPS = car.rpm/240
    clock.tick(Game.FPS)

# Quit pygame
pygame.quit()

plt.plot(Car.velocity_history, Car.throttle_history)
plt.xlabel('Velocity (kmph)')
plt.ylabel('Throttle (%)')
plt.title('Velocity of the cube over time')
plt.savefig('velocity_plot.png')

plt.show()

