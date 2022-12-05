import cv2
import numpy as np
import pyautogui as pg

screenshot = pg.locateOnScreen("chess_pieces\\wp_white_king_side_castle.png")
print(screenshot)