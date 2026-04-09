#!/usr/bin/python3
import pygame

NUM_PLAYERS = 4

# AI / Human
AI_P1 = True
AI_P2 = True
AI_P3 = True
AI_P4 = True

# app/settings.py
BLOCK_SIZE = 20
WIDTH = 32 * BLOCK_SIZE
HEIGHT = 24 * BLOCK_SIZE
SPEED = 25  

# reward
REWARD_FOOD = 150
REWARD_DEATH = -150
REWARD_DEATH_OPPONENT = REWARD_DEATH - 50
REWARD_STEP = -0.2
REWARD_CLOSER = 1.0
REWARD_FURTHER = -1.5
REWARD_1ST = 10

# colors
COLOR_BG = (255, 255, 255)
COLOR_FOOD = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_FONT = (100, 100, 100)

# Font
F_FONT = "bahnschrift"
F_SIZE = 25


#playes
PLAYERS = {
    'SNAKE_1': [[[WIDTH // 4, HEIGHT // 4], [WIDTH // 4 - BLOCK_SIZE, HEIGHT // 4], [WIDTH // 4 - 2 * BLOCK_SIZE, HEIGHT // 4]], COLOR_GREEN, {
        'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d
    }, (BLOCK_SIZE, 0), AI_P1],
   
    'SNAKE_2' :[[[3 * WIDTH // 4, 3 * HEIGHT // 4], [3 * WIDTH // 4 + BLOCK_SIZE, 3 * HEIGHT // 4], [3 * WIDTH // 4 + 2 * BLOCK_SIZE, 3 * HEIGHT // 4]], COLOR_RED,  {
        'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT
    }, (-BLOCK_SIZE, 0), AI_P2],
    
    'SNAKE_3' :[[[3* WIDTH // 4, HEIGHT // 4], [ 3* WIDTH // 4, HEIGHT // 4 - BLOCK_SIZE], [3* WIDTH // 4, HEIGHT // 4 - 2* BLOCK_SIZE]], COLOR_BLUE,  {
        'up': pygame.K_i, 'down': pygame.K_k, 'left': pygame.K_j, 'right': pygame.K_l
    }, (0, -BLOCK_SIZE), True],
   
    'SNAKE_4' :[[[WIDTH // 4, 3* HEIGHT // 4], [WIDTH // 4, 3 * HEIGHT // 4 + BLOCK_SIZE], [WIDTH // 4, 3 * HEIGHT // 4 + 2* BLOCK_SIZE]], COLOR_YELLOW,  {
        'up': pygame.K_t, 'down': pygame.K_g, 'left': pygame.K_f, 'right': pygame.K_h
    }, (0, BLOCK_SIZE), True]
}

# AI Training
EPSILON_START = 1.0
EPSILON_MIN = 0.01
DECAY_GAMES = 100  # trenings attempts 
EPSILON_DECAY = (EPSILON_START - EPSILON_MIN) / DECAY_GAMES

# Akcje: [FWD, LEFT, RIGHT]
ACTION_SPACE = 3