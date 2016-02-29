with open("eeprom_data.bin", "rb") as f:
    data = f.read()

instruction1_count = 0
instruction2_count = 0

for i in range(1, len(data)):
    if (ord(data[i]) == 0x11) and (ord(data[i+1]) == 0xC1) and (ord(data[i+2]) == 0x01) and (ord(data[i+3]) == 0xE3):
        instruction1_count += 1
    if (ord(data[i]) == 0x22) and (ord(data[i+1]) == 0xC2) and (ord(data[i+2]) == 0x02) and (ord(data[i+3]) == 0xE3):
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
