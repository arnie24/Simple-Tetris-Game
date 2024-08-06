import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
GRID_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes (7 Tetriminos)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 0], [1, 1, 1]],  # T
]

# Shape colors
SHAPE_COLORS = [CYAN, YELLOW, BLUE, ORANGE, GREEN, RED, MAGENTA]


class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.x = 3
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    for y in range(20):
        for x in range(10):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid


def draw_grid(surface, grid):
    for y in range(20):
        for x in range(10):
            pygame.draw.rect(surface, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
    pygame.draw.rect(surface, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)


def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == BLACK] for y in range(20)]
    accepted_positions = [x for item in accepted_positions for x in item]

    formatted_shape = convert_shape_format(shape)

    for pos in formatted_shape:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def convert_shape_format(shape):
    positions = []
    for y, line in enumerate(shape.shape):
        for x, cell in enumerate(line):
            if cell == 1:
                positions.append((shape.x + x, shape.y + y))
    return positions


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            increment += 1
            index = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                new_key = (x, y + increment)
                locked[new_key] = locked.pop(key)
    return increment


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)

    start_x = SCREEN_WIDTH + 50
    start_y = SCREEN_HEIGHT // 2 - 100

    for y, line in enumerate(shape.shape):
        for x, cell in enumerate(line):
            if cell == 1:
                pygame.draw.rect(surface, shape.color, (start_x + x * GRID_SIZE, start_y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    surface.blit(label, (start_x + 10, start_y - 30))


def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Tetrimino(random.choice(SHAPES))
    next_piece = Tetrimino(random.choice(SHAPES))
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Tetrimino(random.choice(SHAPES))
            change_piece = False
            clear_rows(grid, locked_positions)

        draw_grid(screen, grid)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()


def main_menu():
    run = True
    while run:
        screen.fill(BLACK)
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Press Any Key to Play', 1, WHITE)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - label.get_height() // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    main_menu()