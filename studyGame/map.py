from studyGame.mapCells.mapCell import MapCell
from studyGame.mapCells.airCell import AirCell
from studyGame.mapCells.groundCell import GroundCell
from studyGame.mapCells.wallCell import WallCell
from studyGame.mapCells.winCell import WinCell
from studyGame.mapCells.crystalCell import CrystalCell
from studyGame.spriteRenderer import SpriteRenderer
from random import randint


def seq_to_cell(seq: chr) -> MapCell:
    if seq == 'o' or seq == 's':
        return GroundCell()
    elif seq == 'H':
        return WallCell()
    elif seq == 'X':
        return WinCell()
    elif seq == 'C':
        return CrystalCell()
    return AirCell()


class Map:
    def __init__(self, game):
        self.player_spawn_pos = (0, 0)
        self.__data = []
        self.map_size = 0
        self.__crystals = 0
        self.__max_crystals = 0
        self.__random = 0
        self.game = game

    def is_cell_out_of_range(self, x: int, y: int) -> bool:
        return y < 0 or y >= len(self.__data) or x < 0 or x >= len(self.__data[y])

    def is_all_crystals_collected(self):
        return self.__crystals >= self.__max_crystals

    def get_cell(self, x: int, y: int) -> MapCell:
        if self.is_cell_out_of_range(x, y):
            return AirCell()
        else:
            return self.__data[y][x]

    def __get_command_value(self, commands, command, count = 1):
        if command in commands:
            index = commands.index(command)
            response = []
            for i in range(count):
                if index + 1 + i >= len(commands):
                    return None
                response.append(commands[index + 1 + i])
            return response
        return None

    def __check_commands(self, commands):
        value = self.__get_command_value(commands, "crystals")
        if value is not None:
            self.__max_crystals = int(value[0])
        value = self.__get_command_value(commands, "random")
        if value is not None:
            self.__random = int(value[0])
        value = self.__get_command_value(commands, "size")
        if value is not None:
            self.map_size = int(value[0])

    def read_map(self, file_name : str):
        self.__data = []
        self.player_spawn_pos = (0, 0)
        self.map_size = 0
        crystals = 0
        with open('studyGame/levels/' + file_name, 'r') as file:
            while True:
                cells = file.readline()
                if not cells or len(cells) < 4:
                    break
                if cells.startswith("custom"):
                    commands = cells.split()
                    self.__check_commands(commands)
                    if self.__random > 0:
                        rand = randint(0, self.__random - 1)
                        for _ in range(rand * (self.map_size + 1)):
                            file.readline()
                    continue
                to_add = []
                for i in cells:
                    to_add.append(seq_to_cell(i))
                    if i == 's':
                        self.player_spawn_pos = (len(to_add) - 1, len(self.__data))
                    if isinstance(to_add[-1], CrystalCell):
                        crystals += 1
                self.__data.append(to_add)
        if self.map_size == 0:
            self.map_size = max(len(self.__data), len(self.__data[0]))
        if self.__max_crystals == 0:
            self.__max_crystals = crystals

    def set_cell(self, x: int, y: int, cell: MapCell):
        if self.is_cell_out_of_range(x, y):
            return
        self.__data[y][x] = cell
        self.game.prerender_map()

    def collect_crystal(self, x, y):
        self.__crystals += 1
        if not self.is_cell_out_of_range(round(x), round(y)):
            self.set_cell(round(x), round(y), GroundCell())
