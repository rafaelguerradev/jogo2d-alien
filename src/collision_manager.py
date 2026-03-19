import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

# ======================
# COLLISION MANAGER
# ======================
class CollisionManager:
    def __init__(self, bullets, aliens, ship):
        self.bullets = bullets
        self.aliens = aliens
        self.ship = ship

    def check_collisions(self):
        pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("A nave foi atingida!")
            sys.exit()