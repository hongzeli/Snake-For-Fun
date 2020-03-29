# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 13:19:01 2020

@author: lhzcom
"""

import cv2
import numpy as np
import random
#from time import sleep

SIZE = (500, 500)                           # (y, x)
GRID_SIZE = 50                                
SNAKE_INIT = {0:[4,3], 1:[4,2], 2:[4,1], -1:[]}     
DIRECTION_INIT = "right"                               # up:1 down:2 left:3 right:4


def draw_snake(background, grid, snake_color=[255,128,0], init=False):
    '''
    mode: 1 means normal move, 0 means init snake
    '''
    global snake_list
    gap = 2
    if not init:        
        head = snake_list[0]
        begin_point = [head[0]*grid + grid//2-head_icon.shape[0]//2, 
                       head[1]*grid + grid//2-head_icon.shape[1]//2]
        background[begin_point[0]:begin_point[0]+head_icon.shape[0], 
                   begin_point[1]:begin_point[1]+head_icon.shape[1],:] = head_icon
                   
        neck = snake_list[1]
        background[neck[0]*grid+gap:(neck[0]+1)*grid-gap, 
                   neck[1]*grid+gap:(neck[1]+1)*grid-gap, :] = snake_color
        if snake_list[-1]:
            tail = snake_list[-1]
            background[tail[0]*grid:(tail[0]+1)*grid, 
                       tail[1]*grid:(tail[1]+1)*grid, :] = [0,0,0]
            snake_list[-1] = []
    else:
        for m in range(1,len(snake_list)-1):
            i = snake_list[m]
            background[i[0]*grid+gap:(i[0]+1)*grid-gap, 
                       i[1]*grid+gap:(i[1]+1)*grid-gap, :] = snake_color
        head = snake_list[0]
        begin_point = [head[0]*grid + grid//2-head_icon.shape[0]//2, 
                       head[1]*grid + grid//2-head_icon.shape[1]//2]
        background[begin_point[0]:begin_point[0]+head_icon.shape[0], 
                   begin_point[1]:begin_point[1]+head_icon.shape[1],:] = head_icon
            
        
def draw_random_coin(grid):
    global background
    while 1:
        coin = [random.choice(range(y_num)),random.choice(range(x_num))]
        if coin not in [snake_list[i] for i in range(len(snake_list)-2)]:break
#    center = (coin[1]*grid+grid//2, coin[0]*grid + grid//2)
#    dist = 5
#    background = cv2.circle(background, center, (grid//2)-dist, [0,0,255], -1)
    begin_point = [coin[0]*grid + grid//2-coin_icon.shape[0]//2, 
                   coin[1]*grid + grid//2-coin_icon.shape[1]//2]
    background[begin_point[0]:begin_point[0]+coin_icon.shape[0], 
               begin_point[1]:begin_point[1]+coin_icon.shape[1],:] = coin_icon
    return coin


def range_check(head):
    if head[0] < 0: head[0] = head[0] + y_num
    elif head[0] >= y_num: head[0] = head[0] - y_num
    if head[1] < 0: head[1] = head[1] + x_num
    elif head[1] >= y_num: head[1] = head[1] - x_num
    return head
    

def dir_check(snake_list, direction):
    temp = snake_list[0]
    
    if direction == "up": 
        temp = [temp[0]-1, temp[1]]     # up
    elif direction == "down": 
        temp = [temp[0]+1, temp[1]]     # down
    elif direction == "left": 
        temp = [temp[0], temp[1]-1]     # left
    else: 
        temp = [temp[0], temp[1]+1]     # right

    if temp != snake_list[1]: 
        return range_check(temp)
    
    old_dir = direction - (-1)**direction
    return dir_check(snake_list, old_dir)
    
        
def move_snake(snake_list, direction, coin):
    move_head = dir_check(snake_list, direction)
    if move_head in [snake_list[i] for i in range(2, len(snake_list)-1)]:
        return 0
    snake_list_new = {}
    for i in range(len(snake_list)-1):
        if i == 0: snake_list_new[i] = move_head
        else: snake_list_new[i] = snake_list[i-1]
    if move_head == coin: 
        snake_list_new[len(snake_list)-1] = snake_list[len(snake_list)-2] 
        snake_list_new[-1] = []
        global new_coin
        new_coin = True
    else: 
        snake_list_new[-1] = snake_list[len(snake_list)-2]
    return snake_list_new


if __name__ == "__main__":
    debug = 1
    
    # init
    background = np.zeros((SIZE[0], SIZE[1], 3), dtype="uint8")
    y_num = SIZE[0]//GRID_SIZE
    x_num = SIZE[1]//GRID_SIZE
    snake_list = SNAKE_INIT
    direction = DIRECTION_INIT
    ROOT = r"/home/jason/Workstation/Snake-For-Fun"
    coin_icon = cv2.imread(ROOT + r"/images/virus_icon.png",-1)
    coin_icon = cv2.resize(coin_icon, None, fx=(GRID_SIZE-5)/coin_icon.shape[1], 
                           fy=(GRID_SIZE-5)/coin_icon.shape[0],interpolation=cv2.INTER_CUBIC)
    head_icon = cv2.imread(ROOT + r"/images/head_icon.png",-1)
    head_icon = cv2.resize(head_icon, None, fx=(GRID_SIZE-5)/head_icon.shape[1], 
                           fy=(GRID_SIZE-5)/head_icon.shape[0],interpolation=cv2.INTER_CUBIC)
    draw_snake(background, GRID_SIZE, init=True)
    coin = draw_random_coin(GRID_SIZE)
    new_coin = False

#    #gaming
    while(True):
        cv2.imshow('Snake Go 1.0', background)
        snake_list = move_snake(snake_list, direction, coin)
        if not snake_list: break
        if new_coin: 
            coin = draw_random_coin(GRID_SIZE)
            new_coin = False
        draw_snake(background, GRID_SIZE, init=False)
#        sleep(1)
        key = cv2.waitKey(300) & 0xFF  
        if key in [ord('w'), 82]: direction = "up"
        elif key in [ord('s'), 84]: direction = "down"
        elif key in [ord('a'), 81]: direction = "left"
        elif key in [ord('d'), 83]: direction = "right"
        elif key == 27: break
    
    # gameover
    go = cv2.imread(ROOT + r"/images/gameover.jpg", -1)
    go = cv2.resize(go, None, fx=(SIZE[1]/2)/go.shape[1], fy=(SIZE[1]/2)/go.shape[1], 
                    interpolation=cv2.INTER_CUBIC)
    center = [SIZE[0]//2, SIZE[1]//2]
    background[center[0]-go.shape[0]//2:center[0]+go.shape[0]//2, 
               center[1]-go.shape[1]//2:center[1]+go.shape[1]//2,:] = go
    cv2.imshow("Snake Go 1.0",background)
    while 1:
        if cv2.waitKey(1000) & 0xFF == 27:
            cv2.destroyWindow('Snake Go 1.0')
            break
    
    
    
    
    
    
    
    
    
    
    
    
    
    
