from studyGame.Particle import Particle
from studyGame.spriteRenderer import SpriteRenderer
from pygame import Surface


class DestroyCrystalParticle(Particle):
    __anim_time = .3

    def get_sprite_renderer(self, game):
        if self.__anim_time > .1:
            self.__anim_time -= .01
        else:
            return None
        pos_plus = (1 - self.__anim_time) * game.cell_size / 2
        sprite = SpriteRenderer(Surface((self.size * self.__anim_time, self.size * self.__anim_time)),
                              (self.x * self.size + pos_plus, self.y * self.size + pos_plus))
        sprite.sprite.fill((0, 255, 120))
        return sprite
