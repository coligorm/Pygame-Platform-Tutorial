import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_multiple_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()

        # Name the game window
        pygame.display.set_caption("Ninja Game")
        # Create screen window and set the resolution
        self.screen = pygame.display.set_mode((640, 480))
        # Render images onto display
        self.display = pygame.Surface((320, 240))
        # Set game clock to 60 FPS
        self.clock = pygame.time.Clock()

        # Demonstrational code for collision:
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
            'stone': load_multiple_images('tiles/stone'),
            'background': load_image('background.png'),
            'clouds' : load_multiple_images('clouds')
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        self.tilemap = Tilemap(self)

        # Look at the scroll like the camera position
        # We had this scroll as an offset to anything we render below while running the game
        self.scroll = [0,0]


    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0,0))

            # If we centered the camera on the player, the player would be positioned in the top left of the camera,
            # Due to how pygame renders images from top left.
            # So here, we minus half the wdith of the display from the center in order to actually have the player in the centre
            # The whole equation is finding where we want the camera to be (centered around the player) and adding to the scroll
            # Adding the divide 30 at the end, makes the camera move quicker the further away the player is from the centre, and slows
            # upon getting closer to the player to create a smooth scrolling camera
            self.scroll[0] += (self.player.rect().centerx -self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery -self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # Note: Render order is important. We want to render the tiles before the player as the player is ontop of the tiles.
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            # For debugging:
            # print(self.tilemap.tiles_around(self.player.pos))

            # Demonstrational code for collision:
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
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key ==   pygame.K_d:
                        self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)


Game().run()