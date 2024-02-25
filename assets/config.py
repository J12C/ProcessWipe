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
███████╗███████╗████████╗██╗   ██╗██████╗ 
██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
███████╗█████╗     ██║   ██║   ██║██████╔╝
╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
███████║███████╗   ██║   ╚██████╔╝██║     
╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
                                                                                                  
    """
    terminal_width = shutil.get_terminal_size().columns
    centered_logo = "\n".join(line.center(terminal_width) for line in logo_ascii.split('\n'))
    print(f"{Fore.RED}{centered_logo}{Style.RESET_ALL}\n")

def ask_mode():
    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Select the usage mode: \n")
    print(f"{Fore.GREEN}[1] {Fore.WHITE}Online {Fore.LIGHTCYAN_EX}[An internet connection and a Discord webhook URL will be required]")
    print(f"{Fore.GREEN}[2] {Fore.WHITE}Offline {Fore.LIGHTCYAN_EX}[You won't receive any notification once the program is deleted] \n")

    while True:
        try:
            mode_choice = int(input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter the corresponding number for the desired mode: "))
            if mode_choice in [1, 2]:
                break
            else:
                print("Please enter 1 for online or 2 for offline.")
        except ValueError:
            print("Please enter a valid number.")

    return mode_choice

def copy_exec_file(mode):
    if mode == 1:
        shutil.copyfile("py-online/exec-online.py", "../build/exec-online.py")
        print(f"{Fore.GREEN}[+] {Style.RESET_ALL}Exec file copied to build directory for online mode.")
    elif mode == 2:
        shutil.copyfile("py-offline/exec-offline.py", "../build/exec-offline.py")
        print(f"{Fore.GREEN}[+] {Style.RESET_ALL}Exec file copied to build directory for offline mode.")

def get_additional_info(mode):
    clear_screen()
    print_ascii_logo()

    process_name = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter the name of the process to delete: ")
    year = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter the year for the deletion date (YYYY): ")
    month = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter the month for the deletion date (MM): ")
    day = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter the day for the deletion date (DD): ")
    delay = int(input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter delay time in seconds before starting the script (0 for no delay): "))

    if mode == 1:
        webhook_url = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Enter the Discord webhook URL: ")
    else:
        webhook_url = ""

    clear_screen()
    print_ascii_logo()

    print(f"{Fore.GREEN}[?] {Style.RESET_ALL}Process Name: {process_name}")
    print(f"{Fore.GREEN}[?] {Style.RESET_ALL}Deletion Date: {year}-{month}-{day}")
    print(f"{Fore.GREEN}[?] {Style.RESET_ALL}Delay Time: {delay} seconds")

    if mode == 1:
        print(f"{Fore.GREEN}[?] {Style.RESET_ALL}Webhook URL: {webhook_url}")

    while True:
        confirmation = input(f"{Fore.GREEN}[?] {Style.RESET_ALL}Are these details correct? (yes/no): ").lower()
        if confirmation in ['yes', 'no']:
            if confirmation == 'no':
                return get_additional_info(mode)
            else:
                break
        else:
            print(f"{Fore.RED}[!] {Style.RESET_ALL}Please enter 'yes' or 'no'.")

    return process_name, year, month, day, delay, webhook_url

def write_to_exec_file_online(process_name, year, month, day, delay, webhook_url):
    exec_file_path = "../build/exec-online.py"

    with open(exec_file_path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if "anio_personalizado =" in lines[i]:
            lines[i] = f"anio_personalizado = {year}\n"
        elif "mes_personalizado =" in lines[i]:
            lines[i] = f"mes_personalizado = {month}\n"
        elif "dia_personalizado =" in lines[i]:
            lines[i] = f"dia_personalizado = {day}\n"
        elif "nombre_del_proceso =" in lines[i]:
            lines[i] = f"nombre_del_proceso = \"{process_name}\"\n"
        elif "time.sleep()" in lines[i]:
            lines[i] = f"time.sleep({delay})\n"
        elif "webhook_url =" in lines[i]:
            lines[i] = f"webhook_url = \"{webhook_url}\"\n"

    with open(exec_file_path, 'w') as file:
        file.writelines(lines)

def write_to_exec_file_offline(process_name, year, month, day, delay):
    exec_file_path = "../build/exec-offline.py"

    with open(exec_file_path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if "anio_personalizado =" in lines[i]:
            lines[i] = f"anio_personalizado = {year}\n"
        elif "mes_personalizado =" in lines[i]:
            lines[i] = f"mes_personalizado = {month}\n"
        elif "dia_personalizado =" in lines[i]:
            lines[i] = f"dia_personalizado = {day}\n"
        elif "nombre_del_proceso =" in lines[i]:
            lines[i] = f"nombre_del_proceso = \"{process_name}\"\n"
        elif "time.sleep()" in lines[i]:
            lines[i] = f"time.sleep({delay})\n"

    with open(exec_file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    print_ascii_logo()
    
    shutil.rmtree('../build', ignore_errors=True)
    
    os.makedirs('../build')
    
    mode = ask_mode()
    print(f"You have selected the {'Online' if mode == 1 else 'Offline'} mode.")
    copy_exec_file(mode)

    if mode == 1:
        process_name, year, month, day, delay, webhook_url = get_additional_info(mode)
        write_to_exec_file_online(process_name, year, month, day, delay, webhook_url)
        print("Values successfully written to the script file.")


    elif mode == 2:
        process_name, year, month, day, delay, _ = get_additional_info(mode)
        write_to_exec_file_offline(process_name, year, month, day, delay)
        print("Values successfully written to the script file.")
