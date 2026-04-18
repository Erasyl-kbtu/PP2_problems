import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, center_x, center_y, width, height):
        self.center = (center_x, center_y)
        self.screen_size = (width, height)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(base_dir, "images")
        

        bg_path = os.path.join(image_dir, "C:\\Users\\Erasyl\\OneDrive\\Desktop\\PP2_problems\\week_9\\pngwing.com.png")
        self.background_img = pygame.image.load(bg_path)
        self.background_img = pygame.transform.scale(self.background_img, self.screen_size)

        m_path = os.path.join(image_dir, "C:\\Users\\Erasyl\\OneDrive\\Desktop\\PP2_problems\\week_9\\mickeyclock_m.png")
        self.minute_hand = pygame.image.load(m_path).convert_alpha()

        s_path = os.path.join(image_dir, "C:\\Users\\Erasyl\\OneDrive\\Desktop\\PP2_problems\\week_9\\mickeyclock_s.png")
        self.second_hand = pygame.image.load(s_path).convert_alpha()

    def rotate_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=self.center)
        return rotated_image, rotated_rect

    def draw(self, surface):
        surface.blit(self.background_img, (0, 0))
        
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = -(minutes * 6 + (seconds / 60.0) * 6)
        second_angle = -(seconds * 6)

        m_img_rotated, m_rect = self.rotate_center(self.minute_hand, minute_angle)
        s_img_rotated, s_rect = self.rotate_center(self.second_hand, second_angle)

        surface.blit(m_img_rotated, m_rect)
        surface.blit(s_img_rotated, s_rect)
        
        pygame.draw.circle(surface, (30, 30, 30), self.center, 12)