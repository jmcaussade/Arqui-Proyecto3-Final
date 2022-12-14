
from dataclasses import replace
import re


Exp = []
Exp.append(r'(SUB|CMP|MOV|AND|OR|XOR|ADD)\s(A|B),(\d+|#\w+|-\d+)$')
Exp.append(r'(XOR|ADD|AND|SUB|OR|MOV)\sB,A$')
Exp.append(r'(XOR|OR|SUB|AND|ADD|MOV|CMP)\sA,B$')
Exp.append(r'(SHR|SHL|NOT)\s(A|B),(A|B)$')
Exp.append(r'(MOV|NOT|SHL|SHR)\s(\(#\w+\)|\(\d+\)|\([a-zC-Z0-9]+\)|\(-\d+\)),(A|B)|(\w+)$')
Exp.append(r'(XOR|AND|SUB|ADD|OR|MOV|CMP)\s(A),\(B\)$')
Exp.append(r'(MOV)\s(B),\(B\)$')
Exp.append(r'(INC)\sB$')
Exp.append(r'(JMP|JEQ|JNE|JGT|JLT|JGE|JLE|JCR|JOV)\s((\d+|#\w+)|-\d+|[a-zC-Z0-9]+)|(\w+)$')
Exp.append(r'(NOT|SHL|SHR|INC|RST)\s\(B\)$')
Exp.append(r'(MOV)\s\(B\),(A)$')
Exp.append(r'(ADD|SUB|AND|OR|XOR|INC|RST)\s(\(#\w+\)|\(\d+\)|\([a-zC-Z0-9]+\)|\(-\d+\))$')
Exp.append(r'(MOV|ADD|SUB|AND|OR|XOR|CMP)\s(A|B),(\(#\w+\)|\(\d+\)|\([a-zC-Z0-9]+\)|\(-\d+\))$')
Exp.append(r'(NOT|SHL|SHR|INC|RST)\s\(B\)$')






def revisar(lista,expresiones):
    malos = []
    x = 1
    for e in lista:
        c = True
        for i in expresiones:
            e_state = re.match(i,e)
            if e_state != None:
                c = False
        if c == True:
            Incorrecta = (f'La sentencia {e} de la linea {x} es incorrecta')
            print(Incorrecta)
            malos.append(1)
        x += 1
    if len(malos) > 0:
        return False
    else:
        return True


def CheckBinary(string):
    if "b" in string:
        return True
    else:
        return False

def CheckHexa(string):
    if "#" in string:
        return True
    else:
        return False


def CleanLine(line):
    list1 = line.replace("(","")
    list1 = list1.replace(")","")
    list1 = list1.split(",")
    return list1


def Write(result, line, linecounter, opcode, ErrorCounter):
    if result == False:
        print("El numero de la expresion: " + line + " en la linea " + str(linecounter) +
        " está fuera de rango")
        ErrorCounter.append("1")
    else:
        ListLine.append(line)
        ListOp.append(opcode + result)
        

def ToBinary(number, binary, decimal, hexa):
    if binary == True:
        return number
    elif hexa == True:
        scale = 16 ## equals to hexadecimal
        num_of_bits = 8
        result1 = int(number, scale)
        #print(result1)
        if result1 <= 255 and result1 >= -125:
            result = bin(int(number, scale))[2:].zfill(num_of_bits)
            return result
        else:
            return False
    elif decimal == True:
        num = bin(int(number)).replace("0b","")
        i = 0
        while len(num) < 8:
            num = "0" + num
            i+=1
        return num
    



