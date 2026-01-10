import numpy as np
import random


class grid:
    def __init__(self):
        self.grid = np.full((3, 10), "", dtype=object)
        self.b_swap = 0
        self.w_swap = 0
        rows, cols = self.grid.shape
        # Special cells
        self.grid[1][5] = "𓋹"
        self.grid[2][5] = "𓋣"
        self.grid[2][6] = "𓂴"
        self.grid[2][7] = "𓅢"
        self.grid[2][8] = "𓁨"
        self.grid[2][9] = "𓂀"
        pieces_w = 7
        pieces_b = 7
        count_w = 0
        count_b = 0
        w_num = 1
        b_num = 1
        next_type = 'W'

        for x in range(rows):
            for y in range(cols):
                if self.grid[x][y] != "":
                    continue

                if count_w < pieces_w and count_b < pieces_b and x==0:
                    if next_type == 'W':
                        self.grid[x][y] = f"{w_num}W"
                        w_num += 1
                        count_w += 1
                        next_type = 'B'
                    else:
                        self.grid[x][y] = f"{b_num}B"
                        b_num += 1
                        count_b += 1
                        next_type = 'W'
                elif count_w < pieces_w and x==1 and y>5 and next_type == 'W':
                    self.grid[x][y] = f"{w_num}W"
                    w_num += 1
                    count_w += 1
                    next_type = 'B'
                elif count_b < pieces_b and x==1 and y>5 and next_type == 'B':
                    self.grid[x][y] = f"{b_num}B"
                    b_num += 1
                    count_b += 1
                    next_type = 'W'

    def display_grid(self):
        # reprint special cells
        for i in range(3):
            for j in range(10):
                if (i == 1 and j == 5):
                    if self.grid[i][j] == "":
                     self.grid[i][j] = "𓋹"
                elif (i == 2 and j == 5):
                    if self.grid[i][j] == "":
                     self.grid[i][j] = "𓋣"
                elif (i == 2 and j == 6):
                    if self.grid[i][j] == "":
                     self.grid[i][j] = "𓂴"
                elif (i == 2 and j == 7):
                    if self.grid[i][j] == "":
                     self.grid[i][j] = "𓅢"
                elif (i == 2 and j == 8):
                    if self.grid[i][j] == "":
                     self.grid[i][j] = "𓁨"
                elif (i == 2 and j == 9):
                    if self.grid[i][j] == "":
                     self.grid[i][j] = "𓂀"
        # Pretty-print the grid with column headers
        rows, cols = self.grid.shape
        col_width = 6
        header = "   " + "".join(f"{i:^{col_width}}" for i in range(cols))
        sep = "  " + "".join("-" * col_width for _ in range(cols))
        print(header)
        print(sep)
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                val = self.grid[r, c]
                row_cells.append(f"{str(val) if val != '' else '.':^{col_width}}")
            print(f"{r} " + "".join(row_cells))

    def get_counts(self) -> tuple:
        flat = self.grid.flatten()
        count_w = sum(1 for v in flat if isinstance(v, str) and v.endswith('W'))
        count_b = sum(1 for v in flat if isinstance(v, str) and v.endswith('B'))
        return count_w, count_b
    def get_pos(self, piece=None):
        if piece is None:
            piece = input("Enter piece to move: ")

        rows, cols = self.grid.shape
        for x in range(rows):
            for y in range(cols):
                if self.grid[x, y] == piece:
                    return (x, y)

        print("Piece doesn't exist or left the board")
        return None

    def get_roll(self) -> int:
        return random.randint(1, 5)

    def move_piece(self, piece)-> bool:
        pos = self.get_pos(piece)
        if pos is None:
            return False
        x, y = pos
        rows, cols = self.grid.shape
        roll = self.get_roll()
        print(f"Rolled a {roll} for piece {piece} at position {(x,y)}")
        current_index = x * cols + y
        new_index = current_index + roll

        total_cells = rows * cols
        if new_index >= total_cells:
            print("piece is off board successfully")
            self.grid[x, y] = ""
            return True

        new_x = new_index // cols
        new_y = new_index % cols
        
        #exchange v2.0
        dest = self.grid[new_x, new_y]
        src = self.grid[x, y]
        orig_dest = dest
        swapped = False
        if isinstance(dest, str) and isinstance(src, str):
            if dest.endswith("W") and src.endswith("B"):
                print("exchanged with white piece")
                self.grid[new_x, new_y] = src
                self.grid[x, y] = orig_dest
                swapped = True
                self.b_swap +=1
            elif dest.endswith("B") and src.endswith("W"):
                print("exchanged with black piece")
                self.grid[new_x, new_y] = src
                self.grid[x, y] = orig_dest
                swapped = True
                self.w_swap +=1
        if new_x == 1 and new_y ==5:
            print("{peice} landed on the house of water,moving to the house of resiriction if available")
            if self.grid[1,5]=="𓋹":
                new_x,new_y = 1,5
            else:
                for i in range(rows):
                    for j in range(cols):
                        if self.grid[i,j]=="":
                            new_x,new_y = i,j
                            break
        elif new_x == 2 and new_y >5:
            print("you cannot jump over the house of happeness")
            new_x,new_y = 2,7
        if x ==2 and y in [7,8,9]:
            if roll + y>9:
                print("peice is off the bord successfully")
                self.grid[x, y] = ""
                return True
            elif self.grid[1,5]=="𓋹":
                new_x,new_y = 1,5
            else:
                for i in range(rows):
                    for j in range(cols):
                        if self.grid[i,j]=="":
                            new_x,new_y = i,j
                            break


        
        if not swapped:
            self.grid[x, y] = ""
            self.grid[new_x, new_y] = piece
            print(f"Moved {piece} from {(x,y)} to {(new_x,new_y)} (roll={roll})")
        else:
            print(f"Swapped {piece} at {(x,y)} with {orig_dest} at {(new_x,new_y)} (roll={roll})")
        return True
    def check_win(self) ->bool:
        count_w,count_b = self.get_counts()
        if count_w == 0 :
            print("white player wins")
            return True
        elif count_b == 0:
            print('black player wins')
            return True
        else:
            return False

