# File Names: GameTester.py, GameFile.py, SpriteFile.py
# Author: Asa Barton
# Final Project Submission
# Created on 5/27/2021
# Last Changed: 6/05/2021
from GameFile import PokerGame
import pygame


##
# 'main()', where the program starts
#
def main():
    aGame = PokerGame(618, 400)

    try:
        aGame.run()
    except pygame.error:  # Happens when the game window gets closed
        print("Thanks for playing!")


main()

"""
Sample Run:

pygame 2.0.1 (SDL 2.0.14, Python 3.8.2)
Hello from the pygame community. https://www.pygame.org/contribute.html
Thanks for playing!
"""