def MOV(list, file):  #MOV (RealLine) -> ins basicas
    linea = list1[1].split(",")  
    if "(" in linea[0]: # #EJ: MOV (Lit),A
        linea[0] = linea[0].replace("(","")
        linea[0] = linea[0].replace(")","")
        pos1 = linea[0].isnumeric()
        pos2 = CheckBinary(linea[0])
        linea[0] = linea[0].replace("b","")
        pos3 = CheckHexa(linea[0])
        linea[0] = linea[0].replace("#","")
        if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
            num = linea[0]
            binary = ToBinary(num, pos2, pos1, pos3)
            if linea[1] == "A":
                Write(binary, line, linecounter,"0100111", ErrorCounter)

            elif linea[1] == "B":
                Write(binary, line, linecounter,"0101000", ErrorCounter)

                
        else:
            ListOp.append("010101100000000")
            ListLine.append(line)


    elif "(" in linea[1] :   #EJ: MOV A,(Dir)
        linea[1] = linea[1].replace("(","")
        linea[1] = linea[1].replace(")","")
        pos1 = linea[1].isnumeric()
        pos2 = CheckBinary(linea[1])
        linea[1] = linea[1].replace("b","")
        pos3 = CheckHexa(linea[1])
        linea[1] = linea[1].replace("#","")
        if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
            num = linea[1]
            binary = ToBinary(num, pos2, pos1, pos3)
            if linea[0] == "B":
                Write(binary, line, linecounter,"0100110", ErrorCounter)

            elif linea[0] == "A":
                Write(binary, line, linecounter,"0100101", ErrorCounter)

        else: 
            if linea[0] == "A":
                ListOp.append("010100100000000")
                ListLine.append(line)

            elif linea[0] == "B":
                ListOp.append("010101000000000")
                ListLine.append(line)
                
                
    else:   # para abajo instrucciones basicas
        if len(linea) > 1:
            pos1 = linea[1].isnumeric()
            pos2 = CheckBinary(linea[1])
            linea[1] = linea[1].replace("b","")
            pos3 = CheckHexa(linea[1])
            linea[1] = linea[1].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[1]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[0] == "A":
                    Write(binary, line, linecounter,"0000010", ErrorCounter)

                elif linea[0] == "B":
                    Write(binary, line, linecounter,"0000011", ErrorCounter)

            else:
                if linea[0] == "A":
                    ListOp.append("000000000000000")
                    ListLine.append(line)
                elif linea[0] == "B":
                    ListOp.append("000000100000000")
                    ListLine.append(line)
    
def ADD(list, file):  
    linea = list1[1].split(",") # EJ A,B 
    if len(linea) > 1: #Ej ADD A,(Dir)
        if "(" in linea[1]: # #EJ: ADD A,(Dir)
            linea[1] = linea[1].replace("(","")
            linea[1] = linea[1].replace(")","")
            pos1 = linea[1].isnumeric()
            pos2 = CheckBinary(linea[1])
            linea[1] = linea[1].replace("b","")
            pos3 = CheckHexa(linea[1])
            linea[1] = linea[1].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[1]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[0] == "A": # ADD A,(Dir)
                    Write(binary, line, linecounter,"0101100", ErrorCounter)

                if linea[0] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"0101101", ErrorCounter)

                    
            else:
                ListOp.append("010111000000000")
                ListLine.append(line)

        else: #XOR -> ins basicas
            if len(linea) > 1:
                pos1 = linea[1].isnumeric()
                pos2 = CheckBinary(linea[1])
                linea[1] = linea[1].replace("b","")
                pos3 = CheckHexa(linea[1])
                linea[1] = linea[1].replace("#","")
                if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                    num = linea[1]
                    binary = ToBinary(num, pos2, pos1, pos3)
                    if linea[0] == "A":
                        Write(binary, line, linecounter,"0000110", ErrorCounter)

                    elif linea[0] == "B":
                        Write(binary, line, linecounter,"0000111", ErrorCounter)

                else:
                    if linea[0] == "A":
                        ListOp.append("000010000000000")
                        ListLine.append(line)
                    elif linea[0] == "B":
                        ListOp.append("000010100000000")
                        ListLine.append(line)
            else:
                    pos1 = list[1].isnumeric()
    else: #Ej ADD (Dir)
        linea[0] = linea[0].replace("(","")
        linea[0] = linea[0].replace(")","")
        num = linea[0]
        pos1 = linea[0].isnumeric()
        pos2 = CheckBinary(linea[0])
        linea[0] = linea[0].replace("b","")
        pos3 = CheckHexa(linea[0])
        linea[0] = linea[0].replace("#","")
        binary = ToBinary(num,pos2, pos1, pos3 )
        Write(binary, line, linecounter,"0101111", ErrorCounter)

  
