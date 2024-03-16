from view_preferences_pb2 import ViewPreferences
from gps_data_pb2 import GPSData
from lightheader_pb2 import LightHeader

import sys
import os
import struct

# Enumerate your BlockTypes in Python to match the Rust definition
class BlockType:
    LightHeader = 0
    ViewPreferences = 1
    GPSData = 2

def parse_header_mod(data):
    magic = b"LELR"
    if data[:4] != magic:
        raise ValueError("Magic number is incorrect")

    combined_length, message_offset, message_length = struct.unpack('<QQL', data[4:24])
    kind = data[24]

    if kind == BlockType.LightHeader:
        message_type = "lightheader_pb2.LightHeader"
    elif kind == BlockType.ViewPreferences:
        message_type = "view_preferences_pb2.ViewPreferences"
    elif kind == BlockType.GPSData:
        message_type = "gps_data_pb2.GPSData"
    else:
        raise ValueError(f"Unknown block type {kind}")

    return combined_length, message_offset, message_length, message_type

def read_binary_file(filepath):
    with open(filepath, "rb") as file:
        content = file.read()
    return content

file_path = "../lrifiles/goose.lri"
binary_content = read_binary_file(filepath)
binary_content_temp = binary_content
previous = 0 
json_light_header = []
json_view_preferences = []
json_view_GPSData = []
while len(binary_content_temp)>0:
    header_info = (parse_header_mod(binary_content_temp))
    print(header_info)
    if(header_info[3]=="lightheader_pb2.LightHeader"):
        light_header = LightHeader()
        light_header.ParseFromString(binary_content_temp[header_info[1]:header_info[1]+header_info[2]])
        light_header_json = MessageToJson(light_header)
        json_light_header.append(json.loads(light_header_json))
        
    if(header_info[3]=="view_preferences_pb2.ViewPreferences"):
        light_header = ViewPreferences()
        light_header.ParseFromString(binary_content_temp[header_info[1]:header_info[1]+header_info[2]])
        light_header_json = MessageToJson(light_header)
        json_view_preferences.append(json.loads(light_header_json))
        
    if(header_info[3]=="gps_data_pb2.GPSData"):
        light_header = GPSData()
        light_header.ParseFromString(binary_content_temp[header_info[1]:header_info[1]+header_info[2]])
        light_header_json = MessageToJson(light_header)
        json_view_GPSData.append(json.loads(light_header_json))
        
    binary_content_temp=binary_content_temp[header_info[0]:]
    print(len(binary_content_temp))
    
    # block = binary_content_temp[binary_content:]
    # header_info = ((parse_header_mod(block)))