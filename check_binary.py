with open("eeprom_data.bin", "rb") as f:
    data = f.read()

instruction1 = [0x11, 0xC1, 0x01, 0xE3]
instruction2 = [0x22, 0xC2, 0x02, 0xE3]

instruction1_count = 0
instruction2_count = 0

for i in range(0, len(data)):
    if (ord(data[i]) == instruction1[0]) and (ord(data[i+1]) == instruction1[1]) \
            and (ord(data[i+2]) == instruction1[2]) and (ord(data[i+3]) == instruction1[3]):
        instruction1_count += 1
    if (ord(data[i]) == instruction2[0]) and (ord(data[i+1]) == instruction2[1]) \
            and (ord(data[i+2]) == instruction2[2]) and (ord(data[i+3]) == instruction2[3]):
        instruction2_count += 1

if instruction1_count == 1 and instruction2_count == 1:
    print "Binary valid. It can be flashed to the EEPROM"
elif instruction1_count > 1:
    print "Binary NOT valid. Number of times the instruction 1 appears:", instruction1_count
elif instruction2_count > 1:
    print "Binary NOT valid. Number of times the instruction 2 appears:", instruction2_count
elif instruction1_count == 0 and instruction2_count == 0:
    print "Binary NOT valid. Magic instructions cannot be found"
elif instruction1_count == 0:
    print "Binary NOT valid. The first magic instruction cannot be found"
elif instruction2_count == 0:
    print "Binary NOT valid The second magic instruction cannot be found"
