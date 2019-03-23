import operator
from enum import IntEnum
from dataclasses import dataclass

class ArkheException(Exception):
    pass
    
class HLT(ArkheException):
    def __init__(self):
        super().__init__("Program stopped!")

class Operation(IntEnum):
    LOAD = 0
    ADD = 1
    SUB = 2
    MUL = 3
    TRUEDIV = 4
    JMP = 5
    JMPF = 6
    JPMB = 7
    EQ = 8
    NE = 9
    GT = 10
    LT = 11
    GE = 12
    LE = 13
    JEQ = 14
    JNE = 15
    NOP = 0xFFE
    HLT  = 0xFFF

@dataclass
class Instr:
    operation: Operation


class VM:
    instrset = {}

    def __init__(self, arkhe):
        self.arkhe = arkhe

    @classmethod
    def instr(cls, instr):
        def wrapper(f):
            cls.instrset[instr] = f
            return f

        return wrapper

    def dispatch(self, instr):
        return self.instrset.get(instr)(self.arkhe, instr)


@VM.instr(Operation.LOAD)
def load(vm, instr):
    target = vm.get_next_8()
    vm.registers[target] = vm.get_next_16()
    
@VM.instr(Operation.ADD)
@VM.instr(Operation.SUB)
@VM.instr(Operation.MUL)
@VM.instr(Operation.TRUEDIV)
def math(vm, instr):
    operand1 = vm.registers[vm.get_next_8()]
    operand2 = vm.registers[vm.get_next_8()]
    vm.registers[vm.get_next_8()] = getattr(operator, instr.name.lower())(operand1, operand2)
    
@VM.instr(Operation.EQ)
@VM.instr(Operation.NE)
@VM.instr(Operation.LE)
@VM.instr(Operation.GE)
@VM.instr(Operation.GT)
@VM.instr(Operation.LT)
def comparison(vm, instr):
    operand1 = vm.registers[vm.get_next_8()]
    operand2 = vm.registers[vm.get_next_8()]
    vm._eqflag = getattr(operator, instr.name.lower())(operand1, operand2)
    vm.get_next_8()
    
@VM.instr(Operation.JMP)
def jmp(vm, instr):
    vm.counter = vm.registers[vm.get_next_8()]
    
@VM.instr(Operation.JMPF)
def jmp_forward(vm, instr):
    value = vm.registers[vm.get_next_8()]
    vm.counter += value
        
@VM.instr(Operation.JPMB)
def jmp_backward(vm, instr):
    value = vm.registers[vm.get_next_8()]
    vm.counter -= value

@VM.instr(Operation.JEQ)
def jmp_ifeq(vm, instr):
    value = vm.registers[vm.get_next_8()]
    if vm._eqflag:
        vm.counter = value

@VM.instr(Operation.JNE)
def jmp_ifne(vm, instr):
    value = vm.registers[vm.get_next_8()]
    if not vm._eqflag:
        vm.counter = value
                 
@VM.instr(Operation.HLT)
def hlt(vm, instr):
    raise HLT()