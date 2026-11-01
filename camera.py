import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self, zoom=3):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.zoom = zoom

        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()

        # Camera dead-zone box
        box_width = screen_width * 0.4
        box_height = screen_height * 0.4

        self.camera_box = pygame.Rect(0,0, box_width, box_height)
        self.camera_box.center = (screen_width // 2, screen_height // 2)

        self.image_cache = {}

    def update_camera(self, target):

        player_screen_x = (target.rect.centerx - self.offset.x) * self.zoom
        player_screen_y = (target.rect.centery - self.offset.y) * self.zoom


        if player_screen_x < self.camera_box.left:
            self.offset.x -= (self.camera_box.left - player_screen_x) / self.zoom

        elif player_screen_x > self.camera_box.right:
            self.offset.x += (player_screen_x - self.camera_box.right) / self.zoom

        if player_screen_y < self.camera_box.top:
            self.offset.y -= (self.camera_box.top - player_screen_y) / self.zoom 

        elif player_screen_y > self.camera_box.bottom:
           self.offset.y += (player_screen_y - self.camera_box.bottom) / self.zoom 

        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()

        max_x = max(0, self.map_width - screen_width / self.zoom)
        max_y = max(0, self.map_height - screen_height / self.zoom)

        self.offset.x = max(0, min(self.offset.x, max_x))
        self.offset.y = max(0, min(self.offset.y, max_y))

    def get_scaled_image(self,image):

        key = (id(image), self.zoom)

        if key not in self.image_cache:
            width = round(image.get_width() * self.zoom)
            height = round(image.get_height() * self.zoom)

            self.image_cache[key] = pygame.transform.scale(image, (width,height))

        return self.image_cache[key]

    def set_bounds(self,width,height):
        self.map_width = width
        self.map_height = height

    def draw(self,surface):

        for sprite in self.sprites():
            scaled_image = self.get_scaled_image(sprite.image)

            screen_x = (sprite.rect.centerx - self.offset.x) * self.zoom
            screen_y = (sprite.rect.centery - self.offset.y) * self.zoom

            scaled_rect = scaled_image.get_rect(center=(round(screen_x),round(screen_y)))

            surface.blit(scaled_image,scaled_rect)

            if hasattr(sprite,'hitbox'):

                hitbox = sprite.hitbox.copy()

                hitbox.x = round((hitbox.x - self.offset.x) * self.zoom)
                hitbox.y = round((hitbox.y - self.offset.y) * self.zoom)

                hitbox.width = round(hitbox.width * self.zoom)
                hitbox.height = round(hitbox.height * self.zoom)

                # pygame.draw.rect(surface, 'red',hitbox,2)
            

