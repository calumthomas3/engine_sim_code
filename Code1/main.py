# Main file for the engine simulation
# Import packages
import pandas as pd
import pygame
import matplotlib.pyplot as plt
import sounddevice as sd
# Import Classes
from Code1.checkfiles import check_files
from Code1.game_class import Game
from Code1.car_class import Car
from Code1.Functions import ImportFunctions, GearFunctions
from Code1.gear_contour_plot import find_rpm


# Define the input files and the gear change data
input_files = ('sound_files/rear_1000.wav',
               'sound_files/rear_1500.wav',
               'sound_files/rear_2000.wav',
               'sound_files/rear_2500.wav',
               'sound_files/rear_3000.wav'
               )

# Import Gear Change Data
gear_change_data = '2D_gear_change_profile.xlsx'

# Set the number of rpm sections
min_rpm = 1000
max_rpm = 3000
rpm_sectioning = 5
maxspeed = 200 # kmph

# Define delay, responsiveness of the throttle and rpm
delay = 10

# Block Write Method
# Check if the files exist for engine running
file_checkers = check_files(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning)

# Set Up the engine
print('\nSet Up Engine')

# Import the RPM matrices
rpm_signals = {}
for i in range(len(file_checkers)):
    file_checker = file_checkers[i]
    rpm_signals[file_checker] = pd.read_csv(file_checker, header=None).values.flatten()

ulines_dir, dlines_dir = ImportFunctions.import_gear_change(gear_change_data)
rpm_planes, gear_planes = find_rpm(min_rpm, max_rpm, maxspeed, dlines_dir, ulines_dir)
graphdata = GearFunctions.gear_change_graph(ulines_dir, dlines_dir)

# Run the engine
print('\nRunning Engine')

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
clock = pygame.time.Clock()

# Initialise Joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# Initialise the Sound Stream
# Create an instance of the Stream class
block_size = 2048
stream = sd.OutputStream(channels=1, blocksize=block_size)

# Create a Car object
car = Car(100, Game.HEIGHT - 100, 50, 50)

# Start the stream
stream.start()

# Define prev_rpm for use in delay function
prev_rpm = min_rpm - 1

# Notify User
print('Playing')
print(rpm_signals)

# Define the idle loop
idle = True
while idle:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            idle = False
            drive = False
        elif event.type == pygame.JOYBUTTONDOWN:
            idle = False
            drive = True
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                car.throttle = (event.value + 1) / 2

    car.rpm = min_rpm + (max_rpm - min_rpm) * car.throttle
    car.rpm = round(car.rpm / rpm_sectioning) * rpm_sectioning
    # Update the sound stream
    # Write the signal to the stream in blocks
    prev_rpm = prev_rpm + (car.rpm - prev_rpm) / delay
    prev_rpm = round(prev_rpm / rpm_sectioning) * rpm_sectioning
    for i in range(0, len(rpm_signals['sound_files/front_' + str(prev_rpm) + '_signal.csv']), block_size):
        signal_block = rpm_signals['sound_files/front_' + str(prev_rpm) + '_signal.csv'][i:i + block_size]
        # Change type of signal_block to float32
        signal_block = signal_block.astype('float32')
        stream.write(signal_block)

    car.drawidle(screen)

    # Define Car rpm
    Game.FPS = prev_rpm / 480
    clock.tick(Game.FPS)

# Define the main loop
while drive:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drive = False
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

    # Update to new sound
    car.rpm = min_rpm + (max_rpm - min_rpm) * car.throttle
    car.rpm = round(car.rpm / rpm_sectioning) * rpm_sectioning
    # Update the sound stream
    # Write the signal to the stream in blocks
    prev_rpm = prev_rpm + (car.rpm - prev_rpm) / delay
    prev_rpm = round(prev_rpm / rpm_sectioning) * rpm_sectioning
    for i in range(0, len(rpm_signals['sound_files/front_' + str(prev_rpm) + '_signal.csv']), block_size):
        signal_block = rpm_signals['sound_files/front_' + str(prev_rpm) + '_signal.csv'][i:i + block_size]
        # Change type of signal_block to float32
        signal_block = signal_block.astype('float32')
        stream.write(signal_block)

    # Update the screen
    pygame.display.flip()
    clock.tick(Game.FPS)

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
