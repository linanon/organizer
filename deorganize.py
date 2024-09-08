import shutil, os , sys

class Color():
    reset = "\033[0m"
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    white = "\033[37m"

# Status Codes
E = f'{Color.red}{Color.bold}[X] Error{Color.red}'
W = f'{Color.yellow}{Color.bold}[!] Warning{Color.reset}'
I = f'{Color.blue}{Color.blue}[*] Info{Color.reset}'

def header():
    global Usage
    
    Usage = f'{Color.blue}Usage{Color.bold}:{sys.argv[0]} <directory>{Color.reset}'
    print(r"""{}
  ____                                   _                     
 / __ \                                 (_)                    
| |  | |  _ __    __ _    __ _   _ __    _   ____   ___   _ __ 
| |  | | | '__|  / _` |  / _` | | '_ \  | | |_  /  / _ \ | '__|
| |__| | | |    | (_| | | (_| | | | | | | |  / /  |  __/ | |   
 \____/  |_|     \__, |  \__,_| |_| |_| |_| /___|  \___| |_|   
                  __/ |                                        
                 |___/                            {} V1.0

{}
        """.format(Color.blue,Color.green,Usage))
    
header()

if len(sys.argv) == 2:
    pathList = [sys.argv[1]]
    path = pathList[-1]
else:
    print(f"{E}: Path to Organize is required!{Color.reset}")
    quit()

try:
    fList = os.listdir(path)
    
    if ".config" in fList:
        _config = os.path.abspath(os.path.join(path,".config"))
        sys.path.append(_config)
        from config import config # type: ignore
except FileNotFoundError:
    try:
        if os.path.exists(os.path.abspath(path)):
            pathList.pop(-1)
            pathList.append(os.path.abspath(path))
    except:
        print(f'{E}: {path} does not exist!{Color.reset}')
        quit()
except PermissionError:
    print(f"{E}: Permission denied! Unable to list {path}.{Color.reset}")
    quit()
except Exception as e:
    print(f"{Color.red}{Color.bold}[X] An unexpected error occurred: {e}{Color.reset}")
    quit()

rm = []

# src is the unorganized place and config[src] is the organized place of the files
def deorganizer(config):
    for src in list(config.keys()):
        try:
            shutil.copy2(config[src], src)
            category = config[src].split("/")
            category.remove(category[-1])
            category = "/".join(category)
            rm.append(category)
            print(f"{I}: Deorganized {config[src]} back to {src}")
        except FileNotFoundError:
            print(f'{E}: {config[src]} does not exist!{Color.reset}')
        except PermissionError:
            print(f"{E}: Permission denied! Unable to deorganize {config[src]} back to {src}.{Color.reset}")
            quit()
        except Exception as e:
            print(f"{Color.red}{Color.bold}[X] An unexpected error occurred: {e}{Color.reset}")
            quit()

deorganizer(config)

def remove(rm):
    ask = str(input(f"\n{Color.red}{Color.bold}Do you want to remove the folder catagories?{Color.reset} (y/n) ")).lower()
    
    if ask == "y":
        rm = list(set(rm))

        while rm != []:
            for f in rm:
                try:
                    shutil.rmtree(f)
                    rm.remove(f)
                    print(f"{I}: Removed {f}.")
                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"{W}: Unable to remove {f}! {E}: {e}{Color.reset}")
                    continue

remove(rm)

try:
    shutil.rmtree(_config)
except Exception as e:
    print(f"{W}: Unable to remove {_config}! {E}: {e}{Color.reset}")