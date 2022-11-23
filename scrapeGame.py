"""
1. Scrape live game from Chess.com
2. Input Opponent's move into engine.py
3. Output engine.py's result
"""

from bs4 import BeautifulSoup
import requests
import time
import numpy 
# Test ID: 446046523
game_id = input("Game ID: ")
player = input("Are you playing white or black (w/b): ")

# Only analyses position of the opponent
if player == "w":
    opponent = "b"
elif player != "w":
    opponent = "w"

playing = True
first_pass = True
position_coordination = {
    "square-81" : "h1",
    "square-82" : "h2",
    "square-83" : "h3",
    "square-84" : "h4",
    "square-85" : "h5",
    "square-86" : "h6",
    "square-87" : "h7",
    "square-88" : "h8",

    "square-71" : "g1",
    "square-72" : "g2",
    "square-73" : "g3",
    "square-74" : "g4",
    "square-75" : "g5",
    "square-76" : "g6",
    "square-77" : "g7",
    "square-78" : "g8",

    "square-61" : "f1",
    "square-62" : "f2",
    "square-63" : "f3",
    "square-64" : "f4",
    "square-65" : "f5",
    "square-66" : "f6",
    "square-67" : "f7",
    "square-68" : "f8",

    "square-51" : "e1",
    "square-52" : "e2",
    "square-53" : "e3",
    "square-54" : "e4",
    "square-55" : "e5",
    "square-56" : "e6",
    "square-57" : "e7",
    "square-58" : "e8",

    "square-41" : "d1",
    "square-42" : "d2",
    "square-43" : "d3",
    "square-44" : "d4",
    "square-45" : "d5",
    "square-46" : "d6",
    "square-47" : "d7",
    "square-48" : "d8",

    "square-31" : "c1",
    "square-32" : "c2",
    "square-33" : "c3",
    "square-34" : "c4",
    "square-35" : "c5",
    "square-36" : "c6",
    "square-37" : "c7",
    "square-38" : "c8",

    "square-21" : "b1",
    "square-22" : "b2",
    "square-23" : "b3",
    "square-24" : "b4",
    "square-25" : "b5",
    "square-26" : "b6",
    "square-27" : "b7",
    "square-28" : "b8",

    "square-11" : "a1",
    "square-12" : "a2",
    "square-13" : "a3",
    "square-14" : "a4",
    "square-15" : "a5",
    "square-16" : "a6",
    "square-17" : "a7",
    "square-18" : "a8",
}
unchanged_positions = []

# Request to website and download HTML contents
url = 'https://www.chess.com/game/daily/{}'.format(game_id)

while playing:

    req = requests.get(url)
    content = req.text

    soup = BeautifulSoup(content, features="html.parser")

    # Create one array with original positions. Compare this with following arrays. 
    # If later array is different, that later array becomes the original array and the pattern continues.
    if first_pass:

        # Append position of each piece into an array
        for position in soup.find_all("div"):
            piece_position = position.get("class")

            if piece_position == None:
                continue
            
            # Position of the opponent
            elif piece_position[0] == "piece" and piece_position[1][0] == opponent:
                unchanged_positions.append(piece_position[2])

        # print(unchanged_positions)
        first_pass = False

    elif not first_pass:
        # Reset new_positions array each iteration
        new_positions = []

        for position in soup.find_all("div"):
            piece_position = position.get("class")

            if piece_position == None:
                continue

            elif piece_position[0] == "piece" and piece_position[1][0] == opponent:
                new_positions.append(piece_position[2])
        # print(new_positions)

        # compare new array and original array with positions
        if new_positions.sort() != unchanged_positions.sort():
            print("It changed!!")
    time.sleep(1)

