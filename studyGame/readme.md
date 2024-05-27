# ��� ����������
���� �� ����� ������� ��� ��������� studyGame ������ ���������� � ����� � ��������. ���� ����� studyGame ��������� ��� � �����-�� ����� studyGame, �������� ��� �� �����
����� ����� ��������� ������ �� ���� main.py, � ������� ������� ���� �������� ���, � ����� ���� ��������� ������
```python
import pygame
```
���� ����� ����� ����������, ��� �� �����, ��� ����� pygame, �� ��������� ������ �� ��� �������, �������� ������. ��� ����� �������
> import module pygame  

��������. ������� ��� ������� ��, ��� ����.
����� ����� ������� ```import pygame``` ����� �������. ��� ������ �� �����.  
�� ������ � �������������.
# �������
�������� ���� � ����� ������:
```python
from studyGame.Game import Game #������ ����������

game = Game() #�������� ����
game.load_level(1) #�������� ������� ������
```

�������� ������
```python
game.player.move_down()
game.player.move_left()
game.player.move_up()
game.player.move_right()
```

���� ����������
```python
game.player.collect_crystals()
```

��� ������, �� ����� ������ ��������� ����� �� �����������?
```python
x = game.player.get_x()
y = game.player.get_y()
```

����� ������, ���� �� ����� � �����-�� ������� ���������
```python
if game.has_crystals_near(x, y):
    print("����� ���� ��������")
else:
    print("��� ����������")
```

����� ������� ����� ������������� ��������� �� ������� ���������� � �������� ��
```python
if game.has_crystals_near(game.player.get_x(), game.player.get_y()):
    game.player.collect_crystals()
```

����� ������, ��� �� ������ ��������� �� �����������
```python
cell = game.get_encapsule_cell(x, y)

player_cell = game.get_encapsule_cell(game.player.get_x(), game.player.get_y())

left_cell = game.get_encapsule_cell(
    game.player.get_x() - 1, game.player.get_y()
)
```

����� ����, ��� ������ ��������, � ����� ���������. �������� ������, ����� �� �� ��� ������ ���������, ��� ������� �� ����� ��� ������ ������
```python
if left_cell.is_can_step():
    print("�� ��� ������ ����� ���������")
if left_cell.is_meeting():
    print("����� ������� ������ ��� ������")

if left_cell.is_can_step() and not left_cell.is_meeting():
    print("�� ��� ������ ����� ��� �� ��������, ���� �����")
    game.player.move_left()

if left_cell.is_crystal():
    print("��� ������ - �������. ���� �������")
    game.player.collect_crystals()
```

����� ��������� ���� �� �����. ����� �������, ���� ������ �� Enter
```python
game.pause_and_wait_for_enter()
```

# ������� �������
������� 8-��� ������
```python
from studyGame.Game import Game

game = Game()
game.load_level(8)

for _ in range(3): game.player.move_up()
for _ in range(3): game.player.move_right()
up_cell = game.get_encapsule_cell(game.player.get_x(), game.player.get_y() - 3)
if up_cell.is_crystal():
    for _ in range(2): game.player.move_up()
    game.player.collect_crystals()
    for _ in range(2): game.player.move_down()
else:
    for _ in range(2): game.player.move_down()
    game.player.collect_crystals()
    for _ in range(2): game.player.move_up()
for _ in range(3): game.player.move_right()
for _ in range(4): game.player.move_up()
```

������� 10-��� ������
```python
from studyGame.Game import Game

game = Game()
game.load_level(10)


while not game.is_game_over():
    x, y = game.player.get_x(), game.player.get_y()
    if game.has_crystals_near(x, y):
        game.player.collect_crystals()

    cell = game.get_encapsule_cell(x - 1, y)
    if cell.is_can_step() and not cell.is_meeting():
        game.player.move_left()
        continue

    cell = game.get_encapsule_cell(x + 1, y)
    if cell.is_can_step() and not cell.is_meeting():
        game.player.move_right()
        continue

    cell = game.get_encapsule_cell(x, y + 1)
    if cell.is_can_step() and not cell.is_meeting():
        game.player.move_down()
        continue

    cell = game.get_encapsule_cell(x, y - 1)
    if cell.is_can_step() and not cell.is_meeting():
        game.player.move_up()
```

# ������� � ������� ������ (��� �����������)
�� ����� ���� ����� ��������� �������. ��� ������, �������������� �� ������ PlayerCommand
����� � ������ ���� 5 ������:
```python
CollectCrystals
MoveDownCommand
MoveRightCommand
MoveLeftCommand
MoveUpCommand
```

������ ������� ������ ����� � ������� ������:
```python
game.player.add_command(command)
```

����� ������� �������, ����� � �������������, � ����� ������� ��������� �������, ������� � ����������� ������ � ������������ ������, �� ������� ����������� �������.
��������, ��� ������������ ������ ����� ������� ������.
```python
from studyGame.playerCommands.moveUp import MoveUpCommand

x, y = game.player.get_x(), game.player.get_y()
game.player.add_command(MoveUpCommand((x, y)))
```

���� ��� ���������� ������ ������ move_up(). ������� ���������, ��� ������ �������� � ������ move_up()
```python
    def move_up(self):
        self.add_command(MoveUpCommand((self.__x, self.__y)))
```
�������������, � ������ move_up() ������ ������� ������� MoveUpCommand.
����� ����� ������� ����� ���������� ���� ����� ������� � ����������, ������ ������� ������������ ����� ������� ��������� ���� ���� ���.
# ������� ����� � ������� ������
������� 8-��� ������
```python
from studyGame.Game import Game
from studyGame.playerCommands.moveUp import MoveUpCommand
from studyGame.playerCommands.moveDown import MoveDownCommand

game = Game()
game.load_level(8)

for _ in range(3): game.player.move_up()
for _ in range(3): game.player.move_right()
up_cell = game.get_encapsule_cell(game.player.get_x(), game.player.get_y() - 3)
commands = [MoveDownCommand, MoveUpCommand]
if up_cell.is_crystal():
    commands = [MoveUpCommand, MoveDownCommand]
for _ in range(2): game.player.add_command(commands[0](
    (game.player.get_x(), game.player.get_y())))
game.player.collect_crystals()
for _ in range(2): game.player.add_command(commands[1](
    (game.player.get_x(), game.player.get_y())))
for _ in range(3): game.player.move_right()
for _ in range(4): game.player.move_up()
```

������� 10-��� ������
```python
from studyGame.Game import Game
from studyGame.playerCommands.moveUp import MoveUpCommand
from studyGame.playerCommands.moveDown import MoveDownCommand
from studyGame.playerCommands.moveLeft import MoveLeftCommand
from studyGame.playerCommands.moveRight import MoveRightCommand

game = Game()
game.load_level(10)

while not game.is_game_over():
    poses = [(-1, 0, MoveLeftCommand), (1, 0, MoveRightCommand),
             (0, -1, MoveUpCommand), (0, 1, MoveDownCommand)]
    if game.has_crystals_near(game.player.get_x(), game.player.get_y()):
        game.player.collect_crystals()
    for pose in poses:
        cell = game.get_encapsule_cell(game.player.get_x() + pose[0],
                                       game.player.get_y() + pose[1])
        if cell.is_can_step() and not cell.is_meeting():
            game.player.add_command(pose[2]((game.player.get_x(),
                                             game.player.get_y())))
```