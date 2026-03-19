import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

# ======================
# RENDERER
# ======================
class Renderer:
    def __init__(self, screen, bg_color, ship, aliens, bullets):
        self.screen = screen
        self.bg_color = bg_color
        self.ship = ship
        self.aliens = aliens
        self.bullets = bullets

    def draw(self):
        self.screen.fill(self.bg_color)

        self.ship.blitme()
        self.aliens.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()