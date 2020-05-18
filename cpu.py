"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8 
        self.pc = 0
        self.running = False
        self.sp = 7
        self.equal = 0
        self.less_than = 0
        self.greater_than = 0
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.ADD = 0b10100000

        self.CMP = 0b10100111 
        self.JMP = 0b01010100
        self.JNE = 0b01010110
        self.JEQ = 0b01010101

    

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print("Need proper file name passed")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                container = []
                for line in f:

                    comment_split = line.split("#")

                    num = comment_split[0].strip()

                    if num == '':
                        continue
                    container.append(num)
                    program = [int(c, 2) for c in container]

        except FileNotFoundError:
            print(f"{sys.argv[0]}! {sys.argv[1]} not found")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1 


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.load()
        self.run_start()
        
        while self.running:

            command = self.ram_read(self.pc)

            if command == self.HLT:
                self.run_HLT()

            elif command == self.LDI:
                self.run_LDI()

            elif command == self.PRN:
                self.run_PRN()

            elif command == self.MUL:
                self.run_MUL()

            elif command == self.PUSH:
                self.run_PUSH()

            elif command == self.POP:
                self.run_POP()
  
            elif command == self.CALL:
                self.run_CALL()

            elif command == self.RET:
                self.run_RET()

            elif command == self.ADD:
                self.run_ADD()
     
            elif command == self.CMP:
                self.run_CMP()

            elif command == self.JMP:
                self.run_JMP()

            elif command == self.JEQ:
                self.run_JEQ()

            elif command == self.JNE:
                self.run_JNE()


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return

    def run_start(self):
        self.running = True

    def run_HLT(self):
        self.running = False
        self.pc = 0

    def run_LDI(self):
        self.register[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        self.pc += 3

    def run_PRN(self):
        print(self.register[self.ram_read(self.pc+1)])
        self.pc += 2

    def run_MUL(self):
        self.register[self.ram_read(self.pc+1)] = self.register[
            self.ram_read(self.pc+1)] * self.register[self.ram_read(self.pc+2)]
        self.pc += 3

    def run_PUSH(self):
        reg = self.ram[self.pc + 1]
        val = self.register[reg]
        self.register[self.sp] -= 1
        self.ram[self.register[self.sp]] = val
        self.pc += 2

    def run_POP(self):
        reg = self.ram[self.pc + 1]
        val = self.ram[self.register[self.sp]]
        self.register[reg] = val
        self.register[self.sp] += 1
        self.pc += 2

    def run_CALL(self):
        self.register[self.sp] -= 1
        self.ram[self.register[self.sp]] = self.pc + 2
        register = self.ram[self.pc + 1]
        reg_value = self.register[register]
        self.pc = reg_value

    def run_RET(self):
        return_value = self.ram[self.register[self.sp]]
        self.register[self.sp] += 1
        self.pc = return_value

    def run_ADD(self):
        self.alu('ADD', self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc +=3

    def run_CMP(self):
        # If registerA is greater than registerB, set the Greater-than `G` flag to 1, otherwise set it to 0.
        if self.register[self.ram_read(self.pc+1)] > self.register[self.ram_read(self.pc+2)]:
            self.greater_than = 1
            self.equal = 0
            self.less_than = 0

        # If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
        elif self.register[self.ram_read(self.pc+1)] == self.register[self.ram_read(self.pc+2)]:
            self.greater_than = 0
            self.equal = 1
            self.less_than = 0
        
        # If registerA is less than registerB, set the Less-than `L` flag to 1, otherwise set it to 0.
        elif self.register[self.ram_read(self.pc+1)] < self.register[self.ram_read(self.pc+2)]:
            self.greater_than = 0
            self.equal = 0
            self.less_than = 1
        self.pc += 3

    def run_JMP(self):
        # Jump to the address stored in the given register.
        # Set the `PC` to the address stored in the given register.
        self.pc = self.register[self.ram_read(self.pc+1)]

    def run_JEQ(self):
        # If `equal` flag is set (true), jump to the address stored in the given register.
        if self.equal == 1:
            self.pc = self.register[self.ram_read(self.pc+1)]
        else:
            self.pc += 2

    def run_JNE(self):
        # If `E` flag is clear (false, 0), jump to the address stored in the given register.
        if self.equal == 0:
            self.pc = self.register[self.ram_read(self.pc+1)]
        else:
            self.pc += 2