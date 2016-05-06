import crc16
import serial
import sys

# User definitions
DEBUG = 1
file = "eeprom_data.bin"
packet_length = 100
serial_baudrate = 115200
ACK = b'\x06'
NACK = b'\x15'

# Detect OS and select the appropriate serial port
if sys.platform == 'linux':
    serial_port = "/dev/ttyUSB0"
else:
    serial_port = "COM4"


def debug_print(msg):
    if DEBUG:
        print(msg)


def print_hex(packet):
    return " ".join("{:02x}".format(c) for c in packet)


def add_crc(packet):
    crc = crc16.crc16xmodem(packet)
    crc = crc.to_bytes(2, byteorder="big")
    packet += crc
    return packet


def send_packet(buffer, packet):
    while True:
        debug_print("Sending: " + print_hex(packet))
        buffer.write(packet)
        response = buffer.read(1)
        debug_print("Received: " + print_hex(response))
        if response == ACK:
            break


def main():
    # Global variables
    global file
    global packet_length

    # Open binary file and extract the data
    with open(file, "rb") as f:
        data = f.read()

    # Length of the data
    data_length = (len(data))
    debug_print("Data length: " + str(data_length))

    # Check if the last packet is complete
    number_of_packets = data_length//packet_length
    remaining = data_length % packet_length

    # Zero pad last packet
    if remaining != 0:
        number_of_packets += 1
        while packet_length - remaining != 0:
            remaining += 1
            data += '\0'.encode()

    # Print the data
    debug_print(print_hex(data))
    debug_print("Number of packets: " + str(number_of_packets))

    # Add 2 bytes to packet_length_with_crc corresponding to the CRC
    packet_length_with_crc = packet_length + 2

    # Establish serial communication
    try:
        ser = serial.Serial(port=serial_port, baudrate=serial_baudrate)

        # First we send the packet length
        debug_print("Sending packet length")
        send_packet(ser, packet_length_with_crc.to_bytes(4, byteorder="big"))

        # Then we send the number of packets
        debug_print("Sending number of packets")
        send_packet(ser, number_of_packets.to_bytes(4, byteorder="big"))

        for i in range(0, number_of_packets):
            # Extract packet from data
            packet = data[packet_length*i:packet_length*i+packet_length]

            # Calculate CRC16 and add it to the packet
            packet = add_crc(packet)

            # Send packet
            debug_print("Sending packet " + str(i))
            send_packet(ser, packet)

        debug_print("Task completed")

    except serial.serialutil.SerialException:
        debug_print("ERROR: Serial port not connected")

if __name__ == "__main__":
    main()
