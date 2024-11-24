import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human Crossing Problems")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
RED = (200, 0, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load assets
player_image = pygame.Surface((40, 60))
player_image.fill(GREEN)

enemy_image = pygame.Surface((40, 60))
enemy_image.fill(RED)

cactus_image = pygame.Surface((20, 50))
cactus_image.fill(BLACK)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 70
        self.velocity = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -15

    def update(self):
        # Apply gravity
        self.velocity += 1
        self.rect.y += self.velocity

        # Keep player on the ground
        if self.rect.y >= HEIGHT - 70:
            self.rect.y = HEIGHT - 70
            self.is_jumping = False

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -self.rect.width:
            self.kill()

# Initialize groups
player = Player()
player_group = pygame.sprite.GroupSingle(player)

obstacles = pygame.sprite.Group()
self_enemies = pygame.sprite.Group()

# Variables
score = 0
game_over = False

# Main game loop
def main_game():
    global score, game_over

    running = True
    obstacle_timer = 0
    enemy_timer = 0

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over and event.key == pygame.K_SPACE:
                    player.jump()
                if game_over and event.key == pygame.K_r:
                    restart_game()

        if not game_over:
            # Update timers
            obstacle_timer += 1
            enemy_timer += 1

            # Add obstacles
            if obstacle_timer > 60:
                obstacle_timer = 0
                obstacle = Obstacle(WIDTH, HEIGHT - 70, 20, 50, cactus_image)
                obstacles.add(obstacle)

            # Add self-enemy
            if enemy_timer > 300:
                enemy_timer = 0
                self_enemy = Obstacle(WIDTH, HEIGHT - 70, 40, 60, enemy_image)
                self_enemies.add(self_enemy)

            # Update all sprites
            player_group.update()
            obstacles.update()
            self_enemies.update()

            # Check for collisions
            if pygame.sprite.spritecollideany(player, obstacles) or pygame.sprite.spritecollideany(player, self_enemies):
                game_over = True

            # Increase score
            score += 1

        # Draw everything
        player_group.draw(screen)
        obstacles.draw(screen)
        self_enemies.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, RED)
            screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(30)

def restart_game():
    global score, game_over
    score = 0
    game_over = False
    obstacles.empty()
    self_enemies.empty()
    player.rect.y = HEIGHT - 70
    player.is_jumping = False
    player.velocity = 0

# Run the game
main_game()
