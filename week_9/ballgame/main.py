import pygame
from week_9.ballgame.ball import Ball

def main():
    pygame.init()
    
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock = pygame.time.Clock()
    
    ball = Ball(WIDTH // 2, HEIGHT // 2, 25, RED, WIDTH, HEIGHT)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            ball.move_up()
        if keys[pygame.K_DOWN]:
            ball.move_down()
        if keys[pygame.K_LEFT]:
            ball.move_left()
        if keys[pygame.K_RIGHT]:
            ball.move_right()

        screen.fill(WHITE)
        ball.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()