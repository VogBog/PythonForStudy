import abc


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    @abc.abstractmethod
    def get_sprite_renderer(self, game):
        raise NotImplemented
