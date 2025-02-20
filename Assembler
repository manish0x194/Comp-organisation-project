ABI_encoding = {"zero": 0,"ra": 1,"sp": 2,"gp": 3,"tp": 4,"t0": 5,"t1": 6,"t2": 7,"s0": 8,"fp": 8,"s1": 9,"a0": 10,
    "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15, "a6": 16, "a7": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21,
    "s6": 22,"s7": 23,"s8": 24,"s9": 25,"s10": 26,"s11": 27,"t3": 28,"t4": 29,"t5": 30,"t6": 31
}

riscv_opcodes = {
    'lw': '0000011',     
    'sw': '0100011',  
       
    'addi': '0010011',   
    'jalr': '1100111',   
    'jal': '1101111',  

    'beq': '1100011',   
    'bne': '1100011',    
    'blt': '1100011',   

    'add': '0110011',    
    'sub': '0110011',    
    'slt': '0110011',    
    'srl': '0110011',   
    'or': '0110011',     
    'and': '0110011',    
    'xor': '0110011'     
}

riscv_funct3 = {
    'lw': '010',   
    'sw': '010',  

    'addi': '000', 
    'jalr': '000', 

    'beq': '000',  
    'bne': '001',  
    'blt': '100',  

    'add': '000',  
    'sub': '000',  
    'slt': '010',  
    'srl': '101', 
    'or': '110',   
    'and': '111',  
    'xor': '100'   
}

riscv_funct7 = {
    'add': '0000000',  
    'sub': '0100000',  
    'slt': '0000000',  
    'srl': '0000000',  
    'or': '0000000',  
    'and': '0000000',  
    'xor': '0000000'  
}

def decimal_to_binary(n,type):
   
    if n >=0 :
        if n == 0:
            return "0"*5 if type == 'R' else '0'*12
        
        binary = ""

        while n > 0:
            remainder = n % 2  
            binary = str(remainder) + binary 
            n //= 2  
        
        if type == 'I' or type =='B':
            binary = "0"*(12-len(binary)) + binary
        elif type == 'R':
            binary = "0"*(5-len(binary)) + binary

        
        
        return binary
    else :
        return twos_complement(n)

def dec_to_binJB(n,type):
    # both j and B have one bit right shift thing which doubles their memory 
    n = n//2
    binary = ''
    if n < 0:
        if type == 'J':
            if n < (-2**20):
                return 'overflow'
            return twos_complement(n,20)
        else:
            if n < (-2**13):
                return 'overflow'
            return twos_complement(n)
    elif n>=0 :
        if type == 'J':
            if n == 0:
                return '0'*20 
            elif n > 2**20 - 1:
                return 'overflow'
        elif type == 'B':
            if n == 0:
                return '0'*12
            elif n > 2**13 - 1:
                return 'overflow'
        
        while n > 0:
            remainder = n % 2  
            binary = str(remainder) + binary 
            n //= 2  
        if type == 'J':
            binary = "0"*(20-len(binary)) + binary
        else:
            binary = "0"*(12-len(binary)) + binary
        return binary
        
def twos_complement(value, bit_width=12):

    twos_comp_value = (1 << bit_width) + value  

    return format(twos_comp_value, f'0{bit_width}b')
