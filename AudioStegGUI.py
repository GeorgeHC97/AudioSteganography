import AudioSteg
from tkinter import *
from tkinter import filedialog


#cipherText = input("Enter your cipher text: \n")
#testEn = AudioSteg.Encoder(r"Silent.wav",r"SilentCipher.wav")
#testEn.encode(cipherText,1,1)
#testDe = AudioSteg.Decoder(r"SilentCipher.wav")
#print("Message says: ",testDe.decode(1,1))
def radioButtonFunc(value):
    if value:
        return 0
    else:
        return 1

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

master = Tk()
master.title("Test")
Label(master, text="Input File: ").grid(row=0)
Label(master, text="Output File: ").grid(row=1)

inputFileString = StringVar()
outputFileString = StringVar()

inputFileButton = Button(master, text='Browse', command=inputBrowseButtonFunc)
outputFileButton = Button(master, text='Browse',command=outputBrowseButtonFunc)
inputFileEntry = Entry(master,textvariable=inputFileString)
outputFileEntry = Entry(master,textvariable=outputFileString)
convertButton = Button(master,text="Convert!")

randomOffsetTest = IntVar()
randomOffsetTest = 0
randomOffsetRadioButton = Radiobutton(master,text='Offset',variable=randomOffsetTest,value=randomOffsetTest,command=radioButtonFunc(randomOffsetTest))

Label(master, text="Number of Repeats: ").grid(row=2,column=0)
nRepeatVar = IntVar()
nRepeatVar = 1
nRepeatsEntry = Entry(master,textvariable = nRepeatVar)

Label(master, text="Message: ").grid(row=3,column=0)
messageVar = StringVar()
messageVar = ""
messageEntry = Entry(master,textvariable = messageVar)


inputFileEntry.grid(row=0, column=1)
inputFileButton.grid(row=0,column=2)

outputFileEntry.grid(row=1, column=1)
outputFileButton.grid(row=1,column=2)

randomOffsetRadioButton.grid(row = 2, column=2)
nRepeatsEntry.grid(row=2,column=1)

messageEntry.grid(row=3,column=1,columnspan=1)

convertButton.grid(row=4,column=1,columnspan=1)


mainloop()
