import time

import pygame

from studyGame.actions import Action
from studyGame.spriteRenderer import SpriteRenderer
from studyGame.map import Map
from studyGame.player import Player
from studyGame.mapCells.encapsuleCell import EncapsuleCell


class Game:
    SCREEN_RESOLUTION = (720, 720)
    BACKGROUND_COLOR = (0, 30, 0)
    FPS = 60

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Study Python")
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)
        self.on_every_frame = Action()
        self.background = []
        self.foreground = []
        self.top = []
        self.particles = []
        self.is_running = False
        self.__map = Map(self)
        self.player = Player(self)
        self.cell_size = 10
        self.is_map_loaded = False
        self.__is_game_over = False
        self.is_on_pause = False

    def get_map(self) -> Map:
        if self.is_map_loaded and not self.is_running:
            raise Exception('Cheats', 'Calling get_map while the game is running is CHEATING!')
        return self.__map

    def get_encapsule_cell(self, x, y) -> EncapsuleCell:
        rounded_x, rounded_y = int(round(x)), int(round(y))
        cell = self.__map.get_cell(rounded_x, rounded_y)
        return EncapsuleCell(cell)

    def has_crystals_near(self, x, y) -> bool:
        poses = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                 (x - 1, y), (x, y), (x + 1, y),
                 (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        for pose in poses:
            cell = self.get_encapsule_cell(pose[0], pose[1])
            if cell.is_crystal():
                return True
        return False

    def load_level(self, level_number: int):
        self.load_map('level_' + str(level_number))

    def prerender_map(self):
        self.background = []
        self.foreground = []
        self.top = []
        for y in range(self.__map.map_size):
            for x in range(self.__map.map_size):
                cell = self.__map.get_cell(x, y)
                renderer = SpriteRenderer(cell.get_drawable(self.cell_size), (x * self.cell_size, y * self.cell_size))
                if cell.get_color() is not None:
                    renderer.sprite.fill(cell.get_color())
                if cell.get_layer() == 0:
                    self.background.append(renderer)
                elif cell.get_layer() == 1:
                    self.foreground.append(renderer)
                else:
                    self.top.append(renderer)

    def load_map(self, map_name: str):
        self.__map.read_map(map_name + '.txt')
        self.player.set_pos(self.__map.player_spawn_pos[0], self.__map.player_spawn_pos[1])
        self.cell_size = min(self.SCREEN_RESOLUTION[0], self.SCREEN_RESOLUTION[1]) // self.__map.map_size
        self.prerender_map()
        self.is_map_loaded = True

    def pause(self):
        self.is_running = False

    def stop(self):
        self.is_running = False
        self.__is_game_over = True
        pygame.quit()

    def win(self):
        if not self.__map.is_all_crystals_collected():
            return

        self.background = []
        self.foreground = []
        self.top = []
        self.BACKGROUND_COLOR = (0, 255, 0)
        self.player.die()

    def pause_and_wait_for_enter(self):
        self.is_on_pause = True
        if not self.is_running and self.is_map_loaded:
            self.start()

    def is_game_over(self):
        return self.__is_game_over

    def start(self):
        if self.__is_game_over:
            return
        self.is_running = True

        while self.is_running:
            time.sleep(1 / self.FPS)
            self.screen.fill(self.BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == 13 and self.is_on_pause:
                        self.is_on_pause = False

            for i in self.background:
                self.screen.blit(i.sprite, i.pos)
            for i in self.foreground:
                self.screen.blit(i.sprite, i.pos)
            for i in self.top:
                self.screen.blit(i.sprite, i.pos)
            particles_to_delete = []
            for i in self.particles:
                particle = i.get_sprite_renderer(self)
                if particle is None:
                    particles_to_delete.append(i)
                else:
                    self.screen.blit(particle.sprite, particle.pos)
            for i in particles_to_delete:
                if i in self.particles:
                    self.particles.remove(i)
            if self.player is not None:
                self.screen.blit(self.player.get_drawable(self.cell_size),
                                 (self.player.get_x() * self.cell_size, self.player.get_y() * self.cell_size))

            if not self.is_on_pause:
                self.on_every_frame.invoke()

            if self.is_running:
                pygame.display.update()
