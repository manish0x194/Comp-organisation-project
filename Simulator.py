import sys

ABI_encoding = {"zero": 0,"ra": 0,"sp": 380,"gp": 0,"tp": 0,"t0": 0,"t1": 0,"t2": 0,"s0": 0,"s1": 0,"a0": 0,
    "a1": 0, "a2": 0, "a3": 0, "a4": 0, "a5": 0, "a6": 0, "a7": 0, "s2": 0, "s3": 0, "s4": 0, "s5": 0,
    "s6": 0,"s7": 0,"s8": 0,"s9": 0,"s10": 0,"s11": 0,"t3": 0,"t4": 0,"t5": 0,"t6": 0
}
ABI_encoding_flipped = {0: "zero", 1: "ra", 2: "sp", 3: "gp", 4: "tp", 5: "t0", 6: "t1", 7: "t2", 8: "s0", 9: "s1",
    10: "a0", 11: "a1", 12: "a2", 13: "a3", 14: "a4", 15: "a5", 16: "a6", 17: "a7", 18: "s2", 19: "s3", 20: "s4",
    21: "s5", 22: "s6", 23: "s7", 24: "s8", 25: "s9", 26: "s10", 27: "s11", 28: "t3", 29: "t4", 30: "t5", 31: "t6"
}
def twos_complement_32bit(n: int) -> str:
    
    if not (-2**31 <= n < 2**31):  
        raise ValueError("Number out of 32-bit range!")

    return f"0b{n & 0xFFFFFFFF:032b}"
def twos_complement_to_decimal(binary_str):
    # Check if the binary number is negative (MSB = 1)
    if binary_str[0] == '1':
        # Find the two's complement by inverting the bits and adding 1
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        # Add 1 to the inverted binary string
        twos_complement = bin(int(inverted_binary, 2) + 1)[2:]
        # Convert to decimal and make it negative
        return -int(twos_complement, 2)
    else:
        # For positive binary numbers, just convert to decimal
        return int(binary_str, 2)

def decimal_to_hex(num):
    # Set the 4th byte (most significant byte) to '01' and keep the rest intact
    modified_num = (num & 0x00FFFFFF) | 0x00000000
    return '0x' + hex(modified_num)[2:].upper().zfill(8)

hex_dict = {
    '0x00010000': 0, '0x00010004': 0, '0x00010008': 0, '0x0001000C': 0, '0x00010010': 0, '0x00010014': 0, '0x00010018': 0, '0x0001001C': 0, 
    '0x00010020': 0, '0x00010024': 0, '0x00010028': 0, '0x0001002C': 0, '0x00010030': 0, '0x00010034': 0, '0x00010038': 0, '0x0001003C': 0, 
    '0x00010040': 0, '0x00010044': 0, '0x00010048': 0, '0x0001004C': 0, '0x00010050': 0, '0x00010054': 0, '0x00010058': 0, '0x0001005C': 0, 
    '0x00010060': 0, '0x00010064': 0, '0x00010068': 0, '0x0001006C': 0, '0x00010070': 0, '0x00010074': 0, '0x00010078': 0, '0x0001007C': 0
}
def binary_to_decimal(binary_str):
    decimal = 0
    length = len(binary_str)
    for i in range(0,length):
        decimal+= 2**i * int(binary_str[length-i-1])
    return decimal

def decimal_to_binary( num, bits):
    binary=''
    while num%2 >=0:
        binary += str(num%2)

    pass


def R_type_instruction(instruction,ABI_encoding,ABI_encoding_flipped):
    func7= instruction[0:7]
    rs2= instruction[7:12]
    rs1= instruction[12:17]
    func3= instruction[17:20]
    rd= instruction[20:25]

    def add_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped):
        rd = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]] + ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]]
        return rd

    def sub_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped):
        rd = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]] - ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]]
        return rd

    def slt_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped):
        if ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]] < ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]]:
            rd = 1
        else:
            rd = 0
        return rd

    def srl_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped):
        val = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]]
        last5 = bin(val)[2:]
        last5 = '00000' + last5
        last5 = last5[-5:]
        shift = binary_to_decimal(last5)
        return ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]]//(2**shift)


    def or_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped):
        rd = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]] | ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]]
        return rd

    def and_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped):
        rd = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]] & ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]]
        return rd
    k = 0
    if func3 =='010':
        k=slt_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped)
        
    elif func3 =='101':
        k=srl_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped)
    elif func3 =='110':
        k=or_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped)
    elif func3 =='111':
        k=and_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped)
    elif func3 == '000' and func7 =='0000000':
        k=add_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped)
    else :
        k=sub_instruction(rs1,rs2,rd,ABI_encoding,ABI_encoding_flipped)
    return k


def S_type_instruction(instruction,ABI_encoding,ABI_encoding_flipped):
    imm= instruction[0:7] + instruction[20:25]
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    return twos_complement_to_decimal(imm) + ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]]


