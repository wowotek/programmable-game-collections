import random, time, os
from colorama import Fore, init, Style
init()

class Block:
    def __init__(self, name: str, block: list[list[1 | 1]], posx: int = 0, posy: int = 0):
        self.name = name
        self.__block = block
        self.posx = posx
        self.posy = posy
    
    @property
    def block(self):
        return [i for i in self.__block if sum(i) != 0]
    
    def rotate_left(self):
        # Transpose the matrix
        transposed = [[row[i] for row in self.__block] for i in range(len(self.__block[0]))]
        
        # Reverse the rows of the transposed matrix
        self.__block = [row[::-1] for row in transposed]

    def rotate_right(self):
        # Transpose the matrix
        transposed = [[row[i] for row in self.__block] for i in range(len(self.__block[0]))]
        
        # Reverse the columns of the transposed matrix
        self.__block = [list(reversed(row)) for row in transposed]
    
    def get_bottom_most(self):
        _x = [i for i in self.__block if sum(i) != 0]
        return _x[-1]

    def __str__(self):
        s = []
        for i in self.__block:
            d = ""
            for j in i:
                d = d + ("X" if j == 1 else "-")
            s.append(d)
        return "\n".join(s)
    

class I(Block): 
    def __init__(self, posx: int = 0, posy: int = 0):
        super().__init__("I", [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], posx, posy)
class J(Block): 
    def __init__(self, posx: int = 0, posy: int = 0):
        super().__init__("J", [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0]
        ], posx, posy)
class L(Block): 
    def __init__(self, posx: int = 0, posy: int = 0):
        super().__init__("L", [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ], posx, posy)
class O(Block): 
    def __init__(self, posx: int = 0, posy: int = 0):
        super().__init__("O", [
            [1, 1],
            [1, 1]
        ], posx, posy)
class S(Block):
    def __init__(self, posx: int = 0, posy: int = 0):
        super().__init__("S", [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ], posx, posy)
class Z(Block): 
    def __init__(self, posx: int = 0, posy: int = 0):
        super().__init__("Z", [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ], posx, posy)
class T(Block): 
    def __init__(self, posx: int = 0, posy: int = 0):
        super().__init__("T", [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ], posx, posy)

BLOCK_COLOR = {
    "I": Fore.CYAN,
    "J": Fore.BLUE,
    "L": Fore.YELLOW,
    "O": Fore.RED,
    "S": Fore.GREEN,
    "Z": Fore.MAGENTA,
    "T": Fore.WHITE
}
BLOCKS = [I, J, L, O, S, Z, T]
def get_random_block() -> Block:
    block: Block = BLOCKS[random.randint(0, len(BLOCKS)-1)]()

    for _ in range(random.randint(0, 400)):
        is_left = True if random.randint(0, 100) >= 50 else False
        if is_left:
            block.rotate_left()
        else:
            block.rotate_right

    return block

class Playfield:
    def __init__(self):
        self.is_lost = False
        self.next_block = get_random_block()
        self.running: Block | None = None
        self.field = [
            [0 for _ in range(10)] for _ in range(24)
        ]
    
    def tick(self):
        if self.is_lost: return

        if self.running == None:
            self.running = self.next_block
            self.next_block = get_random_block()
            return
        
        add_posx = True
        if((self.running.posx + len(self.running.block)) > len(self.field)):
            add_posx = False

        if(add_posx):
            for r in range(len(self.field)):
                for c in range(len(self.field[r])):
                    if(r == self.running.posx and c == self.running.posy + c): continue 
                    if(self.field[r][c] == 1): continue
                    self.field[r][c] = 0

            for r in range(len(self.running.block)):
                for c in range(len(self.running.block[r])):
                    self.field[self.running.posx + r][self.running.posy + c + 1] = 2 if self.running.block[r][c] == 1 else (2 if self.field[self.running.posx + r][self.running.posy + c + 1] == 1 else 0)

            self.running.posx += 1

            last_from_block = [1 if i == 2 else 0 for i in self.field[self.running.posx + len(self.running.block) - 2]]
            try:
                next_after_block = self.field[self.running.posx + len(self.running.block) - 1]
            except:
                self.end_turn()
                return

            for i in range(len(last_from_block)):
                lb = last_from_block[i]
                nb = next_after_block[i]

                if nb == 1 and lb == nb:
                    self.end_turn()
                    return
    
    def end_turn(self):
        self.running = None
        for r in range(len(self.field)):
            for c in range(len(self.field[r])):
                if self.field[r][c] == 2: self.field[r][c] = 1 
        
        if sum(self.field[0]) != 0: self.is_lost = True

    def __str__(self):
        return "\n".join([Style.RESET_ALL.join(str(i)) for i in self.field])
        


p = Playfield()
while True:
    os.system("clear")
    print(p)
    p.tick()
    if p.is_lost:
        print()
        print("You Are Lost")
    
    time.sleep(0.1)