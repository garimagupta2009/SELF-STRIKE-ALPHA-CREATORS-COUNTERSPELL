import pygame
import sys
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self vs Self War")

# Load background image
background = pygame.image.load("background.jpg")  # Replace with your file name
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Constants
PLAYER_SPEED = 5
PROJECTILE_SPEED = 7
CLONE_DELAY = 30  # Delay in frames for clone mimicry

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.projectiles = pygame.sprite.Group()

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Keep player within bounds
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top, -PROJECTILE_SPEED, RED)
        self.projectiles.add(projectile)

    def update(self):
        self.projectiles.update()

class Clone(Player):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.movement_queue = deque(maxlen=CLONE_DELAY)

    def mimic(self, player_rect):
        self.movement_queue.append((player_rect.x, player_rect.y))
        if len(self.movement_queue) == CLONE_DELAY:
            self.rect.topleft = self.movement_queue[0]

    def shoot(self):
        # Clone shoots randomly or based on logic
        projectile = Projectile(self.rect.centerx, self.rect.bottom, PROJECTILE_SPEED, BLUE)
        self.projectiles.add(projectile)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Initialize player and clone
player = Player(WIDTH // 2, HEIGHT - 50, GREEN)
clone = Clone(WIDTH // 2, 50, BLUE)

# Sprite groups
all_sprites = pygame.sprite.Group(player, clone)
player_projectiles = player.projectiles
clone_projectiles = clone.projectiles

# Game variables
running = True
game_over = False

# Main game loop
while running:
    screen.blit(background, (0, 0))  # Draw the background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Clone mimics player movements
        clone.mimic(player.rect)

        # Clone shoots randomly
        clone.shoot()

        # Update projectiles
        player.update()
        clone.update()

        # Collision detection
        for projectile in player_projectiles:
            if clone.rect.colliderect(projectile.rect):
                clone.health -= 10
                projectile.kill()
        for projectile in clone_projectiles:
            if player.rect.colliderect(projectile.rect):
                player.health -= 10
                projectile.kill()

        # Check for game over
        if player.health <= 0 or clone.health <= 0:
            game_over = True

    # Draw everything
    all_sprites.draw(screen)
    player.projectiles.draw(screen)
    clone.projectiles.draw(screen)

    # Display health
    player_health_text = font.render(f"Player Health: {player.health}", True, BLACK)
    clone_health_text = font.render(f"Clone Health: {clone.health}", True, BLACK)
    screen.blit(player_health_text, (10, HEIGHT - 40))
    screen.blit(clone_health_text, (10, 10))

    if game_over:
        winner = "Player" if clone.health <= 0 else "Clone"
        game_over_text = font.render(f"Game Over! {winner} Wins!", True, RED)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)
 