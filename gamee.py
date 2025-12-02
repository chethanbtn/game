import pygame
import sys
import random 

pygame.init()

# -------------------- SCREEN SETUP --------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Mr.Landa")

# -------------------- AUDIO SETUP --------------------
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")  # main menu music
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # loop forever

# -------------------- COLORS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# -------------------- FONTS --------------------
font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 20)

# Helper function for centered text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# -------------------- INSTRUCTIONS SCREEN --------------------
def show_instructions():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Instructions:", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
        draw_text("Use arrow keys to move.", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
        draw_text("Press space to jump.", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text("Click anywhere to return.", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

        pygame.display.flip()

        # Return to title when clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

# -------------------- CREDITS SCREEN --------------------
def show_credit():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Credits:", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
        draw_text("Lead Designer & Coder: Chethan Krishan Battini", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
        draw_text("Lead Programmer & Storyboard: William Arney", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text("Click anywhere to return.", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

        pygame.display.flip()

        # Return to menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

# -------------------- TITLE SCREEN --------------------
def title_screen():
    running = True
    while running:
        screen.fill(BLACK)

        # Game title
        draw_text("The Adventures of Mr.Landa", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        # Button rectangles
        start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
        instructions_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        credits_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 125, 200, 50)

        # Draw buttons
        pygame.draw.rect(screen, WHITE, start_button_rect)
        draw_text("Start Game", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.draw.rect(screen, WHITE, instructions_rect)
        draw_text("Instructions", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75)

        pygame.draw.rect(screen, WHITE, credits_rect)
        draw_text("Credits", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

        pygame.display.flip()

        # Button interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False
                    game_loop()
                elif instructions_rect.collidepoint(event.pos):
                    show_instructions()
                elif credits_rect.collidepoint(event.pos):
                    show_credit()

# -------------------- MAIN GAME LOOP --------------------
def game_loop():
    clock = pygame.time.Clock()

    # Player life system
    lives = 3
    max_lives = 3

    # --- Level-specific music ---
    pygame.mixer.music.stop()
    pygame.mixer.music.load("level 1 music.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    # --- Load images ---
    hallway_img = pygame.image.load("hallway.jpeg").convert()
    hallway_img = pygame.transform.scale(hallway_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    student_img = pygame.image.load("student.png").convert_alpha()
    landa_img = pygame.image.load("landa.png").convert_alpha()
    full_heart = pygame.image.load("Heart.png").convert_alpha()
    broken_heart = pygame.image.load("Broken Heart.png").convert_alpha()

    # Resize heart icons
    heart_size = (40, 40)
    full_heart = pygame.transform.scale(full_heart, heart_size)
    broken_heart = pygame.transform.scale(broken_heart, heart_size)

    # Resize player sprite
    PLAYER_W = 70
    PLAYER_H = 130
    landa_img = pygame.transform.scale(landa_img, (PLAYER_W, PLAYER_H))
    landa_img = pygame.transform.flip(landa_img, True, False)  # flip to face right direction

    # Player start position & movement vars
    player_x = 100
    player_y = SCREEN_HEIGHT - PLAYER_H - 30
    player_speed = 8
    player_rect = pygame.Rect(player_x, player_y, PLAYER_W, PLAYER_H)

    # Jump mechanics
    is_jumping = False
    jump_velocity = 0
    gravity = 1
    jump_height = 20

    # Obstacles
    students = []
    spawn_timer = 0
    spawn_interval = 90  # student spawn rate

    # Win condition
    distance = 0
    distance_goal = 1500

    # Background scroll offset
    bg_scroll = 3
    bg_speed = 15 

    running = True
    while running:
        clock.tick(60)

        # -------------------- BACKGROUND SCROLL --------------------
        bg_scroll -= bg_speed
        if bg_scroll <= -SCREEN_WIDTH:
            bg_scroll = 0

        screen.blit(hallway_img, (bg_scroll, 0))
        screen.blit(hallway_img, (bg_scroll + SCREEN_WIDTH, 0))

        # -------------------- SPAWN STUDENTS --------------------
        spawn_timer += 1
        if spawn_timer > spawn_interval:
            student_w = random.randint(35, 60)
            student_h = random.randint(40, 70)

            student_rect = pygame.Rect(
                SCREEN_WIDTH,
                SCREEN_HEIGHT - student_h - 30,
                student_w,
                student_h
            )

            student_speed = random.randint(6, 12)
            students.append((student_rect, student_speed))
            spawn_timer = 0

        # -------------------- PLAYER MOVEMENT --------------------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x = max(0, player_x - player_speed)

        if keys[pygame.K_RIGHT]:
            player_x = min(SCREEN_WIDTH - PLAYER_W, player_x + player_speed)

        if not is_jumping and keys[pygame.K_SPACE]:
            is_jumping = True
            jump_velocity = -jump_height  # upward force

        # Jump physics
        if is_jumping:
            player_y += jump_velocity
            jump_velocity += gravity  # gravity pulls down

            # Hit the ground
            if player_y >= SCREEN_HEIGHT - PLAYER_H - 30:
                player_y = SCREEN_HEIGHT - PLAYER_H - 30
                is_jumping = False

        # Update rect
        player_rect.x = player_x
        player_rect.y = player_y

        # Draw player
        screen.blit(landa_img, (player_x, player_y))

        # -------------------- STUDENT MOVEMENT & COLLISION --------------------
        for student, speed in students[:]:
            student.x -= speed

            # Draw student resized to its random size
            scaled_student_img = pygame.transform.scale(student_img, (student.width, student.height))
            screen.blit(scaled_student_img, (student.x, student.y))

            # Collision: lose life
            if player_rect.colliderect(student):
                lives -= 1
                students.remove((student, speed))

                # Show hit text ONLY if player still has lives left
                if lives > 0:
                    draw_text("Ouch! You hit a student! -1 life", font_medium, (255, 100, 100),
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.delay(600)

                # Game over screen
                if lives <= 0:
                    draw_text("GAME OVER! You have been sued by the students!", font_medium, (255, 0, 0),
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return


            # Remove if off screen
            if student.x < -student.width:
                students.remove((student, speed))

        # -------------------- DISTANCE & UI --------------------
        distance += 0.5

        draw_text(f"Distance: {int(distance)} / {distance_goal} m",
                  font_small, WHITE, SCREEN_WIDTH // 2, 30)

        # Draw hearts (life system)
        for i in range(max_lives):
            x = 20 + i * 50
            y = 20
            if i < lives:
                screen.blit(full_heart, (x, y))
            else:
                screen.blit(broken_heart, (x, y))

        # -------------------- LEVEL COMPLETE --------------------
        if distance >= distance_goal:
            draw_text("Level One Completed!", font_medium, (0, 255, 0),
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        pygame.display.flip()

        # Quit handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# -------------------- START GAME --------------------
title_screen()
