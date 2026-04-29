import pygame
import random
import time

pygame.init() 

WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Creating a game window

# Load images
image_background = pygame.image.load(r'C:\Users\Erasyl\OneDrive\Desktop\PP2_problems\week_10\pngwing.com.png')
image_player = pygame.image.load(r'C:\Users\Erasyl\OneDrive\Desktop\PP2_problems\week_10\Car_Green_Front.svg')
image_enemy = pygame.image.load(r'C:\Users\Erasyl\OneDrive\Desktop\PP2_problems\week_10\Car_Red_Front.svg')

# Create a Coin graphic dynamically (Golden circle)
image_coin = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.circle(image_coin, (255, 215, 0), (15, 15), 15) # Gold color

# Load sounds

# Setup fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Game variables
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
bg_y = 0 # Y-coordinate for the scrolling background

# Custom User Event to increase speed periodically
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 10000) # Triggers every 10000 milliseconds (10 seconds)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 40 # Slightly raised from the very bottom
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        # Move left and right
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.generate_random_rect()

    def generate_random_rect(self):
        # Spawns enemy at a random X position at the top
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED) # Move downwards at the current global SPEED
        # If enemy falls off the screen, respawn at top and increase score
        if self.rect.top > HEIGHT:
            SCORE += 1
            self.generate_random_rect()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()
        self.generate_random_rect()

    def generate_random_rect(self):
        # Spawns coin at a random X position at the top
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = random.randint(-100, 0) # Slight random offset above screen

    def move(self):
        self.rect.move_ip(0, SPEED) # Moves at the same speed as the traffic
        # If coin falls off the screen without being collected, respawn it
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

# Instantiate objects
player = Player()
enemy = Enemy()
coin = Coin()

# Setup Sprite Groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)

# Game Loop Configuration
running = True
clock = pygame.time.Clock()
FPS = 60

while running: # Main game loop
    for event in pygame.event.get(): # Event loop
        if event.type == pygame.QUIT:
            running = False
        if event.type == INC_SPEED:
            SPEED += 0.2 # Gradually increase game difficulty

    # --- Updates ---
    player.move()

    # --- Drawing Background ---
    # Animated scrolling background logic
    screen.blit(image_background, (0, bg_y))
    screen.blit(image_background, (0, bg_y - HEIGHT))
    bg_y += SPEED # Move background downwards
    if bg_y >= HEIGHT:
        bg_y = 0 # Reset background position to create seamless loop

    # --- Drawing UI (Scores) ---
    score_text = font_small.render(f"Score: {SCORE}", True, "black")
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, "black")
    screen.blit(score_text, (10, 10)) # Top left
    screen.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 10)) # Top right

    # --- Drawing Sprites ---
    for entity in all_sprites:
        if entity != player: # Enemies and coins move automatically
            entity.move()
        screen.blit(entity.image, entity.rect)

    # --- Collision Detection: Coins ---
    # check if player collides with any sprite in the coin_sprites group
    if pygame.sprite.spritecollideany(player, coin_sprites):
        COINS_COLLECTED += 1
        coin.generate_random_rect() # Respawn the coin at the top immediately

    # --- Collision Detection: Enemies ---
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        
        # Flash screen red and show Game Over
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        
        time.sleep(2) # Pause briefly to let the user see "Game Over"
        running = False # Exit the loop
        
    pygame.display.flip() # Updates the entire screen
    clock.tick(FPS) # Locks the framerate

pygame.quit()
  