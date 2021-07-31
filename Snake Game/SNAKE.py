#!/usr/bin/env python
# coding: utf-8

# ## ULTIMATE PYTHON SNAKE GAME SKETCH USING OPENCV ##

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
import random
import operator
import cv2
import pyglet
import time

# sound files from: https://opengameart.org/content/8-bit-sound-effect-pack-vol-001 credits to @Shades

# In[2]:


def paint_grid(LEVEL):
    # Generate Game Grid
    # Pixel = 255 -> Border
    # LEVEL will define the size of the border
    
    grid = np.zeros((40,40),np.float32)
    
    for i in range(LEVEL):
        grid[(0+i),:] = 255
        grid[:,(0+i)] = 255
        grid[:,(39-i)] = 255
        grid[(39-i),:] = 255
    
    return grid

def paint_snake_grid(head, body_before, grid):
    # Paint Grid with Snake Head and Body 
    # Head -> Pixel = 200
    # Body -> Pixels = 25
    grid[head] = 200
    
    for i in range(len(body_before)):
        grid[body_before[i]] = 25

    return grid


# In[3]:


def Rand_Point(grid, LEVEL, SCORE):
    while True:
        x = random.randint(1+LEVEL,38-LEVEL)
        y = random.randint(1+LEVEL,38-LEVEL)

        # For safety, not instakill the snake during a border level transition:
        if ((SCORE == 4) or (SCORE == 14) or (SCORE == 29) or (SCORE == 44) or (SCORE == 99)):
            x = random.randint(10+LEVEL,25-LEVEL)
            y = random.randint(10+LEVEL,25-LEVEL)
    
        if ((grid[x,y] != 255) & (grid[x,y] != 200) & (grid[x,y] != 25)):
            break   
            
    return x, y


# In[4]:


def Start_Conditions():
    
    # Starting Hold Time
    plt.pause(2)
    
    # Start Location for Snake Head and Body
    grid = paint_grid(1)
    head = (20, 20)
    body_before = [(20,19), (20,18), (20,17)]
    grid = paint_snake_grid(head, body_before, grid)
    new_body = [(20,19), (20,18), (20,17)]
    
    # Start move direction
    direction = (1, 0)
    
    # Score and State Variables Starting Values
    got_point_1 = 1
    got_point_2 = 1
    SCORE = 0
    LEVEL = 1
    old_lvl = 1
    new_lvl = 1
    
    return head, body_before, direction, grid, new_body, got_point_1, got_point_2, SCORE, LEVEL, old_lvl, new_lvl


# In[5]:


###################################### Start Conditions ###############################################

head, body_before, direction, grid, new_body, got_point_1, got_point_2, SCORE, LEVEL, old_lvl, new_lvl = Start_Conditions()

#######################################################################################################

# Game Soundtrack:
player = pyglet.media.Player()
player.queue(pyglet.resource.media("spacesong2.mp3", streaming=False))
player.play()
start_time = time.time()
end_time = 0

#######################################################################################################
# Game Title Intro Screen:
snake_intro = cv2.imread('sekiro_snake.jpg')
snake_intro = cv2.resize(snake_intro,(400,400))
cv2.putText(snake_intro, "ULTIMATE PYTHON SNAKE", (40, 300),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 50, 50), 2)
cv2.imshow('SNAKE', snake_intro)
cv2.waitKey(1)
plt.pause(5)

