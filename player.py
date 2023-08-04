import pygame


class Player:
    def __init__(self):
        self.camX = 0
        self.camY = 0
        self.pos = [0, 0, 0]
        self.fov = 400
        