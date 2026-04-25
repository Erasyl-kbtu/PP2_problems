import pygame
import sys
import os
from player import MusicPlayer

def main():
    pygame.init()

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python Music Player")

    BG_COLOR = (30, 30, 30)
    TEXT_COLOR = (230, 230, 230)
    ACCENT_COLOR = (100, 200, 100)
    
    font_large = pygame.font.SysFont('Arial', 24, bold=True)
    font_medium = pygame.font.SysFont('Arial', 18)
    font_small = pygame.font.SysFont('Arial', 14)

    music_dir = os.path.join(os.path.dirname(__file__), 'music')
    player = MusicPlayer(music_dir)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.pause()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)

        title_surface = font_large.render("Interactive Music Player", True, ACCENT_COLOR)
        screen.blit(title_surface, (20, 20))

        track_text = f"Current Track: {player.get_current_track_name()}"
        track_surface = font_medium.render(track_text, True, TEXT_COLOR)
        screen.blit(track_surface, (20, 80))

        status_text = f"Status: {player.get_status()}"
        status_surface = font_medium.render(status_text, True, TEXT_COLOR)
        screen.blit(status_surface, (20, 120))

        if player.is_playing:
            progress = player.get_progress()
            time_text = f"Elapsed Time: {int(progress // 60):02d}:{int(progress % 60):02d}"
            time_surface = font_medium.render(time_text, True, TEXT_COLOR)
            screen.blit(time_surface, (20, 160))

        pygame.draw.line(screen, (100, 100, 100), (20, 220), (WIDTH - 20, 220), 2)

        instructions = [
            "Keyboard Controls:",
            "[ P ] - Play / Resume",
            "[ S ] - Pause",
            "[ N ] - Next Track",
            "[ B ] - Previous Track",
            "[ Q ] - Quit"
        ]
        
        y_offset = 240
        for line in instructions:
            inst_surface = font_small.render(line, True, (170, 170, 170))
            screen.blit(inst_surface, (20, y_offset))
            y_offset += 25

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()