from studyGame.mapCells.mapCell import MapCell
from studyGame.mapCells.wallCell import WallCell
from studyGame.mapCells.crystalCell import CrystalCell


class EncapsuleCell:
    def __init__(self, cell: MapCell):
        self.__cell = cell

    def is_can_step(self) -> bool:
        return self.__cell.is_can_step()

    def is_meeting(self) -> bool:
        return self.__cell.is_meeting()

    def is_wall(self) -> bool:
        return isinstance(self.__cell, WallCell)

    def is_crystal(self) -> bool:
        return isinstance(self.__cell, CrystalCell)
