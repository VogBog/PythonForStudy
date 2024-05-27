import abc


class MapCell(abc.ABC):
    __is_meeting = False

    @abc.abstractmethod
    def is_can_step(self) -> bool:
        raise NotImplemented

    def is_meeting(self):
        return self.__is_meeting

    def on_player_step_me(self, player):
        self.__is_meeting = True
        self.after_player_step_me(player)

    @abc.abstractmethod
    def after_player_step_me(self, player):
        raise NotImplemented

    @abc.abstractmethod
    def get_color(self):
        raise NotImplemented

    @abc.abstractmethod
    def get_drawable(self, size):
        raise NotImplemented

    @abc.abstractmethod
    def get_layer(self):
        raise NotImplemented
