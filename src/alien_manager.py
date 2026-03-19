import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

# ======================
# ALIEN MANAGER
# ======================
class AlienManager:
    def __init__(self, aliens, screen, settings, ship):
        self.aliens = aliens
        self.screen = screen
        self.settings = settings
        self.ship = ship

    def create_fleet(self):
        alien = Alien(self.screen, self.settings)
        alien_width, alien_height = alien.rect.size

        number_aliens_x = self._calculate_aliens_x(alien_width)
        number_rows = self._calculate_rows(alien_height)

        for row in range(number_rows):
            for col in range(number_aliens_x):
                self._create_alien(col, row, alien_width, alien_height)

    def _create_alien(self, col, row, w, h):
        alien = Alien(self.screen, self.settings)
        alien.x = w + 2 * w * col
        alien.rect.x = alien.x
        alien.y = h + 2 * h * row
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _calculate_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - (2 * alien_width)
        return available_space_x // (2 * alien_width)

    def _calculate_rows(self, alien_height):
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        return available_space_y // (2 * alien_height)

    def update(self):
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_direction()
                break

    def _change_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1