import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speed Typing Challenge")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Game variables
word_list = ["you are your own enemy", "counterspell", "challenging", "speed", "typing", "javascript", "code", "programming", "keyboard", "game development","hackclub","garima gupta","New Delhi","The Appocalypse", "baburao","Nerdy By Nature","404: Player Not Found"]
current_word = random.choice(word_list)
input_text = ""
score = 0
timer = 40  # 5 seconds game duration
start_time = time.time()

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, timer - elapsed_time)

    # End game if timer runs out
    if remaining_time <= 0:
        running = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if input_text == current_word:
                    score += len(current_word) * 10  # Points based on word length
                    current_word = random.choice(word_list)  # New word
                else:
                    score -= 5  # Penalty for incorrect input
                input_text = ""
            else:
                input_text += event.unicode

    # Draw the current word
    word_surface = font.render(current_word, True, BLUE)
    word_rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(word_surface, word_rect)

    # Draw the player's input
    input_surface = font.render(input_text, True, GREEN if input_text == current_word[:len(input_text)] else RED)
    input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(input_surface, input_rect)

    # Draw the score
    score_surface = small_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surface, (10, 10))

    # Draw the timer
    timer_surface = small_font.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(timer_surface, (WIDTH - 150, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# End screen
screen.fill(WHITE)
end_text = font.render("Time's Up! Thanks for playing!", True, BLACK)
end_score = font.render(f"Final Score: {score}", True, BLUE)
screen.blit(end_text, (WIDTH // 4, HEIGHT // 3))
screen.blit(end_score, (WIDTH // 3, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(5000)  # Show the end screen for 5 seconds

pygame.quit()
sys.exit()