def SUB(list, file):  
    linea = list1[1].split(",") # EJ A,B
    if len(linea) > 1: #Ej ADD A,(Dir)
        if "(" in linea[1]: # #EJ: ADD A,(Dir)
            linea[1] = linea[1].replace("(","")
            linea[1] = linea[1].replace(")","")
            pos1 = linea[1].isnumeric()
            pos2 = CheckBinary(linea[1])
            linea[1] = linea[1].replace("b","")
            pos3 = CheckHexa(linea[1])
            linea[1] = linea[1].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[1]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[0] == "A": # ADD A,(Dir)
                    Write(binary, line, linecounter,"0110000", ErrorCounter)
                if linea[0] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"0110001", ErrorCounter)
   
            else:
                ListOp.append("011001000000000")
                ListLine.append(line)

        else: #XOR -> ins basicas
            if len(linea) > 1:
                pos1 = linea[1].isnumeric()
                pos2 = CheckBinary(linea[1])
                linea[1] = linea[1].replace("b","")
                pos3 = CheckHexa(linea[1])
                linea[1] = linea[1].replace("#","")
                if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                    num = linea[1]
                    binary = ToBinary(num, pos2, pos1, pos3)
                    if linea[0] == "A":
                        Write(binary, line, linecounter,"0001010", ErrorCounter)

                    elif linea[0] == "B":
                        Write(binary, line, linecounter,"0001011", ErrorCounter)

                else:
                    if linea[0] == "A":
                        ListOp.append("000100000000000")
                        ListLine.append(line)
                    elif linea[0] == "B":
                        ListOp.append("000100100000000")
                        ListLine.append(line)
            else:
                    pos1 = list[1].isnumeric()
    else: #Ej ADD (Dir)
        linea[0] = linea[0].replace("(","")
        linea[0] = linea[0].replace(")","")
        num = linea[0]
        pos1 = linea[0].isnumeric()
        pos2 = CheckBinary(linea[0])
        linea[1] = linea[1].replace("b","")
        pos3 = CheckHexa(linea[0])
        linea[0] = linea[0].replace("#","")
        binary = ToBinary(num,pos2, pos1, pos3 )
        Write(binary, line, linecounter,"0110011", ErrorCounter)

  
def AND(list, file):  
    linea = list1[1].split(",") # EJ A,B 
    if len(linea) > 1: #Ej ADD A,(Dir)
        if "(" in linea[1]: # #EJ: ADD A,(Dir)
            linea[1] = linea[1].replace("(","")
            linea[1] = linea[1].replace(")","")
            pos1 = linea[1].isnumeric()
            pos2 = CheckBinary(linea[1])
            linea[1] = linea[1].replace("b","")
            pos3 = CheckHexa(linea[1])
            linea[1] = linea[1].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[1]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[0] == "A": # ADD A,(Dir)
                    Write(binary, line, linecounter,"0110100", ErrorCounter)

                if linea[0] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"0110101", ErrorCounter)

                    
            else:
                ListOp.append("011011000000000")
                ListLine.append(line)

        else: #XOR -> ins basicas
            if len(linea) > 1:
                pos1 = linea[1].isnumeric()
                pos2 = CheckBinary(linea[1])
                linea[1] = linea[1].replace("b","")
                pos3 = CheckHexa(linea[1])
                linea[1] = linea[1].replace("#","")
                if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                    num = linea[1]
                    binary = ToBinary(num, pos2, pos1, pos3)
                    if linea[0] == "A":
                        Write(binary, line, linecounter,"0001110", ErrorCounter)

                    elif linea[0] == "B":
                        Write(binary, line, linecounter,"0001111", ErrorCounter)

                        
                else:
                    if linea[0] == "A":
                        ListOp.append("000110000000000")
                        ListLine.append(line)
                    elif linea[0] == "B":
                        ListOp.append("000110100000000")
                        ListLine.append(line)
                        
                        
            else:
                    pos1 = list[1].isnumeric()
    else: #Ej ADD (Dir)
        linea[0] = linea[0].replace("(","")
        linea[0] = linea[0].replace(")","")
        num = linea[0]
        pos1 = linea[0].isnumeric()
        pos2 = CheckBinary(linea[0])
        linea[0] = linea[0].replace("b","")
        pos3 = CheckHexa(linea[0])
        linea[0] = linea[0].replace("#","")
        binary = ToBinary(num,pos2, pos1, pos3 )
        file.write(line + "\n")
        file.write("0110111" + binary + "\n")
        Write(binary, line, linecounter,"0110111", ErrorCounter)


