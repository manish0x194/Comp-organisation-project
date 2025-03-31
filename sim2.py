def decimal_to_hex(num):
    return hex(num)[2:].upper().zfill(8)

def binary_to_decimal(binary_str):
    decimal = 0
    length = len(binary_str)
    for i in range(0, length):
        decimal += 2**i * int(binary_str[length - i - 1])
    return decimal

def binary_to_decimal_2(binary_str):
    decimal = 0
    length = len(binary_str)
    if binary_str[0] == '0':
        for i in range(0, length):
            decimal += 2**i * int(binary_str[length - i - 1])
        return decimal
    else:
        return int(binary_str, 2) - (1 << length)

def twos_complement(value, bit_width):
    twos_comp_value = (1 << bit_width) + value
    return format(twos_comp_value, f'0{bit_width}b')

def decimal_to_binary(num, bits):
    binary = ''
    if num == 0:
        return '0' * bits
    elif num > 0:
        while num > 0:
            binary = str(num % 2) + binary
            num = num // 2

        binary = (bits - len(binary)) * '0' + binary
        return binary
    else:
        return twos_complement(num, bits)


def R_type_instruction(instruction):
    global pc
    func7 = instruction[0:7]
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    func3 = instruction[17:20]
    rd = instruction[20:25]
    pc += 4

    def add_instruction(rs1, rs2, rd):
        rv[binary_to_decimal(rd)] = rv[binary_to_decimal(rs1)] + rv[binary_to_decimal(rs2)]

    def sub_instruction(rs1, rs2, rd):
        difference = rv[binary_to_decimal(rs1)] - rv[binary_to_decimal(rs2)]
        rv[binary_to_decimal(rd)] = difference if difference >= 0 else 2**32 + difference

    def slt_instruction(rs1, rs2, rd):
        rv[binary_to_decimal(rd)] = 1 if rv[binary_to_decimal(rs1)] < rv[binary_to_decimal(rs2)] else 0

    def sll_instruction(rs1, rs2, rd):
        shift = binary_to_decimal(decimal_to_binary(rv[binary_to_decimal(rs2)], 32)[-5:])
        y = decimal_to_binary(rv[binary_to_decimal(rs1)], 32)
        rv[binary_to_decimal(rd)] = binary_to_decimal_2(y[shift:] + '0' * shift)

    def srl_instruction(rs1, rs2, rd):
        shift = binary_to_decimal(decimal_to_binary(rv[binary_to_decimal(rs2)], 32)[-5:])
        if shift == 0:
            rv[binary_to_decimal(rd)] = rv[binary_to_decimal(rs1)]
        else:
            y = decimal_to_binary(rv[binary_to_decimal(rs1)], 32)
            rv[binary_to_decimal(rd)] = binary_to_decimal_2('0' * shift + y[0:-shift])

    def or_instruction(rs1, rs2, rd):
        rv[binary_to_decimal(rd)] = rv[binary_to_decimal(rs1)] | rv[binary_to_decimal(rs2)]

    def and_instruction(rs1, rs2, rd):
        rv[binary_to_decimal(rd)] = rv[binary_to_decimal(rs1)] & rv[binary_to_decimal(rs2)]

    def xor_instruction(rs1, rs2, rd):
        rv[binary_to_decimal(rd)] = rv[binary_to_decimal(rs1)] ^ rv[binary_to_decimal(rs2)]

    if func3 == '010':
        slt_instruction(rs1, rs2, rd)
    elif func3 == '101':
        srl_instruction(rs1, rs2, rd)
    elif func3 == '001':
        sll_instruction(rs1, rs2, rd)
    elif func3 == '110':
        or_instruction(rs1, rs2, rd)
    elif func3 == '111':
        and_instruction(rs1, rs2, rd)
    elif func3 == '000' and func7 == '0000000':
        add_instruction(rs1, rs2, rd)
    elif func3 == '000' and func7 == '0100000':
        sub_instruction(rs1, rs2, rd)
    elif func3 == '100':
        xor_instruction(rs1, rs2, rd)
    else:
        return "invalid func3"


