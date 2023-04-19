import math
import sys, os
import pygame
import datetime

# Pygame Constants
from pygame.locals import *
from pygame.color import THECOLORS

class GameWindow:
    def __init__(self, screenpixelsize):
        self.width_px = screenpixelsize[0]
        self.height_px = screenpixelsize[1]

        # Create game surface
        self.surface = pygame.display.set_mode(screenpixelsize)

        # Define the pixel boundaries in Metres
        self.left_boundary_m = 0.0
        self.right_boundary_m = env.m_from_px(self.width_px)
        self.top_boundary_m = 0.0
        self.bottom_boundary_m = env.m_from_px(self.height_px)

        # Colour Screen Black
        self.erase_and_update()

    def update_caption(self, title):
        pygame.display.set_caption(title)
        self.caption = title

    def erase_and_update(self):
        self.surface.fill(THECOLORS["black"])
        pygame.display.flip()

class Object:
    def __init__(self, floor, colour=THECOLORS["white"], left_px=10, width_px=25, height_px=100, v_x_mps=1, v_y_mps=1):
        # Set Colour
        self.colour = colour

        # Set Size in Pixels
        self.height_px = height_px
        self.top_px = game_window.height_px - self.height_px
        self.width_px = width_px

        # Set Size in Metres
        self.width_m = env.m_from_px(width_px)
        self.halfwidth_m = self.width_m/2
        self.height_m = env.m_from_px(height_px)

        # Init position and velocity of car, effected by Physics of track
        self.centre_x_m = env.m_from_px(left_px) + self.halfwidth_m
        self.centre_y_m = env.m_from_px(self.top_px) + self.height_m/2
        self.v_x_mps = v_x_mps
        self.v_y_mps = v_y_mps

        # Set Mass for collisions
        self.density_kgpm2 = 600
        self.m_kg = self.height_m * self.width_m * self.density_kgpm2

        # Increment Object Count
        floor.objectCount += 1

        # Name this car based on the Object count
        self.name = floor.objectCount

        # Create Pygame rectangular object based on these properties (Pos from left, pos from top, width, height)
        self.rect = pygame.Rect(left_px, self.top_px, self.width_px, self.height_px)

    def draw_object(self):
        # Update position based on the objects position
        self.rect.centerx = env.px_from_m(self.centre_m)

        # Draw the rectangular object
        pygame.draw.rect(game_window.surface, self.colour, self.rect)


class Floor:
    def __init__(self):
        # Initialise list of objects
        self.objects = []
        self.objectCount = 0

        # Coefficients of restitution
        self.coef_rest_base = 0.90
        self.coef_rest_object = self.coef_rest_base
        self.coef_rest_wall = self.coef_rest_base

        # Gravity Components
        self.gravity_mps2 = 9.81
        self.base_gravity_mps2 = self.gravity_mps2/20

        self.colour_transfer = False

    def add_object(self):
        self.objectCount += 1

    def update_SpeedandPosition(self, object, dt_s):
        # Total forces on the object
        object_forces_x_N = (object.m_kg)
        object_forces_y_N = (object.m_kg * self.base_gravity_mps2) + 0.0 + 0.0

        # Total Acceleration on the object
        object_accel_y_N = object_forces_x_N / object.m_kg

        # Calculate final velocity at the end of this timestep.
        v_final_x_mps = object.v_x_mps
        v_final_y_mps = object.v_y_mps + (object_accel_y_N * dt_s)

        # Calculate the average velocity across the timestep.
        v_avg_x_mps = (object.v_x_mps + v_final_x_mps)/2
        v_avg_y_mps = (object.v_y_mps + v_final_y_mps) / 2

        # Use average velocity to find the position after timestep.
        object.centre_x_m = object.centre_x_m + (v_avg_x_mps * dt_s)
        object.centre_y_m = object.centre_y_m + (v_avg_y_mps * dt_s)

        # Assign final velocity to object.
        object.v_x_mps = v_final_x_mps
        object.v_y_mps = v_final_y_mps

        if object.name == 1:
            print("dt",dt_s,"v_avg_mps",math.sqrt(v_final_x_mps**2 + v_final_y_mps**2),"object.centre_m",object.centre_x_m)

    def check_for_collisions(self):
        # Collisions with walls and other objects

        fix_wall_stickiness = True

        for object in self.objects:
            # Collisions with Left and Right wall.
            if object.centre_m - object.halfwidth_m < game_window.left_boundary_m or object.centre_m + object.halfwidth_m > game_window.right_boundary_m:

                if fix_wall_stickiness:
                    self.correct_wall_penetrations(object)

                object.v_mps = - object.v_mps * self.coef_rest_wall

    def correct_wall_penetrations(self, object):
        penetration_left_x_m = game_window.left_boundary_m - (object.centre_m - object.halfwidth_m)
        if penetration_left_x_m > 0:
            object.centre_m += 2 * penetration_left_x_m

        penetration_right_x_m = - game_window.right_boundary_m + (object.centre_m - object.halfwidth_m)
        if penetration_right_x_m > 0:
            object.centre_m -= 2 * penetration_right_x_m

    def create_objects(self, nmode):
        # Update caption on screen
        game_window.update_caption("1D Basic Demo: #" + str(nmode))

        if nmode == 1:
            self.base_gravity_mps2 = 0
            self.objectCount = 0
            self.objects.append(Object(self, colour=THECOLORS["red"], left_px=240, width_px=26, v_x_mps=0.2, v_y_mps=0))
            self.objects.append(Object(self, colour=THECOLORS["blue"], left_px=340, width_px=26, v_x_mps=-0.2, v_y_mps=0))

        elif nmode == 2:
            self.base_gravity_mps2 = self.gravity_mps2
            self.objectCount = 0
            self.objects.append(Object(self, colour=THECOLORS["yellow"], left_px=240, width_px=26, v_x_mps=-0.1, v_y_mps=0))
            self.objects.append(Object(self, colour=THECOLORS["red"], left_px=440, width_px=50, v_x_mps=-0.2, v_y_mps=0))

        elif nmode == 3:
            self.objectCount = 0
            self.base_gravity_mps2 = 0
            self.objects.append(Object(self, colour=THECOLORS["yellow"], left_px=240, width_px=26, v_x_mps=-0.1, v_y_mps=0))
            self.objects.append(Object(self, colour=THECOLORS["red"], left_px=440, width_px=50, v_x_mps=-0.2, v_y_mps=0))


