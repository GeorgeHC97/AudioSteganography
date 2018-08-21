import struct





#FUNCTIONS######################################################################
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part

def readLittleEndian4Byte(bytes):
    sum = 0
    list(bytes).reverse()
    for i in range(4):
        sum+=(int(bytes[i]) << (8*i))
    return sum

def twosComplementFix(int):
    if(int < 0):
        int = 255 - (abs(int) - 1)
    return int

def bitsToBytes(bits):
    bytesOut = []

    for i in range(0, len(bits)//8):
        intByte = 0
        buffer = bits[i*8:8+i*8] #read next 8 bits
        #buffer.reverse() #little endian
        j = 0
        for b in buffer:
            intByte += int(b)<<j
            j += 1
        bytesOut.append(intByte)
    return bytesOut


#CODE###########################################################################
#Open fileSizeHEx


wav_filename = r"Silent.wav"
with open(wav_filename, 'rb') as f_wav:
    wav = f_wav.read()
    entry = wav[:]
    entries = struct.unpack("{}b".format(len(entry)), entry) #unpack bytes
hexentries = list(map("{:02X}".format, entries))  #format the input into hex
###fix negative values: signed to unsigned
entries = list(map(twosComplementFix,entries))

#print(entries[:10])
#entries is in ints BYTES



# cipher text bit now
cipherText = input("Enter your cipher text: \n")
cipherTextBits = tobits(cipherText)
#
#print("cipher text bits:  ",cipherTextBits,"  \n")

##create header (length) and repeat 4 times for payload
length = len(cipherTextBits) #####length in bits
header = bitfield(length)
if(len(header)<8):
    diff = (8 - len(header))*[0]
    diff.extend(header)
    header = diff
header.reverse()
#print("header:   ",header,"    \n")

payload = []
for i in range(0,len(cipherTextBits)):
    temp = [cipherTextBits[i]] * 4
    #print("TEMP: ",temp,"  \n")
    for x in temp:
        payload.append(x)

#print("Payload:  ",payload,"   \n")
#print(len(payload))

header.extend(payload)

finalPayload = header
#print("Final Payload:  ",finalPayload,"  \n\n\n")

##FINAL PAYLOAD format
# bits 0-7 = size of ciphertext in tobits
#bits 8-... = ciphertext as bits repeated 4 times so amount of bits after size header is 4*size




#############
#now need to read in the wav file, read in header and inject my data in
#hexentries= bytes

wavHeader = entries[:44]
#fileSizeInt = ''.join(wavHeader[4:8])
#int.from_bytes(wavHeader[4:8], byteorder='little')####
#print(wavHeader,"\n")

fileSizeInt = readLittleEndian4Byte(wavHeader[4:8]) #read file size from wavHeader

finalPayloadLengthBytes = len(finalPayload) / 8
print(finalPayloadLengthBytes)

if(finalPayloadLengthBytes > fileSizeInt - 44):
    print("Size mismatch of payload and file. Adjust either payload or file. \n")
    sys.exit(-1)

#insert payload now
#how many keybits per byte? try 4 to start with


#create list of new sample data
newSampleData = []
exitIndex = 0
#for i in range(0,finalPayloadLengthBytes):
#   #read 44+i*4:48+i*4 in as bytes
#   #put 0+i*8:4+i*8 of final payload into byte 1
#   #put 4+i*8:8+i*8 of final payload into byte3
#   #reconstruct bytes 1-4
#   #add to new sample data

#fixed for now
for i in range(0,int(finalPayloadLengthBytes)):
    buffer = entries[44+i*2:46+i*2] #read in next 2 bytes
    bufferBits0 = bitfield(buffer[0])
    bufferBits1 = bitfield(buffer[1])
    #extend to 8 bits###################
    if(len(bufferBits0)<8):
        diff = (8 - len(bufferBits0))*[0]
        bufferBits0.extend(diff)
    if(len(bufferBits1)<8):
        diff = (8 - len(bufferBits1))*[0]
        bufferBits1.extend(diff)
    #####################################
    bufferBits = bufferBits0
    bufferBits.extend(bufferBits1)
    #print(bufferBits)
    newByte  = finalPayload[i*8:8+i*8]
    newByte.extend(bufferBits[8:16])
    newPair = newByte
    newSampleData.extend(newPair)
    #print(newPair)



exitIndex = int(44+finalPayloadLengthBytes) #where the wav returns to normal
#now need to reconstruct

#convert new sample data to BYTES
newSampleDataBytes = bitsToBytes(newSampleData)

print(wavHeader)
print(len(newSampleDataBytes))

cipherFile = wavHeader
cipherFile.extend(newSampleDataBytes)
cipherFile.extend(entries[exitIndex:])
cipherFile = bytes(cipherFile)


wav_filename = r"SilentCipher.wav"
with open(wav_filename, 'wb') as f_wav:
    f_wav.write(cipherFile)
#works!




#######DECODER###############

wav_filename = r"SilentCipher.wav"
with open(wav_filename, 'rb') as f_wav:
    wav = f_wav.read()
    entryDecode = wav[:]
    entriesDecode = struct.unpack("{}b".format(len(entryDecode)), entryDecode) #unpack bytes

###fix negative values: signed to unsigned
entriesDecode = list(map(twosComplementFix,entriesDecode))

#print(entriesDecode[:44])

##skip first 44
#read first byte to get Size
decodeSize = entriesDecode[44]
#read the next size*2 bytes
#checking lower 4 bits for value
#append value to results list
#convert list to ascii
#join list a sstring and print "voiLa"

messageBits = []

#every other byte
for i in range(0,decodeSize*2,2):
    #print(entriesDecode[46+i])
    bufferBits = bitfield(entriesDecode[46+i])
    if(len(bufferBits)<8):
        bufferBits = [0]*(8-len(bufferBits)) + bufferBits
    #print(bufferBits)
    if(bufferBits[4] == 1):
        messageBits.append(1)
    else:
        messageBits.append(0)
    if(bufferBits[0] == 1):
        messageBits.append(1)
    else:
        messageBits.append(0)

print(messageBits)
print(frombits(messageBits))

#########BUG FIXING NOW#####################
#certain messages cutting off / getting dropped "ayrton", "george"
#issue with size and float arith?
