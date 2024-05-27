import abc


class PlayerCommand(abc.ABC):
    def __init__(self, block: tuple[int, int]):
        self.block = block

    @abc.abstractmethod
    def try_activate(self, player) -> bool:
        raise NotImplemented

    def update(self, block: tuple[int, int]):
        self.block = block
