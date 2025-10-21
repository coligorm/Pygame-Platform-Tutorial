import sys
import pygame

from scripts.utils import load_multiple_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("editor")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_multiple_images('tiles/decor'),
            'grass': load_multiple_images('tiles/grass'),
            'large_decor': load_multiple_images('tiles/large_decor'),
            'stone': load_multiple_images('tiles/stone')
        }

        # For camera, camear can move in all four directions
        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        # Look at the scroll like the camera position
        # We had this scroll as an offset to anything we render below while running the game
        self.scroll = [0,0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.l_clicking = False
        self.r_clicking = False
        self.shift = False

        self.ongrid = True

    def run(self):
        while True:
            self.display.fill((0,0,0,0))

            # Move Camera
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            # Tile HUD to see current tile selected in Editor. set_alpha makes tile image slightly opaque
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            # Get mouse pixel coordinates in respect to the window
            mpos = pygame.mouse.get_pos()
            # Since we are scaling up our pixels to fit display, we must divide by the render scale
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            # Get coordinates of mouse in terms of tile position on the grid (// self.tilemap.tile_size)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                # Overlay of where the next on grid tile will go
                # Takes above tile_pos and converts it back into pixel coords (multiply by tile size) and adjusting based on the camera for rendering
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                # Overlay for placing tile off-grid
                self.display.blit(current_tile_img, mpos)
            
            # When click, place current tile by adding it to the tilemap
            if self.l_clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type' : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos': tile_pos}
            if self.r_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            # Eveything in Pygame needs to be created, even the option to 'Quit' the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # MOUSE CONTROLS
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.l_clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type' : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])}) # Note: We add the coords of the scroll (camera) to convert where we are clicking in the display to where we want to click in the "world"
                    if event.button == 3:
                        self.r_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.l_clicking = False
                    if event.button == 3:
                        self.r_clicking = False

                # KEYBOARD CONTROLS
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = True
                    
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid # Note: if set to false, we would have to hold. Instead 'G' key will toggle the ongrid on/off
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key ==   pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = False
                    
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()