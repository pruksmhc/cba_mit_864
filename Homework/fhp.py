#!/usr/bin/env python
from numpy import *
from numpy.random import randint
import pygame
import sys
import random

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
			if states[i,j][4]: pygame.draw.circle(screen, (255,0, 0), (int(pix2site*(i+.25)),int(pix2site*j)), int(.1*pix2site))
			if states[i,j][5]: pygame.draw.circle(screen, (255,0, 0), (int(pix2site*(i+.25)),int(pix2site*j)), int(.1*pix2site))
	pygame.display.update()

#		   2   3
#			\ /
#        1 - O  - 4
#			/ \
#		   6   5
# COLISSION CASES
#  100100 -> 010010 OR 001001
#. 010010 -> 100100 OR 001001
#. 001001 -> 100100 OR 010010
#  101010 -> 101010
#  010101 -> 010101  --
#  100101 -> 101100
#  100110 -> 110100
#  110010 -> 010110
#. 010011 -> 011011
#  011001 -> 001011 
#  101001 -> 001101
#  REVERSEOF ABOVE 
# 101100 -> 100101
# 110100 -> 100101
#  010110 ->  110010 
# 011011 -> 010011
# 001011 ->011001
# 001101 ->101001
#  011011 -> 110110 OR 101001
#  101101 -> 110110 OR 011011
#  110110 -> 011011 OR 101101



rules= {"101010" : "010010 ", "010010":"100100", "001001":"101010","100101":"101100", "100110":"110100", "110010":"010110", "010011":"011011", 
"011001":"001011", "101001":"001101", "101100": "100101","110100":"00101", "010110":"110010", "011011":"010011", "001011": "011001","001101": "101001", 
 "011011":"110110 ","101101":"110110", "110110":"011011", "100000" : "000100", "010000":"000010", "001000":"000001", "000010":"010000" }
# Collision steps: 
# 1 1 1 

def a_rules(world):
	r= rules[tuple([world[...,i] for i in range(shape(world)[-1])])]
	return r
def apply_rules(world):
	for i in range(len(world)):
		for j in range(len(world[i])):
			curr = map(str, world[i][j])
			curr = "".join(curr)
			print("curr")
			print(curr)
			if (rules.get(curr) is not None):
				new = []
				new.append(rules[curr][0])
				new.append(rules[curr][1])
				new.append(rules[curr][2])
				new.append(rules[curr][3])
				new.append(rules[curr][4])
				new.append(rules[curr][5])
				print(new)
				new = list(map(int, new))
				print(new)
				world[i][j] = new
	return world

n = 2*20 #world has n**2 sites
pix2site = 30
sr = random.randrange(1, 10, 1)

world = [[[0 for k in range(6)] for j in range(n)] for i in range(n)]
world = array(world)
print("initial world")
print(world)
temp = world 
world[n//2-sr:n//2+sr, n//2-sr:n//2+sr] = array([1,1,1,1,1,1],dtype=int8) # this is the region that is most seeded with 1s. 
pygame.init()
screen = pygame.display.set_mode((pix2site*n,pix2site*n))
clock = pygame.time.Clock()

i=0
while(True):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit();
	world = apply_rules(world)
	msElapsed = clock.tick(3)
	pygame.image.save(screen,"%04d.bmp"%i)
	i+=1

	#transport
	temp = zeros((n,n,6),dtype=int)
	temp[:-1,:,5] = world[1:,:,0]
	temp[1:,:, 0] = world[:-1,:,5]

	temp[1:,:-1,1] = world[:-1,1:,4]
	temp[0,1:-1:2,1] = 0 #ragged edge
	temp[:-1,:-1,3] = world[1:,1:,2]
	temp[-1,:-1:2,3] = 0 #ragged edge

	temp[1:,1:, 2] = world[:-1,:-1,3]
	temp[0,1:-1:2,2] = 0 #ragged edge
	temp[:-1,1:,4] = world[1:,:-1,1]
	temp[0,:-1:2,4] = 0 #ragged edge

	world = temp
	msElapsed = clock.tick(3)
	draw_states(world)
	pygame.image.save(screen,"%04d.bmp"%i)
	i+=1

