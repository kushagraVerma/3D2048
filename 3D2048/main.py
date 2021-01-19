# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:37:13 2019

@author: Guest1
"""

print('\n\n\t\tWelcome to 3D 2048!\n')
import random
import pickle
from datetime import datetime as dt
from classes import *
moveSet = {'U':[0,-1],'D':[0,1],'L':[1,-1],'R':[1,1],'B':[2,-1],'F':[2,1]}

#running function simulates 1 game
def game():
    size=0
    box = None
    
    #check for save states
    f = open('saved.dat','rb')
    saved=[]
    currSave=0
    while True:
        try:
            saved.append(pickle.load(f))
        except:
            break
    f.close()
    new=False
    if saved!=[]:
        print('\nSave states found')
        #option to use save states if any
        action=int(input('Begin new game [0] or load saved [1]: '))    
        if action:
            for i in range(len(saved)-1,-1,-1):
                save=saved[i]
                print('\nSAVE STATE #',i+1,'\n')
                print(save[0])
                print('Date-time saved: ',save[1])
                #option to use or delete save state, or move on to next
                action=int(input('Skip [0] or load [1] or delete [2] save state: '))
                if action==2:
                    saved.pop(i)
                elif action==1:
                    print("Loading save state")
                    box = save[0].copy()
                    size=box.size
                    currSave=i
                    break
            else:
                new=True #if none of the save states are loaded
        else:
            new=True #if player chooses not to load save states
    else:
        new=True #if no save states exist
    if new:
        print("Creating new game")
        size=int(input('Enter size of grid [2 to 6](recommended: 4): '))
        #size limit enforced
        if size not in range(2,7):
            print('Invalid size entered')
            return
        #initialise new grid
        box=Box(size)
        randPos=[random.randint(0,size-1) for i in range(3)]
        box[randPos]=2
        
    #Recommended display settings for terminal
    x=2800//(5*size*(size+1))
    f=36 if x>36 else x
    print('\nRECOMMENDED DISPLAY SETTINGS ')
    print('\tBackground color: black\n\tText color: white')    
    print('\tFont: Consolas\n\tFont size: ',f)
    input("'Enter' to continue\n")
    
    print('GAME BEGIN\n')    
    #loop continues with each move
    while True:
        #ignore out-of-space condition if a save state has just been loaded
        if new or box.moves!=saved[currSave][0].moves:
            #get positions of 0-valued elements
            empty = box.emptyPos()
            #out-of-space condition, game ends
            if len(empty) == 0:
                print('Out of space!')
                break
            #randomly assign value 2 to a 0-valued (empty) element
            randPos = random.choice(empty)
            box[randPos] = 2
        
        #display current grid
        box.display()
        
        #controls
        s = "Save and end game- 'S'\n"
        s+="Move - 'U' for UP, 'R' for RIGHT, 'D' for DOWN,\n"
        s+="\t'L' for LEFT, 'F' for FORWARD, 'B' for BACKWARD\n"    
        s+="End game- 'Enter' or any other key: "
        moveKey = input(s).upper()
        print()
        
        #save game to file with timestamp and end
        if moveKey=='S':
            save = [box,dt.now()]
            if new:
                saved.append(save)
            else:
                #option to save as new or rewrite current save state
                s="Rewrite current save state [0] or save as separate [1]: "
                action = int(input(s))
                if action:
                    saved.append(save)
                else:
                    saved[currSave] = save
            print('Saving...\n')
            break
        
        #end game without saving
        if moveKey not in moveSet.keys():
            print('Exiting...\n')
            break
        
        #handle move input and execute corresponding move
        m = moveSet[moveKey]
        move = Move(m[0],m[1],box)
        move.execute(box)
        
    #update save file    
    f = open('saved.dat','wb')    
    for i in saved:
        pickle.dump(i,f)
    f.close()
    
    #game ended, display score and no. of moves
    print('GAME END')
    print('Score: ',box.score)
    print('Moves: ',box.moves)
    
#loop continues with each game
while True:
    game()
    #option to play another game or exit
    end=int(input('\nRetry [0] or quit [1]: '))
    if end:
        break





