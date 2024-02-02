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

from hue_shift import return_color
from datetime import datetime

WIDTH = 1280
HEIGHT = 720
BACKGROUND = (255, 255, 255)
tile_width = 32
tile_height = 32


def logger_debug(e):
    """Simple print debug messages"""

    print(f"[DEBUG] {datetime.now().strftime('%H:%M:%S')} :: {return_color()}{e}")


def get_tile(x, y, width, height, tileset):
    """Extract a single tile from the tileset."""
    tile = pygame.Surface((width, height))
    tile.blit(tileset, (0, 0), (x * width, y * height, width, height))
    return tile


def create_background(tile, width, height):
    """Create a background surface filled with tiles."""
    background = pygame.Surface((width, height))
    for y in range(0, height, tile_height):
        for x in range(0, width, tile_width):
            background.blit(tile, (x, y))
    return background


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("assets/PNG/sprites/player/idle/player-idle-1.png", startx, starty)
        self.stand_image = self.image

        # Load jump animations
        self.jump_up_image = pygame.image.load("assets/PNG/sprites/player/jump/player-jump-1.png")
        self.jump_down_image = pygame.image.load("assets/PNG/sprites/player/jump/player-jump-2.png")

        self.walk_cycle = [pygame.image.load(f"assets/PNG/sprites/player/run/player-run-{i}.png") for i in range(1, 6)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_speed = -10
        self.on_ground = True

    def move(self, x, y):
        dx = x
        dy = y
        self.rect.move_ip([dx,dy])

    def update(self):
        key = pygame.key.get_pressed()

        # Horizontal movement
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            self.move(-self.speed, 0)
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            self.move(self.speed, 0)
        else:
            self.image = self.stand_image

        # Vertical movement
        if key[pygame.K_UP] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False  # This would be set to True when the player lands on the ground

        # Apply gravity
        self.velocity_y += self.gravity
        self.move(0, self.velocity_y)

        # If falling or jumping, change the player image to the jump animation
        if self.velocity_y < 0:
            self.image = self.jump_up_image
        elif self.velocity_y > 0:
            self.image = self.jump_down_image

        # Flip the image if facing left
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        # Reset to the ground state for the example, this should be based on collision with the ground in your game
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0


class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("assets/PNG/environment/props/house.png", startx, starty)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    tileset = pygame.image.load("assets/PNG/environment/layers/tileset.png")
    clock = pygame.time.Clock()
    tile = get_tile(tileset=tileset, height=200, width=200, x=0, y=0)
    background = create_background(tile, 640, 480)

    logger_debug("Initialized Screen")

    player = Player(100, 200)
    boxes = pygame.sprite.Group()
    for bx in range(0, 400, 70):
        boxes.add(Box(bx, 300))

    while True:
        screen.fill(BACKGROUND)
        screen.blit(background, (0, 0))
        pygame.event.pump()
        player.update()
        player.draw(screen)
        boxes.draw(screen)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
