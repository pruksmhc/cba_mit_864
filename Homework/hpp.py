#!/usr/bin/env python
from numpy import *
from numpy.random import randint
import pygame
import sys
import random
import numpy as np

""" 
Code for visualization based off of Sam's code
"""
def draw_states(states):
	screen.fill((255,255,255))
	n = shape(states)[-2]
	for i in range(n):
		for j in range(n):
			pygame.draw.circle(screen, (255, 255, 255), (int(pix2site*i),int(pix2site*j)), int(.2*pix2site))
			if states[i,j][0]: pygame.draw.circle(screen, (255,0, 0), (int(pix2site*(i-.25)),int(pix2site*j)), int(.1*pix2site))
			if states[i,j][1]: pygame.draw.circle(screen, (255,0, 0), (int(pix2site*i),int(pix2site*(j-.25))), int(.1*pix2site))
			if states[i,j][2]: pygame.draw.circle(screen, (255,0, 0), (int(pix2site*i),int(pix2site*(j+.25))), int(.1*pix2site))
			if states[i,j][3]: pygame.draw.circle(screen, (255,0, 0), (int(pix2site*(i+.25)),int(pix2site*j)), int(.1*pix2site))

	pygame.display.update()

# left - 0 , up - 1, down = 2, right - 3.  Based on these, 

"""
How this happens. 
Theres two stages, 
There's rules IN the cell, so you transport in the cell. 
So at step 1a, you have 
1000 (with everything being incoming, all particles are incoming to that cell), 
Then in 1a), 1000 becomes 0001, you pass through that cell, or collide and switch places. 
By the end of 1a), all particles are in the outgoing state, and you want to switch them to become incoming. 
1b) 
You propagate or transport by looping through 4 times, and then you pass through 4 ways, transporting the previous one 
to the right (use same rules, but here you're moving between particles), and when you mov,e this is incomign ad your'e back 
to the state right before 1a. 
Be careful of not "undoing" the move. 
o -1-> <-1 - o - 0 ->, here if you have 2 outgoing particles that are with each other, they just swithc. 
BUT if they're both incoming, then they collide. 
But everything else seems good. 


"""
rules= {"0001":"1 0 0 0", "0010":"0 1 0 0", "0011":"1 1 0 0","0100":"0 0 1 0", "0101":"1 0 1 0", "0110":"1 0 0 1", "0111":"1 1 1 0", "1000":"0 0 0 1","1001":"0 1 1 0", "1010":"0 1 0 1", "1011":"1 1 0 1", 
"1100":"0 0 1 1", "1101":"1 0 1 1", "1110":"0 1 1 1", "0000":"0 0 0 0", "1111":"1 1 1 1"}

# keep the state of the direction
# Given the cell coordinates, for each of the vectors, show which direction they are going in. 

def a_rules(world):
	r= rules[tuple([world[...,i] for i in range(shape(world)[-1])])]
	return r

def apply_rules_incoming(world):
	for i in np.arange(len(world)):
	    for j in np.arange(len(world[0])):
	    	x = "".join(world[i,j].astype(str))
	    	new_x = rules[x]
	    	new_x = np.array(new_x.split(" ")).astype(int)
	    	world[i,j] = new_x
	return world

def apply_rules_outgoing(world):
	check_state =np.zeros((40, 40,4), dtype=bool)
	# first pass, going through and  oving eveyrthing to the right.
	for i in range(len(world)):
		for j in range(1, len(world[i])):
			if check_state[i][j-1][3] == False:  # 3 is left
				prev_state = world[i][j-1][3]
				if check_state[i][j][0] == False:
					curr_state = world[i][j][0]
				else:
					curr_state = 0
				world[i][j][0] = prev_state
				world[i][j-1][3] = curr_state
				check_state[i][j - 1][3] = True # update state to true
				check_state[i][j][0] = True
				# left side, shifting to the right
	for i in range(len(world[0])):
		for j in range(1, len(world)):
			if check_state[j-1][i][2] == False:  # 3 is left
				prev_state = world[j-1][i][2]
				if check_state[j][i][1] == False:
					curr_state = world[j][i][1]
				else:
					curr_state = 0
				world[j][i][1] = prev_state
				world[j-1][i][2] = curr_state
				world[j][i][1] = True # update state to true
				world[j-1][i][2] = True

	return world

n = 2*20 #world has n**2 sites
pix2site = 30
radius = random.randrange(1, 10, 1)
sr = 5 #radius of seeded region
world = zeros((n,n,4),dtype=int8)
#orld = randint(0,2,(n,n,4))

temp = world 
world[n//2-sr:n//2+sr, n//2-sr:n//2+sr] = array([1,1,1,1],dtype=int8) # this is the region that is most seeded with 1s. 
print(world)
pygame.init()
screen = pygame.display.set_mode((pix2site*n,pix2site*n))
clock = pygame.time.Clock() 


i=0
while(True):
	msElapsed = clock.tick(10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit()
	#world = apply_rules_incoming(world)
	world = apply_rules_incoming(world)
	#world = apply_rules_outgoing(world)
	print(world)
	#world = apply_rules_outgoing(world)
	draw_states(world)
	pygame.image.save(screen,"%04d.bmp"%i)
	i+=1
	# transport
	temp[:-1,:,3] = world[1:,:,0] # shift to the right
	temp[1:,:, 0] = world[:-1,:,3] # shift to the left
	temp[:,:-1,1] = world[:,1:,2] # shift down
	temp[:,1:, 2] = world[:,:-1,1]
	# bounce back for border conditions
	world = temp
	draw_states(world)
	pygame.image.save(screen,"%04d.bmp"%i)


