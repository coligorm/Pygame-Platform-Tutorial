# Pygame-Platform-Tutorial

Repo for following Pygame Plaformer Tutorial on YouTube by DaFluffyPotato

[Source](https://www.youtube.com/watch?v=2gABYM5M0ww&)

# Notes:

First thing import pygame

initialise pygame

create screen window along with the resolution

then create a clock to force the game to run in 60fps
Do this as programs try to run the code as quick as possible, however, a game is a series of loops running over and over updating the screen for players, so we set a cap on this to 60fps in order for the game to continue running smoothly

Then create the game loop.
Each frame is an iteration in a loop (sometimes multiple)
Every loop we update everything and then update the screen and so on.

`clock.tick(60)`
forces the loop to at 60 fps - function is basically a dynamic sleep to keep the game a continuous 60fps

In SDL you have full control of the input.
`for event in pygame.event.get():`

For example, we have to create a quit event in order to close the application.

```python
if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
```

Making the game with OOP techniques is advisable.

Creating the game as it's own object using:

```python
class Game:

    def __init__(self):
```

And then make the screen and the clock as attribute of the game object with
`self.screen`

Then we move the game loop inside its own `def run(self)` function.

Once everything is inside the `Game` object, we have to initialise the game to run it using `Game().run()` to call the `def run(self)` function.

To put an image on the screen we use the `pygame.image.load([url to image])`
To put the image on the screen we use the screen's `blit()` function.

Position the image using x,y coordinates. The **top left of the screen is 0,0** which is different from the expected bottom left (or the centre) that would be used in graphs in maths.
This is similar to pixels of web dev.

`screen.blit()` is a memory copy. Copying a section of memory onto another surface.

In Pygame, a everything as a surface. The screen itself is a surface. Most images we use we want to copy the surface of the image from memory onto the screen surface. **Like a sticker book, or a collage of layering images onto other images.**

Now for movement.
We need to add a new event check to our `event in pygame.event.get()` loop.
The event for a button press is `KEYDOWN`.

These events are fired when you press or release the keys, not when it is held down.
There are built-in functions for this - however, we will make our own.

So far, this updates the Boolean `self.movement`. We want to make this change our `self.iamge_pos` in order to move the image.
`self.image_pos[1] += (self.movement[1] - self.movement[0]) * 5`

Doing this moves the image, but it leaves a trail of where the image last was. In order to fix this, we have to reset/refresh the screen every time something moves.

We also need to remove the background of the image. The background of the cloud is black so we use `set_colorkey` to black to tell the program which colour to make transparent.
`self.img.set_colorkey((0,0,0))`

**Collisions**
Collision detection is the first step in applying physics to your game.
Not collision in the sense that your character has ran into a wall, it is collision in the sense that you are making contact with an area.

Pygame supports basic rectangle collision
`self.collision_area = pygame.Rect(50, 50, 300, 50)`
`// top left position (first two parameters), size (next two parameters: width, height)`

We also want to add a collision rectangle for our cloud.

Now we add our collision test for the cloud and the `collision_area`.

```python
if img_r.collidedict(self.collision_area): // if the rectangles are touching
```

**Layering is based on the render order**
Note: the sticker book/collage simile

## Creating a player in OOP style

[Chapter Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=1987s)

creating a folder for your scripts
Inside create an entity script and call it `PhysicsEntity` as we will use this to define our physics later.

Initialise the function and take the game as a parameter so that the script can access everything within the game. (quick and easy way to handle the scope of the entity)

Moving your player, it is best to use basic level of physics - using acceleration and velocity.

Creating a vector for how we want to control movement for the entity in each frame:
`frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])`

For example, moving up will apply gravity to the velocity to determine the movement, however, moving right and left, gravity wont effect the movement.

In order to actually move we have to update seperatly x and y dimensions:

```python
self.pos[0] += frame_movement[0]
self.pos[1] += frame_movement[1]
```

Then we have to create our player entity in the game code and render them.
Inside the `init`:
`self.player = PhysicsEntity(self, 'player', (50,50), (8,15))`
And inside the run function:

```python
self.player.update((self.movement[1] - self.movement[0], 0))
self.player.render(self.screen)
```

### Utility code

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=42m15s)

