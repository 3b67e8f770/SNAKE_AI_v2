from collections import deque
from settings import *
import random
import pygame

class Snake:
    def __init__(self, name, initial_segments, color, controls, initial_direction, is_ai=True):
        self.name = name
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
        self.score = 0
        self.total_reward = 0  
        self.prev_distance = 0 
        self.epsilon = EPSILON_START
        self.games_played = 0

    def __str__(self):
        return self.name
    
    def get_action(self, state):
        # 1. (Exploration)
        if self.is_ai and random.random() < self.epsilon:
            # 0 (FWD), 1 (LEFT), 2 (RIGH)
            return random.randint(0, 2)
        
        # 2. NEURAL NETWORK
        # FWD for now
        return 0

    def get_distance_to_food(self, food_x, food_y):
        # distance  |x1 - x2| + |y1 - y2|
        return abs(self.x - food_x) + abs(self.y - food_y)
    
    def update_reward(self, event_type, food_pos=None, other_score=0):
        event_type = event_type.upper()
        reward = 0

        # rewards
        if event_type == "FOOD":
            reward = REWARD_FOOD - REWARD_STEP # food - movement cost
            if self.score > other_score:
                reward += REWARD_1ST# Reward if winning
        elif event_type == "DEATH_WALL_SELF":
            reward = REWARD_DEATH 
        elif event_type == "DEATH_OPPONENT":
            reward = REWARD_DEATH_OPPONENT  
        
        #every step reward
        if food_pos and event_type == "STEP":
            curr_dist = self.get_distance_to_food(food_pos[0], food_pos[1])
            if curr_dist < self.prev_distance:
                reward += REWARD_CLOSER
            else:
                reward += REWARD_FURTHER
            self.prev_distance = curr_dist
            reward += REWARD_STEP 

        self.total_reward += reward
        return reward

        

    def handle_keys(self, key):
        if key == self.controls['up'] and self.dy == 0:
            self.dx, self.dy = 0, -BLOCK_SIZE
        elif key == self.controls['down'] and self.dy == 0:
            self.dx, self.dy = 0, BLOCK_SIZE
        elif key == self.controls['left'] and self.dx == 0:
            self.dx, self.dy = -BLOCK_SIZE, 0
        elif key == self.controls['right'] and self.dx == 0:
            self.dx, self.dy = BLOCK_SIZE, 0

    def ai_move(self, food_x, food_y):
        #Random move
        possible_directions = [(0, -BLOCK_SIZE), (0, BLOCK_SIZE), (-BLOCK_SIZE, 0), (BLOCK_SIZE, 0)]
    
        # cannot tun back
        valid_directions = [d for d in possible_directions if not (d[0] == -self.dx and d[1] == -self.dy)]
        random_move = random.choice(range(10))
        if random_move > 5:
            self.dx, self.dy = random.choice(valid_directions)
        elif food_x > self.x and possible_directions[3] in valid_directions:
            self.dx, self.dy = possible_directions[3]
        elif food_x < self.x and possible_directions[2] in valid_directions:
            self.dx, self.dy=  possible_directions[2]
        elif food_y < self.y and possible_directions[0] in valid_directions:
            self.dx, self.dy = possible_directions[0]
        elif food_y > self.y and possible_directions[1] in valid_directions:
            self.dx, self.dy = possible_directions[1]
        else:
            # choice from valids
            self.dx, self.dy = random.choice(valid_directions)

    def move_by_action(self, action):
        #0 - FWD, 1-LEFT, 2- RIGHT

        #clock_wise from UP
        clock_wise = [(0, -BLOCK_SIZE), (BLOCK_SIZE, 0), (0, BLOCK_SIZE), (-BLOCK_SIZE, 0)]
        idx = clock_wise.index((self.dx, self.dy))

        if action == 0:   # FWD
            new_dir = clock_wise[idx]
        elif action == 1: # LEFT
            new_dir = clock_wise[(idx - 1) % 4]
        elif action == 2: # RIGHT
            new_dir = clock_wise[(idx + 1) % 4]

        self.dx, self.dy = new_dir
        self.move() 

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.body.appendleft([self.x, self.y])
        if len(self.body) > self.length:
            self.body.pop()
    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

    def check_collision(self, other_snake_body):
        body_list = list(self.body)
        # border and ow body
        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT or body_list.count([self.x, self.y]) > 1:
            return "WALL_SELF"
       
        # opponent
        if [self.x, self.y] in other_snake_body:
            return "OPPONENT"
        return None
    
    def decay_epsilon(self):
        # EPSILON update
        if self.epsilon > EPSILON_MIN:
            self.epsilon -= EPSILON_DECAY
            self.games_played += 1