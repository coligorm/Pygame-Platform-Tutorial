import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # Converting iterable into list, each entity will have its own list
        self.size = size
        self.velocity = [0,0]

    def update(self, movement=(0,0)):
        # Creating a vector to represent movement, so if gravity is being applied it is taken into account when moving up and down
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]


    def render(self, surface):
        surface.blit(self.game.assets['player'], self.pos)