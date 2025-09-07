import pygame
import math
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Heart for Maria")

# Colors
BACKGROUND = (10, 10, 20)  # Dark blue-black background
HEART_COLOR = (200, 30, 30)  
HIGHLIGHT = (255, 150, 150)  # Pink highlight
SHADOW = (120, 10, 10)  # Darker red for shadow
TEXT_COLOR = (255, 255, 255)  # White text

# Create a surface for lighting effects
light_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Heart parameters
def generate_heart_points(scale=10, detail=200):
    points = []
    for t in range(0, detail):
        t = t / detail * 2 * math.pi
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        points.append((x * scale, -y * scale))
    return points

heart_points = generate_heart_points(10, 200)

# Scale and center the heart
scaled_heart = []
for x, y in heart_points:
    scaled_heart.append((x + WIDTH // 2, y + HEIGHT // 2))

# Font for the name
font = pygame.font.SysFont("Arial", 48, bold=True)
name_text = font.render("Maria", True, TEXT_COLOR)
name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Generate 3D points with depth
def generate_3d_heart_points():
    points = []
    for z in range(-5, 6, 2):  # Multiple layers for 3D effect
        scale = 10 + z * 0.5  # Scale based on depth
        layer_points = generate_heart_points(scale, 150)
        for x, y in layer_points:
            points.append((x + WIDTH // 2, y + HEIGHT // 2, z))
    return points

heart_3d_points = generate_3d_heart_points()

# Animation variables
pulse = 0
pulse_dir = 1
rotation = 0
beat_count = 0

# Particles for floating effect
particles = []
for _ in range(50):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(1, 3)
    speed = random.uniform(0.2, 1.0)
    color = (random.randint(200, 255), random.randint(150, 200), random.randint(150, 200))
    particles.append([x, y, size, speed, color])

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear screen
    screen.fill(BACKGROUND)
    
    # Update and draw particles
    for particle in particles:
        particle[1] -= particle[3]  # Move up
        if particle[1] < 0:
            particle[1] = HEIGHT
            particle[0] = random.randint(0, WIDTH)
        alpha = min(255, int(255 * (particle[1] / HEIGHT)))
        particle_color = (particle[4][0], particle[4][1], particle[4][2], alpha)
        pygame.draw.circle(screen, particle_color, (int(particle[0]), int(particle[1])), particle[2])
    
    # Pulse animation for heartbeat effect
    pulse += 0.05 * pulse_dir
    if pulse > 1:
        pulse_dir = -1
        beat_count += 1
    elif pulse < 0:
        pulse_dir = 1
    
    # Calculate current scale based on pulse
    current_scale = 10 + pulse * 1.5
    
    # Draw the 3D heart with realistic coloring
    for x, y, z in heart_3d_points:
        # Calculate color based on depth and position
        depth_factor = (z + 5) / 10  # Normalize z between 0 and 1
        center_dist = math.sqrt((x - WIDTH/2)**2 + (y - HEIGHT/2)**2)
        dist_factor = 1 - min(1, center_dist / 200)
        
        # Base color with depth shading
        r = int(HEART_COLOR[0] * depth_factor)
        g = int(HEART_COLOR[1] * depth_factor * 0.7)
        b = int(HEART_COLOR[2] * depth_factor * 0.7)
        
        # Add highlights
        if depth_factor > 0.7:
            highlight_strength = (depth_factor - 0.7) / 0.3
            r = min(255, int(r + HIGHLIGHT[0] * highlight_strength))
            g = min(255, int(g + HIGHLIGHT[1] * highlight_strength))
            b = min(255, int(b + HIGHLIGHT[2] * highlight_strength))
        
        # Scale point based on pulse
        scaled_x = WIDTH/2 + (x - WIDTH/2) * (current_scale/10)
        scaled_y = HEIGHT/2 + (y - HEIGHT/2) * (current_scale/10)
        
        # Draw the point
        size = max(1, int(3 * depth_factor))
        pygame.draw.circle(screen, (r, g, b), (int(scaled_x), int(scaled_y)), size)
    
    # Draw the heart outline for definition
    for i in range(len(scaled_heart) - 1):
        x1, y1 = scaled_heart[i]
        x2, y2 = scaled_heart[i+1]
        
        # Scale points based on pulse
        x1 = WIDTH/2 + (x1 - WIDTH/2) * (current_scale/10)
        y1 = HEIGHT/2 + (y1 - HEIGHT/2) * (current_scale/10)
        x2 = WIDTH/2 + (x2 - WIDTH/2) * (current_scale/10)
        y2 = HEIGHT/2 + (y2 - HEIGHT/2) * (current_scale/10)
        
        pygame.draw.line(screen, SHADOW, (x1, y1), (x2, y2), 2)
    
    # Draw the name with pulsing effect
    name_scale = 1 + pulse * 0.1
    scaled_font = pygame.font.SysFont("Arill", int(48 * name_scale), bold=True)
    name_text = scaled_font.render("M  I R H A", True, TEXT_COLOR)
    name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    # Add a subtle shadow to the text
    shadow_font = pygame.font.SysFont("Arial", int(48 * name_scale), bold=True)
    shadow_text = shadow_font.render("M I R H A", True, (50, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))
    screen.blit(shadow_text, shadow_rect)
    
    screen.blit(name_text, name_rect)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
