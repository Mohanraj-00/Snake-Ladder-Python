import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake and Ladder')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
snake_color = (153, 0, 0)
ladder_color = (0, 153, 0)

# Fonts
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 60)

# Board settings
board_size = 10
cell_size = width // board_size

# Snakes and Ladders positions
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Player positions
player1_pos = 1
player2_pos = 1

# Dice
dice = [1, 2, 3, 4, 5, 6]

def draw_board():
    window.fill(white)
    for row in range(board_size):
        for col in range(board_size):
            num = row * board_size + col + 1
            if row % 2 == 0:
                actual_num = num
            else:
                actual_num = (row + 1) * board_size - col

            x = col * cell_size
            y = (board_size - 1 - row) * cell_size
            if actual_num in snakes:
                pygame.draw.rect(window, red, [x, y, cell_size, cell_size])
            elif actual_num in ladders:
                pygame.draw.rect(window, green, [x, y, cell_size, cell_size])
            pygame.draw.rect(window, black, [x, y, cell_size, cell_size], 1)
            text = font.render(str(actual_num), True, black)
            window.blit(text, (x + 5, y + 5))

def draw_players():
    p1_x, p1_y = get_coordinates(player1_pos)
    p2_x, p2_y = get_coordinates(player2_pos)
    pygame.draw.circle(window, blue, (p1_x + cell_size // 2, p1_y + cell_size // 2), cell_size // 4)
    pygame.draw.circle(window, yellow, (p2_x + cell_size // 2, p2_y + cell_size // 2), cell_size // 4)

def draw_snakes_and_ladders():
    for start, end in snakes.items():
        draw_curve(start, end, snake_color)
    for start, end in ladders.items():
        draw_ladder(start, end, ladder_color)

def draw_curve(start, end, color):
    start_x, start_y = get_coordinates(start)
    end_x, end_y = get_coordinates(end)
    control_x = (start_x + end_x) // 2
    control_y = min(start_y, end_y) - abs(start_x - end_x) // 2
    num_points = 100
    points = []
    for t in range(num_points + 1):
        t /= num_points
        x = (1 - t)**2 * start_x + 2 * (1 - t) * t * control_x + t**2 * end_x
        y = (1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * end_y
        points.append((x + cell_size // 2, y + cell_size // 2))
    pygame.draw.lines(window, color, False, points, 5)

def draw_ladder(start, end, color):
    start_x, start_y = get_coordinates(start)
    end_x, end_y = get_coordinates(end)
    pygame.draw.line(window, color, (start_x + cell_size // 2, start_y + cell_size // 2), (end_x + cell_size // 2, end_y + cell_size // 2), 4)

def get_coordinates(pos):
    row = (pos - 1) // board_size
    col = (pos - 1) % board_size
    if row % 2 == 0:
        x = col * cell_size
    else:
        x = (board_size - 1 - col) * cell_size
    y = (board_size - 1 - row) * cell_size
    return x, y

def roll_dice():
    return random.choice(dice)

def move_player(player_pos):
    roll = roll_dice()
    player_pos += roll
    if player_pos in snakes:
        player_pos = snakes[player_pos]
    elif player_pos in ladders:
        player_pos = ladders[player_pos]
    return player_pos, roll

def check_win(player_pos):
    return player_pos >= 100

def display_message(msg, color):
    mesg = large_font.render(msg, True, color)
    rect = mesg.get_rect(center=(width // 2, height // 2))
    window.blit(mesg, rect)

def game_loop():
    global player1_pos, player2_pos
    game_over = False
    turn = 1
    winner = None

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not winner:
                    if turn == 1:
                        player1_pos, roll = move_player(player1_pos)
                        if check_win(player1_pos):
                            game_over = True
                            winner = "Player 1 Wins!"
                        turn = 2
                    elif turn == 2:
                        player2_pos, roll = move_player(player2_pos)
                        if check_win(player2_pos):
                            game_over = True
                            winner = "Player 2 Wins!"
                        turn = 1

        draw_board()
        draw_snakes_and_ladders()
        draw_players()
        if winner:
            display_message(winner, blue if turn == 2 else yellow)
        pygame.display.update()

        if game_over:
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

game_loop()
