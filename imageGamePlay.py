import cv2
import numpy as np
import pyautogui as pg
import time
from pynput import keyboard
from pynput.keyboard import Key
import sys

"""
GENERAL NOTES

Note that pyautogui functions works on primary monitor display (I think)
Take a ss with the pg.screenshot("file_name") function, crop it with photos, and save before
using it in code - otherwise doing it manually will not work unless you use confidence= kwarg.

X-coordinate increases to the right
Y-coordinate increases downwards

Computer visualisation does not work with highlighted pieces - turn off in settings in Chess.com

Only works in Chess.com. change images to work on other platforms or board themes

The dimensions and location of the board is 'hard-coded' to the primary display monitor

It can only play when it starts from the beginning (cannot start halfway through because of engine)
"""

class Tile:
    """Defining characteristics of a tile on a chessboard"""

    def __init__(self, opponent_is_white=False, x_centred_location=0, y_centred_location=0):
        # If chess board begins in a different position, then use the default board dimensions
        if board_dimensions is None:
            self.left = 292
            self.top = 167
            self.width = 802/8
            self.height = 801/8

        elif board_dimensions is not None:
            self.left = board_dimensions.left
            self.top = board_dimensions.top
            self.width = board_dimensions.width/8
            self.height = board_dimensions.height/8

        self.x_centred_location = x_centred_location
        self.y_centred_location = y_centred_location
        self.key_row = (0, 0)
        self.key_column = (0, 0)
        self.x_pos = "X"
        self.y_pos = "#"

        # Assign range of x-coordinates to column chess notation
        self.columns_player_is_white = {
            (self.left, self.left + self.width): "a",
            (self.left + self.width, self.left + 2 * self.width): "b",
            (self.left + 2 * self.width, self.left + 3 * self.width): "c",
            (self.left + 3 * self.width, self.left + 4 * self.width): "d",
            (self.left + 4 * self.width, self.left + 5 * self.width): "e",
            (self.left + 5 * self.width, self.left + 6 * self.width): "f",
            (self.left + 6 * self.width, self.left + 7 * self.width): "g",
            (self.left + 7 * self.width, self.left + 8 * self.width): "h",
        }

        self.rows_player_is_white = {
            (self.top, self.top + self.height): "8",
            (self.top + self.height, self.top + 2 * self.height): "7",
            (self.top + 2 * self.height, self.top + 3 * self.height): "6",
            (self.top + 3 * self.height, self.top + 4 * self.height): "5",
            (self.top + 4 * self.height, self.top + 5 * self.height): "4",
            (self.top + 5 * self.height, self.top + 6 * self.height): "3",
            (self.top + 6 * self.height, self.top + 7 * self.height): "2",
            (self.top + 7 * self.height, self.top + 8 * self.height): "1",
        }      

        self.columns_player_is_black = {
            (self.left, self.left + self.width): "h",
            (self.left + self.width, self.left + 2 * self.width): "g",
            (self.left + 2 * self.width, self.left + 3 * self.width): "f",
            (self.left + 3 * self.width, self.left + 4 * self.width): "e",
            (self.left + 4 * self.width, self.left + 5 * self.width): "d",
            (self.left + 5 * self.width, self.left + 6 * self.width): "c",
            (self.left + 6 * self.width, self.left + 7 * self.width): "b",
            (self.left + 7 * self.width, self.left + 8 * self.width): "a",
        }

        self.rows_player_is_black = {
            (self.top, self.top + self.height): "1",
            (self.top + self.height, self.top + 2 * self.height): "2",
            (self.top + 2 * self.height, self.top + 3 * self.height): "3",
            (self.top + 3 * self.height, self.top + 4 * self.height): "4",
            (self.top + 4 * self.height, self.top + 5 * self.height): "5",
            (self.top + 5 * self.height, self.top + 6 * self.height): "6",
            (self.top + 6 * self.height, self.top + 7 * self.height): "7",
            (self.top + 7 * self.height, self.top + 8 * self.height): "8",
        }

        
        self.opponent_is_white = opponent_is_white
    
    def calculate_position(self):
        """Convert coordinate position of piece to chess notation"""

        # If player is white, a1 is bottom left
        if self.opponent_is_white == False:
            # Iterates through each key in columns dictionary
            # If centre x-coordinate is between tuple values, then the corresponding chess column notation (value) is retrieved by saving the key
            for column_range in self.columns_player_is_white.keys():
                if column_range[0] <= self.x_centred_location <= column_range[1]:
                    self.key_column = column_range
                else:
                    continue
            
            # Finds tuple range in row dictionary
            for row_range in self.rows_player_is_white.keys():
                if row_range[0] <= self.y_centred_location <= row_range[1]:
                    self.key_row = row_range
                else:
                    continue
            
            self.x_pos = self.columns_player_is_white[self.key_column]
            self.y_pos = self.rows_player_is_white[self.key_row]

        # If player is black, a1 is top right
        elif self.opponent_is_white == True:
            for column_range in self.columns_player_is_black.keys():
                if column_range[0] <= self.x_centred_location <= column_range[1]:
                    self.key_column = column_range
                else:
                    continue
            
            # Finds tuple range in row dictionary
            for row_range in self.rows_player_is_black.keys():
                if row_range[0] <= self.y_centred_location <= row_range[1]:
                    self.key_row = row_range
                else:
                    continue
            
            self.x_pos = self.columns_player_is_black[self.key_column]
            self.y_pos = self.rows_player_is_black[self.key_row]

        return "{}{}".format(self.x_pos, self.y_pos)

