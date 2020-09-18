"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [number for number in range(256)]
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.flag = 0b00000000 
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.ADD = 0b10100000
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.CMP = 0b10100111
        self.JEQ = 0b01010101
        self.JNE = 0b01010110
        self.JMP = 0b01010100
        self.JGE = 0b01011010
        self.JGT = 0b01010111
        self.JLE = 0b01011001
        self.JLT = 0b01011000
        self.AND = 0b10101000
        self.DEC = 0b01100110
        self.DIV = 0b10100011
        self.INC = 0b01100101
        self.INT = 0b01010010
        self.IRET = 0b00010011
        self.LD = 0b10000011
        self.NOP = 0b00000000
        self.NOT = 0b01101001
        self.OR = 0b10101010
        self.PRA = 0b01001000
        self.PRN = 0b01000111
        self.SHL = 0b10101100
        self.SHR = 0b10101101
        self.ST = 0b10000100
        self.SUB = 0b10100001
        self.XOR = 0b10101011
        self.MOD = 0b10100100
        self.program = [
            # Default program
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

    def ram_read(self,MAR):

        return self.ram[MAR]

    def ram_write(self, MAR, MDR):

        self.ram[MAR] = MDR

    def halt(self):

        sys.exit()

    def ldi(self,LDI,value):

        self.reg[LDI] = value

    def prn(self,value):

        print(self.reg[value])


    def load(self, program_route=None):
        """Load a program into memory."""

        address = 0

        if not program_route:

            program = self.program

        else:

            program = []

            with open(program_route) as f:

                for line in f:

                    if line[0].isdigit():

                        program.append(int(line[:8].split('#',1)[0],2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            else:
                self.flag = 0b00000010

        elif op == 'AND':

            self.reg[reg_a] = bin(self.reg[reg_a] & self.reg[reg_b])
        
        elif op == 'OR':

            self.reg[reg_a] = bin(self.reg[reg_a] | self.reg[reg_b])

        elif op == 'XOR':

            self.reg[reg_a] = bin(self.reg[reg_a] ^ self.reg[reg_b])

        elif op == 'NOT':

            self.reg[reg_a] = bin(~self.reg[reg_a])

        elif op == 'SHL':

            self.reg[reg_a] = bin(self.reg[reg_a] << self.reg[reg_b])    

        elif op == 'SHR':

            self.reg[reg_a] = bin(self.reg[reg_a] >> self.reg[reg_b])   

        elif op == 'MOD':

            if self.reg[reg_b] != 0:

                self.reg[reg_a] = bin(self.reg[reg_a] % self.reg[reg_b])

            else:

                raise Exception("You cannot divide by zero.")

        elif op == 'DEC':

            self.reg[reg_a] -= 0b00000001

        elif op == 'DIV':

            if self.reg[reg_b] != 0:

                self.reg[reg_a] = bin(self.reg[reg_a] / self.reg[reg_b])

            else:

                raise Exception("You cannot divide by zero.") 

        elif op == 'INC':

            self.reg[reg_a] += 0b00000001

        elif op == 'ST':

            self.reg[reg_a] = self.reg[reg_b]

        elif op == 'SUB':

            self.reg[reg_a] -= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def push_to_stack(self,value):

        # Decrement the SP

        self.reg[self.sp] -= 1 

        # Copy the register value into SP's location
        # Get the reg num to push

        # reg_num = self.ram[self.pc + 1]

        # # Get the value to push

        # value = self.reg[reg_num]

        # # Copy the value to the SP's location

        # top_of_the_stack = self.reg[self.sp]

        # self.ram_write(top_of_the_stack,value)
        
        # In one line:
        self.ram_write(self.reg[self.sp],value)

  

    def pop_from_stack(self):

        # Copy the value from SP's location to the register
        # Get the register number to pop into
        
        # reg_num = self.ram[self.pc +1]

        # # Get the top of the stack address

        # top_of_stack_addr = self.reg[self.sp]

        # # Get the value of the top of the stack

        # value = self.ram_read(top_of_stack_addr)

        # # Store the value into the register

        # self.reg[reg_num] = value

        # In fewer lines:

        # Increment the SP
        
        top_of_stack_addr = self.reg[self.sp]

        self.reg[self.sp] += 1

        return self.ram_read(top_of_stack_addr)


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        running = True

        while running:

            IR = self.ram_read(self.pc)

            if IR == self.LDI:

                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)

                self.ldi(operand_a,operand_b)

                self.pc += 3
           
            elif IR == self.PRN:

                operand_a = self.ram_read(self.pc + 1)
                self.prn(operand_a)

                self.pc += 2

            elif IR == self.HLT:

                self.halt()

            elif IR == self.ADD:

                self.alu('ADD',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.MUL:

                self.alu('MUL',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.PUSH:

                self.push_to_stack(self.reg[self.ram[self.pc + 1]])

                self.pc += 2

            elif IR == self.POP:

                self.reg[self.ram_read(self.pc +1)] = self.pop_from_stack()

                self.pc += 2

            elif IR == self.CALL:

                # Push to the stack the next instruction after call
                self.push_to_stack(self.pc + 2)

                # The PC is set to the address stored in the given register.
                self.pc = self.reg[self.ram_read(self.pc + 1)]

            elif IR == self.RET:

                # Pop the value from the top of the stack and store it in the PC.
                self.pc = self.pop_from_stack()              

            elif IR == self.CMP:

                self.alu('CMP',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.JEQ:

                if self.flag == 0b00000001:

                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                
                else:

                    self.pc += 2

            elif IR == self.JNE:

                if self.flag == 0b00000100 or self.flag == 0b00000010 or self.flag == 0b00000000:
                    
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                
                else:

                    self.pc += 2
           
            elif IR == self.JMP:

                self.pc = self.reg[self.ram_read(self.pc + 1)]

            elif IR == self.AND:

                self.alu('AND',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.OR:
                self.alu('OR',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.XOR:
                self.alu('XOR',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3
            
            elif IR == self.NOT:
                self.alu('NOT',self.ram_read(self.pc + 1),None)
                self.pc += 2

            elif IR == self.SHL:
                self.alu('SHL',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.SHR:
                self.alu('SHR',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            elif IR == self.MOD:
                self.alu('MOD',self.ram_read(self.pc + 1),self.ram_read(self.pc + 2))
                self.pc += 3

            else:

                print(f'Unknown instruction {IR}')
                
                self.pc += 1
                
        