"""
Copyright (C) 2024  Johannes Habel, Piotr Rayzacher, Hubertus Keimer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pygame

from sys import exit
from hue_shift import return_color
from datetime import datetime

WIDTH = 800
HEIGHT = 400
BACKGROUND = (255, 255, 255)
tile_width = 32
tile_height = 32


def logger_debug(e):
    """Simple print debug messages"""
    print(f"[DEBUG] {datetime.now().strftime('%H:%M:%S')} :: {return_color()}{e}")


pygame.init()
logger_debug("Initialized pygame")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Run")
clock = pygame.time.Clock()

background_surface = pygame.image.load()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    screen.blit(background_surface, (200, 100))



    pygame.display.update()
    clock.tick(60)
