#!/usr/bin/python3
# AI / Human
AI_P1 = True
AI_P2 = True

# app/settings.py
BLOCK_SIZE = 20
WIDTH = 32 * BLOCK_SIZE
HEIGHT = 24 * BLOCK_SIZE
SPEED = 5  

# reward
REWARD_FOOD = 150
REWARD_DEATH = -150
REWARD_STEP = -0.2
REWARD_CLOSER = 1.0
REWARD_FURTHER = -1.5

# colors
COLOR_BG = (255, 255, 255)
COLOR_FOOD = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_FONT = (100, 100, 100)

# Font
F_FONT = "bahnschrift"
F_SIZE = 25