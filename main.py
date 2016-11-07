import pygame, random
from math import sin, cos, radians
import numpy as np
from pygame.locals import *


class Agent:
    def __init__(self):
        self.position = (100.0, 100.0)
        self.speed = 0.333
        self.direction = random.randint(0,359)
        self.total_turned = 0
        self.total_food = 0
        self.last_int_pos = (int(round(self.position[0])),int(round(self.position[1])))

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
        if self.debug is True:
            self.visiblePath = True
        else:
            self.visiblePath = False

    def draw_info_overlay(self):
        font = pygame.font.SysFont("monospace", 40)
        text = font.render("score: " + str(self.agent.total_food), 1, (200, 200, 200))
        textpos = text.get_rect(centerx=self._display_surf.get_width() / 2)
        self._display_surf.blit(text, textpos)

    def on_init(self):
        if self.debug is False:
            self.subjectID = raw_input("Enter subject ID: ")
        pygame.init()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.env = Environment()
        self.mapSurface = self.env.gen_diffuse()
        self.seenSurface = pygame.Surface((200, 200), flags=0)
        self.seenSurface.fill((0, 0, 0))
        self.agent = Agent()

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
            seenpxarray[position[0], position[1]] = pygame.Color(255, 0, 255)
            if position != self.agent.last_int_pos:
                self.agent.total_food += 1
        self.agent.last_int_pos = position

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
    theApp = App(debug=True)
    theApp.on_execute()


