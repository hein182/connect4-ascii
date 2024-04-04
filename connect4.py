import os,sys
import time
import tty
import termios
import atexit

#ascii
rch = '🔴'
ych = '🟡'
wch = '⚪'

#variables
won = False
board = [
        [],
        [],
        [],
        [],
        [],
        []
        ]
#fill board
for r in range(len(board)):
    board[r] = [wch,wch,wch,wch,wch,wch,wch]

#essential functions

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

def update_board():
    for y in range(6):
        print("║", end = "")
        for x in range(7):
            print(board[y][x], end= '║')
        print("")
    print("╚══╩══╩══╩══╩══╩══╩══╝")
while not won:
    update_board()
    
    #clear cursor
    sys.stdout.write("\033[?25l")  # Hide cursor on Unix-like systems
    sys.stdout.flush()
    
    #fps
    time.sleep(1/30)
    
    #clear
    os.system('clear')
