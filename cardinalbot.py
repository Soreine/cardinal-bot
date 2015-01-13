#! python3
"""Cardinal Bot
Soreine soreine.plume@gmail.com

A bot program to automatically play the Cardinal flash game at http://www.newgrounds.com/portal/view/634256
"""

import pyautogui, time, os, logging, sys, random, copy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.DEBUG) # uncomment to block debug log messages

LOSE_MESSAGE = 'lose' # checkForGameOver() returns this value if the game is lost

# Settings

# Global variables
GAME_WIDTH = 550
GAME_HEIGHT = 550 # the game screen is always 550 x 550
SQUARE_COLOR = (249, 8, 42)
WALL_COLOR = (176, 1, 26)


# various coordinates of objects in the game
GAME_REGION = () # (left, top, width, height) values coordinates of the entire game window
PLAY_COORDS = None # Coordinates of the play button
LEFT_WALL = None
UP_WALL = None
DOWN_WALL = None
RIGHT_WALL = None

def main():
    """Runs the entire program. The Cardinal game must be visible on the screen and the PLAY button visible."""
    logging.debug('Program Started. Press Ctrl-C to abort at any time.')
    logging.debug('To interrupt mouse movement, move mouse to upper left corner.')
    getGameRegion()
    navigateGameWindow()
    startPlaying()


def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)


def getGameRegion():
    """Obtains the region that the Cardinal game occupies on the screen and assigns it to GAME_REGION. The game must be at the start screen (where the PLAY button is visible)."""
    global GAME_REGION, PLAY_COORDS, LEFT_WALL, UP_WALL, DOWN_WALL, RIGHT_WALL, GAME_CENTER

    # identify the top-left corner
    logging.debug('Finding game region...')
    region = pyautogui.locateOnScreen(imPath('top-left-corner.png'))
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')

    # calculate the region of the entire game
    GAME_REGION = (region[0], region[1], GAME_WIDTH, GAME_HEIGHT)
    logging.debug('Game region found: %s' % (GAME_REGION,))

    # Calculate the position of the PLAY button
    PLAY_COORDS = (GAME_REGION[0] + 275, GAME_REGION[1] + 522)

    # Calculate the coordinates of the surrounding walls
    RIGHT_WALL = (GAME_REGION[0] + 460, GAME_REGION[1] + 275)
    LEFT_WALL = (GAME_REGION[0] + 88, GAME_REGION[1] + 270)
    UP_WALL = (GAME_REGION[0] + 270, GAME_REGION[1] + 88)
    DOWN_WALL = (GAME_REGION[0] + 275, GAME_REGION[1] + 460)

    # Calculate the center of the screen
    GAME_CENTER = (GAME_REGION[0] + GAME_REGION[2]/2, GAME_REGION[1] + GAME_REGION[3]/2)

def navigateGameWindow():
    """Get the initial focus on the game window and mute the game, getting ready to play."""
    # Get focus on the game by clicking the center of the game region
    pyautogui.click(GAME_CENTER[0], GAME_CENTER[1], duration=1)

    # Mute game (it helps too because it disables some in-game effects :-p)
    pyautogui.press('m')


def newGame():
    """Start a new game by clicking on the PLAY button."""
    # click on Play
    pyautogui.click(PLAY_COORDS, duration=0.25)
    logging.debug('New game...')

def startPlaying():
    """The main game playing function. This function handles all aspects of game play, including starting a new game, playing and detecting game overs."""

    # Start a new game
    newGame()
    
    while True:
        # Wait before searching for the square
        time.sleep(0.1)

        # Wait until the square is at the center of the screen
        while not pyautogui.pixelMatchesColor(GAME_CENTER[0], GAME_CENTER[1], SQUARE_COLOR):
            time.sleep(0.05)
        
        logging.debug('Must move...')

        while True:
            # The direction to go
            direction = None

            # Check for edges until one is open
            if not pyautogui.pixelMatchesColor(LEFT_WALL[0], LEFT_WALL[1], WALL_COLOR):
                direction = 'left'
            elif not pyautogui.pixelMatchesColor(RIGHT_WALL[0], RIGHT_WALL[1], WALL_COLOR):
                direction = 'right'
            elif not pyautogui.pixelMatchesColor(UP_WALL[0], UP_WALL[1], WALL_COLOR):
                direction = 'up'
            elif not pyautogui.pixelMatchesColor(DOWN_WALL[0], DOWN_WALL[1], WALL_COLOR):
                direction = 'down'

            if direction is not None:
                pyautogui.press(direction)
                logging.debug('Moving ' + direction)
                break

        

def checkForGameOver():
    """Checks the screen for the "You Win" or "You Fail" message.

    On winning, returns the string in LEVEL_WIN_MESSAGE.

    On losing, the program terminates."""

    # check for "You Win" message
    result = pyautogui.locateOnScreen(imPath('you_win.png'), region=(GAME_REGION[0] + 188, GAME_REGION[1] + 94, 262, 60))
    if result is not None:
        pyautogui.click(pyautogui.center(result))
        return LEVEL_WIN_MESSAGE

    # check for "You Fail" message
    result = pyautogui.locateOnScreen(imPath('you_failed.png'), region=(GAME_REGION[0] + 167, GAME_REGION[1] + 133, 314, 39))
    if result is not None:
        logging.debug('Game over. Quitting.')
        sys.exit()


if __name__ == '__main__':
    main()
