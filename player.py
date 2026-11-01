import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.status = 'down'
        self.speed = 80
        self.moving = False
        self.frame_index = 0
        

        self.animations = {
        'up': [],
        'down':[],
        'left': [],
        'right': [],
        'idle_up': [],
        'idle_down': [],
        'idle_left': [],
        'idle_right': []
        }

        self.import_assets()

        self.image = self.animations[self.status][0]

        self.rect = self.image.get_rect(center=pos)
        self.hitbox = pygame.Rect(0,0,12,8)
        self.hitbox.midbottom = self.rect.midbottom
        
        self.pos = pygame.math.Vector2(self.hitbox.center)

        self.direction = pygame.math.Vector2()

    def import_assets(self):
        for animation in self.animations:
            full_path = f"animation/{animation}"

            self.animations[animation] = [pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1)) for img in import_folder(full_path)]
            if not self.animations[animation]:
                raise ValueError(f"No animation frames found in {full_path}")


    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'

        self.moving = self.direction.magnitude() > 0

    def move(self,dt,collision_rects):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)

        for obstacle in collision_rects:

            if self.hitbox.colliderect(obstacle):

                if self.direction.x > 0:
                    self.hitbox.right = obstacle.left

                elif self.direction.x < 0:
                    self.hitbox.left = obstacle.right

                self.pos.x = self.hitbox.centerx

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)

        for obstacle in collision_rects:

            if self.hitbox.colliderect(obstacle):

                if self.direction.y > 0:
                    self.hitbox.bottom = obstacle.top 

                elif self.direction.y < 0:
                    self.hitbox.top = obstacle.bottom 

                self.pos.y = self.hitbox.centery

        self.rect.midbottom = self.hitbox.midbottom

    def animate(self,dt):

        if self.moving:
            animation = self.status
            self.frame_index += 4 * dt

            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
            
            self.image = self.animations[self.status][int(self.frame_index)]
        else:
            animation = f'idle_{self.status}'
            self.frame_index += 2 * dt

            if self.frame_index >= len(self.animations[animation]):
                self.frame_index = 0

        self.image = self.animations[animation][int(self.frame_index)]

    def update(self,dt,collision_rects):
        self.input()
        self.move(dt,collision_rects)
        self.animate(dt)

