from copy import deepcopy
from config import EMPTY, BLACK, WHITE

class Board:

    def __init__(self, board = None):
        if board:
            pass
        else:
            self.board = [[0 for i in range(8)] for j in range(8)] # 8 by 8 empty board
            self.board[3][4] = BLACK
            self.board[4][3] = BLACK
            self.board[3][3] = WHITE
            self.board[4][4] = WHITE
            self.white_pieces = 2
            self.black_pieces = 2
            self.empty_spaces = 60
        self.valid_moves = []

    def get_possible_moves(self, row, column, color):
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        moves = []

        if row < 0 or row > 7 or column < 0 or column > 7:
            return moves

        # north
        i = row - 1
        if i >= 0 and self.board[i][column] == other:
            i = i - 1
            while i >= 0 and self.board[i][column] == other:
                i = i - 1
            if i >= 0 and self.board[i][column] == 0:
                moves = moves + [( i, column)]

        # northeast
        i = row - 1
        j = column + 1
        if i >= 0 and j < 8 and self.board[i][j] == other:
            i = i - 1
            j = j + 1
            while i >= 0 and j < 8 and self.board[i][j] == other:
                i = i - 1
                j = j + 1
            if i >= 0 and j < 8 and self.board[i][j] == 0:
                moves = moves + [(i, j)]

        # east
        j = column + 1
        if j < 8 and self.board[row][j] == other:
            j = j + 1
            while j < 8 and self.board[row][j] == other:
                j = j + 1
            if j < 8 and self.board[row][j] == 0:
                moves = moves + [(row, j)]

        # southeast
        i = row + 1
        j = column + 1
        if i < 8 and j < 8 and self.board[i][j] == other:
            i = i + 1
            j = j + 1
            while i < 8 and j < 8 and self.board[i][j] == other:
                i = i + 1
                j = j + 1
            if i < 8 and j < 8 and self.board[i][j] == 0:
                moves = moves + [(i, j)]

        # south
        i = row + 1
        if i < 8 and self.board[i][column] == other:
            i = i + 1
            while i < 8 and self.board[i][column] == other:
                i = i + 1
            if i < 8 and self.board[i][column] == 0:
                moves = moves + [(i, column)]

        # southwest
        i = row + 1
        j = column - 1
        if i < 8 and j >= 0 and self.board[i][j] == other:
            i = i + 1
            j = j - 1
            while i < 8 and j >= 0 and self.board[i][j] == other:
                i = i + 1
                j = j - 1
            if i < 8 and j >= 0 and self.board[i][j] == 0:
                moves = moves + [(i, j)]

        # west
        j = column - 1
        if j >= 0 and self.board[row][j] == other:
            j = j - 1
            while j >= 0 and self.board[row][j] == other:
                j = j - 1
            if j >= 0 and self.board[row][j] == 0:
                moves = moves + [(row, j)]

        # northwest
        i = row - 1
        j = column - 1
        if i >= 0 and j >= 0 and self.board[i][j] == other:
            i = i - 1
            j = j - 1
            while i >= 0 and j >= 0 and self.board[i][j] == other:
                i = i - 1
                j = j - 1
            if i >= 0 and j >= 0 and self.board[i][j] == 0:
                moves = moves + [(i, j)]

        return moves

    def get_valid_moves(self, color):
        if color == BLACK:
            num_pieces = self.black_pieces
        else:
            num_pieces = self.white_pieces
        if num_pieces < self.empty_spaces:
            return self.get_valid_moves_by_colored_squares(color)
        else:
            return self.get_valid_moves_by_empty_squares(color)

    def get_valid_moves_by_colored_squares(self, color):
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        valid_moves = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    valid_moves = valid_moves + self.get_possible_moves(i, j, color)
        valid_moves = list(set(valid_moves)) # Make each move in valid_moves unique
        self.valid_moves = valid_moves
        return valid_moves

    def get_valid_moves_by_empty_squares(self, color):
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        moves = []

        # For each empty space on the board, check if there are
        # any of the opponents pieces available to flip
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == EMPTY:
                    for direction in range(1,9):
                        if len(self.pieces_to_flip_in_row((i, j), color, direction)) > 0:
                            moves = moves + [(i, j)]
        self.valid_moves = moves
        return moves

    def apply_move(self, move, color):
        if move in self.valid_moves:
            self.board[move[0]][move[1]] = color
            if color == BLACK:
                self.black_pieces += 1
            else:
                self.white_pieces += 1
            self.empty_spaces -= 1
            for i in range(1, 9):
                self.flip_pieces(move, color)

    def flip_pieces(self, position, color):
        for direction in range(1,9): # Flip row for each of the 8 possible directions
            pieces_to_flip = self.pieces_to_flip_in_row(position, color, direction)
            for piece in pieces_to_flip:
                self.board[piece[0]][piece[1]] = color
            if color == BLACK:
                self.black_pieces += len(pieces_to_flip)
                self.white_pieces -= len(pieces_to_flip)
            else:
                self.black_pieces -= len(pieces_to_flip)
                self.white_pieces += len(pieces_to_flip)

    def pieces_to_flip_in_row(self, position, color, direction):
        row_inc = 0
        col_inc = 0
        if direction >= 5:
            direction += 1 # Have directions correspond to numberpad
        if direction == 1 or direction == 2 or direction == 3:
            row_inc = -1
        elif direction == 7 or direction == 8 or direction == 9:
            row_inc = 1
        if direction == 1 or direction == 4 or direction == 7:
            col_inc = -1
        elif direction == 3 or direction == 6 or direction == 9:
            col_inc = 1

        pieces = []
        i = position[0] + row_inc
        j = position[1] + col_inc

        if color == WHITE:
            other = BLACK
            add_attr = 'white_pieces'
            rem_attr = 'black_pieces'
        else:
            other = WHITE
            add_attr = 'black_pieces'
            rem_attr = 'white_pieces'

        if i in range(8) and j in range(8) and self.board[i][j] == other:
            # assures there is at least one piece to flip
            pieces = pieces + [(i,j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(8) and j in range(8) and self.board[i][j] == other:
                # search for more pieces to flip
                pieces = pieces + [(i,j)]
                i = i + row_inc
                j = j + col_inc
            if i in range(8) and j in range(8) and self.board[i][j] == color:
                # found a piece of the right color to flip the pieces between
                return pieces
        return []

    def game_won(self):
        # Game Won if One Player Has No Pieces on the Board
        if self.white_pieces == 0:
            return BLACK
        elif self.black_pieces == 0:
            return WHITE
        # Game also over if no valid moves for both players or no empty spaces left on board
        elif (self.get_valid_moves( BLACK ) == [] and self.get_valid_moves( WHITE ) == []) or self.empty_spaces == 0:
            if self.white_pieces > self.black_pieces:
                return WHITE
            elif self.black_pieces > self.white_pieces:
                return BLACK
            else:
                return EMPTY # returning EMPTY denotes a tie
        return None

    # Function to print board for text based game
    def print_board(self):
        print '  ',
        for i in range(8):
            print ' ', i,
        print
        for i in range(8):
            print i, ' |',
            for j in range(8):
                if self.board[i][j] == BLACK:
                    print 'B',
                elif self.board[i][j] == WHITE:
                    print 'W',
                else:
                    print ' ',
                print '|',
            print
