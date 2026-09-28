"""An input handler for PyJellyTerm."""
import os
import sys
from getpass import getpass
from typing import Any

if os.name == 'nt':
    import msvcrt # pylint: disable=import-error
    def get_key() -> str | None:
        """Get an arrow key / escape (Windows)

        Returns:
            str|None: 'up'/'down'/'left'/'right' for arrows, 'esc' for ESC, and None for other keys
        """
        ret=None
        ch = msvcrt.getch()
        # Arrow keys on Windows prefix with 0x00 or 0xE0
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            match ch2:
                case b'H':
                    return "up"
                case b'P':
                    return "down"
                case b'K':
                    return "left"
                case b'M':
                    return "right"
        if ch == b'\x1b':
            ret="esc"
        if ch in (b'\r', b'\n'):
            ret="enter"  # Added to catch submission
        return ret
else:
    import termios # pylint: disable=import-error
    import tty # pylint: disable=import-error
    def get_key() -> str | None:
        """Get an arrow key / escape

        Returns:
            str|None: 'up'/'down'/'left'/'right' for arrows, 'esc' for ESC, and None for other keys
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        ret=None
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    match ch3:
                        case b'A':
                            return "up"
                        case b'B':
                            return "down"
                        case b'D':
                            return "left"
                        case b'C':
                            return "right"
                return "esc"
            if ch in ('\r', '\n'):
                ret="enter"  # Added to catch submission
            return ret
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_from_list(options: list, heading: str) -> Any:
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
    c=len(heading.split("\n"))+len(options)
    # Hide terminal cursor if possible to make it look cleaner
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            print(heading)

            for i, opt in enumerate(options):
                if i == selected_index:
                    print(f" > \033[1;36m{opt}\033[0m") # Bold Cyan cursor item
                else:
                    print(f"   {opt}")

            key = get_key()
            if key == "up":
                selected_index = (selected_index - 1) % num_options
            elif key == "down":
                selected_index = (selected_index + 1) % num_options
            elif key == "enter":
                return options[selected_index]
            elif key == "esc":
                return None

            sys.stdout.write(f"\033[{c}A")
    except (EOFError, KeyboardInterrupt):
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
