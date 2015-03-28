#! python3
"""Cardinal Bot
Soreine soreine.plume@gmail.com

A bot program to automatically play the Cardinal flash game at
http://www.newgrounds.com/portal/view/634256

"""
import pyautogui
import time
import os
import logging
import sys
import random
import copy
import ctypes
from ctypes import cdll

# Our custom C screenshot shared library, faster to get images
libscreen = cdll.LoadLibrary("./libscreenshot.so")

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s.%(msecs)03d: %(message)s", datefmt="%H:%M:%S")
#logging.disable(logging.DEBUG) # uncomment to block debug log messages

LOSE_MESSAGE = "lose" # checkForGameOver() returns this value if the game is lost

# Settings

# Global variables
GAME_WIDTH = 550
GAME_HEIGHT = 550 # the game screen is always 550 x 550
SQUARE_COLOR = (249, 8, 42)
WALL_COLOR = (176, 1, 26)


# various coordinates of objects in the game
GAME_REGION = () # (left, top, width, height) values coordinates of the entire game window
PLAY_COORDS = None # Coordinates of the play button
SQUARE_LOCATION = (GAME_WIDTH/2, GAME_HEIGHT/2)
RIGHT_WALL = (460, 275)
LEFT_WALL = (88, 270)
UP_WALL = (270, 88)
DOWN_WALL = (275, 460)

def main():
    """Runs the entire program. The Cardinal game must be visible on the
    screen and the PLAY button visible."""
    logging.debug("Program Started. Press Ctrl-C to abort at any time.")
    logging.debug("To interrupt mouse movement, move mouse to upper left corner.")
    getGameRegion()
    navigateGameWindow()
    startPlaying()

def get_pixel(img, coord):
    """Return the value of the pixel located on the given coordinates.
    
    Args:
        img     (XImage): The image to get the pixel value from.
        coord (int, int): The tuple of image coordinates.
    Returns:
        (R, G, B)
    """
    c = libscreen.XGetPixel(img, coord[0], coord[1])
    # Convert to R, G, B values
    color = (0x0000ff & c,
             (0x00ff00 & c) >> 8,
             (0xff0000 & c) >> 16)
    return color

def imPath(filename):
    """A shortcut for joining the 'images/' file path, since it is used
    so often. Returns the filename with 'images/' prepended."""
    return os.path.join("../images", filename)


def getGameRegion():
    """Obtains the region that the Cardinal game occupies on the screen
    and assigns it to GAME_REGION. The game must be at the start screen
    (where the PLAY button is visible)."""
    global GAME_REGION, PLAY_COORDS, GAME_CENTER

    # identify the top-left corner
    logging.debug("Finding game region...")
    region = pyautogui.locateOnScreen(imPath("top-left-corner.png"))
    if region is None:
        raise Exception("Could not find game on screen. Is the game visible?")

    # calculate the region of the entire game
    GAME_REGION = (region[0], region[1], GAME_WIDTH, GAME_HEIGHT)
    logging.debug("Game region found: %s" % (GAME_REGION,))

    # Calculate the position of the PLAY button
    PLAY_COORDS = (GAME_REGION[0] + 275, GAME_REGION[1] + 522)

    # Calculate the center of the screen
    GAME_CENTER = (GAME_REGION[0] + GAME_REGION[2]/2, GAME_REGION[1] + GAME_REGION[3]/2)

def navigateGameWindow():
    """Get the initial focus on the game window and mute the game, getting
    ready to play."""
    # Get focus on the game by clicking the center of the game region
    pyautogui.click(GAME_CENTER[0], GAME_CENTER[1], duration=1)

    # Mute game (it helps too because it disables some in-game effects :-p)
    pyautogui.press("m")


def newGame():
    """Start a new game by clicking on the PLAY button."""
    # click on Play
    pyautogui.click(PLAY_COORDS, duration=0.25)
    logging.debug("New game...")

def startPlaying():
    """The main game playing function. This function handles all aspects
    of game play, including starting a new game, playing and detecting
    game overs."""

    # Start a new game
    newGame()
    
    while True:
        # Wait until the square is at the center of the screen
        for i in range(0, 3):
            img = libscreen.screenshot(region=GAME_REGION)
            c = get_pixel(img, SQUARE_LOCATION)
            if c == SQUARE_COLOR:
                break
            elif i == 2:
                logging.debug("OK I lost... PLAY AGAIN :D")
                pyautogui.press("space");
                break
            else:
                # we don't need this image again
                libscreen.destroy_image(img)
                logging.debug("Waiting for square...")
        
        logging.debug("Must move!")

        # The direction to go
        direction = None
        logging.debug("Checking walls")
        # Check for an opening in on of the 4 directions
        if not get_pixel(img, LEFT_WALL) == WALL_COLOR:
            direction = "left"
        elif not get_pixel(img, RIGHT_WALL) == WALL_COLOR:
            direction = "right"
        elif not get_pixel(img, UP_WALL) == WALL_COLOR:
            direction = "up"
        elif not get_pixel(img, DOWN_WALL) == WALL_COLOR:
            direction = "down"
            
        if direction is not None:
            pyautogui.press(direction)
            logging.debug("Moving " + direction + "!")
            # Wait a moment for the square to move
            time.sleep(0.29)
        else:
            logging.debug("No opening found...")
        # Free the XImage
        libscreen.destroy_image(img)

        

def checkForGameOver():
    """Checks the screen for the "You Win" or "You Fail" message.

    On winning, returns the string in LEVEL_WIN_MESSAGE.

    On losing, the program terminates."""

    # check for "You Win" message
    result = pyautogui.locateOnScreen(imPath("you_win.png"),
                                      region=(GAME_REGION[0] + 188,
                                              GAME_REGION[1] + 94, 262, 60))
    if result is not None:
        pyautogui.click(pyautogui.center(result))
        return LEVEL_WIN_MESSAGE

    # check for "You Fail" message
    result = pyautogui.locateOnScreen(imPath("you_failed.png"),
                                      region=(GAME_REGION[0] + 167,
                                              GAME_REGION[1] + 133, 314, 39))
    if result is not None:
        logging.debug("Game over. Quitting.")
        sys.exit()

def test_lib():
    dc = libscreen.open_display_context()
    img = libscreen.screenshot(dc, 700, 500, 400, 300)
    print(get_pixel(img, (200, 0)))
    libscreen.destroy_image(img)
    libscreen.close_display_context(dc)

if __name__ == "__main__":
    main()
