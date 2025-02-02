# todo:
# - finish dltools()
# - uninstall function
# - update pre-installed mods/tools (if json ver number greater than installed ver)
# - make tomb incompatibility disclaimer show *before* proceeding w downloading a mod

# imports
from pathlib import Path
import os
import sys
import json
import urllib.request
import traceback
import zipfile

# -- global variables --
mods = { }
tools = { }
fanworks = { }

# -- json parse function --
def parse(file):
    p = Path(file)
    if p.is_file():
        with open(p) as raw:
            return json.loads(raw.read())

# -- json setup function --
def jsons():
    # mods
    global mods
    mods = parse("database/repo/mods.json")

    # tools
    global tools
    tools = parse("database/repo/tools.json")

    # fanworks
    global fworks
    tools = parse("database/repo/fanworks.json")

# -- mod download function --
def dlmods():
    dl = False

    # check for 3 command line arguments
    if len(sys.argv) < 3:
        quit()
    
    # pass 2nd command line argument to "m" variable
    m = str(sys.argv[2])

    # check if input is in modids
    if m in mods:
        # ask for tcoaal install path
        print("TCoAaL Install Path:")
        path = input()

        # more variables
        tomb = mods[m]["tomb"]
        dlpath = path + "tomb/mods/"
        modname = mods[m]["id"][0]
        modurl = mods[m]["dl"]

        # check if mod download url isn't null
        if not modurl == None:
            # check if tomb is installed
            if not os.path.isdir(path + "tomb/"):
                print("Error - Tomb is not installed.")
                quit()
            
            # check if "tomb/mods/" exists
            if not os.path.isdir(path + "tomb/mods"):
                print('Error - Tomb does not have a "mods" folder in its directory.')
                quit()

            # check if mod is already installed
            if not os.path.isdir(modname):
                print("Downloading...")

                # download + catch errors
                try:
                    # download from url
                    urllib.request.urlretrieve(modurl[0], dlpath + modname + ".zip")
                
                    # signal that download is complete
                    dl = True

                    # unzip mod
                    with zipfile.ZipFile(dlpath + modname + ".zip", "r") as zip_ref:
                        zip_ref.extractall(dlpath + modname)

                    # delete .zip
                    os.remove(dlpath + modname + ".zip")
                except:
                    print("Download failed.")
                    traceback.print_exc()
                    quit()

                if dl == True:
                    print("Download complete.")

                # non-tomb disclaimer
                if tomb == False:
                    print("Disclaimer - This mod isn't compatible with the Tomb modloader.")

                quit()
            else:
                print("This mod has already been installed.")
        else:
            print("No download available.")
            quit()
    else:
        print("That mod doesn't exist in Visions Database.")
        quit()

# -- tools download function --
def dltools():
    # check for 3 command line arguments
    if len(sys.argv) < 3:
        quit()
    
    # pass 3rd command line argument to "t" variable
    t = str(sys.argv[2])

    # variables
    dl = False

# -- help function --
def vhelp():
    print("Visions CLI commands:")
    print("-h       Shows this list of commands.")
    print("-m       Download mods from Visions Database.")
    print("-t       Download tools from Visions Database.")
    print("-lm      List mods available on Visions Database.")
    quit()

# -- list mods function --
def lsmods():
    for m in mods:
        print(mods[m])

# -- main function --
def main():
    # json setup
    jsons()

    # read command line arguments
    for a in sys.argv:
        if a == "-m":
            # -m runs dlmods()
            dlmods()
            break
        if a == "-t":
            # -t runs dltools()
            dltools()
            break
        if a == "-h":
            # -h runs vhelp()
            vhelp()
            break
        if a == "-lm":
            # -lm runs lsmods()
            lsmods()
            break
    
    # if there's no command line argument
    if len(sys.argv) == 1:
        vhelp()

# -- run main function --
if __name__ == "__main__":
    main()