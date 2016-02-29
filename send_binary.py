import serial
import sys

with open("eeprom_data.bin", "rb") as f:
    data = f.read()

print " ".join("{:02x}".format(ord(c)) for c in data)

len1 = (len(data))
len2 = (len(str(len1)))
print "Number of chars:", len1
print "Length of the number of chars:", len2

packet_length = 16

# Check if the last packet is complete
remaining = len1 % packet_length

try:
    ser = serial.Serial(port='COM4', baudrate=115200)

    # First we send the data length
    print "Sending length of the data length:", len2
    ser.write(str(len2))
    response = ser.read(1)
    print "Received:", response
    print "Sending data length:", len1
    ser.write(str(len1))
    response = ser.read(1)
    print "Received:", response

    # Tell if the last packet is complete or not
    print "Sensing remaining length:", len(str(remaining))
    ser.write(str(len(str(remaining))))
    response = ser.read(1)
    print "Received:", response
    print "Sending remaining:", remaining
    ser.write(str(remaining))
    response = ser.read(1)
    print "Received:", response

    # Now we send the data
    sys.stdout.write("Sending data")

    for i in range(0, len1/packet_length):
        sys.stdout.write('.')
        for c in data[packet_length*i:packet_length*i+packet_length]:
            ser.write(c)
        response = ser.read(1)
        if response == '1':
            continue
        else:
            break

    if remaining != 0:
        sys.stdout.write('.')
        for c in data[packet_length*(i+1):packet_length*(i+1)+remaining]:
            ser.write(c)
        response = ser.read(1)

    ser.close()

    print "Task completed"

except serial.serialutil.SerialException:
    print "\nERROR: Serial port not connected"
