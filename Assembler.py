import sys
import os
import shutil

def read_file(filename: str):
    try:
        while True:  
            if not filename.endswith(".bnr"):
                filename += ".bnr"

            lines = read(filename)
            if lines is not None:
                return lines

            filename = input("[>] Enter filename (.bnr): ")
    except KeyboardInterrupt:
        print("\n\n[?] Interrupt: No file provided.")
        raise SystemExit

def read(filename: str):
    try:
        with open(filename, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        os.system('cls')
        print(f"[?] File '{filename}' not found.")
        return None
    
def creu(filename: str):
    try:
        if os.path.exists(filename):
            shutil.rmtree(filename)
        os.mkdir(filename)

        txtfilenamepath = os.path.join(filename, filename + ".txt")
        with open(txtfilenamepath, "w") as f:
            f.write(":Machine code\n")

        return txtfilenamepath
    except OSError:
        print("\n[?] Error deleting folder or no folder found")
        raise SystemExit

def build(lîns):
    programData = []
    for line in lîns:
        parts = line.split(":")
        comment = parts[1].strip() if len(parts) > 1 else ""
        before_colon = parts[0].strip()
        number, rest = before_colon.split(maxsplit=1)
        rest_parts = rest.split(maxsplit=1)
        operand_number = rest_parts[0]
        if len(rest_parts) > 1:
            opcode_text = rest_parts[1]
        else:
            opcode_text = operand_number[3:]
            operand_number = operand_number[:3]

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
        "SAVZ" : "10010",
        "MEM" : "10011",
        "CLSOU" : "11000",
        "CLSAL" : "11010",
        "CLSA" : "11011",
        "CLSB" : "11100",
        "CLSO" : "11101",
        "CLSP" : "11110",
        "HALT" : "11111"
    }
    withOperandsDic = ["LOGIC", "MATH", "RAND", "SAVJ", "IF", "WRITP", "SEG", "MEM", "CLSOU", "CLSO"]
    with open(txtfilenamepath, "w") as f:
        for data in programData: 
            number, operand_number, opcode_text, comment = data
            number = int(number)
            if loadAddress == True:
                if operand_number == "LWD":
                    B8binary = opcode_text
                    try :
                        B8binary = int(B8binary)
                        B8binary = format(B8binary, '08b')
                        f.write(B8binary + ":" + comment + "\n")
                    except ValueError:
                        issue_found[number] = f"Invalid LOAD address : {B8binary}"
                    address += 1
                    loadAddress = False
                elif operand_number == "PLT":
                    yplot, xplot = opcode_text.split()
                    try :
                        yplot_int = int(yplot)
                        xplot_int = int(xplot)
                        if yplot_int > 11 or yplot_int == 0 or xplot_int > 11 or xplot_int == 0:
                            issue_found[number] = f"Out of Bounds Display address : Y:{yplot}  X:{xplot}"
                        yplot_bin = format(yplot_int, '04b')
                        xplot_bin = format(xplot_int, '04b')
                        B8binary = yplot_bin + xplot_bin
                        f.write(B8binary + ":" + comment + "\n")
                    except ValueError:
                        issue_found[number] = f"Invalid Display address : {yplot} {xplot}"
                    address += 1
                    loadAddress = False
                else:
                    issue_found[number] = f"Invalid LOAD TYPE : {operand_number}"
                    address += 1
                    loadAddress = False
            while address < number:
                f.write("11111111\n")
                address += 1
            if number == address:
                if opcode_text in opcodeDic:
                    opcode = opcodeDic[opcode_text]
                    # print(opcode_text)
                    if opcode_text == ("LOAD"):
                        loadAddress = True
                    issue_found = oprand_check(opcode_text, operand_number, issue_found, number)
                elif operand_number + opcode_text in opcodeDic:
                    # print(operand_number + opcode_text)
                    opcode_text = operand_number + opcode_text
                    if opcode_text in opcodeDic:
                        if opcode_text not in withOperandsDic:
                            opcode = opcodeDic[opcode_text]
                            operand_number = "000"
                            if opcode_text == ("LOAD"):
                                loadAddress = True
                        else:
                            issue_found[number] = f"Opcode given with no Operand: {opcode_text}"
                else:
                    issue_found[number] = f"Unknown opcode: {opcode_text}"
                f.write(operand_number + opcode + ":" + comment + "\n")
                address += 1
        f.write("11111111:End of Program\n")       
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
        "100" : "<<",
        "101" : "!=="
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
    MEMRANS = {
        "001" : "RAM",
        "010" : "USERINPUT",
        "011" : "BŴTIN",
    }
    CLSOURANDS = {
        "001" : "RAM",
        "010" : "USERINPUT",
        "011" : "BŴTIN",
    }
    CLSOOPRANDS = {
        "001" : "SCR-1",
        "010" : "SCR-2",
        "011" : "SCR-3",
        "100" : "SCR-ALL"
    }
    operandDic = {
        "LOGIC": LOGICOPRANDS,
        "MATH": MATHOPRANDS,
        "RAND": RANDOPRANDS,
        "SAVJ": SAVJOPRANDS,
        "IF": IFOPRANDS,
        "WRITP": WRITPOPRANDS,
        "SEG": SEGOPRANDS,
        "MEM": MEMRANS,
        "CLSOU": CLSOURANDS,
        "CLSO": CLSOOPRANDS
    }
    #  and operand_number != "000"
    if operand_number not in operandDic.get(opcode_text, {}):
        issue_found[number] = f"Out of Bounds Operand: {operand_number}"
    return issue_found        

def main():    
    print("=== Binari'n Rhesymegol Token Assembler ===")
    print("-------------------------------------------")
    print()

    if len(sys.argv) > 2:
        print("[?] Usage: Token-Assembler <filename [OPTIONAL]>")
        print("[-] Exiting...")
        return

    filename = sys.argv[1] if len(sys.argv) == 2 else None
    if not filename:
        filename = input("[>] Enter filename (.bnr): ")

    try:
        lînes = read_file(filename)
        txtfilenamepath = creu(filename)
        programData = build(lînes)
        issue_found = compile(programData, txtfilenamepath)

        if issue_found:
            print("Issues found during compilation:")
            for line, issue in issue_found.items():
                print(f"Line {line}: {issue}")
        else:
            print("Compilation successful with no issues.")
        
        input("\n[>] Press any key to exit...")
        raise SystemExit
    except SystemExit:
        print("[-] Exiting...")
        return
    
if __name__ == "__main__":
    print()
    main()
    print()