def analyse_positions():
    # screenshot of chess screen (must be primary display)
    screenshot = pg.screenshot()

    # Computer vision. 1st arg must be photo in a numpy array and 2nd arg changes colour theme.
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    #################################
    # VISUALISATION OF WHITE PIECES #
    #################################

    # Draw rectangles around pawns dark background
    for pawn in pg.locateAllOnScreen("chess_pieces\\white_pawn.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (pawn.left, pawn.top),
            (pawn.left + pawn.width, pawn.top + pawn.height),
            (0, 0, 255),
            3
        )

        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(pawn.left + pawn.width/2), y_centred_location=(pawn.top + pawn.height/2)).calculate_position()
            white_positions.append(pos)
    
    # Draw rectangles around pawns light background
    for pawn in pg.locateAllOnScreen("chess_pieces\\white_pawn_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (pawn.left, pawn.top),
            (pawn.left + pawn.width, pawn.top + pawn.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(pawn.left + pawn.width/2), y_centred_location=(pawn.top + pawn.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white knight dark background
    for knight in pg.locateAllOnScreen("chess_pieces\\white_knight.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (knight.left, knight.top),
            (knight.left + knight.width, knight.top + knight.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(knight.left + knight.width/2), y_centred_location=(knight.top + knight.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white knight light background
    for knight in pg.locateAllOnScreen("chess_pieces\\white_knight_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (knight.left, knight.top),
            (knight.left + knight.width, knight.top + knight.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(knight.left + knight.width/2), y_centred_location=(knight.top + knight.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white bishop dark background
    for bishop in pg.locateAllOnScreen("chess_pieces\\white_bishop.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (bishop.left, bishop.top),
            (bishop.left + bishop.width, bishop.top + bishop.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(bishop.left + bishop.width/2), y_centred_location=(bishop.top + bishop.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white bishop light background
    for bishop in pg.locateAllOnScreen("chess_pieces\\white_bishop_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (bishop.left, bishop.top),
            (bishop.left + bishop.width, bishop.top + bishop.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(bishop.left + bishop.width/2), y_centred_location=(bishop.top + bishop.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white rook dark background
    for rook in pg.locateAllOnScreen("chess_pieces\\white_rook.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (rook.left, rook.top),
            (rook.left + rook.width, rook.top + rook.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(rook.left + rook.width/2), y_centred_location=(rook.top + rook.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white rook light background
    for rook in pg.locateAllOnScreen("chess_pieces\\white_rook_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (rook.left, rook.top),
            (rook.left + rook.width, rook.top + rook.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(rook.left + rook.width/2), y_centred_location=(rook.top + rook.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white queen dark background
    for queen in pg.locateAllOnScreen("chess_pieces\\white_queen.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (queen.left, queen.top),
            (queen.left + queen.width, queen.top + queen.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(queen.left + queen.width/2), y_centred_location=(queen.top + queen.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white queen light background
    for queen in pg.locateAllOnScreen("chess_pieces\\white_queen_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (queen.left, queen.top),
            (queen.left + queen.width, queen.top + queen.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(queen.left + queen.width/2), y_centred_location=(queen.top + queen.height/2)).calculate_position()
            white_positions.append(pos)

    # Draw rectangles around white king dark/ light background - note only one king is always present
    # A for loop is used to prevent errors if none are present
    for white_king in pg.locateAllOnScreen("chess_pieces\\white_king.png"):
        cv2.rectangle(
            screenshot,
            (white_king.left, white_king.top),
            (white_king.left + white_king.width, white_king.top + white_king.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(white_king.left + white_king.width/2), y_centred_location=(white_king.top + white_king.height/2)).calculate_position()
            white_positions.append(pos)

    for white_king_light in pg.locateAllOnScreen("chess_pieces\\white_king_light.png"):
        cv2.rectangle(
            screenshot,
            (white_king_light.left, white_king_light.top),
            (white_king_light.left + white_king_light.width, white_king_light.top + white_king_light.height),
            (0, 0, 255),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(white_king_light.left + white_king_light.width/2), y_centred_location=(white_king_light.top + white_king_light.height/2)).calculate_position()
            white_positions.append(pos)
    # #################################
    # # VISUALISATION OF BLACK PIECES #
    # #################################

    # Draw rectangles around pawns dark background
    for pawn in pg.locateAllOnScreen("chess_pieces\\black_pawn.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (pawn.left, pawn.top),
            (pawn.left + pawn.width, pawn.top + pawn.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(pawn.left + pawn.width/2), y_centred_location=(pawn.top + pawn.height/2)).calculate_position()
            black_positions.append(pos)
    
    # Draw rectangles around pawns light background
    for pawn in pg.locateAllOnScreen("chess_pieces\\black_pawn_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (pawn.left, pawn.top),
            (pawn.left + pawn.width, pawn.top + pawn.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(pawn.left + pawn.width/2), y_centred_location=(pawn.top + pawn.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white knight dark background
    for knight in pg.locateAllOnScreen("chess_pieces\\black_knight.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (knight.left, knight.top),
            (knight.left + knight.width, knight.top + knight.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(knight.left + knight.width/2), y_centred_location=(knight.top + knight.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white knight light background
    for knight in pg.locateAllOnScreen("chess_pieces\\black_knight_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (knight.left, knight.top),
            (knight.left + knight.width, knight.top + knight.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(knight.left + knight.width/2), y_centred_location=(knight.top + knight.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white bishop dark background
    for bishop in pg.locateAllOnScreen("chess_pieces\\black_bishop.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (bishop.left, bishop.top),
            (bishop.left + bishop.width, bishop.top + bishop.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(bishop.left + bishop.width/2), y_centred_location=(bishop.top + bishop.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white bishop light background
    for bishop in pg.locateAllOnScreen("chess_pieces\\black_bishop_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (bishop.left, bishop.top),
            (bishop.left + bishop.width, bishop.top + bishop.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(bishop.left + bishop.width/2), y_centred_location=(bishop.top + bishop.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white rook dark background
    for rook in pg.locateAllOnScreen("chess_pieces\\black_rook.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (rook.left, rook.top),
            (rook.left + rook.width, rook.top + rook.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(rook.left + rook.width/2), y_centred_location=(rook.top + rook.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white rook light background
    for rook in pg.locateAllOnScreen("chess_pieces\\black_rook_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (rook.left, rook.top),
            (rook.left + rook.width, rook.top + rook.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(rook.left + rook.width/2), y_centred_location=(rook.top + rook.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white queen dark background
    for queen in pg.locateAllOnScreen("chess_pieces\\black_queen.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (queen.left, queen.top),
            (queen.left + queen.width, queen.top + queen.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(queen.left + queen.width/2), y_centred_location=(queen.top + queen.height/2)).calculate_position()
            black_positions.append(pos)

    # Draw rectangles around white queen light background
    for queen in pg.locateAllOnScreen("chess_pieces\\black_queen_light.png", confidence=0.95):
        cv2.rectangle(
            screenshot,
            (queen.left, queen.top),
            (queen.left + queen.width, queen.top + queen.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(queen.left + queen.width/2), y_centred_location=(queen.top + queen.height/2)).calculate_position()
            black_positions.append(pos)
    
    for black_king in pg.locateAllOnScreen("chess_pieces\\black_king.png"):
        cv2.rectangle(
            screenshot,
            (black_king.left, black_king.top),
            (black_king.left + black_king.width, black_king.top + black_king.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(black_king.left + black_king.width/2), y_centred_location=(black_king.top + black_king.height/2)).calculate_position()
            black_positions.append(pos)

    for black_king_light in pg.locateAllOnScreen("chess_pieces\\black_king_light.png"):
        cv2.rectangle(
            screenshot,
            (black_king_light.left, black_king_light.top),
            (black_king_light.left + black_king_light.width, black_king_light.top + black_king_light.height),
            (255, 0, 0),
            3
        )
        if first_pass:
            pos = Tile(opponent_is_white=opponent, x_centred_location=(black_king_light.left + black_king_light.width/2), y_centred_location=(black_king_light.top + black_king_light.height/2)).calculate_position()
            black_positions.append(pos)

    # display computer's vision of screenshot
    cv2.destroyAllWindows()
    cv2.imshow("ss", screenshot)
    cv2.waitKey(refresh_rate)

if __name__ == "__main__":

    first_pass = True
    # Original list of positions
    white_positions = []
    black_positions = []

    
    refresh_rate = 5000

    # locate centre of elements on screen to determine colour of opponent
    board = pg.locateCenterOnScreen("chess_pieces\\board.png", confidence=0.5)
    white_king = pg.locateCenterOnScreen("chess_pieces\\white_king.png", confidence=0.9)
    board_dimensions = pg.locateOnScreen("chess_pieces\\board.png")
    # print(board,white_king,board_dimensions)

    if board_dimensions is None:
        board_dimensions = pg.locateOnScreen("chess_pieces\\board_black.png")
    
    # Player is on bottom of screen, so determined opponent's colour based on position
    # of the white king relative to the centre of the board
    opponent = ""
    try:
        if white_king.y > board.y:
            opponent = "b"
        elif white_king.y < board.y:
            opponent = "w"

    # If chess is analysed not in starting position
    except:
        while opponent != "w" and opponent != "b":
            opponent = input("Is your opponent black (b) or white (w)?:\n")
            if opponent != "w" and opponent != "b":
                print("Enter 'w' or 'b'")

    if opponent == "w":
        opponent = True
    elif opponent == "b":
        opponent = False

    while True:
        # king_centre = pg.locateCenterOnScreen("chess_pieces\\black_knight_light.png", confidence=0.95)
        # print(king_centre)
        # print(Tile(opponent_is_white=opponent, x_centred_location=king_centre.x, y_centred_location=king_centre.y).calculate_position())
        analyse_positions()
        first_pass = False

        # remove duplicate elements
        white_positions = list(dict.fromkeys(white_positions))
        black_positions = list(dict.fromkeys(black_positions))
        
        print("white: {}".format(white_positions))
        print("black: {}".format(black_positions))





# def on_press(key):
#     pass
# def on_release(key):
#     # Reload cv analysis of chess board
#     if (key == Key.enter):
#         cv2.destroyAllWindows()
#         analyse_positions()

#     if (key == Key.esc):
#         # Escape program
#         sys.exit("User has exited the program")

# # Bind functions to key
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()