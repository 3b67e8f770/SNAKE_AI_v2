#!/usr/bin/python3
import pygame
import random
import sys
from collections import deque
from settings import *


class Snake:
    def __init__(self, initial_segments, color, controls, initial_direction, is_ai=True):
        self.color = color
        self.controls = controls
        # Teraz body[0] to głowa, appendleft dodaje nową głowę
        self.body = deque(initial_segments)
        self.length = len(initial_segments)
        # Głowa to body[0]
        self.x, self.y = self.body[0]
        self.dx, self.dy = initial_direction
        self.score = 0
        self.is_ai = is_ai

    def handle_keys(self, key):
        if key == self.controls['up'] and self.dy == 0:
            self.dx, self.dy = 0, -BLOCK_SIZE
        elif key == self.controls['down'] and self.dy == 0:
            self.dx, self.dy = 0, BLOCK_SIZE
        elif key == self.controls['left'] and self.dx == 0:
            self.dx, self.dy = -BLOCK_SIZE, 0
        elif key == self.controls['right'] and self.dx == 0:
            self.dx, self.dy = BLOCK_SIZE, 0

    def ai_move(self):
        #Random move
        possible_directions = [
            (0, -BLOCK_SIZE), (0, BLOCK_SIZE), 
            (-BLOCK_SIZE, 0), (BLOCK_SIZE, 0)
        ]
        
        # cannot tun back
        valid_directions = [
            d for d in possible_directions 
            if not (d[0] == -self.dx and d[1] == -self.dy)
        ]
        
        # Wybieramy losowy kierunek z tych "bezpiecznych" konstrukcyjnie
        self.dx, self.dy = random.choice(valid_directions)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.body.appendleft([self.x, self.y])
        if len(self.body) > self.length:
            self.body.pop()
        
        # tail
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

    def check_collision(self, other_snake_body):
        body_list = list(self.body)
        #borders
        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT or body_list.count([self.x, self.y]) > 1:
            self.score -= 5  # you died
            return True
        
        # oponent body
        elif [self.x, self.y] in other_snake_body:
            self.score -= 5  # Obiecane -5 punktów
            return True
        
        return False
    
def show_info(surface, s1, s2):
    font = pygame.font.SysFont(F_FONT, 20)
    # Wyświetlanie wyników i statusu AI
    mode1 = "AI" if s1.is_ai else "HUMAN"
    mode2 = "AI" if s2.is_ai else "HUMAN"
    
    val_1 = font.render(f"P1 ({mode1}): {s1.score}", True, COLOR_GREEN)
    val_2 = font.render(f"P2 ({mode2}): {s2.score}", True, COLOR_RED)
    hint = font.render("Press [1] to switch P1 contol or [2] to switch P2 control ", True, COLOR_FONT)
    
    surface.blit(val_1, [10, 10])
    surface.blit(val_2, [WIDTH - 180, 10])
    surface.blit(hint, [WIDTH // 2 - 120, HEIGHT - 30])

def game_loop():
    pygame.init()
    dis = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake AI - Bot Testing')
    clock = pygame.time.Clock()

    s1_pos = [[WIDTH // 4, HEIGHT // 4], [WIDTH // 4 - BLOCK_SIZE, HEIGHT // 4], [WIDTH // 4 - 2 * BLOCK_SIZE, HEIGHT // 4]]
    SNAKE_1 = Snake(s1_pos, COLOR_GREEN, {
        'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d
    }, (BLOCK_SIZE, 0), is_ai=AI_P1)

    s2_pos = [[3 * WIDTH // 4, 3 * HEIGHT // 4], [3 * WIDTH // 4 + BLOCK_SIZE, 3 * HEIGHT // 4], [3 * WIDTH // 4 + 2 * BLOCK_SIZE, 3 * HEIGHT // 4]]
    SNAKE_2 = Snake(s2_pos, COLOR_RED, {
        'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT
    }, (-BLOCK_SIZE, 0), is_ai=AI_P2)

    # FOOD
    def spawn_food():
        fx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE
        fy = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE
        return fx, fy

    food_x, food_y = spawn_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #  AI/Human
                if event.key == pygame.K_1:
                    SNAKE_1.is_ai = not SNAKE_1.is_ai
                if event.key == pygame.K_2:
                    SNAKE_2.is_ai = not SNAKE_2.is_ai

                # Human playing
                SNAKE_1.handle_keys(event.key)
                SNAKE_2.handle_keys(event.key)
       
        # AI playing
        if SNAKE_1.is_ai:
            SNAKE_1.ai_move()
        if SNAKE_2.is_ai:
            SNAKE_2.ai_move()
      
        SNAKE_1.move()
        SNAKE_2.move()

        # collision
        col_1 = SNAKE_1.check_collision(list(SNAKE_2.body))
        col_2 = SNAKE_2.check_collision(list(SNAKE_1.body))

        if col_1 or col_2:
            print(f"Collision! Results -> Player1: {SNAKE_1.score}, Player2: {SNAKE_2.score}")
            pygame.time.delay(1000) 
            game_loop() # Restart

        # FOOD?
        for s in [SNAKE_1, SNAKE_2]:
            if s.x == food_x and s.y == food_y:
                s.length += 1
                s.score += 1
                food_x, food_y = spawn_food()

        # Rendering
        dis.fill(COLOR_BG)
        pygame.draw.rect(dis, COLOR_FOOD, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        SNAKE_1.draw(dis)
        SNAKE_2.draw(dis)
        show_info(dis, SNAKE_1, SNAKE_2)
        
        pygame.display.update()
        clock.tick(SPEED)

if __name__ == "__main__":
    game_loop()