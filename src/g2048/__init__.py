import random, os
from enum import Enum

class Tile:
    def __init__(self, value: int, posx: int, posy: int):
        self.value = value
        self.posx = posx
        self.posy = posy
    
    def __str__(self):
        return str(self.value) + "(" + str(self.posx) + " " + str(self.posy) + ")"

class Game2048:
    def __init__(self, size = 4):
        self.is_lost = False
        self.score = 0
        self.size = size
        self.board: list[list[None | Tile]] = [
            [None for i in range(self.size)] for j in range(self.size)
        ]

        self.reset()
    
    def __get_all_tiles(self) -> list[Tile]:
        tiles = []
        [[tiles.append(j) for j in i if j != None] for i in self.board]

        return tiles
    
    def getState(self):
        return {
            "board": [[0 if i == None else i.value for i in j] for j in self.board],
            "score": self.score
        }

    def reset(self):
        self.is_lost = False
        self.score = 0
        self.board: list[list[None | Tile]] = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        while True:
            x, y = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if self.board[y][x] is None:
                break
        if random.randint(0, 100) <= 10: val = 4
        else: val = 2
        self.board[y][x] = Tile(val, x, y)

    def tick(self, direction: str = "LEFT"):        
        tiles = self.__get_all_tiles()
        if all(self.board[i][j] is not None for i in range(len(self.board)) for j in range(len(self.board[0]))):
            self.is_lost = True
            return

        if direction == "UP":
            for tile in tiles:
                for i in range(tile.posy-1, -1, -1):
                    if self.board[i][tile.posx] == None:
                        last_y = tile.posy
                        self.board[i][tile.posx] = tile
                        tile.posy = i
                        self.board[last_y][tile.posx] = None
                    elif self.board[i][tile.posx].value == tile.value:
                        self.score += tile.value
                        self.board[i][tile.posx].value += tile.value
                        self.board[tile.posy][tile.posx] = None
        elif direction == "DOWN":
            for tile in tiles:
                for i in range(tile.posy+1, len(self.board)):
                    if self.board[i][tile.posx] == None:
                        last_y = tile.posy
                        self.board[i][tile.posx] = tile
                        tile.posy = i
                        self.board[last_y][tile.posx] = None
                    elif self.board[i][tile.posx].value == tile.value:
                        self.score += tile.value
                        self.board[i][tile.posx].value += tile.value
                        self.board[tile.posy][tile.posx] = None
        elif direction == "LEFT":
            for tile in tiles:
                for i in range(tile.posx-1, -1, -1):
                    if self.board[tile.posy][i] == None:
                        last_x = tile.posx
                        self.board[tile.posy][i] = tile
                        tile.posx = i
                        self.board[tile.posy][last_x] = None
                    elif self.board[tile.posy][i].value == tile.value:
                        self.score += tile.value
                        self.board[tile.posy][i].value += tile.value
                        self.board[tile.posy][tile.posx] = None
        elif direction == "RIGHT":
            for tile in tiles:
                for i in range(tile.posx+1, len(self.board[0])):
                    if self.board[tile.posy][i] == None:
                        last_x = tile.posx
                        self.board[tile.posy][i] = tile
                        tile.posx = i
                        self.board[tile.posy][last_x] = None
                    elif self.board[tile.posy][i].value == tile.value:
                        self.score += tile.value
                        self.board[tile.posy][i].value += tile.value
                        self.board[tile.posy][tile.posx] = None
        
        self.add_random_tile()
        
    def __str__(self):
        return "\n".join([" ".join([str(j.value).ljust(2, " ").rjust(3, " ") if j != None else " O " for j in i]) for i in self.board])