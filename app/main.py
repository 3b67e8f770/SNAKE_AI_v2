#!/usr/bin/python3
import pygame
import random
import sys
from snake import Snake
from collections import deque
from settings import *
import math

    
def show_info(surface, snakes, current_speed):
    font = pygame.font.SysFont(F_FONT, 20)
    mode1 = "AI" if snakes['SNAKE_1'].is_ai else "HUMAN"
    mode2 = "AI" if snakes['SNAKE_2'].is_ai else "HUMAN"
    mode3 = "AI" 
    mode4 = "AI" 
    
    val_1 = font.render(f"P1 ({mode1}): {snakes['SNAKE_1'].score}  Rew: {round(snakes['SNAKE_1'].total_reward, 1)}", True, snakes['SNAKE_1'].color)
    val_2 = font.render(f"P2 ({mode2}): {snakes['SNAKE_2'].score}  Rew: {round(snakes['SNAKE_2'].total_reward, 1)}", True, snakes['SNAKE_2'].color)
    val_3 = font.render(f"P1 ({mode3}): {snakes['SNAKE_3'].score}  Rew: {round(snakes['SNAKE_3'].total_reward, 1)}", True, snakes['SNAKE_3'].color)
    val_4 = font.render(f"P2 ({mode4}): {snakes['SNAKE_4'].score}  Rew: {round(snakes['SNAKE_4'].total_reward, 1)}", True, snakes['SNAKE_4'].color)
    hint = font.render("Press [1] or [2] to switch player mode", True, COLOR_FONT)
    surf_speed = font.render(f"Speed: {current_speed} (9: + | 0: -)", True, COLOR_FONT)

    surface.blit(val_1, [10, 10])
    surface.blit(val_2, [WIDTH - 250, 10])
    surface.blit(val_3, [10, HEIGHT -30])
    surface.blit(val_4, [WIDTH - 250, HEIGHT -30])
    surface.blit(hint, [WIDTH // 2 - 150, HEIGHT - 60])

def game_loop(current_speed):
    pygame.init()
    dis = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake AI - Bot Testing')
    clock = pygame.time.Clock()
    
    snakes = {key: Snake(key, *value) for key, value in PLAYERS.items()}
  
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
                snakes['SNAKE_1'].handle_keys(event.key)
                snakes['SNAKE_2'].handle_keys(event.key)
       
        # AI playing
        for key in snakes:
            if snakes[key].is_ai: snakes[key].ai_move(food_x, food_y)

            snakes[key].move()

            snakes[key].update_reward("step", (food_x, food_y), snakes[key].score)


        # collision
        for s in snakes:
            for other in snakes:
                if snakes[s] != snakes[other]:
                    collision = snakes[s].check_collision(list(snakes[other].body))
                    if collision:
                        if collision == "WALL_SELF":
                            snakes[s].update_reward("DEATH_WALL_SELF")
                            snakes[s].score -= 2
                            print(f"Snake {snakes[s]} died...")
                        elif collision == "OPPONENT":
                            snakes[s].update_reward("DEATH_OPPONENT")
                            snakes[s].score -= 2
                            snakes[other].score += 3
                            print(f"Snake {snakes[s]} hit an {snakes[other]}")
                        
                        full_score = {key: snakes[key].score for key in snakes}
                        full_score = (sorted(full_score.items(), key=lambda item: item[1], reverse = True))
                        print(f' Score: {full_score}')
                        pygame.time.delay(500)
                        game_loop(current_speed)



        # FOOD?
        for s in snakes:
            if snakes[s].x == food_x and snakes[s].y == food_y:
                snakes[s].score += 1
                snakes[s].length += 1
                snakes[s].update_reward("FOOD") # +150
                food_x, food_y = spawn_food()

        # Rendering
        dis.fill(COLOR_BG)
        pygame.draw.rect(dis, COLOR_FOOD, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        for i in snakes:
            snakes[i].draw(dis)
        
        show_info(dis, snakes, current_speed)
        
        pygame.display.update()
        clock.tick(current_speed)

if __name__ == "__main__":
    game_loop(SPEED)