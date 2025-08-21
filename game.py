import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_multiple_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        # Name the game window
        pygame.display.set_caption("Ninja Game")
        # Create screen window and set the resolution
        self.screen = pygame.display.set_mode((640, 480))
        # Render images onto display
        self.display = pygame.Surface((320,240))

        # Set game clock to 60 FPS
        self.clock = pygame.time.Clock()

        # Demonstrational code for collision
        # 
        # self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        # self.img.set_colorkey((0,0,0))

        # self.img_pos = [160, 260]

        # self.collision_area = pygame.Rect(50, 50, 300, 50)

        self.movement = [False, False]

        self.assets = {
            'player' : load_image('entities/player.png'),
            'decor': load_multiple_images('tiles/decor'),
            'grass': load_multiple_images('tiles/grass'),
            'large_decor': load_multiple_images('tiles/large_decor'),
            'stone': load_multiple_images('tiles/stone')
        }

        self.player = PhysicsEntity(self, 'player', (50,50), (8,15))

        self.tilemap = Tilemap(self)


    def run(self):
        while True:
            self.display.fill((14,219,248))

            # Note: Render order is important. We want to render the tiles before the player as the player is ontop of the tiles.
            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            # For debugging:
            # print(self.tilemap.tiles_around(self.player.pos))

            # Demonstrational code for collision
            # 
            # img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            # if img_r.colliderect(self.collision_area):
            #     pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            # else:
            #     pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)
            
            # self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            # self.screen.blit(self.img, self.img_pos)

            # Eveything in Pygame needs to be created, even the option to 'Quit' the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key ==   pygame.K_d:
                        self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))
            pygame.display.update()
            self.clock.tick(60)


Game().run()