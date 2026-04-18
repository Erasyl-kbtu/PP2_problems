import pygame
import sys
from clock import MickeyClock

def main():
    pygame.init()
    
    WIDTH, HEIGHT = 600, 600
    FPS = 1
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")
    timer_clock = pygame.time.Clock()
    
    mickey_clock = MickeyClock(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        mickey_clock.draw(screen)
        
        pygame.display.flip()
        timer_clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()