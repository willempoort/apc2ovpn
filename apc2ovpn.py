#!/usr/bin/python3
import sys, getopt, codecs
from pathlib import Path

# Willem M. Poort
# !Bien BV
# willem@bien.nl
# oct 19 2020
# Version 2.0
# File converts Sophos .apc file to:
# xxx.ovpn file + xxx.ovpn.auth file that stores the username and password
#
# start programm with:
# apc2ovpn -i yourapcfile.apc -o youroutput.ovpn file
#
# the programm expects the template.ovpn to be in the same directory
# .apc will be scanned for available fieldnames plus their values
# found fields with first caracters will be printed on screen as well
"""
.apc file decomposed. (according to me ;) 
The file starts with a fixed 16 bytes header
Right after the header the data & field definitions starts.
Right after every field the next 4 bytes (hex) define the length of the fieldname followed by the fieldname.


Type  How to read  
------- -----------------------------
0A     text data length (hex) in next 1 caracter field content in next "length" caracters.
01   certificate (multiline) length (hex) in next 4 caracters field content in next "length" caracters.
06   integer field. data in hex in next 3 bytes.
08   Boolean ?? not sure what hex 81 stands for.
17   Distinquised name length (hex) in next 1 caracter field content in next "length" caracters.

Header 16 bytes Hex:
04 07 04 31 32 33 34 04 04 04 08 03 0D 00 00 00    (31 32 33 34 is readable as 1234)
T  L
y  e
p  n
e  g                    Veldnaam start met [lengte veldnaam][00 00 00][veldnaam]
------ -----------------------------------------------------   -------------- ----------------------------------------------------------
0A 03 tcp             (3 caracters)    08 00 00 00 protocol
0A 03 MD5             (3 caracters)    18 00 00 00 authentication_algorithm 
01 5D 13 00 00 Certificate: ...    (4957 tekens)  0B 00 00 00  certificate
01 84 11 00 00 Certificate:....    (4484 tekens)  07 00 00 00 ca_cert
0A 0B REF_AaaUse1         (11 caracters)   08 00 00 00 username
01 A8 06 00 00 -----BEGIN..     ...      03 00 00 00 key
0A 0B AES-128-CBC              14 00 00 00 encryption_algorithm
08 81 ??ON?? not sure what 81 stands for?         0B 00 00 00 compression
0A 26 REF_SSLSERVPNxxxx0000ref_sslservpnxxxx   08 00 00 00 password
0A 00                   06 00 00 00 engine
17 61 C=nl, L=Rotterdam, O=Fam....        09 00 00 00 server_dn
06 AA 04 00 (-> 1194)             0B 00 00 00 server_port
0A 0D 11.11.111.111              0E 00 00 00 server_address


Veldtypes
-----------------------------------------------------------------------------------------------------------------------------------------
Type 0A -> Length in 1 Byte, Followed By nBytes data
Type 01 -> Field length in next 4 Bytes, Followed By nBytes data
Type 06 -> Field data (int) in next 3 Bytes
Type 08 -> Boolean ? Field data (int) in next 1 Byte
Type 17 ->  Length in 1 Byte, Followed By nBytes data

"""

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       print ('apc2ovpn.py -i <inputfile> -o <outputfile>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print ('apc2ovpn.py -i <inputfile> -o <outputfile>')
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
    data = Path(inputfile).read_bytes()
  
    # extract value & fieldnames from data
    # find header and point right behind it.
    searchstr = bytearray(b'\x04\x07\x04\x31\x32\x33\x34\x04\x04\x04\x08\x03\x0D\x00\x00\x00')
    offset = data.find(searchstr) + len(codecs.decode(searchstr))
    ftype = data[offset:offset+1]
    lendata = len(data)
    offset = offset + 1
    fields_dict = {}
    while offset < lendata:
       if ftype == bytearray(b'\x0A'):
            strlen = int.from_bytes(data[offset:offset+1], byteorder='little', signed=False)
            offset = offset + 1
            value = codecs.decode(data[offset:offset+strlen])
            offset = offset+strlen
            strlen = int.from_bytes(data[offset:offset+4], byteorder='little', signed=False)
            offset = offset + 4
            name = codecs.decode(data[offset:offset+strlen])
            offset = offset + strlen
       elif ftype == bytearray(b'\x01'):
            strlen = int.from_bytes(data[offset:offset+4], byteorder='little', signed=False)
            offset = offset + 4
            value = codecs.decode(data[offset:offset+strlen])
            offset = offset+strlen
            strlen = int.from_bytes(data[offset:offset+4], byteorder='little', signed=False)
            offset = offset + 4
            name = codecs.decode(data[offset:offset+strlen])
            offset = offset + strlen
       elif ftype == bytearray(b'\x06'):
            value =  str(int.from_bytes(data[offset:offset+4], byteorder='little', signed=False))
            offset = offset+4
            strlen = int.from_bytes(data[offset:offset+4], byteorder='little', signed=False)
            offset = offset + 4
            name = codecs.decode(data[offset:offset+strlen])
            offset = offset + strlen
       elif ftype == bytearray(b'\x08'):
            value =  str(int.from_bytes(data[offset:offset+1], byteorder='little', signed=False))
            offset = offset+1
            strlen = int.from_bytes(data[offset:offset+4], byteorder='little', signed=False)
            offset = offset + 4
            name = codecs.decode(data[offset:offset+strlen])
            offset = offset + strlen
       elif ftype == bytearray(b'\x17'):
            strlen = int.from_bytes(data[offset:offset+1], byteorder='little', signed=False)
            offset = offset + 1
            value = codecs.decode(data[offset:offset+strlen])
            offset = offset+strlen
            strlen = int.from_bytes(data[offset:offset+4], byteorder='little', signed=False)
            offset = offset + 4
            name = codecs.decode(data[offset:offset+strlen])
            offset = offset + strlen
       fields_dict.update({name:value})
       ftype = data[offset:offset+1]
       offset = offset + 1
    
    print("\n\n"+str(len(fields_dict))+" Keys found\nListed with first 25 caracters of value")
    for key in fields_dict:
         print(f"{key:<30}" + " = " + fields_dict[key][:20].replace('\n',''))
    # create .ovpn file from template
    # read template data from 
    template = open("template.ovpn","r")
    ovpndata = template.read()
    template.close()

    for key in fields_dict:
        ovpndata = ovpndata.replace("{"+key+"}",fields_dict[key])
    ovpndata = ovpndata.replace("{outputfile}",outputfile)
    ovpnfile = open(outputfile, "w")
    ovpnfile.write(ovpndata)
    ovpnfile.close()

    ovpnpass = outputfile + ".auth"
    passfile = open(ovpnpass, "w")
    passfile.write(fields_dict["username"]+"\n")
    passfile.write(fields_dict["password"]+"\n")
    passfile.close()

def filterstr(data,searchstr,lenbytes):
    # searchstr is string to jump to in the data string, then 
    # lenbytes is number of caracters that will define the string length.
    # return the string after lenbytes for lenbytes long
    # lenbytes is in hex 16 bit little byte decoded.
    offset = data.find(searchstr) + len(codecs.decode(searchstr))
    strlen = int.from_bytes(data[offset:offset+lenbytes], byteorder='little', signed=False)
    return codecs.decode(data[offset+lenbytes:offset+lenbytes+strlen])

if __name__ == "__main__":
   main(sys.argv[1:])
