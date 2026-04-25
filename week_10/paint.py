import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pygame Paint Tool")
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    tool = 'line'  # Options: 'line', 'rect', 'circle', 'eraser'
    
    # Create a separate surface to hold the permanent drawing
    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0)) # Fill with black background
    
    # Track state for shape drawing
    drawing = False
    start_pos = None
    last_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held: return
                if event.key == pygame.K_F4 and alt_held: return
                if event.key == pygame.K_ESCAPE: return
            
                # Color Selection
                if event.key == pygame.K_1: mode = 'red'
                elif event.key == pygame.K_2: mode = 'green'
                elif event.key == pygame.K_3: mode = 'blue'
                
                # Tool Selection
                elif event.key == pygame.K_l: tool = 'line'
                elif event.key == pygame.K_r: tool = 'rect'
                elif event.key == pygame.K_c: tool = 'circle'
                elif event.key == pygame.K_e: tool = 'eraser'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click begins drawing
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
                elif event.button == 3: # Right click shrinks brush
                    radius = max(1, radius - 1)
                elif event.button == 2: # Middle click grows brush
                    radius = min(200, radius + 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    if tool in ['rect', 'circle']:
                        # Draw the final permanent shape to the canvas
                        draw_shape(canvas, tool, start_pos, event.pos, mode, radius)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'line':
                        # Draw smoothly to the canvas as the mouse moves
                        draw_line(canvas, last_pos, event.pos, mode, radius)
                    elif tool == 'eraser':
                        # Eraser is just drawing with the background color
                        draw_line(canvas, last_pos, event.pos, 'black', radius)
                    last_pos = event.pos
                    
        # 1. Blit the permanent canvas to the screen
        screen.blit(canvas, (0, 0))
        
        # 2. Overlay the "preview" shape if currently dragging a rect/circle
        if drawing and tool in ['rect', 'circle']:
            current_pos = pygame.mouse.get_pos()
            draw_shape(screen, tool, start_pos, current_pos, mode, radius)

        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    """Helper function to return RGB tuples."""
    if mode == 'red': return (255, 0, 0)
    if mode == 'green': return (0, 255, 0)
    if mode == 'blue': return (0, 0, 255)
    if mode == 'black': return (0, 0, 0)
    return (255, 255, 255)

def draw_shape(surface, tool, start, end, mode, width):
    """Draws a rectangle or circle."""
    color = get_color(mode)
    
    if tool == 'rect':
        # Create a rect using start and end points
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        rect.normalize() # Fixes negative width/height if dragged backwards
        
        # Prevent pygame crashing if line width is larger than the shape itself
        safe_width = min(width, rect.width // 2, rect.height // 2)
        if safe_width < 1: safe_width = 0 # 0 means fill the shape entirely
        
        pygame.draw.rect(surface, color, rect, safe_width)
        
    elif tool == 'circle':
        # Calculate radius using the distance between start and end point
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        circ_radius = int(math.hypot(dx, dy))
        
        safe_width = min(width, circ_radius)
        if safe_width < 1: safe_width = 0
        
        pygame.draw.circle(surface, color, start, circ_radius, safe_width)

def draw_line(surface, start, end, mode, width):
    """Draws a smooth line by interpolating circles between mouse events."""
    color = get_color(mode)
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    if iterations == 0:
        pygame.draw.circle(surface, color, start, width)
        return
        
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(surface, color, (x, y), width)

if __name__ == "__main__":
    main()