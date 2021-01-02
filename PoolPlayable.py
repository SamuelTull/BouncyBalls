import pygame
import random
import math
import numpy as np
width=440
height=880
borderx=250
bordery=50
pygame.init()
outerscreen=pygame.display.set_mode((width+2*borderx,height+2*bordery))
screen=pygame.Surface((width,height))
clock=pygame.time.Clock()
class Ball:
    def __init__(self,x,y,xv,yv,colour):
        self.xpos=x
        self.ypos=y
        self.xvel=xv
        self.yvel=yv
        self.xacc=0
        self.yacc=0
        self.colour=colour
        self.mass=ballradius
        self.radius= self.mass 
        self.moving=True
        self.potted=False
    def move(self):
        self.xvel=friction*self.xvel
        self.yvel=friction*self.yvel
        norm=np.sqrt(self.xvel*self.xvel+self.yvel*self.yvel)
        if norm<0.01:
            self.moving=False
        else:
            self.moving=True
        self.xpos+=self.xvel
        self.ypos+=self.yvel
        self.xvel+=self.xacc
        self.yvel+=self.yacc
        ball.bounceWallAddtobounce()
       
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
    def bounceWallAddtobounce(self):
        if self.ypos-self.radius<=0:
            if self.xpos<holesize or self.xpos>width-holesize:
                self.potted=True
            self.ypos=self.radius
            self.yvel=-elasticity*self.yvel
        if self.ypos+self.radius>=height:
            if self.xpos<holesize or self.xpos>width-holesize:
                self.potted=True
            self.ypos=height-self.radius
            self.yvel=-elasticity*self.yvel
        if self.xpos-self.radius<=0:
            if self.ypos<holesize or self.ypos>height-holesize or (self.ypos<height/2+holesize/2 and self.ypos>height/2-holesize/2):
                self.potted=True
            self.xpos=self.radius
            self.xvel=-elasticity*self.xvel
        if self.xpos+self.radius>=width:
            if self.ypos<holesize or self.ypos>height-holesize or (self.ypos<height/2+holesize/2 and self.ypos>height/2-holesize/2):
                self.potted=True
            self.xpos=width-self.radius
            self.xvel=-elasticity*self.xvel
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
            
   
def draw(outerscreen,screen,balls):
    global customising
    outerscreen.fill((255,255,255))
    screen.fill((50,80,255))
    pygame.draw.line(screen,(255,255,255),(0,width/2),(width,width/2))
    for i in range(len(balls)):
        if not balls[i].potted:
            pygame.draw.circle(screen,balls[i].colour,(balls[i].xpos,balls[i].ypos),balls[i].radius)
        else:
            x=borderx+width+height/17
            y=bordery+height/17*(i+1)
            pygame.draw.circle(outerscreen,balls[i].colour,(x,y),balls[i].radius)
    pygame.draw.line(screen,(0),(0,height/2-holesize/2),(0,height/2+holesize/2),6)
    pygame.draw.line(screen,(0),(width-3,height/2-holesize/2),(width-3,height/2+holesize/2),6)
    pygame.draw.polygon(screen,(0),[(width,0),(width-holesize,0),(width,holesize)])
    pygame.draw.polygon(screen,(0),[(0,0),(holesize,0),(0,holesize)])
    pygame.draw.polygon(screen,(0),[(width,height),(width-holesize,height),(width,height-holesize)])
    pygame.draw.polygon(screen,(0),[(0,height),(holesize,height),(0,height-holesize)])
    outerscreen.blit(screen,(borderx,bordery))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        elif pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos()
            x=max(borderx,x)
            x=min(borderx+width,x)
            y=max(bordery,y)
            y=min(bordery+height,y)
            x=x-borderx
            y=y-bordery
            dx=x-balls[0].xpos
            dy=y-balls[0].ypos
            balls[0].xvel=6*dx/800
            balls[0].yvel=6*dy/800
            customising=False
        elif pygame.mouse.get_pressed()[2]:
            #x,y = pygame.mouse.get_pos()
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                customising=not customising 
            if event.key == pygame.K_RETURN:
                balls[0].xpos=width/2
                balls[0].ypos=width/2
                balls[0].xvel=0
                balls[0].yvel=0
                balls[0].potted=False   

def rerackBalls():
    balls=[]
    xv=random.uniform(-0.01,0.01)
    yv=random.uniform(0.5,5)
    balls.append(Ball(width/2,width/2,0,1,(255,220,200)))
    bx=width/2
    by=height-width/2
    balls.append(Ball(bx,by,0,0,(0,0,0)))
    r=ballradius+1
    r3=math.sqrt(3)
    posR=[(bx,by-2*r3*r),(bx+r,by-r3*r),(bx-2*r,by),(bx-r,by+r3*r),(bx+3*r,by+r3*r),(bx-4*r,by+2*r3*r),(bx+2*r,by+2*r3*r)]
    posY=[(bx-r,by-r3*r),(bx+2*r,by),(bx-3*r,by+r3*r),(bx+r,by+r3*r),(bx,by+2*r3*r),(bx-2*r,by+2*r3*r),(bx+4*r,by+2*r3*r)]
    for pos in posR:
        balls.append(Ball(pos[0],pos[1],0,0,(255,0,0)))
    for pos in posY:
        balls.append(Ball(pos[0],pos[1],0,0,(255,255,0)))

    return balls
friction=0.999
elasticity=1
ballradius=21
r=ballradius
balls=[]
holesize=50
while True:
    customising=True
    balls=rerackBalls()
    potted=[]   
    while customising:
        draw(outerscreen,screen,balls)
    alive=True
    while not customising and alive:
        alive=False
        for ball in balls:
            if not ball.potted:
                ball.move()
               # if ball.moving:
                alive=True

        for i in range(len(balls)):
            if not balls[i].potted:
                for j in range(len(balls)-(i+1)):
                    j+=i+1
                    if not balls[j].potted:
                        balls[i].collide(balls[j])
        draw(outerscreen,screen,balls)
        clock.tick()