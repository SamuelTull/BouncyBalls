import pygame
import random
import math
import numpy as np
width=800
height=800
pygame.init()
screen=pygame.display.set_mode((width,height ))
clock=pygame.time.Clock()
class Ball:
    def __init__(self,x,y):
        self.xpos=x
        self.ypos=y
        self.xvel=random.uniform(-26,25)
        self.yvel=random.uniform(-26,25)
        self.xacc=0
        self.yacc=1
        self.colour=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.mass=random.uniform(10,40)
        self.radius= self.mass 
        self.bounced=False
    def move(self):
        self.xpos+=self.xvel
        self.ypos+=self.yvel
        self.xvel+=self.xacc
        self.yvel+=self.yacc
        ball.bounceWall()
    def collide(self,other):
        distx=other.xpos-self.xpos
        disty=other.ypos-self.ypos
        dist=math.sqrt(distx*distx+disty*disty)
        if dist<self.radius+other.radius:
            angle=math.atan2(disty,distx)
            sin=math.sin(angle) 
            cos=math.cos(angle)
            #rotate velocities
            vx1 = self.xvel*cos+self.yvel*sin
            vy1 = self.yvel*cos-self.xvel*sin
            vx2 = other.xvel*cos+other.yvel*sin
            vy2 = other.yvel*cos-other.xvel*sin
            #bounce x vels(like 1d)
            v1=(self.mass-other.mass)*vx1+2*other.mass*vx2
            v2=(other.mass-self.mass)*vx2+2*self.mass*vx1
            vx1=v1/(other.mass+self.mass)
            vx2=v2/(other.mass+self.mass)
            #rotate back
            self.xvel=vx1*cos-vy1*sin
            self.yvel=vy1*cos+vx1*sin
            other.xvel=vx2*cos-vy2*sin
            other.yvel=vy2*cos+vx2*sin
            #relative position 
            x1,y1 = 0,0
            x2,y2 = distx*cos+disty*sin,disty*cos-distx*sin
            #shift apart slightly 
            absV = abs(vx1)+abs(vx2)
            overlap = (self.radius+other.radius)-dist
            x1 += vx1/absV*overlap
            x2 += vx2/absV*overlap
            other.xpos=self.xpos+x2*cos-y2*sin
            other.ypos=self.ypos+y2*cos+x2*sin
            self.xpos+=x1*cos-y1*sin
            self.ypos+=y1*cos+x1*sin
            
       


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
 
   
def draw(screen,balls):
    global customising
    screen.fill(0)
    for ball in balls:
        pygame.draw.circle(screen,ball.colour,(ball.xpos,ball.ypos),ball.radius)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        elif pygame.mouse.get_pressed()[0]:
            #x,y = pygame.mouse.get_pos()
            pass
        elif pygame.mouse.get_pressed()[2]:
            #x,y = pygame.mouse.get_pos()
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                customising=not customising  

airres=0
elasticity=0.75
numberOfBalls=10
balls=[]
while True:
    customising=True
    balls=[]
    for i in range(numberOfBalls):
        x=random.uniform(100,700)
        balls.append(Ball(x,100))
   
    while customising:
        draw(screen,balls)
    while not customising:
        for ball in balls:
            ball.move() 
            draw(screen,balls)
        for i in range(len(balls)):
            for j in range(len(balls)-(i+1)):
                j+=i+1
                balls[i].collide(balls[j])
        draw(screen,balls)
        clock.tick(60)