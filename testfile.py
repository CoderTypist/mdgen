import platform
import re
import subprocess
from typing import List
import warnings

OTHER = -1
WINDOWS = 0
CMD = 1
POWERSHELL = 2
LINUX = 3
WSL = 4


class InvalidTargetException(Exception):
    def __init__(self, source, target):
        message = f'{str_stat(source)} cannot target {str_stat(target)}'
        super().__init__(message)


class UnexpectedValueException(Exception):
    def __init__(self, item):
        message = f'Unexpected value: {item}'
        super().__init__(message)


class UnknownPlatformException(Exception):
    def __init__(self, platform):
        message = f'Could not resolve platform: {str(platform)}'
        super().__init__(message)


class UnknownShellException(Exception):
    def __init__(self, shell):
        message = f'Could not resolve shell: {str(shell)}'
        super().__init__(message)


def get_platform() -> int:
    p = platform.platform().lower()

    if 'windows' in p:
        return WINDOWS
    elif 'microsoft' in p:
        return WSL
    elif 'linux' in p:
        return LINUX
    else:
        return -1


def str_stat(p: int) -> str:
    if WINDOWS == p:
        return 'Windows'
    elif CMD == p:
        return 'CMD'
    elif POWERSHELL == p:
        return 'PowerShell'
    elif WSL == p:
        return 'WSL'
    elif LINUX == p:
        return 'Linux'
    elif WSL == p:
        return 'WSL'
    raise UnexpectedValueException(p)


def win_or_linux() -> int:

    p = get_platform()

    if WINDOWS == p:
        return WINDOWS
    elif WSL == p or LINUX == p:
        return LINUX
    raise UnknownPlatformException(p)


def win_lstrip(text: str) -> str:

    while len(text) >= 2:

        if '\r' == text[0] and '\n' == text[1]:
            text = text[2:]
        else:
            return text


def win_rstrip(text: str) -> str:

    while len(text) >= 2:

        if '\r' == text[-2] and '\n' == text[-1]:
            text = text[:-2]
        else:
            return text


def win_strip(text: str) -> str:
    return win_lstrip(win_rstrip(text)).strip()


def win_default_shell() -> int:

    p = get_platform()

    # platform must be Windows
    if WINDOWS != p and WSL != p:
        raise UnknownPlatformException(p)

    default_shell = subprocess.run(['cmd.exe', '/c', 'echo', '%ComSpec%'], stdout=subprocess.PIPE).stdout.decode()

    # remove ending '\n\r'
    default_shell = default_shell[:-2]

    if '\\cmd.exe' == default_shell[-8:]:
        return CMD

    elif '\\powershell.exe' == default_shell[-15:]:
        return POWERSHELL

    # if the default shell was not cmd or powershell
    raise UnknownShellException(default_shell)


# A wrapper for subprocess()
# The only thing that may need to be changed is the target.
def shell(target: int, args: List, tab=False, verbose=False, strip=True, win_remove_carriage=True) -> str:

    p = get_platform()
    # command to execute in the shell
    com = None
    # output from running com
    ret = None

    if verbose:
        print()
        print(f'shell(): source: {str_stat(p)}')
        print(f'shell(): target: {str_stat(target)}')
        print()

    # The windows default shell is CMD, but it can be changed
    # The code only accounts for the default shell being set to POWERSHELL
    if WINDOWS == target:
        default_shell = win_default_shell()
        target = default_shell

    if WINDOWS == p:
        if CMD == target:
            com = args

        elif POWERSHELL == target:
            com = ['powershell.exe']
            com.extend(args)

        # On WINDOWS, LINUX will default to mean WSL
        elif WSL == target or LINUX == target:
            com = ['wsl']
            com.extend(args)

        else:
            raise UnknownShellException(target)

        ret = subprocess.run(com, shell=True, stdout=subprocess.PIPE).stdout

    elif WSL == p:

        if CMD == target:
            com = ['cmd.exe', '/c']
            com.extend(args)

        elif POWERSHELL == target:
            com = ['powershell.exe']
            com.extend(args)

        # On WSL, LINUX will default to mean WSL
        elif WSL == target or LINUX == target:
            com = args

        else:
            raise UnknownShellException(target)

        ret = subprocess.run(com, stdout=subprocess.PIPE).stdout

    elif LINUX == p:
        if CMD == target or POWERSHELL == target or WSL == target:
            raise InvalidTargetException(p, target)

        elif LINUX == target:
            com = args

        else:
            raise UnknownShellException(target)

        ret = subprocess.run(com, stdout=subprocess.PIPE).stdout.decode()

    else:
        raise UnknownPlatformException(target)

    if ret:

        text = ret.decode()

        if strip:

            # cmd and powershell use '\r\n' as padding
            if CMD == target or POWERSHELL == target:
                text = win_strip(text)
            else:
                text = text.strip()

        # remove carriage returns ('\r') for CMD and POWERSHELL
        if win_remove_carriage and (CMD == target or POWERSHELL == target):
            text = text.replace('\r', '')

        # add a '\t' in front of each line of output
        if tab:
            if text[0] != '\t':
                text = '\t' + text
            text = re.sub('\n', '\n\t', text)

        return text

    else:
        return None


