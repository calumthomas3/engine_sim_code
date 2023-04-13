import sys, os
import pygame
import datetime

# Pygame Constants
from pygame.locals import *
from pygame.color import THECOLORS

class Environment:
    # Set up different variables that a system can have.
    def __init__(self):
        # 2D Rotational
        a_theta = 0
        v_theta = 0
        theta = 0

        # 2D Directional
        a_x = 0
        a_y = 0
        v_x = 0
        v_y = 0
        p_x = 0
        p_y = 0

        # 2D Forces
