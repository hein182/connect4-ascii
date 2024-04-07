import os
import sys
import time
import termios
import atexit
import getch
import termwidth


# Define ANSI escape codes for colors
class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# ascii
rch = Color.RED + "⨂" + Color.END
ych = Color.YELLOW + "⨁" + Color.END
wch = "◯"
cur_p = Color.RED + "⨂" + Color.END

# variables
won = False
px = 7
pn = 1
termw = termwidth.get_terminal_width()
whitespace = int(termw / 2 - 7) * " "

# arrays objects
cursor = ["╔", "═", "═", "═", "═", "═", "═", cur_p, "═", "═", "═", "═", "═", "═", "╗"]
board = [[], [], [], [], [], []]


# fill board
def fill_board():
    for r in range(len(board)):
        board[r] = [
            "║",
            wch,
            "║",
            wch,
            "║",
            wch,
            "║",
            wch,
            "║",
            wch,
            "║",
            wch,
            "║",
            wch,
            "║",
        ]


# essential functions
def resize():
    global whitespace
    termw = termwidth.get_terminal_width()
    whitespace = int(termw / 2 - 7) * " "


# TODO: create function to detect a connect 4 of yellow or red.
def connect4(cur_y):
    global px
    global cur_p
    yspd = 0
    con4 = 0  # horizontal
    con42 = 0  # vertical
    con43 = 0  # diagonal bottom right
    con44 = 0  # diagonal bottom top
    # horizontal check
    for x in range(0, 14, 2):
        offset = px + 6 - x
        offset3 = cur_y + 3 - yspd
        offset4 = cur_y - 3 + yspd
        if offset >= 0 and offset <= 13:
            if board[cur_y][offset] == cur_p:  # do a horizontal search for a connect 4
                con4 += 1
            if board[cur_y][offset] != cur_p:
                con4 = 0
            if con4 == 4:
                board[cur_y][px] = cur_p
                show_restart()
            # diagonal check
            if offset3 >= 0 and offset3 <= 5:
                if board[offset3][offset] == cur_p:
                    con43 += 1
                else:
                    con43 = 0
                if con43 == 4:
                    board[cur_y][px] = cur_p
                    show_restart()
            # diagonal check opposite side
            if offset4 >= 0 and offset4 <= 5:
                if board[offset4][offset] == cur_p:
                    con44 += 1
                else:
                    con44 = 0
                if con44 == 4:
                    board[cur_y][px] = cur_p
                    show_restart()
        yspd += 1
    # vertical check
    for y in range(9):
        offset2 = cur_y + 3 - y
        if offset2 >= 0 and offset2 <= 5:
            if board[offset2][px] == cur_p:
                con42 += 1
            else:
                con42 = 0
            if con42 == 4:
                board[cur_y][px] = cur_p
                show_restart()


def show_restart():
    switch_p()
    os.system("clear")
    update_board()
    print("")
    print(whitespace + "   CONNECT 4")
    pause = getch.get_char()
    fill_board()


def show_board():
    for y in range(6):
        print(whitespace, end="")
        for x in range(len(board[y])):
            print(board[y][x], end="")
        print("")


def put():
    global px
    global cur_p
    if px % 2 != 0:
        for y in range(6):
            if board[y][px] == rch or board[y][px] == ych:
                board[y - 1][px] = cur_p
                connect4(y - 1)
                switch_p()
                # update cursor
                cursor[px] = cur_p
                break
            if y == 5 and board[5][px] == wch:
                board[y][px] = cur_p
                connect4(y)
                switch_p()
                # update cursor
                cursor[px] = cur_p
                break


def switch_p():
    global pn
    global cur_p
    pn += 1
    if pn % 2 == 0:
        cur_p = ych
    else:
        cur_p = rch


def move(d):
    global px
    if px >= 1 and px <= 13:
        cursor[px] = "═"
    if d == "l":
        px -= 2
    if d == "r":
        px += 2
    if px < 1:
        px = 1
    if px > 13:
        px = 13
    # update cursor
    cursor[px] = cur_p


def enable_echo(enable):
    fd = sys.stdin.fileno()
    new = termios.tcgetattr(fd)
    if enable:
        new[3] |= termios.ECHO
    else:
        new[3] &= ~termios.ECHO

    termios.tcsetattr(fd, termios.TCSANOW, new)


atexit.register(enable_echo, True)
enable_echo(False)

os.system("clear")


def update_board():
    for x in range(3):
        print("")
    # cursor for player
    print(whitespace, end="")
    # cursor
    for c in cursor:
        print(c, end="")
    print("")
    show_board()
    print(whitespace + "╚═╩═╩═╩═╩═╩═╩═╝")


# initialize
fill_board()

while not won:
    update_board()

    # clear cursor
    sys.stdout.write("\033[?25l")  # Hide cursor on Unix-like systems
    sys.stdout.flush()

    # fps doesn't work for this but helps a little
    time.sleep(1 / 30)

    # get char
    ch = getch.get_char()

    # right-left
    if ch == "l":
        move("r")
    elif ch == "h":
        move("l")
    # place key
    elif ch == "p":
        put()
    # exit key
    elif ch == "q":
        break

    resize()

    # clear
    os.system("clear")
