import os
import shutil
import time
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_ascii_logo():
    clear_screen()

    logo_ascii = """
 ██████╗ ██████╗ ███╗   ███╗██████╗  █████╗ ██╗██╗     ███████╗██████╗ 
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██║██║     ██╔════╝██╔══██╗
██║     ██║   ██║██╔████╔██║██████╔╝███████║██║██║     █████╗  ██████╔╝
██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██║██║██║     ██╔══╝  ██╔══██╗
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║██║███████╗███████╗██║  ██║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                                                                                                  
    """
    terminal_width = shutil.get_terminal_size().columns
    centered_logo = "\n".join(line.center(terminal_width) for line in logo_ascii.split('\n'))
    print(f"{Fore.RED}{centered_logo}{Style.RESET_ALL}\n")

def compile_file(filename, icon=None):
    os.chdir("../build")
    command = f"pyinstaller {filename}.py --onefile --noconsole"
    if icon:
        command += f" --icon {icon}"
    os.system(f"{command} > log.txt 2>&1")  
    os.chdir("..")

def move_exe():
    build_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build")
    dist_path = os.path.join(build_path, "dist")
    if os.path.exists(dist_path):
        files_to_keep = [f for f in os.listdir(dist_path) if f.endswith(".exe")]
        for item in os.listdir(build_path):
            item_path = os.path.join(build_path, item)
            if os.path.isdir(item_path):
                if item == "dist":
                    for sub_item in os.listdir(dist_path):
                        sub_item_path = os.path.join(dist_path, sub_item)
                        if sub_item not in files_to_keep:
                            if os.path.isfile(sub_item_path):
                                os.remove(sub_item_path)
                            else:
                                shutil.rmtree(sub_item_path)
                    for file in files_to_keep:
                        shutil.move(os.path.join(dist_path, file), build_path)
                    shutil.rmtree(dist_path)
                    os.system("start explorer .")
                else:
                    shutil.rmtree(item_path)
            elif item != "log.txt":
                os.remove(item_path)

def main():
    print_ascii_logo()

    build_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build")
    python_files = [f for f in os.listdir(build_path) if f.endswith(".py")]
    if not python_files:
        print("No Python files found in the ../build directory.")
        return

    python_file = python_files[0]
    compile_choice = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Do you want to compile the file '{python_file}' (Y/N)? ").strip().lower()
    if compile_choice == 'y':
        icon_choice = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Do you want to add an icon to the file (Y/N)? ").strip().lower()
        icon_path = None
        if icon_choice == 'y':
            icon_path = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter the path to the icon file:").strip()
        print()
        print(f"{Fore.GREEN}[+] Compailing...")
        compile_file(os.path.splitext(python_file)[0], icon_path)
        move_exe()
        input(f"{Fore.GREEN}[+] Done")

if __name__ == "__main__":
    main()
