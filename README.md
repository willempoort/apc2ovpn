# apc2ovpn

This is a new attempt to rewrite .apc files to .ovpn
to create an .ovpn file you need to have the template.ovpn in your directory

If in future .apc files more fields/keys are added the program will list them.
Fields in template.ovpn are presented as {fieldname}.
The script will replace them with the value of the responding keys it found. 


The script will find fieldnames and their values in .apc by itself
I did some debugging to try to decompose the .apc file
This is what I came up with so far.

.apc file decomposed. (according to me ;) 
The file starts with a fixed 16 bytes header
Right after the header the data & field definitions starts.
Right after every field the next 4 bytes (hex) define the length of the fieldname followed by the fieldname.

# Format .apc file

**Header** 16 bytes Hex:
04 07 04 31 32 33 34 04 04 04 08 03 0D 00 00 00    (31 32 33 34 is readable as 1234)

Next after header <br>

Record type | Data field length | Data field content | Fieldname length | Fieldname
---- | ---- | ---- | ---- | ---- 

---

**Record Type Hex Code** | **Field Type**
---- | ----
**0A** | **text** data length (hex) in next 1 caracter field content in next "length" caracters.
**01** | **certificate** (multiline) length (hex) in next 4 caracters field content in next "length" caracters.
**06** | **integer** field. data in hex in next 3 bytes.
**08** | **Boolean** ?? not sure what hex 81 stands for in data field (Was used for compression value).
**17** | **Distinquised name** length (hex) in next 1 caracter field content in next "length" caracters.

---

**Type**  | **Hex Length bytes** | **Data** | **Hex Length bytes** | **Fieldname**
------------- | ------------- | ------------- | ------------- | -------------
0A (text) | Length 1 Byte (hex)|nBytes data | Length in 4 Bytes (hex)| Fieldname in nBytes
01 (cert) | Length 4 Bytes (hex) | nBytes data | Length in 4 Bytes (hex)| Fieldname in nBytes
06 (int) |  n/a | Field data in next 3 Bytes (hex -> int) | Length in 4 Bytes (hex)| Fieldname in nBytes
08 (Boolean ?) | n/a |Field data in next 1 Byte (hex -> int ?) | Length in 4 Bytes (hex)| Fieldname in nBytes
17 (dn) | Length 1 Byte (hex)|nBytes data | Length in 4 Bytes (hex)| Fieldname in nBytes

# How to run
You need the following files:<br>
**apc2ovpn.py**<br>
**template.ovpn**<br>
**your-own.apc**<br>
<br>
Run the programm as follows:<br>
**./apc2ovpn -i your-own.apc -o your-own.ovpn**<br>
(Replace your-own with the right filenames ;))<br>
<br>
The script will create the **.ovpn** file and an **.ovpn.auth** file.<br>
The **.ovpn.auth** file contains the username and password extracted from your **.apc** file
