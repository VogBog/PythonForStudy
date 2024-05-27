from studyGame.playerCommand import PlayerCommand
from studyGame.particles.destroyCrystalParticle import DestroyCrystalParticle
from random import randint


class CollectCrystals(PlayerCommand):
    def try_activate(self, player) -> bool:
        x, y = round(player.get_x()), round(player.get_y())
        poses = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                 (x - 1, y), (x, y), (x + 1, y),
                 (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        is_collect_crystals = False
        for pos in poses:
            cell = player.game.get_encapsule_cell(pos[0], pos[1])
            if cell is not None and cell.is_crystal():
                is_collect_crystals = True
                player.game._Game__map.collect_crystal(pos[0], pos[1])

                for iy in range(-3, 4):
                    for ix in range(-3, 4):
                        if randint(0, 3) == 0:
                            player.game.particles.append(DestroyCrystalParticle(pos[0] + ix / 10, pos[1] + iy / 10,
                                                                            player.game.cell_size))
        player.wait_for_seconds(.5)
        if not is_collect_crystals:
            player.die()
        return True
