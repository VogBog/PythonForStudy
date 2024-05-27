# Как установить
Файл со всеми папками под названием studyGame должен находиться в папке с проектом. Если папка studyGame находится ещё в какой-то папке studyGame, работать оно не будет
После этого открываем файлик по типу main.py, в котором пишется весь основной код, и пишем туда следующую строку
```python
import pygame
```
Если Питон будет жаловаться, что не знает, что такое pygame, мы наводимся мышкой на эту строчку, появится окошко. Там будет надпись
> import module pygame  

Нажимаем. Пайчарм сам скачает всё, что надо.
После этого строчку ```import pygame``` можно убирать. Она больше не нужна.  
Всё готово к использованию.
# Команды
Создание игры и выбор уровня:
```python
from studyGame.Game import Game #Импорт библиотеки

game = Game() #Создание игры
game.load_level(1) #Загрузка первого уровня
```

Движение игрока
```python
game.player.move_down()
game.player.move_left()
game.player.move_up()
game.player.move_right()
```

Сбор кристаллов
```python
game.player.collect_crystals()
```

Как узнать, на какой клетке находится игрок по координатам?
```python
x = game.player.get_x()
y = game.player.get_y()
```

Можно узнать, есть ли рядом с какой-то клеткой кристаллы
```python
if game.has_crystals_near(x, y):
    print("Рядом есть кристалы")
else:
    print("Нет кристаллов")
```

Таким образом можно автоматически проверять на наличие кристаллов и собирать их
```python
if game.has_crystals_near(game.player.get_x(), game.player.get_y()):
    game.player.collect_crystals()
```

Можно узнать, что за клетка находится на координатах
```python
cell = game.get_encapsule_cell(x, y)

player_cell = game.get_encapsule_cell(game.player.get_x(), game.player.get_y())

left_cell = game.get_encapsule_cell(
    game.player.get_x() - 1, game.player.get_y()
)
```

После того, как клетка получена, её можно проверять. Например узнать, можно ли на эту клетку наступить, или посещал ли игрок эту клетку раньше
```python
if left_cell.is_can_step():
    print("На эту клетку можно наступить")
if left_cell.is_meeting():
    print("Игрок посещал раньше эту клетку")

if left_cell.is_can_step() and not left_cell.is_meeting():
    print("На эту клетку игрок ещё не наступал, хотя можно")
    game.player.move_left()

if left_cell.is_crystal():
    print("Эта клетка - кристал. Надо собрать")
    game.player.collect_crystals()
```

Можно поставить игру на паузу. Пауза уберётся, если нажать на Enter
```python
game.pause_and_wait_for_enter()
```

# Простые решения
Решение 8-ого уровня
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

Решение 10-ого уровня
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

# Решение с помощью команд (для продвинутых)
На самом деле игрок принимает команды. Это классы, унаследованные от класса PlayerCommand
Всего у игрока есть 5 команд:
```python
CollectCrystals
MoveDownCommand
MoveRightCommand
MoveLeftCommand
MoveUpCommand
```

Отдать команду игроку можно с помощью метода:
```python
game.player.add_command(command)
```

Чтобы создать команду, нужно её импортировать, а потом создать экземпляр команды, передав в конструктор кортеж с координатами клетки, на которой выполняется команда.
Очевидно, что координатами клетки будет позиция игрока.
```python
from studyGame.playerCommands.moveUp import MoveUpCommand

x, y = game.player.get_x(), game.player.get_y()
game.player.add_command(MoveUpCommand((x, y)))
```

Этот код аналогичен вызову метода move_up(). Давайте посмотрим, что вообще написано в методе move_up()
```python
    def move_up(self):
        self.add_command(MoveUpCommand((self.__x, self.__y)))
```
Действительно, в методе move_up() просто отдаётся команда MoveUpCommand.
Такой метод решения может показаться куда более сложным и непонятным, однако знающий пользователь может заметно сократить весь свой код.
# Решение задач с помощью команд
Решение 8-ого уровня
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

Решение 10-ого уровня
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