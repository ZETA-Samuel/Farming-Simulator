import pygame
from os import walk
from os.path import join

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in sorted(img_files):
            if image.lower().endswith(('.png','.jpg','jpeg')):
                full_path = join(path,image)

                image_surf = pygame.image.load(full_path).convert_alpha()

                surface_list.append(image_surf)

    return surface_list