def I_type_instruction(instruction,opcode,PC,ABI_encoding,ABI_encoding_flipped):
    imm = instruction[0:12]
    rs1 = instruction[12:17]
    fun3= instruction[17:20]
    rd = instruction[20:25]
    imm_new= 0
    if imm[0] == '1':
        imm_new = twos_complement_to_decimal(imm)
    else:
        imm_new=binary_to_decimal(imm)
    if opcode == '0000011':
        #print('here',binary_to_decimal(imm) , ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]])
        
        return binary_to_decimal(imm) + ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]]
    
    if opcode == '0010011': #addi
        #print('here',binary_to_decimal(imm) , ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]])
        return ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]] + imm_new
    elif opcode == '1100111':#jalr 
        return PC + 4

def J_type_instruction(instruction):
    imm =  instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11]
    rd = instruction[20:25]
    if imm[0] == '1':
        imm_new = twos_complement_to_decimal(imm)
    else:
        imm_new=binary_to_decimal(imm)
    #print(imm_new)
    return imm_new*2
# blt and bne yet to be implemented

def B_type_instruction(instruction,ABI_encoding,ABI_encoding_flipped): #bool
    imm = instruction[0]+instruction[24]+instruction[1:7] + instruction[20:24]
    rs2= instruction[7:12]
    rs1 = instruction[12:17]
    jump = twos_complement_to_decimal(imm)*2 
    func3 =  instruction[17:20]
    if func3 == '000':
        if ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]] == ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]]:
            k = 1
        else:
            k = 0
        return [jump,k]
    elif func3 == '001':
        if ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs2)]] != ABI_encoding[ABI_encoding_flipped[binary_to_decimal(rs1)]]:
            k = 1
        else:
            k = 0
        return [jump,k]
    






bin_list = []
input_file = sys.argv[1]
f= open(input_file,'r')
s= f.readlines()
for line in s:
    line = line.strip()
    bin_list.append(line)
f.close()

output_file = sys.argv[2]
of3 = sys.argv[3]

with open(output_file,'w+')as f1:
    f1.write('')


PC_prev=0
PC=0
while True: 
    
    ABI_encoding["zero"] = 0
    PC_prev = PC
    
    line = bin_list[PC//4]
    opcode = line[25:32] #12:17 0:12
    
    if opcode == '0110011':
        ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[20:25])]] = R_type_instruction(line,ABI_encoding,ABI_encoding_flipped)
        PC=PC+4
    elif opcode in ['0000011','0010011','1100111']:
        if opcode == '1100111':
            if ABI_encoding_flipped[binary_to_decimal(line[12:17])] == 'zero':
                PC = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[12:17])]] + binary_to_decimal(line[0:12])
                ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[20:25])]] = I_type_instruction(line,opcode,PC,ABI_encoding,ABI_encoding_flipped)
                
            else:
                ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[20:25])]] = I_type_instruction(line,opcode,PC,ABI_encoding,ABI_encoding_flipped)
                PC = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[12:17])]] + binary_to_decimal(line[0:12])
        elif opcode == '0010011':
            ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[20:25])]] = I_type_instruction(line,opcode,PC,ABI_encoding,ABI_encoding_flipped)
            PC = PC + 4
            #print(ABI_encoding["sp"])
        elif opcode == '0000011':
            try:
                #print(I_type_instruction(line,opcode,PC,ABI_encoding,ABI_encoding_flipped))
                ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[20:25])]] = hex_dict[decimal_to_hex(I_type_instruction(line,opcode,PC,ABI_encoding,ABI_encoding_flipped))]
                PC = PC + 4
            except KeyError:
                PC=PC+4
    elif opcode == '0100011':
        #print(S_type_instruction(line,ABI_encoding,ABI_encoding_flipped),'here')
        try:
            #if 65536 <= S_type_instruction(line,ABI_encoding,ABI_encoding_flipped) <= 65536 + 124: 
            hex_dict[decimal_to_hex(S_type_instruction(line,ABI_encoding,ABI_encoding_flipped))] = ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[7:12])]]
            #print(decimal_to_hex(S_type_instruction(line,ABI_encoding,ABI_encoding_flipped)))
            #print(PC)
            PC = PC + 4
        except KeyError:
            PC = PC + 4
    elif opcode =='1101111':
        ABI_encoding[ABI_encoding_flipped[binary_to_decimal(line[20:25])]] = PC + 4
        org = PC
        PC += J_type_instruction(line)
        if PC%4 != 0:
            PC = org + 4
    elif opcode == '1100011':
        z = B_type_instruction(line,ABI_encoding,ABI_encoding_flipped) 
        if z[1] == 1:
            PC = PC + z[0]
        else:
            PC = PC + 4
    else :
        print("invalid opcode")
    buffer = 0
    #output_file = sys.argv[-1]
    ABI_encoding["zero"] = 0 #i forgot resetting zero register
    with open(output_file, 'a') as file1:
        file1.write(twos_complement_32bit(PC)+ ' ')
        for i,j in ABI_encoding.items():
            file1.write(twos_complement_32bit(j)+' ')
        
        file1.write('\n')
    if PC == PC_prev:
        break


with open(output_file, 'a') as file1:
    count = 0
    for i,j in hex_dict.items():
        count +=1
        file1.write(f"{i}:{twos_complement_32bit(j)}\n")
        if count == 32:
            break
# print(ABI_encoding)
# print(hex_dict)



    
    
