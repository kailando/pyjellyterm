import os
import sys
from getpass import getpass
from typing import Any

if os.name == 'nt':
    import msvcrt
    def get_key() -> str | None:
        """Get an arrow key / escape (Windows)

        Returns:
            str | None: 'up' / 'down' / 'left' / 'right' for arrow keys, 'esc' for escape, and None for other keys
        """
        ch = msvcrt.getch()
        # Arrow keys on Windows prefix with 0x00 or 0xE0
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            if ch2 == b'H': return "up"
            if ch2 == b'P': return "down"
            if ch2 == b'K': return "left"
            if ch2 == b'M': return "right"
        if ch == b'\x1b': return "esc"
        if ch in (b'\r', b'\n'): return "enter"  # Added to catch submission
        return None
else:
    import termios
    import tty
    def get_key() -> str | None:
        """Get an arrow key / escape

        Returns:
            str | None: 'up' / 'down' / 'left' / 'right' for arrow keys, 'esc' for escape, and None for other keys
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A': return "up"
                    if ch3 == 'B': return "down"
                    if ch3 == 'D': return "left"
                    if ch3 == 'C': return "right"
                return "esc"
            if ch in ('\r', '\n'): return "enter"  # Added to catch submission
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_from_list(options: list, heading: str, prompt: str) -> Any:
    """Get an item from a list by letting the user navigate with arrow keys.

    Args:
        options (list): The options to choose from
        heading (str): The heading to print before the printing of the options
        prompt (str): Instructions or footer displayed below the menu

    Returns:
        Any: The chosen option, or None if escaped
    """
    selected_index = 0
    num_options = len(options)

    # Hide terminal cursor if possible to make it look cleaner
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            # ANSI escape sequence to clear terminal or overwrite cleanly
            # We rewrite lines dynamically. To keep it simple, we clear screen slice or use ANSI codes.
            # Alternate approach: Print menu, then erase previous lines on redraw
            sys.stdout.write("\033[H\033[J") # Clears terminal cleanly for full redraw
            print(heading)
            
            for i, opt in enumerate(options):
                if i == selected_index:
                    print(f" > \033[1;36m{opt}\033[0m") # Bold Cyan cursor item
                else:
                    print(f"   {opt}")
            
            print(f"\n{prompt}")
            
            key = get_key()
            if key == "up":
                selected_index = (selected_index - 1) % num_options
            elif key == "down":
                selected_index = (selected_index + 1) % num_options
            elif key == "enter":
                return options[selected_index]
            elif key == "esc":
                return None
    finally:
        # Always restore the terminal cursor when exiting
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def passw(prompt: str) -> str:
    """An alias for getpass.getpass

    Args:
        prompt (str): The prompt to feed into getpass()

    Returns:
        str: The inputted password
    """
    return getpass(prompt)
