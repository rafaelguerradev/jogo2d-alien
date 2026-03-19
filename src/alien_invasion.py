import sys
import pygame

from event_manager import EventManager
from alien_manager import AlienManager
from collision_manager import CollisionManager
from renderer import Renderer

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


# ======================
# GAME PRINCIPAL
# ======================
class AlienInvasion:
    def __init__(self):
        pygame.init()

        # CONFIG
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # ESTADO
        self.ship = Ship(self.screen, self.settings)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # SISTEMAS
        self.event_manager = EventManager(self.ship, self.fire_bullet)
        self.alien_manager = AlienManager(
            self.aliens, self.screen, self.settings, self.ship
        )
        self.collision_manager = CollisionManager(
            self.bullets, self.aliens, self.ship
        )
        self.renderer = Renderer(
            self.screen,
            self.settings.bg_color,
            self.ship,
            self.aliens,
            self.bullets,
        )

    def run_game(self):
        self.alien_manager.create_fleet()

        while True:
            self.event_manager.handle_events()
            self._update_game()
            self.renderer.draw()

    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            bullet = Bullet(self.screen, self.settings, self.ship)
            self.bullets.add(bullet)

    def _update_game(self):
        self.ship.update()
        self._update_bullets()
        self.alien_manager.update()
        self.collision_manager.check_collisions()

    def _update_bullets(self):
        self.bullets.update()

        # limpeza simples
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    game = AlienInvasion()
    game.run_game()