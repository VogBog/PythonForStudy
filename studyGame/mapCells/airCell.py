from studyGame.mapCells.mapCell import MapCell
import pygame


class AirCell(MapCell):
    def is_can_step(self) -> bool:
        return False

    def after_player_step_me(self, player):
        pass

    def get_color(self):
        return None

    def get_drawable(self, size):
        img = pygame.image.load("studyGame/sprites/background.png")
        img = pygame.transform.scale(img, (size, size))
        return img

    def get_layer(self):
        return 0
