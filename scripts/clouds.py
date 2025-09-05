import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0,0)):
        # We multply by the depth so if a cloud if further away, when the camera scrolls, the depth is multiplied
        # By the offset in order to create a nice parallax effect
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surface.blit(self.img, (render_pos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width()), (render_pos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height()))


class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for i in range(count):
            self.cloud.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))

        # Sorting the clouds by depth arranges the clouds from closet to furthest helping the clouds display propely when rendering
        # as render order matters
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset=(0,0)):
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)