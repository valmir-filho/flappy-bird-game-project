import pygame
import random

# Initialize Pygame.
pygame.init()

# Screen settings.
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors.
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)  # More realistic green for the pipe.
DARK_GREEN = (0, 100, 0)  # Darker green for depth effect.

# Game variables.
gravity = 0.5
bird_y = HEIGHT // 2
bird_x = 50
bird_velocity = 0
pipe_width = 70
pipe_gap = 200
pipes = []
score = 0

# Load bird image.
bird_image = pygame.image.load('bird.png')  # Replace 'bird.png' with your image path.
bird_image = pygame.transform.scale(bird_image, (50, 35))  # Adjust bird image size.


# Function to create pipes.
def create_pipe():
    height = random.randint(50, HEIGHT - 150)
    top = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return {'top': top, 'bottom': bottom, 'scored': False}


# Function to draw detailed pipes.
def draw_pipe(pipe):
    # Draw top pipe.
    pygame.draw.rect(screen, GREEN, pipe['top'])  # Top pipe body.
    pygame.draw.rect(screen, DARK_GREEN, (pipe['top'].x, pipe['top'].bottom - 10, pipe_width, 10))  # Dark bottom border.
    pygame.draw.ellipse(screen, GREEN, (pipe['top'].x - 10, pipe['top'].bottom - 20, pipe_width + 20, 40))  # Pipe cap.
    # Draw bottom pipe.
    pygame.draw.rect(screen, GREEN, pipe['bottom'])  # Bottom pipe body.
    pygame.draw.rect(screen, DARK_GREEN, (pipe['bottom'].x, pipe['bottom'].top, pipe_width, 10))  # Dark top border.
    pygame.draw.ellipse(screen, GREEN, (pipe['bottom'].x - 10, pipe['bottom'].top - 20, pipe_width + 20, 40))  # Pipe cap.


# Main game loop.
def game_loop():
    global bird_y, bird_velocity, score, pipes
    clock = pygame.time.Clock()
    pipes = []  # Clear pipe list.
    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0
    pipe_timer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = -10  # Jump.
        bird_velocity += gravity
        bird_y += bird_velocity
        # Create pipes.
        pipe_timer += 1
        if pipe_timer > 90:
            pipes.append(create_pipe())
            pipe_timer = 0
        # Update pipe positions.
        for pipe in pipes:
            pipe['top'].x -= 5
            pipe['bottom'].x -= 5
        # Remove pipes that are off-screen.
        pipes = [pipe for pipe in pipes if pipe['top'].x > -pipe_width]
        # Check for collisions.
        bird_rect = pygame.Rect(bird_x, bird_y, 50, 35)  # Adjust rectangle to image size.
        for pipe in pipes:
            if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
                game_loop()  # Restart game if collision occurs.
        # Count points.
        for pipe in pipes:
            if pipe['top'].x + pipe_width < bird_x and not pipe['scored']:
                score += 1
                pipe['scored'] = True
        # Check if the bird went off-screen.
        if bird_y > HEIGHT or bird_y < 0:
            game_loop()
        # Draw everything.
        screen.fill(WHITE)  # Set background to white.
        screen.blit(bird_image, (bird_x, bird_y))  # Draw bird image.
        # Draw detailed pipes.
        for pipe in pipes:
            draw_pipe(pipe)
        # Display score.
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))  # Black score text.
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(30)
if __name__ == "__main__":
    game_loop()
