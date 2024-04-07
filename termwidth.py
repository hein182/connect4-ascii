import os
import struct
import fcntl


def get_terminal_width():
    try:
        # Get terminal width using TIOCGWINSZ system call
        TIOCGWINSZ = 0x5413
        # Create a dummy buffer to store the terminal size
        dummy_buffer = struct.pack("HHHH", 0, 0, 0, 0)
        # Call ioctl with the TIOCGWINSZ command and dummy buffer
        result = fcntl.ioctl(0, TIOCGWINSZ, dummy_buffer)
        # Unpack the result into rows and columns
        _, columns, _, _ = struct.unpack("HHHH", result)
        return columns
    except Exception as e:
        print("Error occurred while getting terminal size:", e)
        return None
