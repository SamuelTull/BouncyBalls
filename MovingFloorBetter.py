import pygame
import random
import math
import numpy as np
width=800
height=800
pygame.init()
screen=pygame.display.set_mode((width,height ))
clock=pygame.time.Clock()
Slow=False
class Floor:
    def __init__(self,start,end):
        self.start=start
        self.end=end
        self.dely=end[1]-start[1]
        self.delx=end[0]-start[0]
        self.gradient=self.dely/self.delx
        self.angle=math.atan(self.gradient)
class Ball:
    def __init__(self,x,y):
        self.xpos=random.uniform(100,700)
        self.ypos=100
        self.xvel=random.uniform(-50,50)
        self.yvel=0#random.uniform(-50,50)
        self.xacc=0
        self.yacc=1
        self.colour=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.mass=1
        self.radius=50
        self.bounced=False
    def move(self,floors):
        self.xpos+=self.xvel
        self.ypos+=self.yvel
        self.xvel+=self.xacc
        self.yvel+=self.yacc
        for i in range(len(floors)):
            ball.BounceFloor(floors[i])
        ball.bounceWall()
    def bounceWall(self):
        if self.ypos-self.radius<=0:
            self.ypos=self.radius
            self.yvel=-elasticity*self.yvel
        if self.ypos+self.radius>=height:
            self.ypos=height-self.radius
            self.yvel=-elasticity*self.yvel
        if self.xpos-self.radius<=0:
            self.xpos=self.radius
            self.xvel=-elasticity*self.xvel
        if self.xpos+self.radius>=width:
            self.xpos=width-self.radius
            self.xvel=-elasticity*self.xvel 
    def bounceWall2(self):
        if self.ypos-self.radius<=0:
            self.ypos=self.radius
            self.xvel=-elasticity*self.xvel
        if self.xpos-self.radius<=0:
            self.xpos=self.radius
            self.xvel=-elasticity*self.xvel
        if self.xpos+self.radius>=width:
            self.xpos=width-self.radius
            self.xvel=-elasticity*self.xvel     
    def BounceFloor(self,floor):
        if self.xpos>=floor.start[0] and self.xpos<=floor.end[0]:
            #distance relative to startpoint of floor
            dx=self.xpos-floor.start[0]
            dy=self.ypos-floor.start[1]
            sin=math.sin(floor.angle)
            cos=math.cos(floor.angle)
            #distance along floor and height abovefloor
            w=cos*dx+sin*dy
            h=cos*dy-sin*dx
            #velocity parralel and perp to floor 
            velParr=cos*self.xvel+sin*self.yvel
            velPerp=-sin*self.xvel+cos*self.yvel
            #if height is less than radius flip the perp velocity
            #and shift the ball slightly so it is not below the floor
            if -h<self.radius:
                h=-self.radius
                velPerp=-elasticity*velPerp
                dx=cos*w-sin*h
                dy=cos*h+sin*w
                self.xvel=cos*velParr-sin*velPerp
                self.yvel=cos*velPerp+sin*velParr
                self.xpos=floor.start[0]+dx
                self.ypos=floor.start[1]+dy



def draw(screen,balls,floors):
    global customising
    global Slow
    screen.fill(0)
    for ball in balls:
        pygame.draw.circle(screen,ball.colour,(ball.xpos,ball.ypos),ball.radius)
    for f in floors:
        pygame.draw.line(screen,(0,255,0),f.start,f.end,1)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        elif pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos()
            y=min(750,y)
            err=47
            x=int(round(x/err)*err)
            for i in range(len(floorpoints)-1):
                if x<floorpoints[i+1][0]:
                    if x==floorpoints[i][0]:
                        floorpoints[i]=(x,y)
                    else:
                        floorpoints.insert(i+1,(x,y))
                    break
            if x>width-(err-1):
                floorpoints[-1]=(width,y)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                customising=not customising  
            if event.key == pygame.K_RETURN:
                Slow=not Slow  




airres=0
elasticity=0.8
numberOfBalls=10

while True:
    customising=True
    balls=[]
    floorpoints=[(0,750),(800,750)]
    for i in range(numberOfBalls):
        x=random.uniform(100,700)
        balls.append(Ball(x,61))
    while customising:
        floors=[]
        for i in range(len(floorpoints)-1):
            floors.append(Floor(floorpoints[i],floorpoints[i+1]))
        draw(screen,balls,floors)
    while not customising:
        for ball in balls:
            ball.move(floors) 
        draw(screen,balls,floors)
        if Slow:
            clock.tick(1)
        else:
            clock.tick(60)