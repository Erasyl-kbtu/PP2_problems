import pygame
from colors import * # Adjusted import assuming it's in the same directory
import random

# Initialize Pygame and its font module for the score/level UI
pygame.init()
pygame.font.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Setup font for displaying score and level
font = pygame.font.SysFont("Arial", 24)

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        # Shift body segments from tail to head
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Move the head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_wall_collision(self):
        head = self.body[0]
        # wall collision
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        
        # self collision
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
                
        return False

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    # food collision
    def check_food_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            # snake growth
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos(self.body)
            return True 
        return False

class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body):
        # Loop until we find a valid position that is NOT on the snake
        while True:
            new_x = random.randint(0, (WIDTH // CELL) - 1)
            new_y = random.randint(0, (HEIGHT // CELL) - 1)
            
            # Check if this new coordinate collides with any part of the snake
            collision = False
            for segment in snake_body:
                if new_x == segment.x and new_y == segment.y:
                    collision = True
                    break
            
            # If no collision, assign the new position and break the loop
            if not collision:
                self.pos.x = new_x
                self.pos.y = new_y
                break


# Game Variables
FPS = 10
score = 0
level = 1
foods_to_next_level = 3 # Level up every 3 foods

clock = pygame.time.Clock()

food = Food()
snake = Snake()

# Initialize the first food position so it doesn't start on the default snake body
food.generate_random_pos(snake.body)

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)
    draw_grid()

    if not game_over:
        snake.move()
        
        # 1. Check for wall/border collisions
        if snake.check_wall_collision():
            print("Game Over! You hit a wall.")
            game_over = True
        
        # 2. Check for food collisions
        if snake.check_food_collision(food):
            score += 10 
            
            # 3 & 4. Check for Level Up and Increase Speed
            if (score / 10) % foods_to_next_level == 0:
                level += 1
                FPS += 2 
                level_up_text = font.render(f"Level Up! Welcome to Level {level}. Speed increased!", True, colorWHITE)
                screen.blit(level_up_text, (WIDTH/2, HEIGHT/2))

    # Draw game objects
    snake.draw()
    if not game_over:   
        food.draw()

    # 5. Add counter for score and level to the UI
    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    # Display Game Over text if the player dies
    if game_over:
        game_over_text = font.render("GAME OVER", True, colorRED)
        text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(game_over_text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()