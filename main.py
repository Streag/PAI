from argparse import ArgumentParser
from pyfiglet import figlet_format
from colorama import Fore, Style
import json
import psutil

"""

@Created by Streag 2022

"""

_FILES = False
_GOOD_PROCESSES = None  # []
_VERSION = 'v1.0.0'


banner = figlet_format("PAI", 'slant')
parser = ArgumentParser(description=print(Fore.LIGHTGREEN_EX, banner, Style.RESET_ALL, end=''))
parser.add_argument('-f', '--file', type=str, metavar='', required=False,
                    help='Defines the path to the file in which the recordings are filed')
args = parser.parse_args()
_FILE_PATH = str(args.file)

load = f'[*]'
info = f'{Fore.LIGHTYELLOW_EX}[i]{Style.RESET_ALL}'
error = f'{Fore.LIGHTRED_EX}[-]{Style.RESET_ALL}'
warn = f'{Fore.RED}[!]{Style.RESET_ALL}'

if not _FILE_PATH == 'None':
    _FILES = True


def get_processes():
    processes = []
    for proc in psutil.process_iter():
        try:
            processname = proc.name()
            processID = proc.pid
            processes.append([processname, processID])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes


def get_status_by_pid(pid):
    try:
        process_pid = psutil.Process(pid)
        process_name = process_pid.status()
    except psutil.NoSuchProcess:
        return f"{Fore.LIGHTRED_EX}DIED{Style.RESET_ALL}"
    if str(process_name).upper() == 'RUNNING':
        return f"{Fore.LIGHTGREEN_EX}RUNNING{Style.RESET_ALL}"
    else:
        return f"{Fore.LIGHTYELLOW_EX}{str(process_name).upper()}{Style.RESET_ALL}"

def save():
    global _GOOD_PROCESSES, _FILES
    processes = get_processes()
    if _FILES:
        with open(_FILE_PATH, 'w+') as f:
            f.write(json.dumps(processes))
        processes = None
    else:
        _GOOD_PROCESSES = processes


def report(new_ps):
    n = 0
    for i in new_ps:
        n += 1
    print("++++++++++++++++++++++++++++++++")
    print(f'{n} New process changes identified')
    print("++++++++++++++++++++++++++++++++")
    for ps in new_ps:
        print(f"{ps} -> {get_status_by_pid(ps[1])}")


def diff(li1, li2):
    try:
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    except TypeError:
        print(warn, 'TypeError: To fix this error you can either use a file or overwrite the memory of the variable '
                    '"_GOOD_PROCESSES"')
        exit(-1)
    return li_dif


def main_check():
    global _GOOD_PROCESSES, _FILES
    print(load, "Loading...")

    if _GOOD_PROCESSES == get_processes():
        print(info, "No changes identified.")
        exit(0)

    if _FILES:
        with open(_FILE_PATH, 'r') as f:
            tmp = f.read()
            _GOOD_PROCESSES = json.loads(tmp)
    report(diff(_GOOD_PROCESSES, get_processes()))


if __name__ == '__main__':
    save()
    input("press enter")
    main_check()
