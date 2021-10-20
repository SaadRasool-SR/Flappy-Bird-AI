#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 21:17:41 2020

@author: Saad

"""
# This code represents flappy bird game and apply machine different
# machine learning algorithm 

from uagame import Window 
import pygame , time
from pygame.locals import *
import math, random 
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
import math



def main():
    display_width = 900
    display_height = 800
    window = Window('Flappy Game',display_width,display_height)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.close()

class Game:
    
    def __init__(self,window):
        self.window = window
        self.bg_colour = pygame.Color('Black')
        self.window_height = window.get_height()
        self.window_width = window.get_width()
        self.close_clicked = False
        self.continue_game = True
        self.x_coord = 200
        self.y_coord = self.window_height//2 - 50
        self.bird_width = 35
        self.bird_height = 35
        self.pause_time = 0.001
        self.bird = Bird(self.window.get_surface(),pygame.Color('Yellow'),self.x_coord,self.y_coord,self.bird_width,self.bird_height, self.window_height)
        self.rect_x = 900
        self.rect_y = 700
        self.rect_y_T = 0
        self.rect_w = 150
        self.rect_h = 100
        self.rect_h_T = 100
        self.speed_rect = 5
        self.rand_hgt = 700
        self.rand_hgt_2 = 700
        self.rect_x_2 = 1600
        self.rect_y_2 = 700
        self.rect_w_2 = 150
        self.rect_h_2 = 100
        self.rect_y_2_T = 0
        self.rect_h_2_T = 100
        self.trees = Trees(self.window.get_surface(),pygame.Color('Red'), self.rect_x, self.rect_y, self.rect_w, self.rect_h, self.speed_rect,self.window_height,self.rand_hgt)
        self.trees_top = Trees(self.window.get_surface(),pygame.Color('Green'), self.rect_x, self.rect_y_T, self.rect_w, self.rect_h_T, self.speed_rect,self.window_height,self.rand_hgt)
        self.tree_2 = Trees(self.window.get_surface(),pygame.Color('Blue'),self.rect_x_2, self.rect_y_2, self.rect_w_2, self.rect_h_2,self.speed_rect,self.window_height,self.rand_hgt_2)
        self.tree_2_top = Trees(self.window.get_surface(),pygame.Color('Orange'),self.rect_x_2, self.rect_y_2_T, self.rect_w_2, self.rect_h_2_T,self.speed_rect,self.window_height,self.rand_hgt_2)
        self.score = Score(self.window.get_surface(), self.window, self.window_width)
        
    def play(self):
       while not self.close_clicked:
           self.handle_event()
           if self.continue_game:
               self.draw()
               self.update()
               self.decide_continue()
           else:
               self.end_game()

           time.sleep(self.pause_time)

    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
            
    def draw(self):
        self.window.clear()
        #self.bird.draw()
        self.trees.draw()
        self.trees_top.draw()
        self.tree_2.draw()
        self.tree_2_top.draw()
        self.bird.draw()
        self.score.draw()
        self.window.update()
    
    def update(self):
        self.rand_Height()
        self.rand_Height_2()
        self.bird.move()           
        self.trees.move(self.rand_hgt)
        self.trees_top.move(self.rand_hgt)
        self.tree_2.move(self.rand_hgt_2)
        self.tree_2_top.move(self.rand_hgt_2)
        self.score_update()

    def rand_Height(self):
        self.rand_hgt = random.randint(200,700)
    
    def rand_Height_2(self):
        self.rand_hgt_2 = random.randint(200,700)
        
        
    def decide_continue(self):
        if self.bird.Collide(self.trees, self.trees_top, self.tree_2, self.tree_2_top):
            self.continue_game = False
       
    def end_game(self):
        self.window.clear()
        self.trees.draw()
        self.trees_top.draw()
        self.tree_2.draw()
        self.tree_2_top.draw()
        self.bird.draw()
        self.bird.drop()
        self.score.end_game_score()
        self.window.update()
    
    def score_update(self):
        if self.trees.x == self.bird.x :
            self.score.update_score()
        elif self.tree_2.x == self.bird.x:
            self.score.update_score()
        
    def replay(self):
        pass
        
        
class Bird:
    def __init__(self,surface,colour,x,y,w,h,window_height):
        self.surface = surface
        self.colour = colour
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.window_height = window_height
        
        
    def draw(self):
        pygame.draw.ellipse(self.surface, self.colour, [self.x, self.y, self.w, self.h])
        
    def move(self):
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONUP:
            self.y = self.y - 100
        else:
            self.y = self.y + 3        
            
    def Collide(self, tree, tree_top, tree_2, tree_2_top):
        if tree.Rect.collidepoint(self.x + self.h, self.y + self.h):
            return True
        elif tree_top.Rect.collidepoint(self.x + self.h, self.y - self.h/2):
            return True
        elif tree_2.Rect.collidepoint(self.x + self.h, self.y + self.h):
            return True
        elif tree_2_top.Rect.collidepoint(self.x + self.h, self.y - self.h/2):
            return True 
        elif self.y - self.h/2 <= 0:
            return True
        elif self.y + self.h >= self.window_height:
            return True
        else:
            return False 
    
    def drop(self):
        if self.y + self.h <= self.window_height:
            self.y += 4
            
    
    
class Trees:
    def __init__(self, surface, color, x, y, w, h, speed, surface_height,rand_H):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = speed
        self.Rect = Rect(self.x, self.y, self.w, self.h)
        self.surface_height = surface_height
        self.rand_h = rand_H
        
    def draw(self):
        pygame.draw.rect(self.surface, self.color, [self.x, self.y, self.w, self.h])
            
    def move(self,Ht):
        self.x = self.x - self.v
        if self.x < 0 and self.y != 0:
            self.x = 1600
            self.y = Ht
            self.h = self.surface_height - self.y
            
        elif self.x < 0 and self.y == 0:
            self.x = 1600
            self.y = 0
            self.h = Ht - 200
            
        self.Rect = Rect(self.x, self.y, self.w, self.h)

class Score:
    def __init__(self, surface, window, w):
        self.cur_score = 0
        self.surface = surface
        self.window = window
        self.window.set_font_size(50)
        self.score_message= 'Your score is: ' + str(self.cur_score)
        self.w = w
        self.x_message = 0
        self.x_length = self.window.get_string_width(self.score_message)
        
    
    def draw(self):
        self.window.draw_string(str(self.cur_score),450,50)
    
    def update_score(self):
        self.cur_score += 1
        
    def end_game_score(self):
        self.score_message= 'Your score is: ' + str(self.cur_score)
        self.x_length = self.window.get_string_width(self.score_message)
        self.window.set_font_size(80)
        self.window.draw_string(self.score_message,(self.w - self.x_length)/2,400)


main()