def S_type_instruction(instruction):
    global pc
    imm = instruction[0:7] + instruction[20:25]
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    pc += 4

    def store_instruction(rs1, rs2, imm):
        memory_address = decimal_to_hex(binary_to_decimal(imm) + rv[binary_to_decimal(rs1)])
        if memory_address in mv:
            mv[memory_address] = rv[binary_to_decimal(rs2)]
        else:
            return "out of memory"

    store_instruction(rs1, rs2, imm)


def I_type_instruction(instruction):
    imm = instruction[0:12]
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    opcode = instruction[25:32]
    func3 = instruction[17:20]

    def addi_instruction(rs1, rd, imm):
        global pc
        rv[binary_to_decimal(rd)] = rv[binary_to_decimal(rs1)] + binary_to_decimal_2(imm)
        pc += 4

    def jalr_instrcution(rs1, rd, imm):
        global pc
        pc = binary_to_decimal_2(imm) + rv[binary_to_decimal(rs1)]
        rv[binary_to_decimal(rd)] = pc + 4

    def load_instruction(rs1, rd, imm):
        global pc
        memory_address = decimal_to_hex(binary_to_decimal_2(imm) + rv[binary_to_decimal(rs1)])
        pc += 4
        if memory_address in mv:
            rv[binary_to_decimal(rd)] = mv[memory_address]
        else:
            return "out of memory"

    def sltiu_instruction(rs1, rd, imm):
        pass

    if opcode == '1100111':
        jalr_instrcution(rs1, rd, imm)

    elif opcode == '0000011':
        load_instruction(rs1, rd, imm)

    elif opcode == '0010011' and func3 == '000':
        addi_instruction(rs1, rd, imm)

    elif opcode == '0010011' and func3 == '011':
        sltiu_instruction(rs1, rd, imm)


def J_type_instruction(instruction):
    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11]
    rd = instruction[20:25]

    def jal_instruction(imm, rd):
        global pc
        rv[binary_to_decimal(rd)] = pc + 4
        pc = pc + binary_to_decimal_2(imm + '0')

    jal_instruction(imm, rd)


def B_type_instruction(instruction):
    imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24]
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    func3 = instruction[17:20]

    def beq_instruction(rs1, rs2, imm):
        global pc
        if rv[binary_to_decimal(rs1)] == rv[binary_to_decimal(rs2)]:
            pc += binary_to_decimal_2(imm)

    def bne_instruction(rs1, rs2, imm):
        global pc
        if rv[binary_to_decimal(rs1)] != rv[binary_to_decimal(rs2)]:
            pc += binary_to_decimal_2(imm)

    def blt_instruction(rs1, rs2, imm):
        if rv[binary_to_decimal(rs1)] < rv[binary_to_decimal(rs2)]:
            pc += binary_to_decimal_2(imm)

    def bltu_instruction(rs1, rs2, imm):
        if rv[binary_to_decimal(rs1)] < rv[binary_to_decimal(rs2)]:
            pc += binary_to_decimal_2(imm)

    def bgeu_instruction(rs1, rs2, imm):
        if rv[binary_to_decimal(rs1)] >= rv[binary_to_decimal(rs2)]:
            pc += binary_to_decimal_2(imm)

    if func3 == '000':
        beq_instruction(rs1, rs2, imm)
    elif func3 == '001':
        bne_instruction(rs1, rs2, imm)
    elif func3 == '100':
        blt_instruction(rs1, rs2, imm)
    elif func3 == '110':
        bltu_instruction(rs1, rs2, imm)
    elif func3 == '111':
        bgeu_instruction(rs1, rs2, imm)


def decode_instruction(line):
    opcode = line[25:32]
    if opcode == '0110011':
        R_type_instruction(line)
    elif opcode in ['0000011', '0010011', '1100111']:
        I_type_instruction(line)
    elif opcode == '0100011':
        S_type_instruction(line)
    elif opcode == '1101111':
        J_type_instruction(line)
    elif opcode == '1100011':
        B_type_instruction(line)
    else:
        print("invalid opcode")


def main():
    f = open("input.txt", 'r')
    s = f.readlines()
    i = 1
    j = 1
    for line in s:
        line = line.strip()
        pcv[4 * (i - 1)] = line
        i += 1

    while pc in pcv:
        if pc == 'halt':
            break
        else:
            print(pc)
            decode_instruction(pcv[pc])
            rv[0] = 0
            print(j, ' :', rv)
            j += 1

    f.close()

main()

print(mv)
