import termios
import tty
import sys
def get_char():
    # Save the terminal settings
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        # Set terminal to raw mode
        tty.setcbreak(sys.stdin.fileno())
        # Read a single character
        char = sys.stdin.read(1)
    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return char