We will create a `utils.py` file to store utility code and scripts that we will build upon as we update the game.
First we will create a `load_image` function that we will use in our main `game.py` file to access the assets and load images

```python
def load_image(path):

    img = pygame.image.load(BASE_IMG_PATH + path).convert() # convert internalised reference of the image for performance

    img.set_colorkey((0,0,0))

    return img
```

> *Note*: Don't forget to add `.convert()` in order to convert the image for better rendering and performance.

Now we can load the images by adding in the game `init`.  We will store all our loaded images and assets inside a `self.assets` dictionary:

```python
self.assets = {
 'player' : load_image('entities/player.png')
}
```

### Image Scaling

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=45m30s)

To scale our player so that they're bigger and we can see it we do the following:
`self.display = pygame.Surface((320,240))`

In this project, we take `self.screen` to be the window and then we render onto `self.display`, which sits "on top" of the screen.

> *Note:* We create the `pygame.Surface()` to be half the resolution of the `pygame.display`. This is because after we render everything onto the surface, we will scale it up to fit the screen, hence, making the images themselves larger and adding a nice pixel art effect.

`Surface` function generates an empty surface/image (All black). This is useful for rendering stuff from memory.

Then we render everything onto the display instead of the screen.
At the bottom of the code add the code to then put the display onto the screen:
`self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))`

We also use this to scale the display to fit the screen, thus, making our player larger in size.

## Tiles and Physics

[Section link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=48m26s)

Create a `tilemap.py` script.

```python
class Tilemap:
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.timemap = {}
        self.offgrid_tiles = []
```

We want two systems of tiles:

- `self.tilemap` = where every single tile is on a grid
- `self.offgrid_tiles` = this is where we have tiles that are off grid (we will use this for tiles that aren't being applied to physics), such as background images

The `tilemap` is a dictionary to keep a record of where the tiles are located.

Example:

```python
[[0,0,0,0]
 [0,1,1,0]
 [1,1,1,1]]
```

Let's say the above is a hill, where the ground is located where the 1 is.
The problem with this list of list method, is that is there is a lot of air in your world then you have to fill in every 0, which gets convoluted.

So we use a dictionary. Example:

```python
{(0,0) : 'grass', (0,1) : 'dirt' (100,0) : 'grass'}
```

This way we can pick where we want tiles, based on the `(x,y)` coordinates located in the dictionary keys. Then we wont have to fill in where air/no tile exists.

However, in our use case, we will use strings as our keys instead of tuples as this makes it easier to work with the tile names saved in our assets folders.

Using a `for` loop in the `tilemap.py` to create a dictionary of a horizontal line of grass tiles from 3 on x-coordinate:
`self.tilemap[str(3 + i) + ';10'] = {'type' : 'grass', 'variant' : 1, 'pos' : (3 + i, 10)}

The key is the tile's positional coordinate represented as a string (stated above as this is easier with the file naming).
The value is a dictionary containing each tile's asset information, i.e. the type, variant and position (position should match the key).

### Load Multiple Images

Then we want to create a `load_multiple_images` function in our `utils.py` file to load all the tile images at once. We could load the full directory at once but for now we will just load the images we need.
`os.listdir` is used to take a path and take all the files within that path, i.e. if we go to the image/tiles/grass directory that contains all the grass_01, grass_02 etc. tiles.

We then load these images into a dictionary called `assets` in `game.py` using our function:

```python
self.assets = {
            'decor': load_multiple_images('tiles/decor'),
            'large_decor': load_multiple_images('tiles/large_decor'),
            'grass': load_multiple_images('tiles/grass'),
            'stone': load_multiple_images('tiles/stone'),
            'player' : load_image('entities/player.png')
        }
```

> *Note:* the images will be contained in a list. This is important for the next render function within `tilemap.py`.

We then create a `render` function inside `tilemap.py`, in order to render the tiles onto the game screen.

```python
def render(self, surface):
        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assests[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
```

> *Explanation:*
`tilemap` is a dictionary we created to store the tiles that are affected by gravity.  When we iterate through a dictionary we access the keys, in our case, the location of the tile in a string format (`4;10`). We access the tile itself (the dictionary value) by calling `self.tilemap[location]`.
To render (and put the image on the screen), we use the `blit` function on the assets variable inside `self.game`.
We want to access `grass`. It is inside the value at the key `type` . The variant is the index of the image we want to use. Then we get the position of the tile. We multiple the position by the tile size, as the coordinates is in reference to the grid. We convert the position to pixels by multiplying by `self.tile_size`.

Then we want to do the same for the `offgrid_tiles`. These tile positions don't need to be multiplied by the tile size, as it is off the grid and is positioned by coordinates on the screen.

### Gravity

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=63m36s)

First, we will apply gravity. We will do this to our `PhysicsEntity` in our `entities.py` file.
We will apply a basic terminal velocity for this. As we fall, we accelerate, but we want to start slow and speed up until we each a max velocity.
`self.velocity[1] = min(5, self.velocity[1] + 0.1)`
Here, we use Python's `min` function to take the lesser of the two values applied. As velocity increases, it gets capped at our max velocity of 5.

> *Note:* That the game screen's top left cover is `(0,0)`, therefore, a positive y-value of 5, is the player "falling down" the screen.

### Physics

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=66m)

We want to add collision to our tiles so that the player doesn't pass through them.
A trick to this, is to check the collision of the nearby tiles to the player, rather than checking all tiles for collision. This improves performance.

Since our player is small, we can check the 3 x 3 grid of tiles around our player:
`NEIGHBOUR_OFFSETS = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (0,0), (-1,1), (0,1), (1,1)]`

Then we can get around the player. However, our player positioned by pixel where our tiles are on a grid. We will do a trick to handle this in our `tiles_around` function:

```python
tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
```

`tile_loc` is a tuple of x-y-coordinates. We simply take in a position in pixels and do a floor division (`//`) by the `tile_size`, which rounds the answer from the division to the nearest integer. We convert the answer to an `int` afterwards for consistency as floating point division can cause small inconsistencies but can make a big difference when it comes to grids.
> *Example:*
> `int(0.9) => 0`
> `int(- 0.9) => 0`
> Here, 0.9 is almost at grid position 1 and - 0.9 is almost at grid position -1, however, both would be position on the same grid space of 0.

After the the `tile_loc` is found, we want to know which tiles to check for collision, `check_loc`. We go through our `NEIGHBOUR_OFFSETS` and add the value to the `pos` that we passed into the function.
This will give us the coordinates of the tiles we want to check, then we simple see `if check_loc in self.tilemap`.
Remember, `tilemap` is a dictionary containing all our physical tiles. If the tile is not in the dictionary then it is empty space and does not have physics or collision.

To test it is working, insert the following code into the main game loop:
`print(self.tilemap.tiles_around(self.player.pos))`

Next, back in the `tilemap.py`, we want to create another function so that the physics only gets applied to certain tiles.
We use the `physics_rect_around` function for this.
We iterate through the returned `tiles_around` and check the `tile['type']`.
Add the **variable constant** `PHYSICS_TILES = {'grass', 'stone'}` as a set (quicker for look-up compared to list).
If the `tile_around` is in `PHYSICS_TILES` then we mark it as a `pygame.Rect()` like we did when applying physics to the clouds as a physics test earlier.

> *Note:* `pygame.Rect()` can be used just as an item in memory to apply physics to or run collisions on them, without needing to "draw a rectangle".

To test:

```python
print(self.tilemap.physics_rects_around(self.player.pos))
```

### Collision Detection

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=77m15s)

Now to apply collisions to these `rect`'s, we have to pass the `tilemap` into the game by adding it to the `update` functions inside the `entities.py` file.

In order to make collisions work, we need to rectangles - one for the entity that has physics, and the other for which the entity collides with.

Add a function for generating the rectangle for the entity:

```python
def rect(self):
 return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
```

> *Note:* The collision point for our entity is the top left, not the centre. That's how Python handles `blit` so it makes sense for our physics to work the same way so that everything works correctly.
>
> [Here's a link to a full tutorial on Pygame Physics](https://youtu.be/a_YTklVVNoQ?si=QIfrtcvDtMbR0E9X)

Because we have separated our movement into two separate axis ( x and y ), it makes it easier to handle collision. If we are moving right along the x-axis, and collide with a wall to the right of us, the movement along the x knows to stop, or respond by snapping the entity's right edge to the left of the tile that is collided with.

```python
self.pos[0] += frame_movement[0]
 entity_rect = self.rect()
 for rect in tilemap.physics_rects_around(self.pos):
  if entity_rect.colliderect(rect):
   if frame_movement[0] > 0:
    entity_rect.right = rect.left
   if frame_movement[0] < 0:
    entity_rect.left = rect.right

   self.pos[0] = entity_rect.x
```

We also want to add a new variable to track our collisions and update the collisions code block above.
We track the collisions as a dictionary with Boolean values:
`self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}`

We also want to reset the collisions back to `False` every frame.

### Jump

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=86m26s)