def I_type_instruction(instruction):
    if instruction[0].strip() == 'lw' :
        opcode = str(riscv_opcodes['lw'])
        func3 = str(riscv_funct3['lw'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction = instruction.split(',')
        rd = str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        instruction = instruction[1]
        y= instruction.index('(')
        rs1= str(decimal_to_binary(ABI_encoding[instruction[y+1:-1]],'R'))
        imm= str(decimal_to_binary(int(instruction[0:y]),'I'))
        output = imm + rs1 + func3 + rd  + opcode 
        return output
    
    elif instruction[0].strip() =='addi':
        opcode = str(riscv_opcodes['addi'])
        func3 = str(riscv_funct3['addi'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd = str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1 = str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        imm= str(decimal_to_binary(int(instruction[2]),'I'))
        output = imm + rs1 + func3 + rd  + opcode 
        return output
    
    elif instruction[0].strip()=='jalr' :
        opcode = str(riscv_opcodes['jalr'])
        func3 = str(riscv_funct3['jalr'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd = str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1 = str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        imm= str(decimal_to_binary(int(instruction[2]),'I'))
        output = imm + rs1 + func3 + rd  + opcode 
        return output
def R_type_instruction(instruction):
    if instruction[0].strip()=='add':
        opcode = str(riscv_opcodes['add'])
        func3 = str(riscv_funct3['add'])
        func7 = str(riscv_funct7['add'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd= str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1= str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        rs2= str(decimal_to_binary(ABI_encoding[instruction[2]],'R'))
        output = func7 + rs2 +  rs1 + func3 + rd +  opcode
        return output

    
    elif instruction[0].strip()=='sub':
        opcode = str(riscv_opcodes['sub'])
        func3 = str(riscv_funct3['sub'])
        func7 = str(riscv_funct7['sub'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd= str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1= str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        rs2= str(decimal_to_binary(ABI_encoding[instruction[2]],'R'))
        output = func7 + rs2 +  rs1 + func3 + rd +  opcode
        return output

    elif instruction[0].strip()=='slt':
        opcode = str(riscv_opcodes['slt'])
        func3 = str(riscv_funct3['slt'])
        func7 = str(riscv_funct7['slt'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd= str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1= str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        rs2= str(decimal_to_binary(ABI_encoding[instruction[2]],'R'))
        output = func7 + rs2 +  rs1 + func3 + rd +  opcode
        return output

    elif instruction[0].strip()=='srl':
        opcode = str(riscv_opcodes['srl'])
        func3 = str(riscv_funct3['srl'])
        func7 = str(riscv_funct7['srl'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd= str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1= str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        rs2= str(decimal_to_binary(ABI_encoding[instruction[2]],'R'))
        output = func7 + rs2 +  rs1 + func3 + rd +  opcode
        return output

    elif instruction[0].strip()=='or':
        opcode = str(riscv_opcodes['or'])
        func3 = str(riscv_funct3['or'])
        func7 = str(riscv_funct7['or'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd= str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1= str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        rs2= str(decimal_to_binary(ABI_encoding[instruction[2]],'R'))
        output = func7 + rs2 +  rs1 + func3 + rd +  opcode
        return output

    elif instruction[0].strip()=='and':
        opcode = str(riscv_opcodes['and'])
        func3 = str(riscv_funct3['and'])
        func7 = str(riscv_funct7['and'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd= str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1= str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        rs2= str(decimal_to_binary(ABI_encoding[instruction[2]],'R'))
        output = func7 + rs2 +  rs1 + func3 + rd +  opcode
        return output


    elif instruction[0].strip()=='xor':
        opcode = str(riscv_opcodes['xor'])
        func3 = str(riscv_funct3['xor'])
        func7 = str(riscv_funct7['xor'])
        instruction = instruction[1]
        instruction= instruction.replace(' ','')
        instruction= instruction.split(',')
        rd= str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
        rs1= str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
        rs2= str(decimal_to_binary(ABI_encoding[instruction[2]],'R'))
        output = func7 + rs2 +  rs1 + func3 + rd +  opcode
        return output


def S_type_instruction(instruction):
    opcode = str(riscv_opcodes['sw'])
    func3 = str(riscv_funct3['sw'])
    instruction = instruction[1]
    instruction= instruction.replace(' ','')
    instruction = instruction.split(',')
    rs2 = str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
    instruction = instruction[1]
    y= instruction.index('(')
    try:
        rs1= str(decimal_to_binary(ABI_encoding[instruction[y+1:-1]],'R'))
    except:
        return "error"

    imm= str(decimal_to_binary(int(instruction[0:y]),'I'))
    output = imm[0:7] + rs2 + rs1 + func3 + imm[7:12] + opcode 
    return output


def J_type_instruction(instruction):
    instruction = instruction[1]
    instruction = instruction.replace(' ','')
    instruction = instruction.split(',') 
    rd = str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
    opcode = str(riscv_opcodes['jal'])

    imm = str(dec_to_binJB(int(instruction[1]),'J'))

    
    complete = imm[0] + imm[10:20] + imm[9] + imm[1:9] + rd + opcode
    return complete
def B_type_instruction(instruction):
    #print(instruction)
    k = instruction[0].strip()
   # print(instruction)
    instruction = instruction[1]
    # print(instruction)
    # instruction = instruction.replace(' ','')
    instruction = instruction.split(',')
    # print(instruction)
    rs1 = str(decimal_to_binary(ABI_encoding[instruction[0]],'R'))
    rs2 =  str(decimal_to_binary(ABI_encoding[instruction[1]],'R'))
  
    imm = str(dec_to_binJB(int(instruction[2]),'B'))
    
    funct3 = ''
    if k == 'beq':
        funct3 = riscv_funct3['beq']
    elif k == 'bne':
        funct3 = riscv_funct3['bne']
    else:
        funct3 = riscv_funct3['blt']
    opcode= '1100011'
    complete = imm[0] + imm[2:8] + rs2 + rs1 + funct3+ imm[8:] + imm[1] +opcode
    return complete
def main(input_filepath,output_filepath):
    # a file.seek(0) need to be implemented at start of this functionn get no. of lines prresent then initialize a list of binary_list = [0]*length thiss willl work
    file_length = 0
    with open("testcase.txt","r") as fo:
        for line in fo:
            if line.strip() != '':
                file_length += 1
    binary_list=[0]*(file_length)
    
    f= open("testcase.txt",'r')
    instructions = f.readlines()
    count = 0
    pc_count = 0
    PC = {}
    label_list = {}
   
    front_label_list = {}
    for instruction in instructions:
        instruction = instruction.strip()
        if instruction=='':
            continue
        
        PC[count] = pc_count

        front_label_flag = 0
        label_flag = 1
        if ':' in instruction:
            front_label_flag = 1
            instruction = instruction.split(':')
            label = instruction[0]
            front_label_list[label] = [count,pc_count]
            instruction[1]=instruction[1].strip()
            instruction1 = instruction[1].split(' ')
            #print(instruction1)
            instruction[1] = instruction[1].split(' ') 
            instruction = instruction[1]
            if_label = instruction[1].split(',')[-1]
            if instruction1[0] in ['add','sub','slt','srl','or','and','xor','sw','lw']:
                label_flag = 0
            else:
                try:
                    if_label = int(if_label)
                    label_flag = 0
                except ValueError:
                    label_flag = 1
                    label_list[count] = [if_label,instruction1]

        else:
            instruction1 = instruction.split(' ',1)
            instruction = instruction.split(' ',1)
            if_label = instruction[1].split(',')[-1]
            if instruction1[0] in ['add','sub','slt','srl','or','and','xor','sw','lw']:
                label_flag = 0
            else:
                try:
                    if_label = int(if_label)
                    label_flag = 0
                except ValueError:
                    label_flag = 1
                    label_list[count] = [if_label,instruction1]
        buffer = 0
        if label_flag == 0:
            if instruction[0].strip() in ['lw','addi','jalr']:
                k = I_type_instruction(instruction1)
                
            elif instruction[0].strip() == 'sw':
                k=S_type_instruction(instruction1)
                
            elif instruction[0].strip() in ['beq','bne','blt']:
                k=B_type_instruction(instruction1)
            elif instruction[0].strip() == 'jal':
                k=J_type_instruction(instruction1)

            elif instruction[0].strip() in ['add','sub','slt','srl','or','and','xor']:
                k=R_type_instruction(instruction1)
            binary_list[count] = k
        count += 1
        pc_count += 4
        
    
    f.seek(0)
    count1 = 0
    
    for line in f:
        line.strip()
        if ':' in line:
            curr_addr = PC[count1]
            
            line = line.split(':')
            label = line[0]
            line[1]=line[1].strip()
            line[1] = line[1].split(' ')
            instr = line[1]
            instr[1] = instr[1].split(',')
            instr = instr[0:1] + instr[1]
            line.pop(1)
            line+=instr
       
            
            for key,j in label_list.items():
                if j[0] == line[0]:
                    abs_addr = PC[key]
                

                    immFound = curr_addr - abs_addr
                    
                    label_mani = j[1][1].split(',')
                    label_mani[-1] = str(immFound)

                    label_mani=','.join(label_mani)
                    j = [j[1][0]] + [label_mani]


                    #now feed this in k type j
                    bin_fetched = ''
                    if j[0].strip() in ['lw','addi','jalr']:
                        bin_fetched=I_type_instruction(j)
                    elif j[0].strip() == 'sw':
                        bin_fetched=S_type_instruction(j)
                    elif j[0].strip() in ['beq','bne','blt']:
                        bin_fetched=B_type_instruction(j)
                    elif j[0].strip() == 'jal':
                
                        bin_fetched=J_type_instruction(j)
                    elif j[0].strip() in ['add','sub','slt','srl','or','and','xor']:
                        bin_fetched=R_type_instruction(j)
                    binary_list[key]=bin_fetched
            
            try:
                if_label2 = int(line[-1])
                for key,j in label_list.items():
                    if j[0] == line[0]:
                        abs_addr = PC[key]
                  

                        immFound = curr_addr - abs_addr
                        
                        label_mani = j[1][1].split(',')
                        label_mani[-1] = str(immFound)

                        label_mani=','.join(label_mani)
                        j = [j[1][0]] + [label_mani]


                        #now feed this in k type j
                        bin_fetched = ''
                        if j[0].strip() in ['lw','addi','jalr']:
                            bin_fetched=I_type_instruction(j)
                        elif j[0].strip() == 'sw':
                            bin_fetched=S_type_instruction(j)
                        elif j[0].strip() in ['beq','bne','blt']:
                            bin_fetched=B_type_instruction(j)
                        elif j[0].strip() == 'jal':
                    
                            bin_fetched=J_type_instruction(j)
                        elif j[0].strip() in ['add','sub','slt','srl','or','and','xor']:
                            bin_fetched=R_type_instruction(j)
                        binary_list[key] = bin_fetched
            except ValueError:
                if_label2 = line[-1]
                key1 = 0
                abs_addr = 0
                if line[1] in ['add','sub','slt','srl','or','and','xor','sw','lw']:
                    buffer = 0
                else:
                    for key,j in front_label_list.items():
                        abs_addr = front_label_list[if_label2][1]
                        key1 = j[0]
                    imm_found = abs_addr - curr_addr
                    line[-1] = str(imm_found)
                    line = line[1:]
                    k=','.join(line[2:])
                    line = [line[1]]
                    line += k
                    j = line
                    bin_fetched = ''
                    if j[0].strip() in ['lw','addi','jalr']:
                        bin_fetched=I_type_instruction(j)
                    elif j[0].strip() == 'sw':
                        bin_fetched=S_type_instruction(j)
                    elif j[0].strip() in ['beq','bne','blt']:
                        bin_fetched=B_type_instruction(j)
                    elif j[0].strip() == 'jal':
        
                        bin_fetched=J_type_instruction(j)
                    elif j[0].strip() in ['add','sub','slt','srl','or','and','xor']:
                        bin_fetched=R_type_instruction(j)
          

        count1 +=1
    for i in binary_list:
        print(i)

    f.close()

main('testcase.txt','testpageQ3.txt')
