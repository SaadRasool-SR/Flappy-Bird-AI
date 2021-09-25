#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 21:17:41 2020

@author: Saad

"""
# This code create a game similar to flappy bird, very similar concept
# Applying machine learing Algorithm so computer can play the game 
# Apply genetics Algorithm so computer can learn how to improve every generation

from uagame import Window 
import pygame , time
from pygame.locals import *
import math, random 
import numpy as np
from tensorflow import keras
#from keras.models import Sequential
#from keras.layers import Dense, Activation
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import Sequential
import requests

def main():
    display_width = 900
    display_height = 800
    window = Window('Flappy Game',display_width,display_height)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.close()
    
############################################################## Gameloop ############################################################################
class Game:
    
    def __init__(self,window):
        self.start_time = time.process_time()
        self.window = window
        self.bg_colour = pygame.Color('Black')
        self.window_height = window.get_height()
        self.window_width = window.get_width()
        self.close_clicked = False
        self.continue_game = True
        self.pop_pool = 10 # of brids
        #self.x_coord = [200] * self.pop_pool
        self.y_coord = [self.window_height//2 - 50] * self.pop_pool
        self.bird_width = 35
        self.bird_height = 35
        self.pause_time = 0.001
        self.rect_x = 900
        self.rect_y = 700
        self.rect_y_T = 0
        self.rect_w = 150
        self.rect_h = 100
        self.rect_h_T = 100
        self.speed_rect = 5
        self.rand_hgt = 700
        self.ML_Jump = False
        self.cur_num_bird = 0
        self.mutation_rate = 1.01 # to add variation
        self.fitness = 0 # initial fitness
        self.fitness_list = []
        self.current_pool = []
        self.P_list = []
        self.Generation = 1
        self.Game_Brain = Brain(self.pop_pool, self.current_pool, self.Generation)
        self.bird = Bird(self.window.get_surface(),pygame.Color('Yellow'),self.bird_width,self.bird_height, self.window_height, self.pop_pool, self.cur_num_bird, self.Game_Brain, self.start_time,self.fitness_list,self.P_list)
        #self.bird = Bird(self.window.get_surface(),pygame.Color('Yellow'),self.x_coord,self.y_coord,self.bird_width,self.bird_height, self.window_height, self.pop_pool, self.cur_num_bird, self.Game_Brain, self.start_time,self.fitness_list,self.P_list)
        self.trees = Trees(self.window.get_surface(),pygame.Color('Red'), self.rect_x, self.rect_y, self.rect_w, self.rect_h, self.speed_rect,self.window_height,self.rand_hgt)
        self.trees_top = Trees(self.window.get_surface(),pygame.Color('Green'), self.rect_x, self.rect_y_T, self.rect_w, self.rect_h_T, self.speed_rect,self.window_height,self.rand_hgt)
        self.score = Score(self.window.get_surface(), self.window, self.window_width)
        self.Genetics_Algo = GA(self.pop_pool, self.mutation_rate, self.Game_Brain, self.bird)
        
        
    def play(self):
       while not self.close_clicked:
           self.handle_event()
           if self.continue_game:
               #self.Creating_pool()
               self.draw()
               self.update()
               self.decide_continue()
           else:
               self.end_game()
               #self.Genetics_Algo.Selection()
               #self.continue_game = True

           time.sleep(self.pause_time)

    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
            
    def draw(self):
        self.window.clear()
        self.bird.draw()
        self.trees.draw()
        self.trees_top.draw()
        self.score.draw(self.bird.fitness_list,self.Generation)
        self.window.update()
    
    def update(self):
        self.rand_Height()
        self.bird.move(self.trees.x, self.trees_top.h,self.trees.y)           
        self.trees.move(self.rand_hgt)
        self.trees_top.move(self.rand_hgt)
        #self.score_update()

    def rand_Height(self):
        self.rand_hgt = random.randint(200,700) 
        
    def decide_continue(self):
        if self.bird.Collide(self.trees, self.trees_top): #, self.tree_2, self.tree_2_top):
            #if self.bird.bird_list == []:
                #print(self.current_pool)
                self.continue_game = self.Genetics_Algo.Selection()
                
                
            
       
    def end_game(self):
        #self.window.clear()
        #self.trees.draw()
        #self.trees_top.draw()
        #self.bird.draw()
        #self.window.update()
        #self.current_pool = []
        #self.fitness_list = []
        #self.bird.Cal_y_coord()
        #self.continue_game = True
        self.Generation += 1
        self.bird.fitness_list = []
        self.bird.Cal_y_coord()
        self.trees.x = 1100
        self.trees_top.x = 1100
        self.bird.start_time = time.process_time()
        
        self.continue_game = True
    
    #def score_update(self):
     #   if self.trees.x == self.bird.x :
     #       self.score.update_score()
        
    def replay(self):
        pass
    
        
        
############################################################## Game Bird/Ball ############################################################################        
        
class Bird:
    def __init__(self,surface,colour,w,h,window_height,pop_pool,cur_num_bird, Brain,time,fit_list,P_list):
        self.surface = surface
        self.colour = colour
        #self.x = x
        self.w = w
        self.h = h
        self.window_height = window_height
        self.pop_pool = pop_pool
        self.cur_num_bird = cur_num_bird
        self.B_Brain = Brain
        self.start_time = time
        self.fitness_list = fit_list
        self.parent_list = P_list
        #self.x = [200] * self.pop_pool
        self.Cal_y_coord()
        #self.x = [200] * self.pop_pool
        #self.bird_list = []
        
    def Cal_y_coord(self):
        self.bird_list = []
        y_coord_list = []
        for n in range(self.pop_pool):
            new_num = random.randint(40,700)
            y_coord_list.append(new_num)
            self.bird_list.append(n)
        self.y = y_coord_list
        self.x = [200] * self.pop_pool
        
        #print(self.bird_list)
        #print(self.y)
        #print(self.x)
        
        
    def draw(self):
        #print(self.pop_pool)
        #print(self.bird_list)
       # print(self.B_Brain.current_pool)
        for t in range(len(self.bird_list)):
            pygame.draw.ellipse(self.surface, self.colour, [self.x[t], self.y[t], self.w, self.h])

        
    def move(self, trees_x, trees_top_h, trees_y): #,To_Jump):
       self.tree_x = trees_x
       self.trees_top_h = trees_top_h
       self.tree_y = trees_y
       for i in range(len(self.bird_list)):
           if self.Bird_brain(i):
               self.y[i] = self.y[i] - 10
           else:
               self.y[i] = self.y[i] + 3       

                
    def Collide(self, tree, tree_top):
        #print(self.bird_list)
        u = 0 
        #for u in range(len(self.bird_list)):
         
        while u < len(self.bird_list):
            #print(self.bird_list)
            #print(u)
            if tree.Rect.collidepoint(self.x[u] + self.h, self.y[u] + self.h):
                self.drop(u)                    
                
            elif tree_top.Rect.collidepoint(self.x[u] + self.h, self.y[u] - self.h/2):
                self.drop(u)
                
            elif self.y[u] - self.h/2 <= 0:
                self.drop(u)
                
            elif self.y[u] + self.h >= self.window_height:
                self.drop(u)                
            u += 1
            
        if self.bird_list == []:
            return True
        

    def drop(self,u):
        self.bird_list.remove(self.bird_list[u])
        self.fitness_Level(u)
        self.x.remove(self.x[u])
        self.y.remove(self.y[u])
        
        #if self.bird_list == []:
        #    print("it works")
        #    return True
        
        #self.fitness_Level(u)
        #if len(self.bird_list) >= 2:
        #    self.B_Brain.current_pool.remove(self.B_Brain.current_pool[u])
          
            
    def Bird_brain(self,i):
        Bird_pos = self.x[i] - self.tree_x
        Dis_Bird_top = self.y[i] - self.trees_top_h
        Dis_Bird_botm = self.y[i] - self.tree_y
        return self.B_Brain.Predict_action(Bird_pos, Dis_Bird_top, Dis_Bird_botm,i)
        
    def fitness_Level(self,u):
        self.fitness = time.process_time() - self.start_time  # number of seconds --> bird fitness level
        self.fitness_for = "{:.2f}".format(self.fitness)
        if self.fitness_for not in self.fitness_list:
            self.fitness_list.append(self.fitness_for)
            
############################################################## Game Trees/Pillars ############################################################################    
    
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
            self.x = 900
            self.y = Ht
            self.h = self.surface_height - self.y

            
        elif self.x < 0 and self.y == 0:
            self.x = 900
            self.y = 0
            self.h = Ht - 200
            
        self.Rect = Rect(self.x, self.y, self.w, self.h)

############################################################## Game Score ############################################################################

class Score:
    def __init__(self, surface, window, w):
        self.cur_score = 0
        self.surface = surface
        self.window = window
        self.window.set_font_size(20)
        self.score_message= 'Your score is: ' + str(self.cur_score)
        self.w = w
        self.x_message = 0
        self.x_length = self.window.get_string_width(self.score_message)
        
    
    def draw(self,score_list,Gen):
        self.window.draw_string('Fitness Score : ' + str(score_list),0,0)
        self.window.draw_string('Gen : ' + str(Gen), 0, 20)
    
    def update_score(self):
        self.cur_score += 1
        
    #def end_game_score(self):
    #    self.score_message= str(self.cur_score)
    #    self.x_length = self.window.get_string_width(self.score_message)
    #    self.window.set_font_size(80)
    #    self.window.draw_string(self.score_message,(self.w - self.x_length)/2,400)
        


############################################################## MACHINE LEARNING ############################################################################
# Using Keras lib from tensorflow module 
# 1 input layer, with 3 nodes  
# 1 hidden layers, with 7 nodes 
# 1 output layer, with 1 nodes
        
#input layer 
        # Distance between the bird and pillars - x axis  = Bird_pos 
        # Distance between the bird and top pillar = Dis_Bird_top
        # Distance between the bird and bottom pillar Dis_Bird_Botm
        
# using Sequential model from keras which is a simple neural network, which takes one input per node and single output 
        
class Brain:
    def __init__(self,total_models, current_pool, Gen):
        self.total_models = total_models
        self.current_pool = current_pool
        self.Gen = Gen
        
        
    def Create_Neural_Network(self):
        if self.Gen == 1:
            for i in range(self.total_models):
                self.Model_Brain = Sequential()
                # creating an input layer with 3 nodes, with an acitivation function that has  a value from 0 to 1 
                # inputshape represent how many input each node would get 
                self.Model_Brain.add(Dense(3, activation = 'relu' ,input_shape = (3,))) # input layer
                
                #creating 1 hidden layer, with 7 nodes and 3 inputs, will be using relu activation
                #self.Model_Brain.add(Dense(7, activation = 'relu' ,input_shape = (3,))) # Hidden Layer
                
                #creating output layer, will be using sigmoid function as activation fucntion, which will give us a probablity to jump or not to jump
                self.Model_Brain.add(Dense(1, activation = 'sigmoid' ,input_shape = (3,))) # Output Layer
                
                self.Model_Brain.compile(loss='mse', optimizer = 'adam')  # mse = mean squared error and adam = stochastic gradient descent
                
                self.current_pool.append(self.Model_Brain)
        else:
            print('New_model')

        
    def Predict_action(self, Bird_pos, Dis_Bird_top, Dis_Bird_Botm,bird_num):
        # feature scaling might be required
        
        self.Bird_pos = Bird_pos
        self.Dis_Bird_top = Dis_Bird_top
        self.Dis_Bird_Botm = Dis_Bird_Botm

        self.Neural_Input = np.asarray([self.Bird_pos, self.Dis_Bird_top, self.Dis_Bird_Botm])
        self.Neural_Input = np.atleast_2d(self.Neural_Input)
        
        self.output = self.current_pool[bird_num].predict(self.Neural_Input, 1)[0]
        
        if self.output[0] >= 0.5:
            #print('Jump')
            return True
        else:
            #print('Dont_Jump')
            return False
        
        
############################################################## Genetics Algorithm ############################################################################

'''
SETUP:
    Step 1: Initialize. Create a population N elements, each with randomly generated DNA 

LOOP:
    Step 2: Selection. Evaluate the fitness of each element of the population and build a mating pool
    
    Step 3: Reproduction. Repeat N times:
        
        a) Pick two parents with the probability according to relative fitness 
        b) Crossover - create a "Child" by combining the DNA of these two Parents
        c) Mutation - mutate the child's DNA based on a given probability 
        d) Add the new child to a new population
    
   Step 4: Replace the old population with the new population and return to step 2 
'''
class GA:
    def __init__(self, pop_pool, mutation_Rate, ML_Brain,bird):
        self.pop_pool = pop_pool # number of birds being generated each time 
        self.Mu_Rate = mutation_Rate # to add variation in the data set 
        self.Neural_Network = ML_Brain
        self.bird = bird
        self.Creating_pool()
        
    def Creating_pool(self):
        self.Neural_Network.Create_Neural_Network()
        
        
    def DNA(self):
        # would be the weight of the neural network and will be paseed on to the next generation 
        # weights from the input layer to the hidden layer
        # weights from the hidden layer to the output layer
        
        print('DNA')
        for i in range(len(self.Neural_Network.current_pool)):
            if i == len(self.Neural_Network.current_pool) - 1:
                z = self.parent_brain[1].get_weights()                
                self.Neural_Network.current_pool[0].set_weights(z)
                
            elif i == len(self.Neural_Network.current_pool) - 2:
                k = self.parent_brain[1].get_weights()
                self.Neural_Network.current_pool[1].set_weights(k)
                
            #else:
            #    q = self.parent_brain[random.randint(17,27)].get_weights()
            #    self.Neural_Network.current_pool[random.randint(0,27)].set_weights(q)
                

        return self.Reproduction()
        #pass
            
    def Selection(self):
        # calculating fitness
        self.probability = []
        self.parent_brain = []
        self.final_fitness_list = self.bird.fitness_list
        self.sum = 0.00
        
        
        
        for t in range(len(self.final_fitness_list)):
            self.sum = self.sum + float(self.final_fitness_list[t])
        
        for i in range(len(self.final_fitness_list)):
            x = float(self.final_fitness_list[i]) / self.sum  
            self.probability.append(float(x))
        
        #print(self.probability)
        self.parents_fitness = np.random.choice(self.final_fitness_list, 30, p = self.probability )
        
        for q in range(len(self.final_fitness_list)):
            for v in range(len(self.parents_fitness)):
                if self.final_fitness_list[q] == self.parents_fitness[v]:
                    self.parent_brain.append(self.Neural_Network.current_pool[q])
        
        
        
        #print(self.final_fitness_list)            
        #print(self.probability)
        #print(self.parents_fitness)
        #print(self.Neural_Network.current_pool)
        #print(self.parent_brain)
        
        
        return self.DNA()
        
    def Reproduction(self):        
        return False 
        
        
        


main()