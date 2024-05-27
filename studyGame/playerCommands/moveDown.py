from studyGame.playerCommand import PlayerCommand


class MoveDownCommand(PlayerCommand):
    def try_activate(self, player) -> bool:
        player._Player__y += player.movement_speed
        if player._Player__y >= self.block[1] + 1:
            player._Player__y = self.block[1] + 1
            player.check_block()
            return True
        return False
