# apc2ovpn

This is a new attempt to rewrite .apc files to .ovpn
to create an .ovpn file you need to have the template.ovpn in your directory

If in future .apc files more fields/keys are added the program will list them.
fields in template.ovpn are presented as {fieldname}.
The script will replace them with the value of the responding keys it found. 


The script will find fieldnames and their values in .apc by itself
I did some debugging to try to decompose the .apc file
This is what I came up with so far.

.apc file decomposed. (according to me ;) 
The file starts with a fixed 16 bytes header
Right after the header the data & field definitions starts.
Right after every field the next 4 bytes (hex) define the length of the fieldname followed by the fieldname.
Type  How to read  
Markup :  - - - -
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
Markup :  - - - -
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
Markup :  - - - -
Type 0A -> Length in 1 Byte, Followed By nBytes data
Type 01 -> Field length in next 4 Bytes, Followed By nBytes data
Type 06 -> Field data (int) in next 3 Bytes
Type 08 -> Boolean ? Field data (int) in next 1 Byte
Type 17 ->  Length in 1 Byte, Followed By nBytes data

