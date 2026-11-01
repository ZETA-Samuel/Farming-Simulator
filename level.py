import pygame
import pytmx

from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from camera import CameraGroup
from inventory import Inventory
from shop import Shop


# from main import dt

class Level:
    def __init__(self):

        # get the display surface aka screen
        self.display_surface = pygame.display.get_surface()

        # sprite gropus
        self.all_sprites = CameraGroup()

        self.tmx_data = load_pygame('maps/farm_map.tmx')
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight
        self.all_sprites.set_bounds(self.map_width, self.map_height)
        self.tile_cache = {}
        self.collision_rects = []
        self.setup_collision()

        self.setup()
        self.setup_interactions()

        self.inventory = Inventory()
        self.shop = Shop(self.inventory)

        self.shop_open = False
        self.near_shop = False


    def setup(self):
        self.player = Player(pos=(TILE_SIZE * 4, TILE_SIZE * 4), group = self.all_sprites)

    def setup_interactions(self):

        self.shop_rect = None

        for obj in self.tmx_data.get_layer_by_name('Interactions'):

            if obj.name == 'chicken_coop_shop':

                self.shop_rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)

    def check_shop(self):

        self.near_shop = (
            self.shop_rect is not None and self.player.hitbox.colliderect(self.shop_rect)
        )

    def setup_collision(self):

        collision_layer = self.tmx_data.get_layer_by_name('collision')

        for x,y,gid in collision_layer:

            if gid != 0:

                rect = pygame.Rect(
                    x * self.tmx_data.tilewidth,
                    y * self.tmx_data.tileheight,
                    self.tmx_data.tilewidth,
                    self.tmx_data.tileheight
                )

                self.collision_rects.append(rect)

    def draw_map(self):

        zoom = self.all_sprites.zoom
        screen_rect = self.display_surface.get_rect()

        for layer in self.tmx_data.visible_layers:

            if isinstance(layer, pytmx.TiledTileLayer):

                for x, y, gid in layer:

                    if gid == 0:
                        continue

                    # Get the already-scaled image from cache
                    image = self.tile_cache.get(gid)

                    # Only scale the image once
                    if image is None:

                        original_image = self.tmx_data.get_tile_image_by_gid(gid)

                        if original_image is None:
                            continue

                        new_size = (
                            round(original_image.get_width() * zoom),
                            round(original_image.get_height() * zoom)
                        )

                        image = pygame.transform.scale(original_image, new_size)

                        self.tile_cache[gid] = image

                    # Calculate screen position
                    world_x = x * self.tmx_data.tilewidth
                    world_y = y * self.tmx_data.tileheight

                    screen_x = (world_x - self.all_sprites.offset.x) * zoom
                    screen_y = (world_y - self.all_sprites.offset.y) * zoom

                    # Skip tiles outside the screen
                    if (
                        screen_x + image.get_width() < 0 or
                        screen_y + image.get_height() < 0 or
                        screen_x > screen_rect.width or
                        screen_y > screen_rect.height
                    ):
                        continue

                    self.display_surface.blit(
                        image,
                        (round(screen_x), round(screen_y))
                    )

    def input(self,event):

        if self.shop_open:

            result = self.shop.handle_event(event)

            if result == "close":
                self.shop_open = False

            return

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                if self.near_shop and not self.shop_open:
                    self.shop_open = True

            if event.key == pygame.K_ESCAPE:
                self.shop_open = False

    # def draw_interaction(self):

    #     if self.near_shop and not self.shop_open:

    #         font = pygame.font.Font(None, 30)

    #         text = font.render("Press E to open shop", True,"white")

    #         rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))

    #         self.display_surface.blit(text,rect)
    
    def run(self,dt):

        self.check_shop()

        if not self.shop_open:
            # updating player
            self.all_sprites.update(dt, self.collision_rects)

        # updating camera based on the player
        self.all_sprites.update_camera(self.player)

        # drawing tiles with camera offset
        self.draw_map()

        self.all_sprites.draw(self.display_surface)

        if self.shop_open:
            self.shop.draw(self.display_surface)

        elif self.near_shop:
            font = pygame.font.Font(None,30)

            text = font.render("Press E to open shop", True, "white")

            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

            self.display_surface.blit(text, rect)

        