def OR(list, file):  
    linea = list1[1].split(",") # EJ A,B 
    if len(linea) > 1: #Ej ADD A,(Dir)
        if "(" in linea[1]: # #EJ: ADD A,(Dir)
            linea[1] = linea[1].replace("(","")
            linea[1] = linea[1].replace(")","")
            pos1 = linea[1].isnumeric()
            pos2 = CheckBinary(linea[1])
            linea[1] = linea[1].replace("b","")
            pos3 = CheckHexa(linea[1])
            linea[1] = linea[1].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[1]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[0] == "A": # ADD A,(Dir)
                    Write(binary, line, linecounter,"0111000", ErrorCounter)

                if linea[0] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"0111001", ErrorCounter)

            else:
                ListOp.append("0111010000000")
                ListLine.append(line)

                

        else: #XOR -> ins basicas
            if len(linea) > 1:
                pos1 = linea[1].isnumeric()
                pos2 = CheckBinary(linea[1])
                linea[1] = linea[1].replace("b","")
                pos3 = CheckHexa(linea[1])
                linea[1] = linea[1].replace("#","")
                if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                    num = linea[1]
                    binary = ToBinary(num, pos2, pos1, pos3)
                    if linea[0] == "A":
                        Write(binary, line, linecounter,"0010010", ErrorCounter)

                    elif linea[0] == "B":
                        Write(binary, line, linecounter,"0010011", ErrorCounter)

                else:
                    if linea[0] == "A":
                        ListOp.append("001000000000000")
                        ListLine.append(line)
                    elif linea[0] == "B":
                        ListOp.append("001000100000000")
                        ListLine.append(line)
                        
            else:
                    pos1 = list[1].isnumeric()
    else: #Ej ADD (Dir)
        linea[0] = linea[0].replace("(","")
        linea[0] = linea[0].replace(")","")
        num = linea[0]
        pos1 = linea[0].isnumeric()
        pos2 = CheckBinary(linea[0])
        linea[0] = linea[0].replace("b","")
        pos3 = CheckHexa(linea[0])
        linea[0] = linea[0].replace("#","")
        binary = ToBinary(num,pos2, pos1, pos3)
        Write(binary, line, linecounter,"0111011", ErrorCounter)


