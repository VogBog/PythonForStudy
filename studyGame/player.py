import pygame
from studyGame.playerCommands.moveRight import MoveRightCommand
from studyGame.playerCommands.moveUp import MoveUpCommand
from studyGame.playerCommands.moveLeft import MoveLeftCommand
from studyGame.playerCommands.moveDown import MoveDownCommand
from studyGame.playerCommands.collectCrystals import CollectCrystals


class Player:
    movement_speed = .05

    def __init__(self, game):
        self.__x = 0
        self.__y = 0
        self.game = game
        game.on_every_frame.add(self.every_frame)
        self.__commands = []
        self.__size_multiplier = 1
        self.__wait_for_timer = 0
        self.__command_attempts = 0

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def die(self):
        self.__commands = []
        self.game.on_every_frame.remove(self.every_frame)
        self.game.on_every_frame.add(self.death_animation)

    def wait_for_seconds(self, value: float):
        self.__wait_for_timer = value
        self.game.on_every_frame.remove(self.every_frame)
        self.game.on_every_frame.add(self.__every_frame_wait_seconds)

    def __every_frame_wait_seconds(self):
        self.__wait_for_timer -= float(1) / self.game.FPS
        if self.__wait_for_timer <= 0:
            self.__wait_for_timer = 0
            self.game.on_every_frame.remove(self.__every_frame_wait_seconds)
            self.game.on_every_frame.add(self.every_frame)

    def death_animation(self):
        self.__size_multiplier -= .05
        self.__x += .025
        self.__y += .025
        if self.__size_multiplier <= .05:
            self.__size_multiplier = .05
            self.game.on_every_frame.remove(self.death_animation)
            self.game.stop()

    def every_frame(self):
        if len(self.__commands) > 0:
            self.__command_attempts = 0
            if self.__commands[0].try_activate(self):
                if len(self.__commands) == 0:
                    return
                self.__commands.pop(0)
                if len(self.__commands) > 0:
                    self.__commands[0].update((self.__x, self.__y))
                else:
                    self.game.pause()
        else:
            if self.__command_attempts < 30:
                self.__command_attempts += 1
            else:
                self.game.pause()

    def check_block(self):
        x = round(self.__x)
        y = round(self.__y)
        cell = self.game.get_map().get_cell(x, y)
        cell.on_player_step_me(self)
        next_x = round(self.__x)
        next_y = round(self.__y)
        if x == next_x and y == next_y and not cell.is_can_step():
            self.die()

    def set_pos(self, x: int, y: int):
        self.__x = x
        self.__y = y
        if self.game.is_map_loaded:
            raise Exception('Cheats', 'Calling set_pos while the game is running is CHEATING!')
        self.check_block()

    def add_command(self, command):
        self.__commands.append(command)
        if not self.game.is_running:
            self.game.start()

    def move_right(self):
        self.add_command(MoveRightCommand((self.__x, self.__y)))

    def move_up(self):
        self.add_command(MoveUpCommand((self.__x, self.__y)))

    def move_left(self):
        self.add_command(MoveLeftCommand((self.__x, self.__y)))

    def move_down(self):
        self.add_command(MoveDownCommand((self.__x, self.__y)))

    def collect_crystals(self):
        self.add_command(CollectCrystals((self.__x, self.__y)))

    def get_drawable(self, size: int):
        surf = pygame.image.load("studyGame/sprites/Mario.png")
        size *= self.__size_multiplier
        surf = pygame.transform.scale(surf, (size, size))
        return surf
