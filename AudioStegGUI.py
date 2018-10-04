import AudioSteg
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


#cipherText = input("Enter your cipher text: \n")
#testEn = AudioSteg.Encoder(r"Silent.wav",r"SilentCipher.wav")
#testEn.encode(cipherText,1,1)
#testDe = AudioSteg.Decoder(r"SilentCipher.wav")
#print("Message says: ",testDe.decode(1,1))

def inputBrowseButtonFunc():
    # Allow user to select a directory and store it in global var
    global inputFileString
    filename = filedialog.askopenfilename()
    inputFileString.set(filename)
    print(filename)

def outputBrowseButtonFunc():
    # Allow user to select a directory and store it in global var
    global outputFileString
    filename = filedialog.askopenfilename()
    outputFileString.set(filename)
    print(filename)

def convertFunction():
    print(messageVar.get(),nRepeatVar.get(),randomOffsetTest.get(),inputFileString.get(),outputFileString.get())
    message = messageVar.get()
    nRepeat = nRepeatVar.get()
    randomOffsetBool = randomOffsetTest.get()
    fileIn = inputFileString.get()
    fileOut = outputFileString.get()
    if (not(isinstance(nRepeat,int)) or not(isinstance(randomOffsetBool,int))):
        print("Value Error")
        return
    testEn = AudioSteg.Encoder(fileIn,fileOut)
    testEn.encode(message,nRepeat,randomOffsetBool)

    convertLabel.grid(row=4,column=0)

def inputDecodeBrowseButtonFunc():
    # Allow user to select a directory and store it in global var
    global inputDecodeString
    filename = filedialog.askopenfilename()
    inputDecodeString.set(filename)
    print(filename)

def decodeFunction():
    global messageDecodeVar
    testDe = AudioSteg.Decoder(inputDecodeString.get())
    #print("Message says: ",testDe.decode(nRepeat,randomOffsetBool))
    messageDecodeVar.set(testDe.decode(nRepeatDecodeVar.get(),randomOffsetDecodeTest.get()))


master = Tk()
master.title(".wav File Steg")
notebook = ttk.Notebook(master)
encodeTab = ttk.Frame(notebook)
decodeTab = ttk.Frame(notebook)
notebook.add(encodeTab, text='Encode',state="normal")
notebook.add(decodeTab, text='Decode',state="normal")
#####MENUS######################################################################
"""
menu = Menu(master)
master.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Decode",command=createDecoder)
"""

#####ENCODE WIDGETS##############################################################
Label(encodeTab, text="Input File: ").grid(row=0,column=0)
Label(encodeTab, text="Output File: ").grid(row=1,column=0)

inputFileString = StringVar()
outputFileString = StringVar()

inputFileButton = Button(encodeTab, text='Browse', command=inputBrowseButtonFunc)
outputFileButton = Button(encodeTab, text='Browse',command=outputBrowseButtonFunc)
inputFileEntry = Entry(encodeTab,textvariable=inputFileString)
outputFileEntry = Entry(encodeTab,textvariable=outputFileString)
convertButton = Button(encodeTab,text="Convert!",command=convertFunction)

randomOffsetTest = IntVar()
randomOffsetTest.set(0)
randomOffsetCheckButton = Checkbutton(encodeTab,text='Offset',variable=randomOffsetTest)

Label(encodeTab, text="Number of Repeats: ").grid(row=2,column=0)
nRepeatVar = IntVar()
nRepeatVar.set(1)
nRepeatsEntry = Entry(encodeTab,textvariable = nRepeatVar)

Label(encodeTab, text="Message: ").grid(row=3,column=0)
messageVar = StringVar()
messageVar.set("")
messageEntry = Entry(encodeTab,textvariable = messageVar)


inputFileEntry.grid(row=0, column=1)
inputFileButton.grid(row=0,column=2)

outputFileEntry.grid(row=1, column=1)
outputFileButton.grid(row=1,column=2)

randomOffsetCheckButton.grid(row = 2, column=2)
nRepeatsEntry.grid(row=2,column=1)

messageEntry.grid(row=3,column=1,columnspan=1)

convertButton.grid(row=4,column=1,columnspan=1)
convertLabel = Label(encodeTab, text="Converted Successfully")

######DECODE WIDGETS###########################################################
Label(decodeTab, text="Decode File: ").grid(row=0,column=0 )
inputDecodeString = StringVar()
inputDecodeBrowseButton = Button(decodeTab, text='Browse', command=inputDecodeBrowseButtonFunc).grid(row=0,column=2)
inputDecodeFileEntry = Entry(decodeTab,textvariable=inputDecodeString).grid(row=0,column=1)
Label(decodeTab, text="Number of Repeats: ").grid(row=1,column=0)
nRepeatDecodeVar = IntVar()
nRepeatDecodeVar.set(1)
nRepeatsDecodeEntry = Entry(decodeTab,textvariable = nRepeatDecodeVar).grid(row=1,column=1)
randomOffsetDecodeTest = IntVar()
randomOffsetDecodeTest.set(0)
randomOffsetCheckDecodeButton = Checkbutton(decodeTab,text='Offset',variable=randomOffsetDecodeTest).grid(row=1,column=2)

decodeButton = Button(decodeTab,text="Decode!",command=decodeFunction).grid(row=2,column=1)
Label(decodeTab,text="Message: ").grid(row=3,column=0)
messageDecodeVar = StringVar()
messageDecodeVar.set("")
Label(decodeTab,textvariable=messageDecodeVar).grid(row=3,column=1)

notebook.grid()
mainloop()
