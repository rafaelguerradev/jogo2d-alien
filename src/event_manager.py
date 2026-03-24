import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

# ======================
# EVENT MANAGER
# ======================

class EventManager:
    def __init__(self, ship, fire_bullet):
        self.ship = ship
        self.fire_bullet = fire_bullet

        # Mapas de ações
        self.keydown_actions = {
            pygame.K_RIGHT: lambda: setattr(self.ship, "moving_right", True),
            pygame.K_LEFT: lambda: setattr(self.ship, "moving_left", True),
            pygame.K_SPACE: self.fire_bullet,
        }

        self.keyup_actions = {
            pygame.K_RIGHT: lambda: setattr(self.ship, "moving_right", False),
            pygame.K_LEFT: lambda: setattr(self.ship, "moving_left", False),
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key, self.keydown_actions)
            elif event.type == pygame.KEYUP:
                self._handle_key(event.key, self.keyup_actions)

    def _handle_key(self, key, action_map):
        action = action_map.get(key)
        if action:
            action()