def XOR(list, file):  
    linea = list1[1].split(",") # EJ A,B 
    if len(linea) > 1: #Ej ADD A,(Dir)
        if "(" in linea[1]: # #EJ: ADD A,(Dir)
            linea[1] = linea[1].replace("(","")
            linea[1] = linea[1].replace(")","")
            pos1 = linea[1].isnumeric()
            pos2 = CheckBinary(linea[1])
            linea[1] = linea[1].replace("b","")
            pos3 = CheckHexa(linea[1])
            linea[1] = linea[1].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[1]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[0] == "A": # ADD A,(Dir)
                    Write(binary, line, linecounter,"0111111", ErrorCounter)
                if linea[0] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"1000000", ErrorCounter)

            else:
                ListOp.append("100000100000000")
                ListLine.append(line)

        else: #XOR -> ins basicas
            if len(linea) > 1:
                pos1 = linea[1].isnumeric()
                pos2 = CheckBinary(linea[1])
                linea[1] = linea[1].replace("b","")
                pos3 = CheckHexa(linea[1])
                linea[1] = linea[1].replace("#","")
                if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                    num = linea[1]
                    binary = ToBinary(num, pos2, pos1, pos3)
                    if linea[0] == "A":
                        Write(binary, line, linecounter,"0011010", ErrorCounter)
                    elif linea[0] == "B":
                        Write(binary, line, linecounter,"0011011", ErrorCounter)
                        
                else:
                    if linea[0] == "A":
                        ListOp.append("001100000000000")
                        ListLine.append(line)
                    elif linea[0] == "B":
                        ListOp.append("001100100000000")
                        ListLine.append(line)
                        
            else:
                    pos1 = list[1].isnumeric()
    else: #Ej ADD (Dir)
        linea[0] = linea[0].replace("(","")
        linea[0] = linea[0].replace(")","")
        num = linea[0]
        pos1 = linea[0].isnumeric()
        pos2 = CheckBinary(linea[0])
        linea[0] = linea[0].replace("b","")
        pos3 = CheckHexa(linea[0])
        linea[0] = linea[0].replace("#","")
        binary = ToBinary(num,pos2, pos1, pos3 )
        Write(binary, line, linecounter,"1000010", ErrorCounter)




def NOT(list, file):   
    linea = list1[1].split(",") # EJ A,B 
    if len(linea) > 1: #Ej NOT (Dir),A
        if "(" in linea[0]: # #EJ: ADD A,(Dir)
            linea[0] = linea[0].replace("(","")
            linea[0] = linea[0].replace(")","")
            pos1 = linea[0].isnumeric()
            pos2 = CheckBinary(linea[0])
            linea[0] = linea[0].replace("b","")
            pos3 = CheckHexa(linea[0])
            linea[0] = linea[0].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[0]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[1] == "A": #  (Dir),A
                    Write(binary, line, linecounter,"0111100", ErrorCounter)
                if linea[1] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"0111101", ErrorCounter)
                    

        else: #ADD -> ins basicas
            if linea[0] == "A" and linea[1] == "A":
                ListOp.append("001010000000000")
                ListLine.append(line)
            elif linea[0] == "A" and linea[1] == "B":
                ListOp.append("001010100000000")
                ListLine.append(line)
            elif linea[0] == "B" and linea[1] == "A":
                ListOp.append("001011000000000")
                ListLine.append(line)
            else:
                ListOp.append("001011100000000")
                ListLine.append(line)
                

    else: #Ej NOT (Dir)
        ListOp.append("0111110000000")
        ListLine.append(line)

def SHL(list, file):   
    linea = list1[1].split(",") # EJ A,B 
    if len(linea) > 1: #Ej NOT (Dir),A
        if "(" in linea[0]: # #EJ: ADD A,(Dir)
            linea[0] = linea[0].replace("(","")
            linea[0] = linea[0].replace(")","")
            pos1 = linea[0].isnumeric()
            pos2 = CheckBinary(linea[0])
            linea[0] = linea[0].replace("b","")
            pos3 = CheckHexa(linea[0])
            linea[0] = linea[0].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[0]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[1] == "A": #  (Dir),A
                    Write(binary, line, linecounter,"1000011", ErrorCounter)
                if linea[1] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"1000100", ErrorCounter)


        else: #ADD -> ins basicas
            if linea[0] == "A" and linea[1] == "A":
                ListOp.append("001110000000000")
                ListLine.append(line) 
            elif linea[0] == "A" and linea[1] == "B":
                ListOp.append("001110100000000")
                ListLine.append(line) 
            elif linea[0] == "B" and linea[1] == "A":
                ListOp.append("001111000000000")
                ListLine.append(line)
            else:
                ListOp.append("001111100000000")
                ListLine.append(line)
                

    else: #Ej NOT (Dir)
        ListOp.append("100010100000000")
        ListLine.append(line)