class Environment:
    def __init__(self, length_px, length_m):
        self.px_to_m = length_m/float(length_px)
        self.m_to_px = float(length_px)/length_m

    # Get pixels from metres
    def px_from_m(self, dx_m):
        return int(round(dx_m * self.m_to_px))

    # Get metres from pixels
    def m_from_px(self, dx_px):
        return float(dx_px) * self.px_to_m

    def get_local_user_input(self):
        # Get all the events since the last call.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'Quit'
                elif event.key == K_1:
                    return 1
                elif event.key == K_2:
                    return 2
                elif event.key == K_3:
                    return 3
                else:
                    return "Nothing set up for this key"

            elif event.type == pygame.KEYUP:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

            elif event.type == pygame.MOUSEBUTTONUP:
                pass


def main():
    # Define Globals
    global env, game_window, air_track

    # Initiate Pygame
    pygame.init()

    # Define Environment Size
    window_size_px = window_width_px, window_height_px = 950, 120

    # Initiate an Environment for converting back and forth from pixels and metres.
    # This also creates local client
    env = Environment(window_width_px, 1.5)

    # Initiate the window.
    game_window = GameWindow(window_size_px)

    # Initiate the Floor.
    floor = Floor()

    # Run Demo 1
    floor.create_objects(1)

    # Initiate clock to help control framerate
    clock = pygame.time.Clock()

    # Control framerate
    framerate_limit = 400

    time_s = 0.0
    user_done = False

    while not user_done:
        # Erase All
        game_window.surface.fill(THECOLORS["black"])

        # Find delta_t from one frame
        dt_s = float(clock.tick(framerate_limit) * 1e-3)

        # Check for user initiated stop
        resetmode = env.get_local_user_input()
        if resetmode in [0,1,2,3,4,5,6,7,8,9]:
            print("Reset Mode = ", resetmode)

            # Remove all objects
            floor.objects = []

            # Erase and Update game window
            game_window.erase_and_update()

            # New set based on reset
            floor.create_objects(resetmode)

        elif resetmode == 'Quit':
            user_done = True

        elif resetmode != None:
            print(resetmode)

        # Update x velocity and x position of the object based on dt_s
        for object in floor.objects:
            floor.update_SpeedandPosition(object, dt_s)

        # Check for collisions
        floor.check_for_collisions()

        # Draw in new position
        for object in floor.objects:
            object.draw_object()

        # Update total time
        time_s += dt_s

        pygame.display.flip()

main()