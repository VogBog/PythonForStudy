from studyGame.mapCells.mapCell import MapCell
import pygame


class WinCell(MapCell):
    def is_can_step(self) -> bool:
        return True

    def after_player_step_me(self, player):
        player.game.win()

    def get_color(self):
        return None

    def get_drawable(self, size):
        img = pygame.image.load("studyGame/sprites/finish.png")
        img = pygame.transform.scale(img, (size, size))
        return img

    def get_layer(self):
        return 1