def SHR(list, file):   
    linea = list1[1].split(",") # EJ A,B 
    if len(linea) > 1: #Ej NOT (Dir),A
        if "(" in linea[0]: # #EJ: ADD A,(Dir)
            linea[0] = linea[0].replace("(","")
            linea[0] = linea[0].replace(")","")
            pos1 = linea[0].isnumeric()
            pos2 = CheckBinary(linea[0])
            linea[0] = linea[0].replace("b","")
            pos3 = CheckHexa(linea[0])
            linea[0] = linea[0].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[0]
                binary = ToBinary(num, pos2, pos1, pos3)
                if linea[1] == "A": #  (Dir),A
                    Write(binary, line, linecounter,"1000110", ErrorCounter)

                if linea[1] == "B": # ADD B,(Dir)
                    Write(binary, line, linecounter,"1000111", ErrorCounter)


        else: #ADD -> ins basicas
            if linea[0] == "A" and linea[1] == "A":
                ListOp.append("010000000000000")
                ListLine.append(line)
            elif linea[0] == "A" and linea[1] == "B":
                ListOp.append("010000100000000")
                ListLine.append(line)
            elif linea[0] == "B" and linea[1] == "A":
                ListOp.append("010001000000000")
                ListLine.append(line)    
            else:
                ListOp.append("010001100000000")
                ListLine.append(line)   

    else: #Ej NOT (Dir)
        ListOp.append("100100000000000")
        ListLine.append(line) 


def INC(list, file):   
    linea = list1[1].split(",") # EJ A,B
    if "(" in linea[0]: # #EJ: ADD A,(Dir)
            linea[0] = linea[0].replace("(","")
            linea[0] = linea[0].replace(")","")
            pos1 = linea[0].isnumeric()
            pos2 = CheckBinary(linea[0])
            linea[0] = linea[0].replace("b","")
            pos3 = CheckHexa(linea[0])
            linea[0] = linea[0].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[0]
                binary = ToBinary(num, pos2, pos1, pos3)
                Write(binary, line, linecounter,"1001001", ErrorCounter)

            else:
                ListOp.append("100101000000000")
                ListLine.append(line)
    #INC -> ins basicas
    else:
        ListOp.append("010010000000000")
        ListLine.append(line)
            
def RST(list, file):   
    linea = list1[1].split(",") # EJ A,B 
    if "(" in linea[0]: # #EJ: ADD A,(Dir)
            linea[0] = linea[0].replace("(","")
            linea[0] = linea[0].replace(")","")
            pos1 = linea[0].isnumeric()
            pos2 = CheckBinary(linea[0])
            linea[0] = linea[0].replace("b","")
            pos3 = CheckHexa(linea[0])
            linea[0] = linea[0].replace("#","")
            if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
                num = linea[0]
                binary = ToBinary(num, pos2, pos1, pos3)
                Write(binary, line, linecounter,"1001011", ErrorCounter)
            else:
                ListOp.append("100110000000000")
                ListLine.append(line)
                

def CMP(list, file):
    linea = list1[1].split(",") # EJ A,B
    if "(" in linea[1]: #Ej CMP A,(Dir)
        linea[1] = linea[1].replace("(","")
        linea[1] = linea[1].replace(")","")
        pos1 = linea[1].isnumeric()
        pos2 = CheckBinary(linea[1])
        linea[0] = linea[0].replace("b","")
        pos3 = CheckHexa(linea[1])
        linea[1] = linea[1].replace("#","")
        if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
            num = linea[1]
            binary = ToBinary(num, pos2, pos1, pos3)
            if linea[0] == "A":
                Write(binary, line, linecounter,"1010000", ErrorCounter)
            else:
                Write(binary, line, linecounter,"1010001", ErrorCounter)
                
        else: #CMP A,(B)
            ListOp.append("101001000000000")
            ListLine.append(line)

    else:
        pos1 = linea[1].isnumeric()
        pos2 = CheckBinary(linea[1])
        linea[1] = linea[1].replace("b","")
        pos3 = CheckHexa(linea[1])
        linea[1] = linea[1].replace("#","")
        if pos1 == True or pos2 == True or pos3 == True: #Ej CMP A,Lit
            num = linea[1]
            binary = ToBinary(num, pos2, pos1, pos3)
            if linea[0] == "A":
                Write(binary, line, linecounter,"1001110", ErrorCounter)

            else:
                Write(binary, line, linecounter,"1001111", ErrorCounter)
        else: #CMP A,B
            ListOp.append("100110100000000")
            ListLine.append(line)


