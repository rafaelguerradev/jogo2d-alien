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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._keydown(event)
            elif event.type == pygame.KEYUP:
                self._keyup(event)

    def _keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def _keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


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