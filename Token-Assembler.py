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
        print("Error deleting folder or no folder found")
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
    loadAddress = False
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
        "CLSAL" : "11010",
        "CLSA" : "11011",
        "CLSB" : "11100",
        "CLSO" : "11101",
        "CLSP" : "11110",
        "HALT" : "11111"
    }
    with open(txtfilenamepath, "w") as f:
        for data in programData: 
            number, operand_number, opcode_text, comment = data
            number = int(number)
            if loadAddress == True:
                B8binary = opcode_text
                try :
                    B8binary = int(B8binary)
                    B8binary = format(B8binary, '08b')
                    f.write(B8binary + ":" + comment + "\n")
                except ValueError:
                    issue_found[number] = f"Invalid LOAD address : {B8binary}"
                address += 1
                loadAddress = False
            while address < number:
                f.write("11111111\n")
                address += 1
            if number == address:
                if opcode_text in opcodeDic:
                    opcode = opcodeDic[opcode_text]
                    if opcode_text == ("LOAD"):
                        loadAddress = True
                    issue_found = oprand_check(opcode_text, operand_number, issue_found, number)
                else:
                    issue_found[number] = f"Unknown opcode: {opcode_text}"
                f.write(operand_number + opcode + ":" + comment + "\n")
                address += 1
            f.write("11111111\n")           
    return issue_found  
                
def oprand_check(opcode_text, operand_number, issue_found, number):

    LOGICOPRANDS = {
        "001" : "AND",
        "010" : "NAND",
        "011" : "OR",
        "100" : "NOR",
        "101" : "XOR",
        "110" : "XNOR",
        "111" : "NOT"
        }
    MATHOPRANDS = {
        "001" : "ADD",
        "010" : "SUB",
        "011" : "MULT",
        "100" : "DIVQ",
        "101" : "DIVR"
    }
    RANDOPRANDS = {
        "000" : "1-bit",
        "001" : "2-bit",
        "010" : "3-bit",
        "011" : "4-bit",
        "100" : "5-bit",
        "101" : "6-bit",
        "110" : "7-bit",
        "111" : "8-bit" 
    }
    SAVJOPRANDS = {
        "001" : "LOW",
        "010" : "HIGH"
    }
    IFOPRANDS = {
        "001" : "NONE",
        "010" : "==",
        "011" : ">>",
        "100" : "<<"
    }
    WRITPOPRANDS = {
        "001" : "Button 1",
        "010" : "Button 2",
        "011" : "Button 3",
        "100" : "Button 4",
        "101" : "Button 5",
        "110" : "Button 6",
        "111" : "Button 7"
    }
    SEGOPRANDS = {
        "001" : "7 Segment 1",
        "010" : "7 Segment 2",
        "011" : "7 Segment 3",
        "100" : "Button 8",
        "101" : "Button 9"
    }
    CLSOOPRANDS = {
        "001" : "SCR-1",
        "010" : "SCR-2",
        "011" : "SCR-3",
        "100" : "SCR-ALL"
    }
    if opcode_text == "LOGIC":
        if operand_number not in LOGICOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    if opcode_text == "MATH":
        if operand_number not in MATHOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    if opcode_text == "RAND":
        if operand_number not in RANDOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    if opcode_text == "SAVJ":
        if operand_number not in SAVJOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    if opcode_text == "IF":
        if operand_number not in IFOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    if opcode_text == "WRITPOPRANDS":
        if operand_number not in WRITPOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    if opcode_text == "SEGOPRANDS":
        if operand_number not in SEGOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    if opcode_text == "CLSOOPRANDS":
        if operand_number not in CLSOOPRANDS:
            issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    return issue_found        

def main():        
    lîns, filename = read_bnr_file()
    txtfilenamepath = creu(filename)
    programData = build(lîns, txtfilenamepath)
    issue_found = compile(programData, txtfilenamepath)
    if issue_found:
        print("Issues found during compilation:")
        for line, issue in issue_found.items():
            print(f"Line {line}: {issue}")
    else:
        print("Compilation successful with no issues.")
    
while True:
    main()
    input("Press Enter to continue...")
    os.system('cls')

