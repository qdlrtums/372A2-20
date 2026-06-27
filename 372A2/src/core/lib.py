import struct
import socket
import time
import random
import os

HEADER_FORMAT = "<IIBH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

TYPE_DATA = 0
TYPE_ACK = 1
TYPE_START = 2
TYPE_END = 3

def serialize(seq, ack, ptype, payload=b""):
    header = struct.pack(HEADER_FORMAT, seq, ack, ptype, 0)
    return header + payload

def deserialize(data):
    seq, ack, ptype, checksum = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    payload = data[HEADER_SIZE:]
    return seq, ack, ptype, checksum, payload