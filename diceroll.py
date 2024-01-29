import time

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (150, 216, 230)
BUTTON_COLOR = (173, 250, 250)
FONT_SIZE = 36

# Fonts
font = pygame.font.Font(None, FONT_SIZE)
victory_font = pygame.font.Font("Victory.ttf", 48)  # Adjusted font size for victory message
PINK = (255, 105, 180)  # Pink color

# Particle class for visual effects
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = [random.uniform(-2, 2), random.uniform(-2, 2)]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

# Function to roll the dice
def roll_dice():
    return random.randint(1, 100)


# Function to draw text on the screen
def draw_text(text, x, y, color, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to create particles
def create_particles(x, y):
    particles = pygame.sprite.Group()
    for _ in range(50):
        particle = Particle(x, y)
        particles.add(particle)
    return particles

# Input box class for player names
class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.typing_index = 0  # Index for typing animation

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.typing_index = min(len(self.text), self.typing_index)  # Keep typing index within text length
            else:
                self.active = False
            self.color = (255, 255, 255) if self.active else (200, 200, 200)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.typing_index = max(0, self.typing_index - 1)  # Decrement typing index
                else:
                    self.text = self.text[:self.typing_index] + event.unicode + self.text[self.typing_index:]
                    self.typing_index += 1  # Increment typing index
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width


    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Rolling Game")
clock = pygame.time.Clock()

# Create sprite groups
all_sprites = pygame.sprite.Group()

# Create input boxes
player1_input = InputBox(WIDTH // 4 - 150, HEIGHT // 2, 120, 40, 'Player 1')  # Adjust x-coordinate and width
player2_input = InputBox(WIDTH // 4 + WIDTH // 2 - 100, HEIGHT // 2, 120, 40, 'Player 2')  # Adjust x-coordinate and width

# Main game loop
def start_screen():
    smooth_text = ""
    smooth_font = pygame.font.Font(None, 24)
    smooth_rect = pygame.Rect(WIDTH // 2 - 100, 3 * HEIGHT // 4, 200, 50)
    smooth_color = WHITE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            player1_input.handle_event(event)
            player2_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player1_input.rect.collidepoint(event.pos) or player2_input.rect.collidepoint(event.pos):
                    continue

                if smooth_rect.collidepoint(event.pos):
                    if smooth_text.lower() == "smooth":
                        return player1_input.text, player2_input.text

                all_sprites.empty()
                screen.fill(DARK_GRAY)
                draw_text("Dice Rolling Game", WIDTH // 2, HEIGHT // 4, WHITE, font)
                draw_text("Enter player names and type 'smooth' to start", WIDTH // 2, HEIGHT // 2, WHITE, font)

                player1_input.update()
                player2_input.update()
                player1_input.draw(screen)
                player2_input.draw(screen)

                pygame.draw.rect(screen, BUTTON_COLOR, smooth_rect)
                draw_text("START", WIDTH // 2, 3 * HEIGHT // 4 + 25, smooth_color, font)

                pygame.display.flip()

                if player1_input.text != 'Player 1' and player2_input.text != 'Player 2':
                    return player1_input.text, player2_input.text

        all_sprites.update()
        screen.fill(DARK_GRAY)
        player1_input.update()
        player2_input.update()
        player1_input.draw(screen)
        player2_input.draw(screen)
        pygame.draw.rect(screen, BUTTON_COLOR, smooth_rect)
        draw_text("START", WIDTH // 2, 3 * HEIGHT // 4 + 25, smooth_color, font)
        pygame.display.flip()
        clock.tick(FPS)


def main(player1_name, player2_name):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.empty()
                player1_roll = roll_dice()
                player2_roll = roll_dice()
                particles = create_particles(WIDTH // 2, HEIGHT // 2)
                all_sprites.add(particles)
                draw_text(f"{player1_name} rolled: {player1_roll}", WIDTH // 2, HEIGHT // 4, WHITE, font)
                draw_text(f"{player2_name} rolled: {player2_roll}", WIDTH // 2, 3 * HEIGHT // 4, WHITE, font)

                if player1_roll > player2_roll:
                    winner_message = f"{player1_name} WINS!\nFlawless Victory!"
                    draw_text(winner_message, WIDTH // 2, HEIGHT // 4 + 60, PINK, victory_font)
                elif player2_roll > player1_roll:
                    winner_message = f"{player2_name} WINS!\nOutsmarted!"
                    draw_text(winner_message, WIDTH // 2, 3 * HEIGHT // 4 + 60, PINK, victory_font)
                else:
                    draw_text("It's a tie!", WIDTH // 2, HEIGHT // 2 + 60, PINK, victory_font)

                pygame.display.flip()
                pygame.time.delay(3000)

        all_sprites.update()
        screen.fill(DARK_GRAY)
        all_sprites.draw(screen)
        pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - 100, HEIGHT - 80, 200, 50))
        draw_text("Roll", WIDTH // 2, HEIGHT - 55, WHITE, font)
        pygame.display.flip()
        clock.tick(FPS)



def main(player1_name, player2_name):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clear previous sprites
                all_sprites.empty()

                # Roll the dice and create particles
                player1_roll = roll_dice()
                player2_roll = roll_dice()
                particles = create_particles(WIDTH // 2, HEIGHT // 2)
                all_sprites.add(particles)

                # Display the results
                draw_text(f"{player1_name} rolled: {player1_roll}", WIDTH // 2, HEIGHT // 4, WHITE, font)
                draw_text(f"{player2_name} rolled: {player2_roll}", WIDTH // 2, 3 * HEIGHT // 4, WHITE, font)

                # Determine the winner
                if player1_roll > player2_roll:
                    winner_message = f"{player1_name} WINS!\nFlawless Victory!"
                    draw_text(winner_message, WIDTH // 2, HEIGHT // 4 + 60, PINK, victory_font)
                elif player2_roll > player1_roll:
                    winner_message = f"{player2_name} WINS!\nOutsmarted!"
                    draw_text(winner_message, WIDTH // 2, 3 * HEIGHT // 4 + 60, PINK, victory_font)
                else:
                    draw_text("It's a tie!", WIDTH // 2, HEIGHT // 2 + 60, PINK, victory_font)

                # Update the screen
                pygame.display.flip()

                # Wait for a moment before clearing the screen
                pygame.time.delay(3000)

        # Update particles
        all_sprites.update()

        # Draw background
        screen.fill(DARK_GRAY)

        # Draw sprites
        all_sprites.draw(screen)

        # Draw roll button
        pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - 100, HEIGHT - 80, 200, 50))
        draw_text("Roll", WIDTH // 2, HEIGHT - 55, WHITE, font)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

player1, player2 = start_screen()
main(player1, player2)
