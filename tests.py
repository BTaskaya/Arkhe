import pytest
from arkhe import Arkhe, Registers, RegisterNotFound

def test_registers():
    registers = Registers(32)
    assert registers[0] == 0

def test_register_key_imm():
    registers = Registers(16)
    with pytest.raises(RegisterNotFound):
        registers[32] = 3

def test_register_set():
    registers = Registers(16)
    registers[5] = 15
    assert registers[5] == 15
    
def test_vm_load():
    code = [0, 0, 0, 100] # Load 100 to r0
    vm = Arkhe(code)
    vm.eval()
    assert vm.registers[0] == 100

def test_vm_multiple_load():
    code = [0, 0, 3, 232, # Load 1k to r0
            0, 1, 1, 244] # Load 500 to r1

    vm = Arkhe(code)
    vm.eval()
    assert vm.registers[0] == 1000 and vm.registers[1] == 500

def test_vm_math():
    code = [0, 0, 3, 232, # r0 = 1000
            0, 1, 1, 244, # r1 = 500
            1, 0, 1, 2,   # r2 = r0 + r1 = 1500
            2, 2, 1, 3,   # r3 = r2 - r1 = 1000
            3, 1, 2, 4,   # r4 = r1 * r2 = 500 * 1500
            4, 2, 3, 5]    # r5 = r2 / r3 = 1500 / 500 * 1500
            
    vm = Arkhe(code)
    vm.eval()
    assert (
        vm.registers[0] == 1000
        and vm.registers[1] == 500
        and vm.registers[2] == 1500
        and vm.registers[3] == 1000
        and vm.registers[4] == 750_000
        and vm.registers[5] == 1.5
    )
    
def test_vm_jmp():
    code = [5, 0, 0, 0]
    vm = Arkhe(code)
    vm.registers[0] = 4
    vm.exc_instr()
    assert vm.counter == 4

def test_vm_jmpf():
    code = [6, 0, 0, 0, 
            0xFFF, 0, 0, 0]
            
    vm = Arkhe(code)
    vm.registers[0] = 2
    vm.exc_instr()
    assert vm.counter == 4

def test_vm_jmpb():
    code = [0, 0, 0, 10, 7, 1, 0, 0]
    vm = Arkhe(code)
    vm.registers[1] = 6
    vm.exc_instr()
    vm.exc_instr()
    assert vm.counter == 0