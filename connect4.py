import os,sys
import time
import tty
import termios
import atexit
import getch

# Define ANSI escape codes for colors
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

#ascii
rch = Color.RED + '⨂' + Color.END
ych = Color.YELLOW + '⨁' + Color.END
wch = '◯'
cur_p = Color.RED + '⨂' + Color.END

#variables
won = False
px = 7
pn = 1

#arrays objects
cursor = ["╔","═","═","═","═","═","═",cur_p,"═","═","═","═","═","═","╗"]
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
    board[r] = ["║",wch,"║",wch,"║",wch,"║",wch,"║",wch,"║",wch,"║",wch,"║"]

#essential functions

def show_board():
    for y in range(6):
        print("    ", end='')
        for x in range(len(board[y])):
            print(board[y][x], end ='')
        print('')

def put():
    global px
    global cur_p
    if px % 2 != 0:
        for y in range(6):
            if board[y][px] == rch or board[y][px] == ych:
                board[y-1][px] = cur_p
                switch_p()
                #update cursor
                cursor[px] = cur_p
                break
            if y == 5 and board[5][px] == wch:
                board[y][px] = cur_p
                switch_p()
                #update cursor
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
        cursor[px] = '═'
    if d == 'l':
        px -= 1
    if d == 'r':
        px += 1
    if px < 1:
        px = 1
    if px > 13:
        px = 13
     #update cursor
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

os.system('clear')

def update_board():
    for x in range(3):
        print('')
    #cursor for player
    print('    ', end="")
    #cursor
    for c in cursor:
        print(c, end='')
    print('')
    show_board()
    print("    ╚═╩═╩═╩═╩═╩═╩═╝")

while not won:
    update_board()
    
    #clear cursor
    sys.stdout.write("\033[?25l")  # Hide cursor on Unix-like systems
    sys.stdout.flush()
    
    #fps doesn't work for this but helps a little
    time.sleep(1/30)
    
    #get char
    ch = getch.get_char()
    
    #right-left
    if ch == 'l':
        move('r')
    elif ch == 'h':
        move('l')
    #place key
    elif ch == 'p':
        put()
    #exit key
    elif ch == 'q':
        break
    
    #clear
    os.system('clear')
