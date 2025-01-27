# todo:
# - choose which function to use (dlmods(), dltools(), setup(), etc) via argument passed in command line
# - show list of possible command when no argument passed in command line
# - finish dltools()
# - uninstall function
# - make tomb incompatibility disclaimer show *before* proceeding w downloading a mod

# imports
import os
import json
import urllib.request
import traceback
import zipfile

# variables
cfgexi = os.path.exists(os.path.join(os.getcwd(), "config.json"))
tcalpath = ""
mods = { }
tools = { }
conf = { }

# -- json parse function --
def parse(path):
     with open(path) as raw:
        return json.loads(raw.read())

# -- setup function --
def setup():
    # create config.json if it doesn't already exist
    if cfgexi == False:
        # prompt user for tcoaal install path
        print("The Coffin of Andy and Leyley Install Path:")
        global tcalpath
        tcalpath = input()

        # if tcoaal install path doesn't exist
        if not os.path.exists(tcalpath):
            print("That directory doesn't exist.")
            quit()

        # write provided tcoaal path to config.json
        cf = open("config.json", "x")
        cf.write('{ "tcoaal-path":"' + tcalpath + '" }')
        cf.close()

# -- mod download function --
def dlmods():
    # prompt user for mod id
    print("Download which mod?")
    m = input()

    # variables
    global mods
    dl = False
    tomb = mods[m]["tomb"]
    dlpath = tcalpath + "tomb/mods/"
    modname = mods[m]["id"][0]
    modurl = mods[m]["dl"]

    # check if input is in modids
    if m in mods:
        if not modurl == None:
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
            print("No download available.")
    else:
        print("That mod doesn't exist in Visions Database.")
        quit()

# -- tools download function --
def dltools():
    # prompt user for tool id
    print("Download which tool?")
    tid = input()

    # variables
    dl = False

# -- main function --
def main():
    # run setup if "config.json" doesn't exist
    if cfgexi == False:
        setup()

    # load + parse json
    global mods
    mods = parse("mods.json")

    global tools
    tools = parse("tools.json")

    global conf
    conf = parse("config.json")

    # load tcalpath from conf
    global tcalpath
    tcalpath = conf["tcoaal-path"]

    # run download mods function
    dlmods()

# -- run main function --
if __name__ == "__main__":
    main()