Simply add another `event.type` check for the up key (`K_UP`) and set it -3 (Moving up on the y-axis is negative). Then the gravity we have applied will kick in and slowly make us fall back down to the ground to create a smooth jump:
`if event.key == pygame.K_UP:
 `self.player.velocity[1] = -3`

## Camera & Sky

[Chapter Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=87m49s)

Camera moving is an illusion. What we do is move the screen and everything to the left if we are moving right etc.

We will add a new `self.scroll` variable to control the movement of the "camera".

To apply this camera, we have to add an `offset=self.scroll` to everything that is rendered in the game loop. Now that it is passed as an argument, we need to add it into the respective functions.

To do this, we deduct the offset from the position of the rendered item. We deduct as by moving the camera negative (to the left, it looks like we are panning right).

The offset needs to be added to the screen, player tile map etc.

### Camera Focus on Player

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=91m2s)

We don't want the camera to be rigid on the player, we want it to slowly follow, but the further the player gets away then the quicker the camera moves to keep up.

Centre the camera:

```python
self.scroll[0] += (self.player.rect().centerx -self.display.get_width() / 2)
```

Again, since everything is rendered at the top left of the screen, we divide by half the width to get the centre of the screen (and the same with the y-axis, but half the height).

To finish the expression so that the camera is a fluid flowing following motion, we deduct `self.scroll[0]`. We are especially getting where we want the camera to move to, by taking the centre of the player, aligning it to the centre of the screen, then finding how far away the scroll is.
Finally, we divide the whole lot by 30, so no matter how far away the scroll is from the player, it takes 30ms to get where it needs to be. The further away, the faster it moves.
Also, convert both x and y values of the scroll  to an int. If not, there is a gitteriness to the player due to both using floating points and there is a sub-pixel difference. Converting the camera scroll to an `int`, removes this by rounding off the excess. This isn't an issue like with the tiles, as it wont be noticeable that the camera might move and be one pixel off, but when it comes to a tile grid it makes a difference.

The whole `self.scroll` block looks like this:

```python
self.scroll[0] += (self.player.rect().centerx -self.display.get_width() / 2 - self.scroll[0]) / 30
self.scroll[1] += (self.player.rect().centery -self.display.get_height() / 2 - self.scroll[1]) / 30
render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
```

### Clouds

[Section Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=97m11s)

First, add `cloud.py` script, with a `random` import and create the `Cloud` class:

```python
class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
```

Create a `update` function and update the position with the speed of the cloud.

Create a `render` function to display the clouds.
`render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)`
We multiply by the depth so if a cloud is further away, when the camera scrolls, the depth is multiplied by the offset in order to create a nice parallax effect.

Then we need to `blit()` the cloud so it displays on the screen.  Here we will apply a trick so that the clouds are constantly panning across the screen.
To make anything loop across the screen in computer graphics, we use the **modulo operator** (`%`).

We take the cloud's `render_pos[0]` and mod the width of the screen's surface with an extra width (the size of the cloud) so that the moment the cloud touches the side of the screen it doesn't teleport over to the other side - we want the whole cloud to continue past the width of the screen and then loop back around. Then subtract the size of the cloud to fully make sure the loop is correct.
`render_pos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width()`
Do the same for the y axis.

Then create a `Clouds` class to store all clouds.
We will use random to generate the size, number and size of the clouds.
We use a `lambda` to sort the clouds by the depth, so that they appear in render order to insure that the clouds are correctly layered when they pass in front or behind one another.

Finally, import them into the game by creating a `self.clouds` and also `load_images` of the cloud image. Redner it on the display etc. etc.

## Optimization

[Chapter Link](https://www.youtube.com/watch?v=2gABYM5M0ww&t=106m43s)
