# Pythong - Pong in Python

import pygame, sys
from pygame.locals import *

def line_line_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    # Taken from http://paulbourke.net/geometry/lineline2d/
    # Denominator for ua and ub are the same, so store this calculation
    d = float((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    # n_a and n_b are calculated as seperate values for readability
    n_a = float((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3))
    n_b = float((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3))
    # Make sure there is not a division by zero - this also indicates that
    # the lines are parallel.  
    # If n_a and n_b were both equal to zero the lines would be on top of each 
    # other (coincidental).  This check is not done because it is not 
    # necessary for this implementation (the parallel check accounts for this).
    if d == 0:
        return False
    # Calculate the intermediate fractional point that the lines potentially intersect.
    ua = n_a / d
    ub = n_b / d
    # The fractional point will be between 0 and 1 inclusive if the lines
    # intersect.  If the fractional calculation is larger than 1 or smaller
    # than 0 the lines would need to be longer to intersect.
    if ua >= 0. and ua <= 1. and ub >= 0. and ub <= 1.:
        return [x1 + (ua * (x2 - x1)), y1 + (ua * (y2 - y1))]
    return False

def resetBall(dir):
    ballRect.topleft = (640/2 - 10, 480/2 - 10)
    ballMotion[1][1] *= -1
    ballMotion[0][0] = 3
    ballMotion[0][1] = 3
    
def p2move():
    paddlespeed = 5
    if difficulty > 3:
        paddlespeed *= 2 ** (difficulty - 3)
    
    ypos = ballRect.centery
    xpos = ballRect.centerx
    
    ymagnitude = ballMotion[0][1]
    yvector = ballMotion[1][1]      
    
    xmagnitude = ballMotion[0][0]
    
    # simulate ball's motion to the p1 paddle, assuming return
    if difficulty >= 3 and ballMotion[1][0] == -1:
        steps = (ballRect.left - p1paddleRect.right) // xmagnitude
        for i in range(steps):
            ypos += ymagnitude * yvector
            if (yvector == -1 and ypos < ymagnitude) or (yvector == 1 and ypos + ymagnitude > window.get_height()):
                yvector *= -1
        xpos = p1paddleRect.right + 1
        ymagnitude += 1
        xmagnitude += 1
    
    if difficulty >= 2:
        steps = (p2paddleRect.left - (xpos + ballRect.width/2)) // xmagnitude
        for i in range(steps):
            ypos += ymagnitude * yvector
            if (yvector == -1 and ypos < ymagnitude) or (yvector == 1 and ypos + ymagnitude > window.get_height()):
                yvector *= -1
    
    '''
    # every loop is one frame of motion
    while distance > 0:
        # simulate horizontal motion
        distance -= ballMotion[0][0]

        # simulate vertical motion
        ypos += ballMotion[0][1] * yvector

        # discern when yvector changes
        if (yvector == -1 and ypos < ballMotion[0][1]) or (yvector == 1 and ypos + ballMotion[0][1] > window.get_height()):
            yvector *= -1
    '''
    print "Predicted YPos: " + str(ypos)
    if p2paddleRect.centery < ypos:
        motion = [paddlespeed, ypos - p2paddleRect.centery]
        motion.sort()
        motion = motion[0]
    elif p2paddleRect.centery > ypos:
        motion = [paddlespeed * -1, ypos - p2paddleRect.centery]
        motion.sort()
        motion = motion[1]
    else:
        motion = 0
    return motion

def moveBall():
    motionx = ballMotion[0][0] * ballMotion[1][0]
    motiony = ballMotion[0][1] * ballMotion[1][1]

    ballRect.move_ip(motionx, motiony)
  
pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((640,480))
pygame.display.set_caption('Pythong')

red = pygame.Color(255,0,0)
blue = pygame.Color(0,0,255)
green = pygame.Color(0,255,0)

mousex, mousey = 0, 0

font = pygame.font.Font('freesansbold.ttf', 32)
msg = "Pythong"

p1pos = [32, 480/2 - 50]
p2pos = [window.get_width() - 20 - 32, 480/2 - 50]
ballpos = [640/2 - 10, 480/2 - 10]

p1paddleRect = pygame.Rect(p1pos[0], p1pos[1], 20, 100)
p2paddleRect = pygame.Rect(p2pos[0], p2pos[1], 20, 100)
ballRect = pygame.Rect(ballpos[0], ballpos[1], 20, 20)

ballMotion = ([3, 3], [1, 1])

p1score = 0
p2score = 0

# 1: no prediction, just movement towards ball
# 2: opponent predicts when the ball is moving toward them
# 3: opponent predicts constantly
# opponent's speed limit doubles for every level above 3 (5 pixels per tick at 3, 10 at 4, 20 at 5, etc)
difficulty = 2

while True:
    window.fill((255,255,255))

    pygame.draw.rect(window, red, p1paddleRect)
    pygame.draw.rect(window, blue, p2paddleRect)
    pygame.draw.rect(window, green, ballRect)

    msg = "Difficulty: " + str(difficulty)
    msgSurface = font.render(msg, False, (160,160,160))
    p1scoretext = font.render("P1: " + str(p1score), False, (60,60,60))
    p2scoretext = font.render("P2: " + str(p2score), False, (60,60,60))

    window.blit(msgSurface, (window.get_width() // 2 - msgSurface.get_width() // 2, 20))
    window.blit(p1scoretext, (20,20))
    window.blit(p2scoretext, (window.get_width() - p2scoretext.get_width() - 20, 20))
    # may need rectSurface for it to work properly

    # process events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == K_UP:
                difficulty += 1
            if event.key == K_DOWN:
                if difficulty > 1:
                    difficulty -= 1

    # control paddles      
    '''
    key = pygame.key.get_pressed()
    if key[K_UP]:
    p1paddleRect.move_ip(0, -5)
    if key[K_DOWN]:
    p1paddleRect.move_ip(0, 5)
    '''
    mousepos = pygame.mouse.get_pos()
    p1paddleRect.centery = mousepos[1]
    # p1paddleRect.centery = ballRect.centery

    #move p2 paddle
    p2paddleRect.move_ip(0, p2move())

    # move ball
    ballx, bally = ballRect.centerx, ballRect.centery
    moveBall()

    if ballRect.bottom >= window.get_height() or ballRect.top < 0:
        ballMotion[1][1] *= -1

    # paddle collision testing
    ballEdgeL = pygame.Rect(ballRect.topleft, (1, 20))
    ballEdgeR = pygame.Rect(ballRect.topright, (1, 20))
    #  if ballEdgeL.colliderect(p1paddleRect.topright, (1, 100)) or ballEdgeR.colliderect(p2paddleRect.topleft, (1, 100)):
    # if ballRect.colliderect(p1paddleRect.topright, (1, 100)) or ballRect.colliderect(p2paddleRect.topleft, (1, 100)):
    
    #left paddle collision test
    intersect = line_line_intersect(
        ballx - ballRect.width/2, bally, 
        ballRect.left, ballRect.centery, 
        p1paddleRect.right, p1paddleRect.top, 
        p1paddleRect.right, p1paddleRect.bottom
    )
    if intersect:
        ballRect.centery = intersect[1]
        ballRect.left = p1paddleRect.right + 1
        ballMotion[1][0] *= -1
        ballMotion[0][0] += 1
        ballMotion[0][1] += 1
        
    #right paddle collision test
    intersect = line_line_intersect(
        ballx + ballRect.width/2, bally, 
        ballRect.right, ballRect.centery, 
        p2paddleRect.left, p2paddleRect.top, 
        p2paddleRect.left, p2paddleRect.bottom
    )
    if intersect: # or ballRect.colliderect(p2paddleRect):
        ballRect.centery = intersect[1]
        ballRect.right = p2paddleRect.left - 1
        ballMotion[1][0] *= -1
        ballMotion[0][0] += 1
        ballMotion[0][1] += 1
        
    # point scored
    if ballRect.right >= window.get_width():
    # p1 scored a point
        p1score += 1
        resetBall(-1)
    if ballRect.left < 0:
    # p2 scored a point
        p2score += 1
        resetBall(1)
        
    pygame.display.update()
    clock.tick(30)