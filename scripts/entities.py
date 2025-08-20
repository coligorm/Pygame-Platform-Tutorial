import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # Converting iterable into list, each entity will have its own list
        self.size = size
        self.velocity = [0,0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0,0)):
        # Creating a vector to represent movement, so if gravity is being applied it is taken into account when moving up and down
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        entity_rect = self.rect()

        self.pos[0] += frame_movement[0]
        
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y

        # Applying terminal velocity to cap the gravity at a speed of 5
        # Note: On the game screen 0,0 is the top left, therefore, positive y is going down on the screen
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

    def render(self, surface):
        surface.blit(self.game.assets['player'], self.pos)