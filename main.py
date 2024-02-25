import os
from colorama import Fore, Style, init
import shutil
import subprocess

init(autoreset=True)

def print_red_ascii_logo():
    os.system('clear' if os.name == 'posix' else 'cls')

    logo_ascii = """
██████╗ ██████╗  ██████╗  ██████╗███████╗███████╗███████╗    ██╗    ██╗██╗██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝██╔════╝██╔════╝    ██║    ██║██║██╔══██╗██╔════╝
██████╔╝██████╔╝██║   ██║██║     █████╗  ███████╗███████╗    ██║ █╗ ██║██║██████╔╝█████╗  
██╔═══╝ ██╔══██╗██║   ██║██║     ██╔══╝  ╚════██║╚════██║    ██║███╗██║██║██╔═══╝ ██╔══╝  
██║     ██║  ██║╚██████╔╝╚██████╗███████╗███████║███████║    ╚███╔███╔╝██║██║     ███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚══════╝     ╚══╝╚══╝ ╚═╝╚═╝     ╚══════╝
                                                                                                                                                                                                     
    """
    terminal_width = shutil.get_terminal_size().columns
    centered_logo = "\n".join(line.center(terminal_width) for line in logo_ascii.split('\n'))
    print(f"{Fore.RED}{centered_logo}{Style.RESET_ALL}", end="")
    text_below_logo = "- By J12C -"
    centered_text = text_below_logo.center(terminal_width)
    print(f"{Fore.LIGHTBLUE_EX}{centered_text}{Style.RESET_ALL}", end="\n\n")
    text_below_logo2 = "Press Enter to continue..."
    centered_text2 = text_below_logo2.center(terminal_width)
    print(f"{Fore.LIGHTBLUE_EX}{centered_text2}{Style.RESET_ALL}", end="\n\n")

if __name__ == "__main__":
    print_red_ascii_logo()
    input()

    
