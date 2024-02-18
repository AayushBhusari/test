import pygame
import random
import time
import sys

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 50
VELO = 5
enemy_velo = 3
initial_spawn_frequency = 4
increase_spawn_rate_interval = 20  # Increase spawn rate every 20 seconds
spawn_rate_increment = 1  # Increment spawn rate by 1 unit

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for sound
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Warrior")

# Load images
spaceship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("./Assets/spaceship_red.png"), (55, 40)), 180)
enemy_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("./Assets/enemy.png"), (55, 40)), 180)
bgImage = pygame.image.load("./Assets/space.png")
bgImage = pygame.transform.scale(bgImage, (WIDTH, HEIGHT))

# Load sounds
bullet_shot_sound = pygame.mixer.Sound("./Assets/bullet_shot.mp3")
enemy_destroyed_sound = pygame.mixer.Sound("./Assets/enemy_destroyed.mp3")

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 15)
        self.color = (255, 0, 0)

    def move(self):
        self.rect.y -= VELO * 2  # Bullets move upward

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Drawing on the screen
def draw_window(ship, enemies, bullets, destroyed_count):
    WIN.blit(bgImage, (0, 0))
    WIN.blit(spaceship, (ship.x, ship.y))
    for enemy in enemies:
        WIN.blit(enemy_img, enemy)
    for bullet in bullets:
        bullet.draw(WIN)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Destroyed: {destroyed_count}", True, WHITE)
    WIN.blit(text, (10, 10))
    pygame.display.update()  # Update the display

# Handle spaceship movements and prevent going out of the window
def handle_movement(keys_pressed, ship):
    if keys_pressed[pygame.K_LEFT] and ship.x - VELO > 0:
        ship.x -= VELO
    if keys_pressed[pygame.K_RIGHT] and ship.x + VELO + ship.width < WIDTH:
        ship.x += VELO
    if keys_pressed[pygame.K_UP] and ship.y - VELO > 0:
        ship.y -= VELO
    if keys_pressed[pygame.K_DOWN] and ship.y + VELO + ship.height < HEIGHT:
        ship.y += VELO

# Generate a random enemy position
def generate_enemy():
    x = random.randint(0, WIDTH - 55)
    y = 10
    return pygame.Rect(x, y, 55, 40)

# Check for collisions between ship and enemies
def check_collisions(ship, enemies):
    for enemy in enemies:
        if ship.colliderect(enemy):
            return True  # Collision detected
    return False  # No collision

# Game over screen
# Game over screen
# Game over screen
def game_over(destroyed_count):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    count_text = font.render(f"Destroyed: {destroyed_count}", True, WHITE)
    prompt_text = font.render("Press Enter to Restart", True, WHITE)  # Added restart prompt
    game_over_time = time.time() + 5  # Set the game over screen time to 5 seconds

    while time.time() < game_over_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game when the close button is pressed
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return False  # User pressed enter, restart the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Quit the game when the 'Esc' button is pressed
                    sys.exit()

        WIN.blit(bgImage, (0, 0))
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))
        WIN.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2 + 20))
        WIN.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2 + 100))  # Added restart prompt
        pygame.display.update()

    return False  # User did not press enter within the time



# Handle bullet creation
def handle_bullet(bullets, ship, bullet_fired):
    keys = pygame.key.get_pressed()

    # Check if the spacebar is pressed and no bullet is currently in motion
    if keys[pygame.K_SPACE] and not bullet_fired:
        bullet_x = ship.x + ship.width // 2 - 2  # Center the bullet on the spaceship
        bullet_y = ship.y
        bullets.append(Bullet(bullet_x, bullet_y))
        bullet_shot_sound.play()  # Play the bullet shot sound
        return True  # Set the bullet_fired flag to True

    # Reset the bullet_fired flag when the spacebar is released
    if not keys[pygame.K_SPACE]:
        return False

    return bullet_fired  # If the bullet is already in motion, do nothing

# Main game loop
def main():
    while True:
        ship = pygame.Rect((WIDTH / 2) - (55 / 2), 550, 55, 40)
        enemies = []
        bullets = []
        destroyed_count = 0
        bullet_fired = False  # Flag to track whether a bullet is currently in motion

        clock = pygame.time.Clock()
        is_running = True
        start_time = time.time()  # Get the start time of the game
        next_spawn_increase_time = start_time + increase_spawn_rate_interval
        spawn_frequency = initial_spawn_frequency

        while is_running:
            clock.tick(FPS)

            # Calculate the elapsed time since the start of the game
            elapsed_time = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Quit the game when the close button is pressed
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()  # Quit the game when the 'Esc' button is pressed
                        sys.exit()

            keys_pressed = pygame.key.get_pressed()
            handle_movement(keys_pressed, ship)

            # Handle bullet creation
            bullet_fired = handle_bullet(bullets, ship, bullet_fired)

            # Increase spawn rate every 20 seconds
            if time.time() > next_spawn_increase_time:
                spawn_frequency += spawn_rate_increment
                next_spawn_increase_time += increase_spawn_rate_interval

            if random.randint(1, 100) < spawn_frequency:
                enemies.append(generate_enemy())

            # Update enemy positions
            for enemy in enemies:
                enemy.y += enemy_velo

            # Update bullet positions
            for bullet in bullets:
                bullet.move()

            # Remove enemies that go out of the screen
            enemies = [enemy for enemy in enemies if enemy.y < HEIGHT]

            # Check for collisions
            for bullet in bullets:
                for enemy in enemies[:]:  # Use a copy of the enemies list to iterate
                    if bullet.rect.colliderect(enemy):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        destroyed_count += 1
                        enemy_destroyed_sound.play()  # Play the enemy destroyed sound

            # Check for collisions with ship
            if check_collisions(ship, enemies):
                is_running = game_over(destroyed_count)  # Set is_running based on game_over result

            draw_window(ship, enemies, bullets, destroyed_count)

if __name__ == "__main__":
    main()
