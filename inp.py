from getpass import getpass
from typing import Any


def get_from_list(options: list, heading: str, prompt: str) -> Any:
    """Get an item from a list, pretty-printing said list and bounds checking. 

    Args:
        options (list): The options to choose from
        heading (str): The heading to print before the printing of the options
        prompt (str): The prompt to pass into input()

    Returns:
        typing.Any: The chosen option
    """
    p=prompt.format(m=len(options))

    print(heading)
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    
    chose=int(input(p))
    while (chose<1) or (chose > len(options)):
        print("Invalid input.")
        chose=int(input(p))
    
    return options[chose-1]

def passw(prompt: str) -> str:
    """An alias for getpass.getpass

    Args:
        prompt (str): The prompt to feed into getpass()

    Returns:
        str: The inputted password
    """
    return getpass(prompt)