def JMP(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1010011", ErrorCounter)

def JEQ(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1010100", ErrorCounter)



def JNE(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1010101", ErrorCounter)

def JGT(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1010110", ErrorCounter)


def JLT(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1010111", ErrorCounter)


def JGE(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1011000", ErrorCounter)

def JLE(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1011001", ErrorCounter)


def JCR(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    linea = linea.replace("b","")
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1011010", ErrorCounter)


def JOV(list, file):
    linea = list1[1] # EJ Dir
    pos1 = linea.isnumeric()
    pos2 = CheckBinary(linea)
    pos3 = CheckHexa(linea)
    linea = linea.replace("#","")
    if pos1 == True or pos2 == True or pos3 == True: #Ej INC (Dir)
        num = linea
        binary = ToBinary(num, pos2, pos1, pos3)
        Write(binary, line, linecounter,"1011011", ErrorCounter)

entry = open("test.ass", "r")
#entry = open("p3_2-correccion1.ass", "r")
salida = open("salida.out", "w")
entrada = entry.readlines()

lenfile = len(entrada)
i = 0

ListaMaxima = []
for r in entrada:
    r = r.replace("\n","")
    ListaMaxima.append(r)

Revisar = revisar(ListaMaxima, Exp)

linecounter = 0
ErrorCounter = []
ListOp = []
ListLine = []
while i <lenfile:
    RealLine = []
    line = entrada[i].strip() #linea de entrada
    list1 = line.split(" ")
    x = list1[1]
    #print("list1 " , list1)
    y = len(list1)
    if Revisar == True:
        if len(x) > 1:
            RealLine.append(list1[0]) #MOV
            RealLine.append(x[0]) 
            RealLine.append(x[1])
        else:
            RealLine.append(list1[0])
            RealLine.append(x[0])
            #print(RealLine)

        if RealLine[0] == "MOV":
            MOV(RealLine, salida)
        elif RealLine[0] == "ADD":
            ADD(RealLine, salida)
        elif RealLine[0] == "SUB":
            SUB(RealLine, salida) 
        elif RealLine[0] == "AND":
            AND(RealLine, salida)    
        elif RealLine[0] == "OR":    
            OR(RealLine, salida)  
        elif RealLine[0] == "XOR":     
            XOR(RealLine, salida)    
        elif RealLine[0] == "NOT":     
            NOT(RealLine, salida)       
        elif RealLine[0] == "SHL":     
            SHL(RealLine, salida)         
        elif RealLine[0] == "SHR":     
            SHR(RealLine, salida)         
        elif RealLine[0] == "INC":     
            INC(RealLine, salida)
        elif RealLine[0] == "RST":     
            RST(RealLine, salida)
        elif RealLine[0] == "CMP":     
            CMP(RealLine, salida)
        elif RealLine[0] == "JMP":     
            JMP(RealLine, salida)
        elif RealLine[0] == "JEQ":     
            JEQ(RealLine, salida)
        elif RealLine[0] == "JNE":     
            JNE(RealLine, salida)
        elif RealLine[0] == "JGT":     
            JGT(RealLine, salida)
        elif RealLine[0] == "JLT":     
            JLT(RealLine, salida)
        elif RealLine[0] == "JGE":     
            JGE(RealLine, salida)
        elif RealLine[0] == "JLE":     
            JLE(RealLine, salida)
        elif RealLine[0] == "JCR":     
            JCR(RealLine, salida)
        elif RealLine[0] == "JOV":     
            JOV(RealLine, salida)

    else:
        pass   

    linecounter+=1
    i+=1


if ErrorCounter.count("1") == 0:
    for i in range(len(ListLine)):
        salida.write(ListLine[i] + "\n")
        salida.write(ListOp[i]+ "\n")


print("Errorcounter", ErrorCounter)

entry.close()
salida.close()