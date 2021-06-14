import pygame

__all__ = ["create_sprite"]


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size[0], sprite_size[1]))
    sprite = pygame.Surface((sprite_size[0], sprite_size[1]), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite
