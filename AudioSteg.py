
import struct
import sys
import random
import tkinter
#FUNCTIONS######################################################################

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
###############################################################################
#Create encoder and decoder objects
class Encoder:
    """Encoder Object"""
    def __init__(self,fileIn,fileOut):
        self.fileIn = fileIn
        self.fileOut = fileOut


    def encode(self,msg,nRepeat,randomOffsetBool):
        #set nRepeat to 8 or 4 if lossy connection otherwise use 2 or 1.
        #set randomOffsetBool to 1 if you want data inserted deeper into file

        #Catch weird arg values
        if (nRepeat != 1 ) and ( nRepeat != 2 ) and ( nRepeat != 4 ) and ( nRepeat != 8):
            print("Error: invalid repeat value. Use power of 2 <= 8.")
            sys.exit(-1)

        if (randomOffsetBool != 0) and (randomOffsetBool != 1):
            print("Error: Bad randomOffsetBool value.")
            sys.exit(-1)



        wav_filename = self.fileIn
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
        #cipherText = input("Enter your cipher text: \n")
        cipherText = msg
        cipherTextBits = tobits(cipherText)
        #
        #print("cipher text bits:  ",cipherTextBits,"  \n")

        ##create header (length) and repeat nRepeat times for payload
        #length = len(cipherTextBits) #####length in bits ##### ????????
        length = len(msg)*nRepeat # NOT SURE YET



        #print(length)
        header = bitfield(length)
        #print(header)
        if(len(header)<8):
            diff = (8 - len(header))*[0]
            diff.extend(header)
            header = diff
        #print("Header: ",header)
        header.reverse()
        #print("header:   ",header,"    \n")

        ##############################TEMPORARY##############################
        # CANT HANDLE SIZES OVER  255
        if(len(header) > 8):
            print("ERROR: Message length exceeded. \n")
            sys.exit(-1)



        payload = []
        for i in range(0,len(cipherTextBits)):
            temp = [cipherTextBits[i]] * nRepeat
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

        finalPayloadLengthBytes = len(finalPayload) // 8
        #print("Payload Length Bytes: ",finalPayloadLengthBytes)


        if(finalPayloadLengthBytes > fileSizeInt - 44) or (44+255+finalPayloadLengthBytes > fileSizeInt):
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

        if randomOffsetBool:
            offset = random.randint(0,255)
            offsetBits = bitfield(offset)
            if(len(offsetBits)<8):
                diff = (8 - len(offsetBits))*[0]
                diff.extend(offsetBits)
                offsetBits = diff
                offsetBits.reverse()

            offsetByte = bitsToBytes(offsetBits)
            #print("Offset: ",offset)
            #print("Offset bits: ",offsetBits)
            #print("TEST: ",bin(offset))
            #print("Offset Byte: ",offsetByte)
        else:
            offset = 0


        #fixed for now
        for i in range(0,int(finalPayloadLengthBytes)):
            buffer = entries[44+i*2+offset:46+i*2+offset] #read in next 2 bytes
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
            #print("Buffer bits: ",bufferBits)
            newByte  = finalPayload[i*8:8+i*8]
            newByte.extend(bufferBits[8:16])
            newPair = newByte
            newSampleData.extend(newPair)
            #print("New Pair: ",newPair)




        #now need to reconstruct

        #convert new sample data to BYTES
        newSampleDataBytes = bitsToBytes(newSampleData)
        exitIndex = int(44+len(newSampleDataBytes)*2+offset) #where the wav returns to normal
        #print("Exit Index: ",exitIndex, "    Len(bytes):", len(newSampleDataBytes))

        #print("WAV header: ",wavHeader)
        #print("Payload Length: ",len(newSampleDataBytes))
        cipherFile = wavHeader
        if randomOffsetBool:
            cipherFile.extend(offsetByte)
            cipherFile.extend(entries[45:(45+offset)])
            cipherFile.extend(newSampleDataBytes)
        else:
            cipherFile.extend(newSampleDataBytes)

        cipherFile.extend(entries[exitIndex:])
        cipherFile = bytes(cipherFile)

        #print("TEST: ",entries[44:exitIndex])


        wav_filename = self.fileOut
        with open(wav_filename, 'wb') as f_wav:
            f_wav.write(cipherFile)
        #works!
################################################################################
class Decoder:
    """Decoder Object"""
    def __init__(self,fileIn):
        self.fileIn = fileIn

    def decode(self,nRepeat,randomOffsetBool):
        wav_filename = self.fileIn
        with open(wav_filename, 'rb') as f_wav:
            wav = f_wav.read()
            entryDecode = wav[:]
            entriesDecode = struct.unpack("{}b".format(len(entryDecode)), entryDecode) #unpack bytes

        ###fix negative values: signed to unsigned
        entriesDecode = list(map(twosComplementFix,entriesDecode))

        #print(entriesDecode[:50])

        if randomOffsetBool:
            offset = entriesDecode[44]
            #print("Offset Decode: ",offset)
        else:
            offset = 0

        ##skip first 44
        #read first byte to get Size
        if randomOffsetBool:
            decodeSize = entriesDecode[45+offset]
        else:
            decodeSize = entriesDecode[44+offset]
        #print("Decode Size: ",decodeSize+1) #including size byte
        #print(entriesDecode[44:50])
        #print("FILE SIZE", len(entriesDecode))
        #read the next size*2 bytes
        #checking lower 4 bits for value
        #append value to results list
        #convert list to ascii
        #join list a sstring and print "voiLa"

        messageBits = []

        ##account for weirdness when adding an offset
        extra = 0
        if randomOffsetBool:
            extra = 1

        #every other byte
        for i in range(0,decodeSize*2,2):
            #print(entriesDecode[46+i])
            bufferBits = bitfield(entriesDecode[46+i+offset+extra])
            if(len(bufferBits)<8):
                bufferBits = [0]*(8-len(bufferBits)) + bufferBits
            #print(bufferBits)
            if nRepeat == 8:
                    if(bufferBits[7] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
            elif nRepeat == 4:
                    if(bufferBits[4] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[0] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
            elif nRepeat == 2:
                    if(bufferBits[7] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[5] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[3] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[1] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
            elif nRepeat == 1:
                    if(bufferBits[7] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[6] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[5] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[4] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[3] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[2] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[1] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)
                    if(bufferBits[0] == 1):
                        messageBits.append(1)
                    else:
                        messageBits.append(0)


        #print(messageBits)
        #print(frombits(messageBits))
        return(frombits(messageBits))




######## M A I N ##############################################################

#cipherText = input("Enter your cipher text: \n")
#testEn = Encoder(r"Silent.wav",r"SilentCipher.wav")
#testEn.encode(cipherText,1,1)
#testDe = Decoder(r"SilentCipher.wav")
#print("Message says: ",testDe.decode(1,1))

##FEATURES TO ADD
#31 character maximum at the moment -> increase
#If short enough message then random offset in file? as command line option DONE
#Maybe make a bigger offset
#one bit per byte rather than full byte every other byte
#GUI
