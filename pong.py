__author__ = 'DipTanU_DaS'
#PONG is a classical video game which was implemented in 1970's.
#It was the successful implementation of Artificial Intelligence in video gaming industry.
#Here, in this game i have tried to implement my algorithm for AI and also altered the laws of collision between ball and bar.

#So, PLAY and ENJOY !!!.... :)
import pygame
import pygame.gfxdraw
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)

pygame.init()
DISPLAY = (600, 600)
FRAME = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("PONG")
FPS = 60
SPEED = 4


def message(text, color, x, y, size=30):
    font_object = pygame.font.SysFont('courierNew', size)
    lines = text.split(r"\n")
    for i in range(0, len(lines)):
        font_surface = font_object.render(lines[i], True, color)
        surface_rect = font_surface.get_rect()
        surface_rect.center = (x, y+i*size)
        FRAME.blit(font_surface, surface_rect)


class GameObject:
    def __init__(self, x, y, type="BAR", speedx=0, speedy=0, color=WHITE, score=0):
        self.x = int(x)
        self.y = int(y)
        self.type = type
        self.speedx = speedx
        self.speedy = speedy
        self.color = color
        self.score = score

    def set_pos(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def set_speed(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def move(self):
        self.set_pos(self.x+self.speedx, self.y+self.speedy)

    def draw(self):
        if self.type == "BAR":
            pygame.gfxdraw.aapolygon(FRAME, ((self.x, self.y), (self.x+100, self.y), (self.x+100, self.y+20), (self.x, self.y+20)), self.color);
            pygame.gfxdraw.aapolygon(FRAME, ((self.x+1, self.y+1), (self.x+99, self.y+1), (self.x+99, self.y+19), (self.x, self.y+19)), self.color);
        elif self.type == "BALL":
            pygame.gfxdraw.aacircle(FRAME, self.x, self.y, 10, self.color)
            pygame.gfxdraw.aacircle(FRAME, self.x, self.y, 9, self.color)


def game(score):
    player = GameObject(DISPLAY[0]/2-50, DISPLAY[1]-25, score=score[0])
    comp = GameObject(DISPLAY[0]/2-50, 5, score=score[1])
    ball = GameObject(DISPLAY[0]/2-5, DISPLAY[1]/2-5, "BALL", SPEED, SPEED)
    sign = [-1, 1]
    ball_speedx = SPEED*sign[random.randrange(0, 2)]*random.randrange(4, 11)/10.00
    ball_speedy = SPEED*sign[random.randrange(0, 2)]*random.randrange(4, 11)/10.00
    ball.set_speed(ball_speedx, ball_speedy)
    AI_flag = (ball_speedy<0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); quit()
                elif event.key == pygame.K_LEFT:
                    player.set_speed(-1*SPEED, 0)
                elif event.key == pygame.K_RIGHT:
                    player.set_speed(SPEED, 0)
                elif event.key == pygame.K_SPACE:
                    pause = True
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            elif event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                                pause = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.set_speed(0, 0)
        # Developing AI for computer player
        if AI_flag:
            t = abs((ball.y-comp.y-30)/ball.speedy)
            d = ball.x + t*ball.speedx
            if int(d/DISPLAY[0])%2 == 0 and d>0: d = d%DISPLAY[0]
            elif int(d/DISPLAY[0])%2 == 0 and d<0: d = (-1*d)%DISPLAY[0]
            elif d>0: d = DISPLAY[0]-d%DISPLAY[0]
            else: d = DISPLAY[0]-(-1*d)%DISPLAY[0]
            d = d-(comp.x+50)
        else: d = ball.x-comp.x-50

        if d>10: comp.speedx = SPEED
        elif d<-10: comp.speedx = -SPEED
        else: comp.speedx = 0

        # Display update
        FRAME.fill(BLACK)
        player.move()
        comp.move()
        ball.move()
        # player boundaries
        if player.x <= 0: player.set_pos(0, player.y)
        if player.x >= DISPLAY[0]-100: player.set_pos(DISPLAY[0]-100, player.y)
        # computer boundaries
        if comp.x <= 0: comp.set_pos(0, comp.y)
        if comp.x >= DISPLAY[0]-100: comp.set_pos(DISPLAY[0]-100, comp.y)
        # ball boundaries
        if 0<ball.y < DISPLAY[1]:
            # Normal elastic collision between ball and board side
            if ball.x <= 10:
                ball.set_pos(10, ball.y)
                ball.set_speed(-1*ball.speedx, ball.speedy)
            elif ball.x >= DISPLAY[0]-10:
                ball.set_pos(DISPLAY[0]-10, ball.y)
                ball.set_speed(-1*ball.speedx, ball.speedy)
            # Creating and altering virtual physics for collision between bar and ball
            if ball.y < comp.y+30 and comp.x-10 < ball.x < comp.x+110:
                ball.set_pos(ball.x, comp.y+30)
                hit = abs(comp.x+50 - ball.x)/50.00
                vx = (.5+hit)*ball.speedx
                vy = -(1.5-hit)*ball.speedy
                if vx<0.4*SPEED and vx>0: vx = 0.4*SPEED
                elif vx>2*SPEED: vx = 2*SPEED
                elif vx<-2*SPEED: vx = -2*SPEED
                elif vx>-0.4*SPEED and vx<0: vx = -0.4*SPEED
                if vy<0.4*SPEED and vy>0: vy = 0.4*SPEED
                elif vy>2*SPEED: vy = 2*SPEED
                elif vy<-2*SPEED: vy = -2*SPEED
                elif vy>-0.4*SPEED and vy<0: vy = -0.4*SPEED
                ball.set_speed(1.2*vx, 1.2*vy)
                AI_flag = False
            elif ball.y > player.y-10 and player.x-10 < ball.x < player.x+110:
                ball.set_pos(ball.x, player.y-10)
                hit = abs(player.x+50 - ball.x)/50.00
                vx = (.5+hit)*ball.speedx
                vy = -(1.5-hit)*ball.speedy
                if vx<0.4*SPEED and vx>0: vx = 0.4*SPEED
                elif vx>2*SPEED: vx = 2*SPEED
                elif vx<-2*SPEED: vx = -2*SPEED
                elif vx>-0.4*SPEED and vx<0: vx = -0.4*SPEED
                if vy<0.4*SPEED and vy>0: vy = 0.4*SPEED
                elif vy>2*SPEED: vy = 2*SPEED
                elif vy<-2*SPEED: vy = -2*SPEED
                elif vy>-0.4*SPEED and vy<0: vy = -0.4*SPEED
                ball.set_speed(1.2*vx, 1.2*vy)
                AI_flag = True
        else:
            player.draw(); comp.draw(); ball.draw()
            message("GAME OVER", WHITE, DISPLAY[0]/2, DISPLAY[1]/4, 60)
            if ball.y <0:
                message("Player WON.", WHITE, DISPLAY[0]/2, 3*DISPLAY[1]/8, 45)
                player.score +=1
            else:
                message("Player LOST.", WHITE, DISPLAY[0]/2, 3*DISPLAY[1]/8, 45)
                comp.score += 1
            message("Player = "+ str(player.score)+"\\nComputer = "+ str(comp.score), WHITE, DISPLAY[0]/2, 3*DISPLAY[1]/4, 45)
            message("Press N to play again.\\nPress R to reset game.\\nPress ESC to quit.", WHITE, DISPLAY[0]/2, DISPLAY[1]/2, 45)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_n:
                            game([player.score, comp.score])
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                        elif event.key == pygame.K_r:
                            game([0, 0])
                pygame.time.Clock().tick(5)

        player.draw()
        comp.draw()
        ball.draw()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)


def intro():
    loop = True
    FRAME.fill(BLACK)
    message("PONG", WHITE, DISPLAY[0]/2, DISPLAY[1]/8, 120)
    message("PONG is a classical video game"+"\\nwhich was implemented in 1970's."+
            "\\nIt was the successful"+"\\nimplementation of Artificial"+
            "\\nIntelligence in video games."+
            "\\nIn this game i have tried to"+"\\nimplement my algorithm for AI"+
            "\\nand also altered the laws of"+"\\ncollision between ball and bar.",
            WHITE, DISPLAY[0]/2, DISPLAY[1]/4, 30)
    message("Press N for new game.\\nPress ESC to quit.", WHITE, DISPLAY[0]/2, 3*DISPLAY[1]/4-20, 45)
    message("Use RIGHT and LEFT arrow to move"+"\\nthe player BAR(at lower side).", WHITE, DISPLAY[0]/2, 7*DISPLAY[1]/8, 30)
    pygame.display.update()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
                    loop = False

if __name__ == '__main__':
    intro()
    game([0, 0])
