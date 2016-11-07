import pygame, random, sys, os
from math import sin, cos, radians
import numpy as np
from pygame.locals import *
from timeit import default_timer as timer


def rotatePolygon(polygon,theta):
    """Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = radians(theta)
    rotatedPolygon = []
    for corner in polygon:
        rotatedPolygon.append(( corner[0]*cos(theta)-corner[1]*sin(theta) , corner[0]*sin(theta)+corner[1]*cos(theta)) )
    return rotatedPolygon

def movePolygon(polygon,x,y):
    """Moves the given polygon which consists of corners represented as (x,y)"""
    movedPolygon = []
    for corner in polygon:
        movedPolygon.append(( corner[0]+x , corner[1]+y))
    return movedPolygon


class Agent:
    def __init__(self):
        self.position = (100.0, 100.0)
        self.speed = 0.333
        self.direction = random.randint(0,359)
        self.total_turned = 0
        self.total_food = 0

    def move(self):
        self.position = (self.position[0] + self.speed * cos(radians(self.direction)),
                         self.position[1] + self.speed * sin(radians(self.direction)))
        self.position = np.clip(self.position, 0, 199)


class Environment:
    def __init__(self):
        self.map = np.zeros((200, 200))

    def gen_diffuse(self, num_patches=624):
        mapSurface = pygame.Surface((200, 200), flags=0)
        mapSurface.fill((0,0,0))
        for i in range(num_patches):
            xpos = random.randint(0,200)
            ypos = random.randint(0,200)
            pygame.draw.polygon(mapSurface, (0,0,255), ((xpos-1,ypos),(xpos,ypos-1),(xpos+1,ypos),(xpos,ypos+1)))
        return mapSurface


    def gen_patchy(self, num_patches=4):
        mapSurface = pygame.Surface((200, 200), flags=0)
        mapSurface.fill((0,0,0))
        for i in range(num_patches):
            xpos = random.randint(0,200)
            ypos = random.randint(0,200)
            pygame.draw.polygon(mapSurface, (0,0,255), ((xpos-19,ypos),(xpos,ypos-19),(xpos+19,ypos),(xpos,ypos+19)))
        return mapSurface


class App:
    def __init__(self, debug=False):
        self._running = True
        self._display_surf = None
        self.debug = debug
        self.size = self.width, self.height = 600, 600
        self.subjectID = 0
        self.condition = 'diffuse'
        self.trialNum = 0
        self.trialStartTime = 0
        if self.debug is True:
            self.visiblePath = True
        else:
            self.visiblePath = False

    def draw_info_overlay(self):
        loc = (int(round(self.agent.position[0]*3)), int(round(self.agent.position[1]*3)))
        polygon_points = rotatePolygon([[0, 10], [-5, -10], [5, -10]], (self.agent.direction + 270)%360)
        polygon_points = movePolygon(polygon_points,loc[0],loc[1])
        pygame.draw.polygon(self._display_surf, (255, 255, 255), polygon_points, 0)

        font = pygame.font.Font(None, 40)
        text = font.render("score: " + str(self.agent.total_food), 1, (200, 200, 200))
        textpos = text.get_rect(topright=(self._display_surf.get_width() - 10, 10))
        self._display_surf.blit(text, textpos)

    def init_datafile(self, filename=None):
        if filename is None:
            filename = str(self.subjectID) + ".txt"
        f = open(filename, 'w')
        output = 'subjectID,condition,timestamp,food_eaten,turn_angle\n'
        f.write(output)
        f.close()

    def write_data(self, filename=None):
        if filename is None:
            filename = str(self.subjectID) + ".txt"
        f = open(filename, 'a')
        output = str(self.subjectID) + self.condition + str(timer() - self.start_time) + str(self.agent.total_food) + str(self.agent.total_turned)
        f.write(output)
        f.close()

    def on_init(self):
        if self.debug is False:
            self.subjectID = raw_input("Enter subject ID: ")
            while self.condition not in ("d", "c", "r"):
                self.condition = raw_input("Condition: (d)iffuse, (c)lustered, (r)andom: ")
                if self.condition == "r":
                    self.condition = random.choice(("c", "d"))
        pygame.init()
        self.init_datafile()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.env = Environment()
        if self.condition == "d":
            self.mapSurface = self.env.gen_diffuse()
        elif self.condition == "c":
            self.mapSurface = self.env.gen_patchy()
        self.seenSurface = pygame.Surface((200, 200), flags=0)
        self.seenSurface.fill((0, 0, 0))
        self.agent = Agent()
        self.start_time = timer()
        self.write_data()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYDOWN and event.key == K_j:
            self.agent.direction = (self.agent.direction - 35)%360
            self.agent.total_turned += 35
        elif event.type == KEYDOWN and event.key == K_l:
            self.agent.direction = (self.agent.direction + 35)%360
            self.agent.total_turned += 35

    def on_loop(self):
        self.agent.move()
        position = (int(round(self.agent.position[0])),int(round(self.agent.position[1])))
        mappxarray = pygame.PixelArray(self.mapSurface)
        seenpxarray = pygame.PixelArray(self.seenSurface)
        if self.visiblePath is True: seenpxarray[position[0], position[1]] = pygame.Color(255, 255, 255)
        if mappxarray[position[0],position[1]] > 0:
            if seenpxarray[position[0],position[1]] == 0:
                self.agent.total_food += 1
            seenpxarray[position[0], position[1]] = pygame.Color(0, 255, 0)

    def on_render(self):
        black = 0, 0, 0
        self._display_surf.fill(black)
        self._display_surf.blit(pygame.transform.scale(self.seenSurface, (600, 600)), (0,0))
        self.draw_info_overlay()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            self.clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App(debug=False)
    theApp.on_execute()


