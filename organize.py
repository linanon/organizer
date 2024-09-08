import os, shutil, sys
from dict import fileExt


class Color():
    reset = "\033[0m"
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"

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


def pCheck(Path):
    global fList
    
    try:
        fList = os.listdir(Path)
        files = ""
        
        for F in fList:
            files += f'{F}\n'

        print(files)
    except FileNotFoundError:
        print(f'{E}: {Path} does not exist!\n{I}: Try with the {Color.bold}"absolute path" instead.{Color.reset}')
        quit()
    except PermissionError:
        print(f"{E}: Permission denied! Unable to list {Path}.{Color.reset}")
        quit()
    except Exception as e:
        print(f"{Color.red}{Color.bold}[X] An unexpected error occurred: {e}{Color.reset}")
        quit()

if len(sys.argv) == 2:
    pathList = [sys.argv[1]]
    path = pathList[-1]
    
    pCheck(path)
else:
    print(f"{E}: Path to Organize is required!{Color.reset}")
    quit()

rm = []
subF = []
configs = dict()

def organizer(ls):
    lsType = dict()
    organizedFiles = []
    organizedDirs = []    

    # Copying files from src to dest and more
    for f in ls: 
        srcFile = os.path.join(pathList[-1], f)
        
        if srcFile not in organizedDirs and srcFile not in organizedFiles:
            if os.path.isfile(srcFile):
                fType = "Other"

                if "." in f: ext = f.split(".")[-1]
                if ext in fileExt: fType = fileExt[ext]
                
                lsType[f] = fType
                _dir = os.path.join(path, fType)
                
                try:
                    os.makedirs(_dir, exist_ok=True)
                except Exception as e:
                    print(f"{Color.red}{Color.bold}[X] An unexpected error occurred: {e}{Color.reset}")
                    quit()
                
                destFile = os.path.join(_dir, f)

                try:
                    shutil.copy2(srcFile,destFile)
                    organizedFiles.append(srcFile)
                    rm.append(srcFile)
                    configs[srcFile] = destFile
                    print(f"{I}: Organized {srcFile} to {destFile}.")
                except PermissionError:
                    print(f"{E}: Permission denied! Unable to access '{srcFile}' or '{destFile}'.\n{W}: Leaving {f} Unorganized!{Color.reset}")
                except Exception as e:
                    print(f"{Color.red}{Color.bold}[X] An unexpected error occurred: {e}!\n{W}: Leaving {f} Unorganized!{Color.reset}")
            elif f != ".config" and os.path.isdir(srcFile):
                subF.append(srcFile)
    
    # To organize sub-folders
    for F in subF:
        subF.remove(F)
        
        if F not in organizedDirs:
            try:
                print(f"\n  {I}: Encountered a directory -> '{F}'")
                ask = str(input(f"\nDo you want to {Color.bold}organize{Color.reset} the files under {Color.bold}{F}{Color.reset}? (y/n) ")).lower()
                
                if ask == "y": 
                    print(f"\n  {I}: Organizing the files under {F}...")
                    lsFolder = os.listdir(F)
                    pCheck(F)

                    def organizeFolder(src): # So that changes for ls,... will only apply in this func(to make var changes "static")
                        global path

                        pathList.append(F)
                        path = pathList[-1]
                        organizer(src)
                        pathList.pop(-1)
                        organizedDirs.append(F)

                    organizeFolder(lsFolder)
            except Exception as e:
                print(f"{Color.red}{Color.bold}[X] An unexpected error occurred: {e}!\n{W}: Leaving files under {srcFile} Unorganized!{Color.reset}")

# A func to make a config file for the purpose of deorganizing the files back
def Config(configDict):
        config = os.path.join(sys.argv[-1], ".config")
        configFile = os.path.join(config, "config.py")
        
        try:
            os.makedirs(config, exist_ok=True)
            
            with open(configFile, "w") as conf:
                confDict = f"config = {configDict}"
                conf.write(confDict)
            
            conf.close()
        except Exception as e:
            print(f"{Color.red}{Color.bold}[X] An unexpected error occurred: {e}!{Color.reset}")
            quit()

# Removing Copies of the organized files from their previous location
def  remove(rm):
    ask = str(input(f"\n{Color.red}{Color.bold}Do you want to remove all the copies of the organized files from their previous paths?{Color.reset} (y/n) ")).lower()
    
    if ask == "y":
        for f in rm:
            try:
                os.remove(f)
                print(f"{I}: Removed {f}.")
            except Exception as e:
                print(f"{W}: Unable to remove {f}! {E}: {e}{Color.reset}")

organizer(fList)
Config(configs)
remove(rm)