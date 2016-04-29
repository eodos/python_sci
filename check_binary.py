with open("eeprom_data.bin", "rb") as f:
    data = f.read()

instruction = 0x00111111
instruction = instruction.to_bytes(4, byteorder="little")
instruction_count = 0

for i in range(0, len(data)):
    if (data[i] == instruction[0]) and (data[i+1] == instruction[1]) \
            and (data[i+2] == instruction[2]) and (data[i+3] == instruction[3]):
        instruction_count += 1

if instruction_count == 1:
    print("Binary valid. It can be flashed to the EEPROM")
elif instruction_count > 1:
    print("Binary NOT valid. Number of times the instruction appears: " + str(instruction_count))
elif instruction_count == 0:
    print("Binary NOT valid. The magic instruction cannot be found")