# Game Loop:
while True:    
    
    # Re-Activate Soundtrack if necessary:
    if ((end_time - start_time)>660): # Check if song duration (660 s) has passed in order to play it again
        end_time = 0
        start_time = time.time()
        player.pause()
        player = pyglet.media.Player()
        player.queue(pyglet.resource.media("spacesong2.mp3", streaming=False))
        player.play()
    
    # Snake Sound Effect:
    pyglet.resource.media("pac.wav", streaming=False).play()
    
    ###################################################################################################
    # Keyboard Configuration:
    
    key = cv2.waitKey(1) or 0xff
    
    # Update Currently Snake Direction
    cur_dir = direction
    
    # The Snake can only do 90° movement changes:
    
    if key == ord('w'): # UP
        if (cur_dir !=(-1, 0)) & (cur_dir !=((1, 0))):
            direction = (-1, 0)
        
    if key == ord('s'): # DOWN
        if (cur_dir !=(-1, 0)) & (cur_dir !=((1, 0))):
            direction = (1, 0)
        
    if key == ord('d'): # RIGHT
        if (cur_dir !=(0, -1)) & (cur_dir !=((0, 1))):
            direction = (0, 1)
            
    if key == ord('a'): # LEFT
        if (cur_dir !=(0, -1)) & (cur_dir !=((0, 1))):
            direction = (0, -1)
    
    # Press K to Close Game:
    if key == ord('k'):
        break
    
    # Press P to stop the music:
    if key == ord('p'):
        player.pause()
    
    ###################################################################################################
    # Clear Game Grid every iteration and if Level UP, increase border size based on LEVEL.
    grid = paint_grid(LEVEL)
           
    ###################################################################################################
    # Update Head Position with Movement made:
    head = tuple(map(operator.add, head, direction))
        
    ###################################################################################################
    # Check if the Grid is now smaller(LEVEL UP) and generate new points to prevent remaining impossible points:
    new_lvl = LEVEL
    
    if old_lvl < new_lvl:
        x1, y1 = Rand_Point(grid, LEVEL, SCORE)
        x2, y2 = Rand_Point(grid, LEVEL, SCORE)
        
        # Level UP Screens:
        snake_image = 'snake_' + str(LEVEL) + '.jpg'
        snake_show = cv2.imread(snake_image)
        snake_show = cv2.resize(snake_show,(400,400))
        
        if (LEVEL < 6):
            cv2.putText(snake_show, "LEVEL: {}".format(LEVEL), (60, 300),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 50, 50), 2)
            
        # Level 6 Ending Game Screen
        if (LEVEL == 6):
            player.pause()
            cv2.putText(snake_show, "CONGRATULATIONS!!!", (60, 300),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.imshow('SNAKE', snake_show)
            cv2.waitKey(1)
            
            creds_player = pyglet.media.Player()
            creds_player.queue(pyglet.resource.media("Creds.mp3", streaming=False))
            creds_player.play()
            plt.pause(5)
            
            Credits = cv2.imread('Credits.png')
            Credits = cv2.resize(Credits,(400,400))
            
            while True:
                cv2.imshow('SNAKE', Credits)
                
                key = cv2.waitKey(1) or 0xff

                # Press K to Close Game:
                if key == ord('k'):
                    creds_player.pause()
                    break
            break
            
        cv2.imshow('SNAKE', snake_show)
        cv2.waitKey(1)
        pyglet.resource.media("fanfare.mp3", streaming=False).play()
        plt.pause(3)
    
    ###################################################################################################
    # Generate and Paint a random Point on the Grid (only if the previous one was caught):
    
    if (got_point_1 == 1):
        x1, y1 = Rand_Point(grid, LEVEL, SCORE)
        got_point_1 = 0
    
    grid[x1,y1] = 150
    
    if (got_point_2 == 1):
        x2, y2 = Rand_Point(grid, LEVEL, SCORE)
        got_point_2 = 0
    
    grid[x2,y2] = 150
  
    ###################################################################################################
    # Check if Snake Head will get Point_1:
    if (head == (x1,y1)):
        grid[head] = 0
        got_point_1 = 1
        
        # Add new Body Part:
        body_add = tuple(map(operator.sub, body_before[len(body_before)-1], direction))
        new_body.append(body_add)
        body_before.append(body_add)
        pyglet.resource.media("Coin 2.wav", streaming=False).play()
        
        # Update score:
        SCORE += 1
        
    # Check if Snake Head will get Point_2:
    if (head == (x2,y2)):
        grid[head] = 0
        got_point_2 = 1
        
        # Add new Body Part:
        body_add = tuple(map(operator.sub, body_before[len(body_before)-1], direction))
        new_body.append(body_add)
        body_before.append(body_add)
        pyglet.resource.media("Coin 2.wav", streaming=False).play()
        
        # Update score:
        SCORE += 1         
        
    ###################################################################################################
    # Update Body Position Condidering Head's Movement:
    for i in range(len(new_body)-1):
        new_body[i+1] = body_before[i]
    
    # The head's following body part pos must be head's previous position(subtract direction of head):
    new_body[0] = tuple(map(operator.sub, head, direction))
    
    ###################################################################################################
    # Update and Paint Game Grid:
    grid = paint_snake_grid(head, new_body, grid)
    
    ###################################################################################################
    # Convert from np grayscale to OpenCV BGR and resize:
    frame = cv2.cvtColor(grid, cv2.COLOR_GRAY2BGR)
    frame = cv2.resize(frame,(400,400))
    
    # Let's paint things out with some colors:
    frame[np.where((frame == [0,0,0]).all(axis = 2))] = [125,0,0]       # Black background to blue
    frame[np.where((frame <= [13,13,13]).all(axis = 2))] = [125,0,0]    # Dark Gray edges to blue
    frame[np.where((frame >= [25,25,25]).all(axis = 2))] = [110,255,0]  # White bodies to green
    frame[np.where((frame <= [25,25,25]).all(axis = 2))] = [0,255,0]    # Remaining white edges to green
    
    # Let's add game info to the screen and show frame:
    cv2.putText(frame, "ULTIMATE PYTHON SNAKE", (65, 12),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, '  SCORE: {}'.format(SCORE), (280, 12),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, "Press K to Close Game", (90, 397),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, '  Level: {}'.format(LEVEL), (300, 397),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.imshow('SNAKE', frame)
    
    ###################################################################################################
    # Predict Death Condition (Head Touching border or own body) and Restart if Death if True:
    Death_Cond = tuple(map(operator.add, head, direction))
    
    if (grid[Death_Cond] == 255) or (grid[Death_Cond] == 25):
        # Death Screen:
        frame = cv2.imread('DEATH.jpg')
        frame = cv2.resize(frame,(400,400))
        cv2.putText(frame, 'SCORE: {}'.format(SCORE), (165, 330),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (30, 30, 255), 2)
        cv2.putText(frame, "RESTARTING...", (155, 90),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (30, 30, 255), 2)
        cv2.imshow('SNAKE', frame)
        
        # Death Sound Effect:
        pyglet.resource.media("Wrong 1.wav", streaming=False).play()
        pyglet.resource.media("DEATH.mp3", streaming=False).play()
        cv2.waitKey(1)
        plt.pause(3) # Wait for Death Screen
        
        # Restarting:
        head, body_before, direction, grid, new_body, got_point_1, got_point_2, SCORE, LEVEL, old_lvl, new_lvl = Start_Conditions()
        
    ###################################################################################################
    # Update body_before with new_body:
    for i in range(len(new_body)):
        body_before[i] = new_body[i]
        
    ###################################################################################################
    # Update old_lvl with currently level before updating level:
    old_lvl = LEVEL 
    
    ###################################################################################################
    # Change Snake Speed based on the Currently Score and Update Level:
    if (SCORE < 5):
        LEVEL = 1
        plt.pause(0.1)
        
    if (SCORE >= 5) & (SCORE < 15):
        LEVEL = 2
        plt.pause(0.05)
        
    if (SCORE >= 15) & (SCORE < 30):
        LEVEL = 3
        plt.pause(0.01)
        
    if (SCORE >= 30) & (SCORE < 45):
        LEVEL = 4
        plt.pause(0.005)
        
    if (SCORE >= 45) & (SCORE < 60):
        LEVEL = 5
        plt.pause(0.0005)
        
    if (SCORE >= 60):
        LEVEL = 6
        plt.pause(0.0005)
            
    end_time = time.time()
    
cv2.destroyAllWindows()
player.pause()


# In[ ]:





# In[ ]:




