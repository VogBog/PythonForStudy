from studyGame.playerCommand import PlayerCommand


class MoveLeftCommand(PlayerCommand):
    def try_activate(self, player) -> bool:
        player._Player__x -= player.movement_speed
        if player._Player__x <= self.block[0] - 1:
            player._Player__x = self.block[0] - 1
            player.check_block()
            return True
        return False
