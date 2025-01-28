# todo:
# - finish dltools()
# - uninstall function
# - update pre-installed mods/tools (if json ver number greater than installed ver)
# - make tomb incompatibility disclaimer show *before* proceeding w downloading a mod

# imports
import os
import sys
import json
import urllib.request
import traceback
import zipfile

# variables
cfgexi = os.path.isfile("config.json")
tcalpath = ""
mods = { }
tools = { }
conf = { }

# -- json parse function --
def parse(path):
    if os.path.isfile(path):
        with open(path) as raw:
            return json.loads(raw.read())

# -- setup function --
def setup():
    # delete config.json if it already exists
    if cfgexi == True:
        os.remove("config.json")

    # create config.json if it doesn't already exist
    if cfgexi == False:
        cf = open("config.json", "x")
        #cf.write("{ }")
        cf.close()

    # prompt user for tcoaal install path
    print("The Coffin of Andy and Leyley Install Path:")
    global tcalpath
    tcalpath = input()

    # if tcoaal install path doesn't exist
    if not os.path.exists(tcalpath):
        print("That directory doesn't exist.")
        quit()

    # write provided tcoaal path to config.json
    cf = open("config.json", "w")
    cf.write('{ "tcoaal-path":"' + tcalpath + '" }')
    cf.close()

# -- mod download function --
def dlmods():
    # exit if tcoaal path isn't set
    if tcalpath == "":
        print("Error - TCoAaL Install Path not set.")
        quit()

    # check for 3 command line arguments
    if len(sys.argv) < 3:
        quit()
    
    # pass 2nd command line argument to "m" variable
    m = str(sys.argv[2])

    # variables
    global mods
    dl = False

    # check if input is in modids
    if m in mods:
        # variables
        tomb = mods[m]["tomb"]
        dlpath = tcalpath + "tomb/mods/"
        modname = mods[m]["id"][0]
        modurl = mods[m]["dl"]

        # check if mod download url isn't null
        if not modurl == None:
            # check if tomb is installed
            if not os.path.isdir(tcalpath + "tomb/"):
                print("Error - Tomb is not installed.")
                quit()
            
            # check if "tomb/mods/" exists
            if not os.path.isdir(tcalpath + "tomb/mods"):
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
    print("-s       Runs setup (prompts you to enter your TCoAaL installation path).")
    print("-m       Download mods from Visions Database.")
    print("-t       Download tools from Visions Database.")
    quit()

# -- main function --
def main():
    # load + parse json
    global mods
    mods = parse("../mods.json")

    global tools
    tools = parse("../tools.json")

    global conf
    conf = parse("config.json")

    # load tcalpath from conf
    global tcalpath
    if cfgexi == True:
        tcalpath = conf["tcoaal-path"]

    # read command line arguments
    for a in sys.argv:
        if a == "-s":
            # -s runs setup()
            setup()
            break
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
    
    # if there's no command line argument
    if len(sys.argv) == 1:
        vhelp()

# -- run main function --
if __name__ == "__main__":
    main()