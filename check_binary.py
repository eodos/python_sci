with open("eeprom_data.bin", "rb") as f:
    data = f.read()

instruction1 = 0x00111111
instruction2 = 0x00222222

instruction1 = instruction1.to_bytes(4, byteorder="little")
instruction2 = instruction2.to_bytes(4, byteorder="little")

instruction1_count = 0
instruction2_count = 0

for i in range(0, len(data)):
    if (data[i] == instruction1[0]) and (data[i+1] == instruction1[1]) \
            and (data[i+2] == instruction1[2]) and (data[i+3] == instruction1[3]):
        instruction1_count += 1
    if (data[i] == instruction2[0]) and (data[i+1] == instruction2[1]) \
            and (data[i+2] == instruction2[2]) and (data[i+3] == instruction2[3]):
        instruction2_count += 1

if instruction1_count == 1 and instruction2_count == 1:
    print("Binary valid. It can be flashed to the EEPROM")
elif instruction1_count > 1:
    print("Binary NOT valid. Number of times the instruction 1 appears: " + str(instruction1_count))
elif instruction2_count > 1:
    print("Binary NOT valid. Number of times the instruction 2 appears: " + str(instruction2_count))
elif instruction1_count == 0 and instruction2_count == 0:
    print("Binary NOT valid. Magic instructions cannot be found")
elif instruction1_count == 0:
    print("Binary NOT valid. The first magic instruction cannot be found")
elif instruction2_count == 0:
    print("Binary NOT valid The second magic instruction cannot be found")
