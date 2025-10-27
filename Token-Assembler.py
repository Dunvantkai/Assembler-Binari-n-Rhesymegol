import os

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
    if os.path.isfile(filename):
        os.remove(filename)
    os.mkdir(filename)
    txtfilenamepath = os.path.join(filename, filename + ".txt")
    with open(txtfilenamepath, "w") as f:
        f.write(":Machine code\n")

# def build():
#     return



def main():        
    lîns, filename = read_bnr_file()
    creu(filename)
    # build(lîns, filename)

main()

