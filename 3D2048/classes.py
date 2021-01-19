# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:30:04 2019

@author: Guest1
"""

class Box:
    def __init__(self,size = 4):
        self.grid = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]
        self.size=size
        self.score=0
        self.moves=0
    
    #list positions of 0 valued elements
    def emptyPos(self):
        empty=[]
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    if self.grid[i][j][k]==0:
                        empty.append([i,j,k])
        return empty
    
    #deep copy of instance
    def copy(self):
        b = Box(self.size)
        b.grid=[[[self.grid[i][j][k] for k in range(b.size)] for j in range(b.size)] for i in range(b.size)]
        b.score=self.score
        b.moves=self.moves
        return b
    
    def __str__(self):
        return 'Size: %d\nScore: %d\nMoves: %d'%(self.size,self.score,self.moves)
        
    def display(self):
        #iterate through rows
        for i in range(self.size):
            #create display-rows (according to height) for the row
            rs = [[] for r in range(self.size)]
            #iterate through columns for the row
            for j in range(self.size):
                #iterate through height for the column
                for k in range(self.size):
                    #add element to display-row at current height
                    rs[k].append(self.grid[i][j][k])
            #iterate through display-rows
            for r in range(len(rs)):
                #display-row string
                s=''
                #iterate through elements of the display-row
                for R in range(len(rs[r])):
                    x=str(rs[r][R])
                    e = x if x=='0' else '<'+x+'>'
                    #adding element to display-row string
                    #spacing corresponds to space taken by element
                    s+=str(e)+' '*(self.size*5-len(e)+1)
                #staggering by height for 3D effect
                print(' '*(self.size-r)*4+s)
        print('\nScore: %d\t Moves: %d'%(self.score,self.moves))
                
    #operator overloading to make handling easier
    def __getitem__(self,key = [0,0,0]):
        return self.grid[key[0]][key[1]][key[2]]
    
    def __setitem__(self,key = [0,0,0],val = 0):
        self.grid[key[0]][key[1]][key[2]] = val
        
class Move:
    def __init__(self,axis,direc,box):
        '''
        Up       -   axis:0, direction: -1
        Down     -   axis:0, direction:  1
        Left     -   axis:1, direction: -1
        Right    -   axis:1, direction:  1
        Backward -   axis:2, direction: -1
        Forward  -   axis:2, direction:  1
        '''
        self.axis=axis
        self.direc=direc
        self.size=box.size
        self.ranges=[range(self.size),range(self.size),range(self.size)]
        
        #set range along axis according to direction
        if direc==-1:
            self.ranges[axis] = range(1,self.size)
            self.condition = lambda e: e>0
        elif direc==1:
            self.ranges[axis] = range(self.size-2,-1,-1)
            self.condition = lambda e: e<self.size-1
            
    def execute(self,box):
        box.moves+=1
        #loop through elements according to axis and direction
        for r in self.ranges[0]:
            for c in self.ranges[1]:
                for h in self.ranges[2]:
                    #get value of current element
                    curr = [r,c,h]
                    elt = box[curr]
                    box[curr] = 0
                    if elt == 0:
                        continue
                    #select dimension to change while iterating according to axis
                    e = [r,c,h][self.axis]
                    #loop while condition (set according to direction) is true
                    while self.condition(e):
                        #check next element along selected dimension
                        curr[self.axis]=e+self.direc
                        #if next element has same value as current element
                        #(tile merge condition)
                        if box[curr] == elt:
                            #double value of next element and add to score
                            box[curr]*=2
                            box.score+=box[curr]
                            break
                        #if  next element doesn't have same value but isn't 0
                        elif box[curr] > 0:
                            #place current element right before next element
                            curr[self.axis]=e
                            box[curr] = elt
                            break
                        e+=self.direc
                    #if edge reached
                    else:
                        #place current element at edge
                        curr[self.axis]=e
                        box[curr] = elt
        