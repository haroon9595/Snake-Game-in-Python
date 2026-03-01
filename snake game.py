import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.grow_pending = 2  # Start with length 3
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # Can't turn 180 degrees
        self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Check for collision with self
        if new_position in self.positions[1:]:
            self.reset()
            return False
        
        self.positions.insert(0, new_position)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
            
        return True
    
    def grow(self):
        self.grow_pending += 1
        self.length += 1
        self.score += 10
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Draw snake body
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            
            # Head is a different color
            if i == 0:
                pygame.draw.rect(surface, BLUE, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)
            else:
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.snake = Snake()
        self.food = Food()
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn(RIGHT)
                elif event.key == pygame.K_r:
                    self.snake.reset()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        if not self.snake.move():
            return
        
        # Check if snake ate food
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food.randomize_position()
            # Make sure food doesn't appear on snake
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WIDTH, y))
        
        # Draw game elements
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw instructions
        instructions = self.font.render("Use arrow keys to move, R to reset, ESC to quit", True, WHITE)
        self.screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 30))
        
        pygame.display.update()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()