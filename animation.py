import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Scorpion Animation")

# Colors
DARK_BROWN = (75, 50, 30)
LIGHT_BROWN = (120, 80, 50)
SAND = (194, 178, 128)
GROUND = (210, 180, 140)

# Scorpion parameters
body_length = 120
body_width = 60
leg_length = 60
tail_segments = 5
tail_length = 100

class Scorpion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # in radians
        self.speed = 0.5
        self.leg_phase = 0
        self.tail_phase = 0
        self.pincers_phase = 0
        
    def update(self):
        # Move forward
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        # Occasionally change direction
        if random.random() < 0.01:
            self.direction += random.uniform(-0.5, 0.5)
            
        # Keep on screen
        if self.x < 50:
            self.direction = random.uniform(-0.5, 0.5)
        elif self.x > WIDTH - 50:
            self.direction = random.uniform(math.pi-0.5, math.pi+0.5)
        if self.y < 50:
            self.direction = random.uniform(0, math.pi)
        elif self.y > HEIGHT - 50:
            self.direction = random.uniform(math.pi, 2*math.pi)
            
        # Animate legs and tail
        self.leg_phase += 0.1
        self.tail_phase += 0.05
        self.pincers_phase += 0.03
        
    def draw(self, surface):
        # Draw body (main oval)
        body_rect = pygame.Rect(0, 0, body_length, body_width)
        body_rect.center = (self.x, self.y)
        pygame.draw.ellipse(surface, DARK_BROWN, body_rect)
        
        # Draw head
        head_x = self.x + math.cos(self.direction) * (body_length/2 - 10)
        head_y = self.y + math.sin(self.direction) * (body_length/2 - 10)
        pygame.draw.circle(surface, DARK_BROWN, (int(head_x), int(head_y)), body_width//3)
        
        # Draw legs (4 on each side)
        for side in [-1, 1]:
            for i in range(4):
                leg_angle = self.direction + side * (math.pi/4 + 0.2 * math.sin(self.leg_phase + i*0.5))
                leg_start_x = self.x + math.cos(self.direction) * (body_length/3 - i*10)
                leg_start_y = self.y + math.sin(self.direction) * (body_length/3 - i*10)
                leg_start_x += math.cos(self.direction + math.pi/2) * side * (body_width/2 - 5)
                leg_start_y += math.sin(self.direction + math.pi/2) * side * (body_width/2 - 5)
                
                leg_end_x = leg_start_x + math.cos(leg_angle) * leg_length
                leg_end_y = leg_start_y + math.sin(leg_angle) * leg_length
                
                pygame.draw.line(surface, LIGHT_BROWN, (leg_start_x, leg_start_y), 
                                (leg_end_x, leg_end_y), 3)
                
                # Draw foot
                foot_angle = leg_angle + side * math.pi/4
                foot_end_x = leg_end_x + math.cos(foot_angle) * 10
                foot_end_y = leg_end_y + math.sin(foot_angle) * 10
                pygame.draw.line(surface, LIGHT_BROWN, (leg_end_x, leg_end_y), 
                                (foot_end_x, foot_end_y), 2)
        
        # Draw tail
        tail_start_x = self.x - math.cos(self.direction) * (body_length/2 - 10)
        tail_start_y = self.y - math.sin(self.direction) * (body_length/2 - 10)
        prev_x, prev_y = tail_start_x, tail_start_y
        
        for i in range(tail_segments):
            segment_angle = self.direction + math.pi + 0.3 * math.sin(self.tail_phase + i*0.5)
            segment_length = tail_length / tail_segments
            segment_end_x = prev_x + math.cos(segment_angle) * segment_length
            segment_end_y = prev_y + math.sin(segment_angle) * segment_length
            
            pygame.draw.line(surface, DARK_BROWN, (prev_x, prev_y), 
                            (segment_end_x, segment_end_y), 5 - i)
            
            prev_x, prev_y = segment_end_x, segment_end_y
        
        # Draw stinger at the end of tail
        stinger_angle1 = segment_angle + math.pi/6
        stinger_angle2 = segment_angle - math.pi/6
        stinger_length = 15
        
        stinger1_x = segment_end_x + math.cos(stinger_angle1) * stinger_length
        stinger1_y = segment_end_y + math.sin(stinger_angle1) * stinger_length
        stinger2_x = segment_end_x + math.cos(stinger_angle2) * stinger_length
        stinger2_y = segment_end_y + math.sin(stinger_angle2) * stinger_length
        
        pygame.draw.line(surface, DARK_BROWN, (segment_end_x, segment_end_y), 
                        (stinger1_x, stinger1_y), 2)
        pygame.draw.line(surface, DARK_BROWN, (segment_end_x, segment_end_y), 
                        (stinger2_x, stinger2_y), 2)
        
        # Draw pincers
        for side in [-1, 1]:
            pincer_base_x = head_x + math.cos(self.direction + math.pi/2) * side * (body_width/3)
            pincer_base_y = head_y + math.sin(self.direction + math.pi/2) * side * (body_width/3)
            
            pincer_angle = self.direction + side * (math.pi/3 + 0.3 * math.sin(self.pincers_phase))
            pincer_length = 30
            pincer_end_x = pincer_base_x + math.cos(pincer_angle) * pincer_length
            pincer_end_y = pincer_base_y + math.sin(pincer_angle) * pincer_length
            
            pygame.draw.line(surface, LIGHT_BROWN, (head_x, head_y), 
                            (pincer_base_x, pincer_base_y), 4)
            pygame.draw.line(surface, LIGHT_BROWN, (pincer_base_x, pincer_base_y), 
                            (pincer_end_x, pincer_end_y), 3)
            
            # Draw pincer claw
            claw_angle = pincer_angle + side * math.pi/4
            claw_length = 15
            claw_end_x = pincer_end_x + math.cos(claw_angle) * claw_length
            claw_end_y = pincer_end_y + math.sin(claw_angle) * claw_length
            
            pygame.draw.line(surface, LIGHT_BROWN, (pincer_end_x, pincer_end_y), 
                            (claw_end_x, claw_end_y), 2)

# Create scorpion
scorpion = Scorpion(WIDTH // 2, HEIGHT // 2)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with sand color
    screen.fill(GROUND)
    
    # Draw some sand texture
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        pygame.draw.circle(screen, SAND, (x, y), size)
    
    # Update and draw scorpion
    scorpion.update()
    scorpion.draw(screen)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()