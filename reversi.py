WHITE_DISC = '⚪️  '
BLACK_DISC = '⚫️  '
EMPTY = ' ■ '
BOARD_SIZE = 8      # board size must be even

class Game:
    def __init__(self, black, white):
        # player_1 = input('Type player name for Player_1: ')
        # player_2 = input('Type player name for Player_2: ')
        self.board = self.new_board()
        self.black = black
        self.white = white
        self.is_black_turn = True

    def new_board(self):
        board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # initial set-up
        HALF = int(BOARD_SIZE / 2)
        board[HALF - 1][HALF - 1] = BLACK_DISC
        board[HALF][HALF] = BLACK_DISC
        board[HALF - 1][HALF] = WHITE_DISC
        board[HALF][HALF - 1] = WHITE_DISC
        return board

    def print_game(self):
        print("It is " + (
            self.black if self.is_black_turn else self.white
            ) + "'s turn.")
        print('  ' + ''.join([' ' + str(i + 1) + ' ' for i in range(BOARD_SIZE)]))
        for i, row in enumerate(self.board):
            print(str(i + 1) + ' ' + ''.join(square for square in row))

    def fill_board(self):
        for row in self.board:
            for i in range(len(row)):
                row[i] = BLACK_DISC

    def place_disc(self, x, y):
        if not (
            0 <= x < BOARD_SIZE and
            0 <= y < BOARD_SIZE and
            self.is_valid_move(x, y)
        ):
            print("This is not a valid move!")
            return True
        self.board[y][x] = (
            BLACK_DISC if self.is_black_turn else WHITE_DISC
        )
        self.flip_discs(x, y)
        self.is_black_turn = not self.is_black_turn
        if not self.has_valid_moves():
            print("No valid moves. Passing!")
            self.is_black_turn = not self.is_black_turn
            if not self.has_valid_moves():
                print("No valid moves. Game over!")
                black_count = 0
                white_count = 0
                for row in self.board:
                    for disc in row:
                        if disc == BLACK_DISC:
                            black_count += 1
                        elif disc == WHITE_DISC:
                            white_count += 1
                if black_count > white_count:
                    print('Player Black wins the game!')
                else:
                    print('Player White wins the game!')
                return False
        return True


    def flip_discs(self, x, y):
        discs = self.get_all_discs_to_flip(x, y)
        color = BLACK_DISC if self.is_black_turn else WHITE_DISC
        for x, y in discs:
            self.board[y][x] = color

    def has_valid_moves(self):
        return any(
            self.is_valid_move(x, y)
            for x in range(BOARD_SIZE)
            for y in range(BOARD_SIZE)
        )

    def is_valid_move(self, x, y):
        return (
            self.board[y][x] == EMPTY and
            bool(self.get_all_discs_to_flip(x, y))
        )

    def get_all_discs_to_flip(self, x, y):
        return sum((self.get_discs_to_flip(x, y, direction) for direction in (
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1),
        )), [])

    def get_discs_to_flip(self, x, y, direction):
        dx, dy = direction
        our_disc = BLACK_DISC if self.is_black_turn else WHITE_DISC
        their_disc = WHITE_DISC if self.is_black_turn else BLACK_DISC
        result = []
        x += dx
        y += dy
        while (
            0 <= x < BOARD_SIZE and
            0 <= y < BOARD_SIZE and
            self.board[y][x] == their_disc
        ):
            result.append((x, y))
            x += dx
            y += dy
        if (
            0 <= x < BOARD_SIZE and
            0 <= y < BOARD_SIZE and
            self.board[y][x] == our_disc
        ):
            return result
        return []

#
# if input("Enter 'y' to proceed to a game of Othello: ") == 'y':
#     othello()

game = Game(
    black='Player Black',
    white='Player White',
)
game.print_game()

while True:
    x = int(input("Type x-coordinate: "))
    y = int(input("Type y-coordinate: "))
    is_game_continue = game.place_disc(x - 1, y - 1)
    game.print_game()
    if not is_game_continue:
        break
