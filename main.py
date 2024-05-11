import pygame
import random
 
 
# Initialize Pygame
pygame.init()
 
 
# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 836, 660
FPS = 80
GRAVITY = 0.5
JUMP_STRENGTH = -10
SCROLL_SPEED = 5
PIPE_WIDTH = 70
PIPE_GAP = 140
PIPE_FREQUENCY = 1500  # milliseconds
BACKGROUND_COLOR = (255, 255, 255)
 
 
# Load images
BACKGROUND_IMG = pygame.image.load('background.png')
GROUND_IMG = pygame.image.load('the-ground.png')
BUTTON_IMG = pygame.image.load('restart.png')
GAME_OVER_IMG = pygame.image.load('gameover.png')
BIRD_IMAGES = [pygame.image.load(f'bluebird{num}.png') for num in range(1, 4)]
PIPE_IMAGE = pygame.image.load('pipe-red.png')
 
 
# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird - The Pycodes')
 
 
# Game variables
ground_scroll = 0
score = 0
is_flying = False
is_game_over = False
last_pipe_time = pygame.time.get_ticks() - PIPE_FREQUENCY
 
 
# Define font
game_font = pygame.font.SysFont('Arial', 60)
 
 
# Define sprite groups
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
 
 
class Player(pygame.sprite.Sprite):
   def __init__(self, x, y):
       super().__init__()
       self.images = BIRD_IMAGES
       self.current_image = 0
       self.animation_time = pygame.time.get_ticks()
       self.image = self.images[self.current_image]
       self.rect = self.image.get_rect(center=(x, y))
       self.velocity = 0
       self.clicked = False
 
 
   def animate(self):
       if pygame.time.get_ticks() - self.animation_time > 100:
           self.current_image = (self.current_image + 1) % len(self.images)
           self.animation_time = pygame.time.get_ticks()
       self.image = self.images[self.current_image]
 
 
   def update(self):
       global is_flying, is_game_over
       if is_flying:
           self.velocity += GRAVITY
           self.velocity = min(self.velocity, 8)
           if self.rect.bottom < 588:
               self.rect.y += int(self.velocity)
       if not is_game_over:
           if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
               self.clicked = True
               self.velocity = JUMP_STRENGTH
           if pygame.mouse.get_pressed()[0] == 0:
               self.clicked = False
       self.animate()
       self.rotate()
 
 
   def rotate(self):
       self.image = pygame.transform.rotate(self.images[self.current_image], self.velocity * -2)
 
 
class Pipe(pygame.sprite.Sprite):
   def __init__(self, x, y, position):
       super().__init__()
       self.image = pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, SCREEN_HEIGHT))
       self.rect = self.image.get_rect()
       if position == 1:
           self.image = pygame.transform.flip(self.image, False, True)
           self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
       else:
           self.rect.topleft = [x, y + int(PIPE_GAP / 2)]
       self.passed = False  # Track if the bird has passed this pipe
 
 
   def update(self):
       if not is_game_over:
           self.rect.x -= SCROLL_SPEED
       if self.rect.right < 0:
           self.kill()
 
 
class Button:
   def __init__(self, x, y, image):
       self.image = image
       self.rect = self.image.get_rect(topleft=(x, y))
 
 
   def draw(self):
       action = False
       pos = pygame.mouse.get_pos()
       if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
           action = True
       screen.blit(self.image, self.rect)
       return action
 
 
def draw_text(text, font, text_color, x, y):
   text_surface = font.render(text, True, text_color)
   screen.blit(text_surface, (x, y))
 
 
def reset_game():
   pipe_group.empty()
   bird.rect.x = 100
   bird.rect.y = SCREEN_HEIGHT // 2
   global score, is_flying, is_game_over
   score = 0
   is_flying = False
   is_game_over = False
 
 
def check_collision():
   global is_game_over
   if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0 or bird.rect.bottom >= 588:
       is_game_over = True
 
 
def score_update():
   global score
   for pipe in pipe_group:
       if bird.rect.centerx > pipe.rect.centerx and not pipe.passed:
           score += 1
           pipe.passed = True
 
 
def create_pipe():
   global last_pipe_time
   time_now = pygame.time.get_ticks()
   if time_now - last_pipe_time > PIPE_FREQUENCY:
       pipe_height = random.randint(-100, 100)
       bottom_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
       top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
       pipe_group.add(bottom_pipe)
       pipe_group.add(top_pipe)
       last_pipe_time = time_now
 
 
# Initialize the player
bird = Player(100, SCREEN_HEIGHT // 2)
bird_group.add(bird)
 
 
# Initialize the restart button
restart_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, BUTTON_IMG)
 
 
# Main game loop
run = True
clock = pygame.time.Clock()
 
 
while run:
   clock.tick(FPS)
   screen.fill(BACKGROUND_COLOR)
   screen.blit(BACKGROUND_IMG, (0, 0))
 
 
   bird_group.draw(screen)
   bird_group.update()
   pipe_group.draw(screen)
   pipe_group.update()
 
 
   # Draw and scroll the ground
   screen.blit(GROUND_IMG, (ground_scroll, SCREEN_HEIGHT - 72))
   if not is_game_over:
       ground_scroll -= SCROLL_SPEED
   if abs(ground_scroll) > 35:
       ground_scroll = 0
 
 
   # Score display
   draw_text(f'Score: {score}', game_font, (255, 255, 255), SCREEN_WIDTH // 2 - 100, 20)
 
 
   if is_flying and not is_game_over:
       create_pipe()
 
 
   check_collision()
   score_update()
 
 
   if is_game_over:
       screen.blit(GAME_OVER_IMG, (SCREEN_WIDTH // 2 - GAME_OVER_IMG.get_width() // 2, SCREEN_HEIGHT // 2 - GAME_OVER_IMG.get_height() // 2))
       if restart_button.draw():
           reset_game()
 
 
   # Handle events
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
       if event.type == pygame.MOUSEBUTTONDOWN and not is_flying and not is_game_over:
           is_flying = True
 
 
   pygame.display.update()
 
 
pygame.quit()