def windows(args: List, tab=False, verbose=False) -> str:
    return shell(WINDOWS, args, tab=tab, verbose=verbose)


def cmd(args: List, tab=False, verbose=False) -> str:
    return shell(CMD, args, tab=tab, verbose=verbose)


def powershell(args: List, tab=False, verbose=False) -> str:
    return shell(POWERSHELL, args, tab=tab, verbose=verbose)


def wsl(args: List, tab=False, verbose=False) -> str:
    return shell(WSL, args, tab=tab, verbose=verbose)


def linux(args: List, tab=False, verbose=False) -> str:
    return shell(LINUX, args, tab=tab, verbose=verbose)


def is_alpha(text: str, extra: List = None) -> bool:

    lower = [chr(_) for _ in range(ord('a'), ord('z')+1)]
    upper = [chr(_) for _ in range(ord('A'), ord('Z')+1)]

    alpha = lower
    alpha.extend(upper)

    if extra:
        alpha.extend(extra)

    for c in text:
        if c not in alpha:
            print('ERROR:', c)
            return False

    return True


# Assumes that the environment variable already exists
#
# Value returned if an environment variable does not exist:
#
#     windows:    depends if cmd or powershell
#     cmd:        var name wrapped in '%'
#     powershell: NoneType
#     wsl:        empty str
#     linux:      empty str
#
# With cmd, it is assumed that if %var_name% is returned that the
# environment variable does not exist, however, this may not be
# the case. It is possible to do something like this:
#
#     Note that the environment variable 'house' does not exist
#     $ echo %house%
#     > %house%
#     $ set house=hello
#     $ echo %house%
#     > hello
#     $ set house=%%house%%
#     $ echo %house%
#     > %house%
#
# Even though this is possible, it is very unlikely that this will
# ever be the case. A more robust check would involve writing a batch
# script that checks to see if the value of the variable is "", however,
# this method is not perfect either.

def env(target: int, var_name: str, cmd_logic=True) -> str:

    # prevent shell injection
    if not is_alpha(var_name, extra=['_']):
        raise Exception('var_name can only contain letters and underscores: ' + var_name)

    if WINDOWS == target:
        target = win_default_shell()

    if CMD == target:
        var = shell(CMD, ['echo', '%' + var_name + '%'])

        # cmd returns %var_name% if the environment variable does not exist
        # although super unlikely, it is possible for the value to be %var_name%
        if cmd_logic:
            if var == '%' + var_name + '%':
                return None

    elif POWERSHELL == target:

        # powershell returns nothing (None) if the environment variable does not exist
        var = shell(POWERSHELL, ['echo', '$env:' + var_name])

    elif WSL == target:
        var = shell(WSL, ['echo', '$' + var_name])

        # linux shell returns an empty string if the environment variable does not exist
        if '' == var:
            return None

    elif LINUX == target:
        var = shell(LINUX, ['echo', '$' + var_name])

        # linux shell returns an empty string if the environment variable does not exist
        if '' == var:
            return None

    else:
        raise InvalidTargetException(get_platform(), target)

    if var:
        return var
    else:
        return None


def wenv(var_name: str) -> str:
    return env(WINDOWS, var_name)


def lenv(var_name: str) -> str:
    return env(LINUX, var_name)


# Using denv() is not recommended
# Behavior will change as the platform/default shell changes
# For more predictable behavior, use wenv() or lenv()
def denv(var_name: str) -> str:

    w = '\n\n\tUsing denv() is not recommended due to potential unexpected behavior'
    w += '\n\t\tConsider wenv() for targeting Windows or lenv() for targeting Linux'
    w += '\n\t\tUse env() if the use of a specific shell is required\n'
    warnings.warn(w)
    p = get_platform()
    return env(p, var_name)
