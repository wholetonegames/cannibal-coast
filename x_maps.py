from w_maze_gen import MazeMaker
import w_grid
import y_helpers
import z_grid
import z_enemy
import random
import math


class MapsModel:
    NAME_FOREST = "forest"
    NAME_TRIBE = "tribe"
    NAME_RIVER_NPC = "swamp"
    NAME_RIVER_ENEMY = "river"
    ALL_BOARDS = [NAME_FOREST, NAME_TRIBE, NAME_RIVER_NPC]

    def __init__(self):
        self.maze = MazeMaker(w=8, h=7)
        self.maze.hasLineBreaks = False
        self.maps = []
        self.add_batch_of_stages(y_helpers.MAX_STAGE_LOOP)

    def add_batch_of_stages(self, amount):
        boards = []
        for _x in list(range(4)):
            boards.append(random.choice(self.ALL_BOARDS))
        for iteration in list(range(amount)):
            self.maps += [
                self.get_ammo_board(boards[0], iteration),
                self.get_enemy_board(
                    boards[1], self.populate_board_with_enemies(3, boards[1])),
                self.get_enemy_board(
                    boards[2], self.populate_board_with_enemies(3, boards[2])),
                self.get_enemy_board(
                    self.NAME_RIVER_ENEMY, self.populate_board_with_enemies(4, self.NAME_RIVER_ENEMY)),
                self.get_enemy_board(
                    boards[3], self.populate_board_with_enemies(4, boards[3])),
                # BOSS
                self.get_enemy_board(
                    self.NAME_TRIBE, self.populate_board_with_enemies(5, self.NAME_TRIBE) + [z_enemy.explorer]),
            ]

    def populate_board_with_enemies(self, amount, stage_name):
        arr = []
        enemies = z_enemy.river_enemies if stage_name == self.NAME_RIVER_ENEMY else z_enemy.land_enemies
        for _i in list(range(amount)):
            e = random.choice(enemies)
            arr.append(e)
        return arr

    @property
    def last_index(self):
        return len(self.maps) - 1

    def get_enemy_board(self, board_type, enemyModels, bullet_type="ammo_spear"):
        enemyNumber = len(enemyModels)
        board = self.get_board(enemyNumber, is_npc_board=False)
        return {
            "board_type": board_type,
            "model": "grid_{}_w25xh15".format(board_type),
            "blockTypes": z_grid.palette[board_type],
            "pattern": board,
            "startPos": 0,
            "BulletHero": "ammo_bullet",
            "BulletEnemy": bullet_type,
            "enemyNumber": enemyNumber,
            "enemyModels": enemyModels,
        }

    def get_ammo_board(self, board_type, level_number):
        item_number = self.get_ammo_number(level_number)
        board = self.get_board(item_number)
        return {
            "board_type": board_type,
            "model": "grid_{}_w25xh15".format(board_type),
            "blockTypes": z_grid.palette[board_type],
            "pattern": board,
            "startPos": 0,
            "itemNumber": item_number,
        }

    def get_ammo_number(self, val):
        bullets = math.ceil((y_helpers.MAX_STAGE_LOOP - val) / 2)
        bullets = min(bullets, 3)
        bullets = max(bullets, 1)
        return bullets

    def get_board(self, chara_number, is_npc_board=True):
        board = self.maze.make_maze()
        board = self.maze.add_exits(board)
        if is_npc_board:
            board = self.maze.add_charas(board, b=chara_number)
        else:
            board = self.maze.add_charas(board, e=chara_number)
        board = self.maze.replace_empty(board)
        return board
