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

def build(lîns,txtfilenamepath):
    programData = []
    for line in lîns:
        parts = line.split(":")
        comment = parts[1].strip() if len(parts) > 1 else ""
        before_colon = parts[0].strip()
        number, opcode = before_colon.split(maxsplit=1)
        operand_number = opcode[:3] 
        opcode_text = opcode[3:]
        programData.append((number, operand_number, opcode_text, comment))
    # print("Number:", number)
    # print("Operand number:", operand_number)
    # print("Opcode text:", opcode_text)
    # print("Comment:", comment)
    return (programData)

def compile(programData, txtfilenamepath): 
    address = 0
    issue_found = {}
    opcodeDic = {
        "NOP": "00000",
        "READL" : "00001",
        "READH" : "00010",
        "WRITL" : "00011",
        "WRITH" : "00100",
        "SAVA" : "00101",
        "SAVB" : "00110",
        "LOGIC" : "00111",
        "MATH" : "01000",
        "RAND" : "01001",
        "SAVJ" : "01010",
        "LOAD" : "01011",
        "IF" : "01100",
        "INPUT" : "01101",
        "READP" : "01110",
        "WRITP" : "01111",
        "SEG" : "10000",
        "PLOT" : "10001",
        "HALT" : "10010",
        "CLSA" : "11011",
        "CLSB" : "11100",
        "CLSO" : "11101",
        "CLSP" : "11110",
        "CLSAL" : "11111"
    }
    with open(txtfilenamepath, "w") as f:
        for data in programData: 
            number, operand_number, opcode_text, comment = data
            number = int(number)
            while address < number:
                f.write("00000000\n")
                address += 1
            if number == address:
                if opcode_text in opcodeDic:
                    opcode = opcodeDic[opcode_text]
                else:
                    issue_found[number] = f"Unknown opcode: {opcode_text}"
                f.write(operand_number + opcode + ":" + comment + "\n")
                address += 1
    return issue_found                  
        
def main():        
    lîns, filename = read_bnr_file()
    txtfilenamepath = creu(filename)
    programData = build(lîns, txtfilenamepath)
    issue_found = compile(programData, txtfilenamepath)
    if issue_found:
        print("Issues found during compilation:")
        for line_num, issue in issue_found.items():
            print(f"Line {line_num}: {issue}")
    else:
        print("Compilation successful with no issues.")
    input("Press Enter to continue...")
while True:
    main()
    os.system('cls')

