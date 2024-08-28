import pygame
import copy
import board
from board import Board, Direction, StackOfMaxNElements


class Game:
    GAP_BETWEEN_TILES = 10
    TILE_SIZE = 100
    BOARD_COLOR = (200, 200, 200)
    COLORS = {
        0: ((90, 80, 70), (90, 80, 70)),
        2: ((238, 228, 218), (119, 110, 101)),
        4: ((237, 224, 200), (119, 110, 101)),
        8: ((242, 177, 121), (249, 246, 242)),
        16: ((245, 149, 99), (249, 246, 242)),
        32: ((246, 124, 95), (249, 246, 242)),
        64: ((246, 94, 59), (249, 246, 242)),
        128: ((237, 207, 114), (249, 246, 242)),
        256: ((237, 204, 97), (249, 246, 242)),
        512: ((237, 200, 80), (249, 246, 242)),
        1024: ((237, 197, 63), (249, 246, 242)),
        2048: ((237, 194, 46), (249, 246, 242))
    }
    INFO_TEXTS = [
        "U - undo move",
        "R - restart game"
    ]

    def __init__(self, size, stack_size):
        self.game_over = False
        self.board = Board(size)
        self.size = size
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.board_size = self.size * self.TILE_SIZE + (self.size + 1) * self.GAP_BETWEEN_TILES
        width, height = self.font.size("Score")
        self.board_position = (0, height)
        self.screen = pygame.display.set_mode((self.board_size, self.board_size + height * (len(self.INFO_TEXTS) + 1)))
        self.board_history = []
        self.stack_size = stack_size
        self.stack = StackOfMaxNElements(stack_size)
        self.winning = False

    def display_board(self):
        self.screen.blit(self.font.render("Score: " + str(self.board.score), False, (255, 255, 255)), (0, 0))
        pygame.draw.rect(self.screen, self.BOARD_COLOR, pygame.Rect((self.board_position,
                                                                     (self.board_size, self.board_size))))
        for i in range(0, self.size * self.size):
            self.display_tile(i)
        if self.game_over:
            self.display_game_over()
        if self.winning:
            self.display_winning()
        for i in range(0, len(self.INFO_TEXTS)):
            self.screen.blit(self.font.render(self.INFO_TEXTS[i], False, (255, 255, 255)),
                             (0, self.board_position[1] * (i + 1) + self.board_size))
        pygame.display.flip()

    def display_tile(self, number_of_tile):
        column = number_of_tile % self.size
        row = int(number_of_tile / self.size)
        x = self.board_position[0] + self.GAP_BETWEEN_TILES * (column + 1) + self.TILE_SIZE * column
        y = self.board_position[1] + self.GAP_BETWEEN_TILES * (row + 1) + self.TILE_SIZE * row
        pygame.draw.rect(self.screen, self.COLORS.get(self.board.values[row][column], self.COLORS[2048])[0],
                         pygame.Rect((x, y, self.TILE_SIZE, self.TILE_SIZE)))
        width, height = self.font.size(str(self.board.values[row][column]))
        text_x = x + int((self.TILE_SIZE - width) / 2)
        text_y = y + int((self.TILE_SIZE - height) / 2)
        self.screen.blit(self.font.render(str(self.board.values[row][column]), False,
                                          self.COLORS.get(self.board.values[row][column],
                                                          self.COLORS[2048])[1]), (text_x, text_y))

    def game(self):
        quit_game = False
        while not quit_game:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit_game = True
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    direction = None
                    if event.key == pygame.K_r:
                        self.board = board.Board(self.size)
                        self.stack = StackOfMaxNElements(self.stack_size)
                        self.game_over = False
                        self.winning = False
                    elif event.key == pygame.K_u:
                        previous_board = self.stack.pop()
                        if previous_board is not None:
                            self.board = previous_board
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        direction = Direction.LEFT
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        direction = Direction.UP
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        direction = Direction.RIGHT
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        direction = Direction.DOWN
                    if direction is not None:
                        board_copy = copy.deepcopy(self.board)
                        if self.board.make_a_move(direction):
                            self.board.insert_new_2_or_4()
                            self.stack.push(board_copy)
                    if not self.board.is_the_move_possible():
                        self.game_over = True
                    if self.board.contains_2048_or_greater() and not self.game_over:
                        self.winning = True
            self.screen.fill((0, 0, 0, 0))
            self.display_board()

    def display_game_over(self):
        self.screen.blit(self.font.render("Game Over", False, (255, 255, 255)),
                         (200, 0))

    def display_winning(self):
        self.screen.blit(self.font.render("You won!", False, (255, 255, 255)),
                         (200, 0))
