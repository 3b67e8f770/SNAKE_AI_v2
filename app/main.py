#!/usr/bin/python3
import pygame
import random
import sys
from snake import Snake
from settings import *

    
def show_info(surface, snakes, current_speed):
    font = pygame.font.SysFont(F_FONT, 20)
    for i, (name, snake) in enumerate(snakes.items()):
        mode = "AI" if snake.is_ai else "HUM"
        text = f"{name} ({mode}): {snake.score}  R:{round(snake.total_reward, 1)}"
        surf = font.render(text, True, snake.color)

        #Players info
        x = 10 if i % 2 == 0 else WIDTH - 260
        y = 10 if i < 2 else HEIGHT - 30
        surface.blit(surf, [x, y])
    
        surf_speed = font.render(f"Speed: {current_speed} (9: + | 0: -)", True, COLOR_FONT)
        surface.blit(surf_speed, [WIDTH // 2 - 70, HEIGHT - 60])

def run_game():
    current_speed = SPEED
    while True:
        current_speed = game_loop(current_speed)
        if current_speed is None: #end game
            break

def game_loop(current_speed):
    pygame.init()
    dis = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake AI - Multisnake')
    clock = pygame.time.Clock()
    
    #snakes generations:
    active_player_keys = list(PLAYERS.keys())[:NUM_PLAYERS]
    snakes = {key: Snake(key, *PLAYERS[key]) for key in active_player_keys}
  
    # FOOD
    def spawn_food():
        return (round(random.randrange(0, WIDTH - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE,
                round(random.randrange(0, HEIGHT - BLOCK_SIZE) / float(BLOCK_SIZE)) * BLOCK_SIZE)

    food_x, food_y = spawn_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: snakes['SNAKE_1'].is_ai = not snakes['SNAKE_1'].is_ai
                if event.key == pygame.K_2: snakes['SNAKE_2'].is_ai = not snakes['SNAKE_2'].is_ai

                #Speed changing
                if event.key == pygame.K_9:
                    current_speed *= 2
                if event.key == pygame.K_0 and current_speed >= 2:
                    current_speed //= 2


                # Human playing
                for s in snakes.values():
                    if not s.is_ai: s.handle_keys(event.key)
       
        # AI playing
        for s in snakes.values():
            if s.is_ai: s.ai_move(food_x, food_y)
            s.move()
            s.update_reward("STEP", (food_x, food_y), s.score)


        # collision
        for name, s in snakes.items():
            collision_type = None

            self_collision = s.check_collision([]) # empty to check ony itself
            if self_collision == "WALL_SELF":
                collision_type = "WALL_SELF"

            # OPPONENTS
            for other_name, other_s in snakes.items():
                if name != other_name:
                    if s.check_collision(list(other_s.body)) == "OPPONENT":
                        collision_type = "OPPONENT"
                        other_s.score += 3 # Bonus for blocker
                        break

            if collision_type:
                s.update_reward(f"DEATH_{collision_type}")
                s.score -= 2
                print(f"{name} died! Type: {collision_type}")
                full_score = {key: snakes[key].score for key in snakes}
                full_score = (sorted(full_score.items(), key=lambda item: item[1], reverse = True))
                print(f' Score: {full_score}')

                for s in snakes.values():
                    s.decay_epsilon()
                print(f"{s.name} Epsilon: {round(s.epsilon, 3)}")
                pygame.time.delay(500)
                return current_speed 
	


        # FOOD?
        for s in snakes.values():
            if s.x == food_x and s.y == food_y:
                s.score += 1
                s.length += 1
                s.update_reward("FOOD") # +150
                food_x, food_y = spawn_food()

        # Rendering
        dis.fill(COLOR_BG)
        pygame.draw.rect(dis, COLOR_FOOD, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        for s in snakes.values():
            s.draw(dis)
        
        show_info(dis, snakes, current_speed)
        
        pygame.display.update()
        clock.tick(current_speed)

if __name__ == "__main__":
    speed = SPEED
    while True:
       speed = game_loop(speed)