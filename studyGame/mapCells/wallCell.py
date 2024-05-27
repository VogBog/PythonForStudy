from studyGame.mapCells.mapCell import MapCell
import pygame


class WallCell(MapCell):
    def is_can_step(self) -> bool:
        return False

    def after_player_step_me(self, player):
        pass

    def get_color(self):
        return 150, 75, 150

    def get_drawable(self, size):
        return pygame.Surface((size, size))

    def get_layer(self):
        return 1
