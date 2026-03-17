import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Gerencia o jogo e seus comportamentos."""

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.bg_color = self.settings.bg_color

        self._criar_nave()
        self._criar_bullets()
        self._criar_aliens()

    def _criar_nave(self):
        # Criando uma instância da classe Ship para representar a nave espacial
        self.ship = Ship(self.screen, self.settings)
    
    def _criar_bullets(self):
        self.bullets = (
            pygame.sprite.Group()
        )  # Cria um grupo para armazenar os projéteis disparados pela nave

    def _criar_aliens(self):
        self.aliens = (
            pygame.sprite.Group()
        )  # Cria um grupo para armazenar os alienígenas presentes no jogo

    def create_fleet(self):
        alien_width, alien_height = self._get_alien_size()
        number_aliens_x = self._calculate_aliens_x(alien_width)
        number_rows = self._calculate_rows(alien_height)

        for row in range(number_rows):
            for col in range(number_aliens_x):
                alien = self._create_alien()
                self._position_alien(alien, col, row, alien_width, alien_height)
                self.aliens.add(alien)
    
    def _get_alien_size(self):
        alien = Alien(self.screen, self.settings)
        return alien.rect.width, alien.rect.height
    
    def _calculate_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - (2 * alien_width)
        return available_space_x // (2 * alien_width)
    
    def _calculate_rows(self, alien_height):
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        return available_space_y // (2 * alien_height)
    
    def _create_alien(self):
        return Alien(self.screen, self.settings)
    
    def _position_alien(self, alien, col, row, alien_width, alien_height):
        alien.x = alien_width + 2 * alien_width * col
        alien.rect.x = alien.x
        alien.y = alien_height + 2 * alien_height * row
        alien.rect.y = alien.y

    def run_game(self):
        self.create_fleet()

        while True:
            self._handle_events()
            self._update_game()
            self._draw_screen()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _handle_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            bullet = Bullet(self.screen, self.settings, self.ship)
            self.bullets.add(bullet)

    def _update_game(self):
        self.ship.update()
        self._update_bullets()
        self._update_aliens()
        self._check_collisions()

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_collisions(self):
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("A nave foi atingida!")
            sys.exit()

    def _draw_screen(self):
        self.screen.fill(self.bg_color)

        self.ship.blitme()
        self.aliens.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()

if __name__ == "__main__":
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
