import os
import shutil

def read_bnr_file():
    while True:
        filename = input("Enter the filename: ")
        fullfilename = filename+".BNR"
        try:
            with open(fullfilename, "r") as f:
                lines = f.readlines()
                return lines, filename
        except FileNotFoundError:
            print("File not found. Please check the filename and try again.")
            input("Press Enter to continue...")
            os.system('cls')

def creu(filename):
    try:
        shutil.rmtree(filename)
    except OSError as e:
        print("Error deleting folder")
    os.mkdir(filename)
    txtfilenamepath = os.path.join(filename, filename + ".txt")
    with open(txtfilenamepath, "w") as f:
        f.write(":Machine code\n")
    return txtfilenamepath

def build():
    return



def main():        
    lîns, filename = read_bnr_file()
    txtfilenamepath = creu(filename)
    build(lîns, txtfilenamepath)

main()

