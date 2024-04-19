import pygame
import sys
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup - fixed size window
SCREEN_WIDTH, SCREEN_HEIGHT = 256, 240
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Define a function to generate NES-style boop sounds
def generate_boop_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Set up the ball and paddles
ball_x = SCREEN_WIDTH / 2
ball_y = SCREEN_HEIGHT / 2
ball_speed_x = 1
ball_speed_y = 1
paddle1_y = SCREEN_HEIGHT / 2 - 25
paddle2_y = SCREEN_HEIGHT / 2 - 25
paddle_speed = 2

# Set up the score counter
score1 = 0
score2 = 0

# Set up the clock for 60 FPS
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < SCREEN_HEIGHT - 50:
        paddle1_y += paddle_speed

    # AI for the right player
    if ball_x > SCREEN_WIDTH / 2 and ball_speed_x > 0:
        if ball_y < paddle2_y and paddle2_y > 0:
            paddle2_y -= paddle_speed
        elif ball_y > paddle2_y + 50 and paddle2_y < SCREEN_HEIGHT - 50:
            paddle2_y += paddle_speed

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision with walls
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - 10:
        ball_speed_y *= -1
        generate_boop_sound().play()

    # Collision with paddles
    if ((ball_x <= 10 and paddle1_y <= ball_y <= paddle1_y + 50) or
        (ball_x >= SCREEN_WIDTH - 20 and paddle2_y <= ball_y <= paddle2_y + 50)):
        ball_speed_x *= -1
        generate_boop_sound().play()

    # Score update
    if ball_x < 0:
        score2 += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_speed_x, ball_speed_y = 1, 1
        generate_boop_sound().play()
    elif ball_x > SCREEN_WIDTH:
        score1 += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_speed_x, ball_speed_y = -1, 1
        generate_boop_sound().play()

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (ball_x, ball_y, 10, 10))
    pygame.draw.rect(screen, (255, 255, 255), (0, paddle1_y, 10, 50))
    pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH - 10, paddle2_y, 10, 50))
    
    # Draw the score counter
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"{score1} - {score2}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
