__author__ = 'spencer nuttall'
"""Translator takes 2 files:
    -1.) human-readable commands e.g. click button 1
    These correspond to the commands to execute in an automated fashion
    -2.) A file that maps buttons/action to the appropriate x/y coordinates
    It then outputs a command file that combines information from the files into one,
    that will be interpreted and sent using the rdpy protocol.
    Please note that both files are case-sensitive, so all commands in the User File
    e.g. click button1 must have a corresponding definition in the interface file.
    e.g. button1 100 100, if the interface file contained for example: Button1 100 100,
    this will not work, as one button is capitialized and the other is not.
    Additionally, only the keywords 'click' and 'type'.
    The command-line arguments taken in,  are: UserInterface,UserInput.
        Both of these files must be of '.txt' type (and have that extension).
        The Interface file must be formatted like: label x-coordinate y-coordinate
        The User file must be formated like: click/type label/-thing-to-type

"""
#Usercommands = []
#Usercommandlocations = []
import sys

def getCommandindex(commandname):
    global Usercommands
    return  Usercommands.index(commandname)

def ReadUserFile(Usercommandfile):
    CheckFileValid(Usercommandfile)
    global Instructions
    Instructions = []
    UserFile = open(Usercommandfile)
    for lines in UserFile:
        Instructions.append(lines)


def ReadInterfaceFile(UserInterfaceFile):
    global Usercommands
    Usercommands = []
    global Usercommandxlocations
    Usercommandxlocations = []
    global Usercommandylocations
    Usercommandylocations = []
    CheckFileValid(UserInterfaceFile)
    UserCommandInterface= open(UserInterfaceFile)
    for labels in UserCommandInterface:
        parts = labels.split()
        Usercommands.append(parts[0])
        Usercommandxlocations.append(parts[1])
        Usercommandylocations.append(parts[2])


def getcommandindex(command):
    global Usercommands
    index = 0
    for index in range(len(Usercommands)):
        if Usercommands[index] == command:
            return index
def writtenarguments(line):
    returnarguments = line.split()
    returnarguments.remove('type')
    return returnarguments

def buttonarguments(buttonname):
    global Usercommands
    global Usercommandxlocations
    global Usercommandylocations
    buttonindex = Usercommands.index(buttonname)
    return Usercommandxlocations[buttonindex],Usercommandylocations[buttonindex]

def getcommandarguments(commandtype, fullline):
        lineitems = fullline.split()
        if commandtype == 'click':
            return buttonarguments(lineitems[1])
        elif commandtype == 'type':
            typearguments = writtenarguments(fullline)
            return typearguments

def commandrepresentative(UserCommand):
        if (UserCommand =='click'):
            return 'C'
        elif (UserCommand == 'type'):
            return 'T'
        else:
            return ' '

def ConsolidateFileData():
    global Instructions
    global Usercommands
    global  Usercommandxlocations
    global Usercommandlocations
    global FileToWrite
    FileToWrite = []
    for line in Instructions:
        lineitems = line.split()
        outputcommand =commandrepresentative(lineitems[0])
        outputarguments = getcommandarguments(lineitems[0],line)
        fullline = outputcommand, outputarguments
        FileToWrite.append(fullline)
    #print FileToWrite



def FileLineToString(line):
    fixedline = ' '
    fixedline+=line[0]
    fixedline+= ' '
    for elements in line[1]:
        fixedline+=str(elements)
        fixedline+= ' '
    return fixedline

def WriteCommandFile():
    global FileToWrite
    outputfile = open('commands.txt', 'w')
    for outputcommands in FileToWrite:
        properline = FileLineToString(outputcommands)
        outputfile.write("%s\n" % properline)



def CheckFileValid(filename):
    filetype = filename[-4:]

    if filetype != '.txt':
        raise TypeError('All files must be .txt files only!!')


def main():
    global Usercommands
    ReadInterfaceFile(sys.argv[1])
    ReadUserFile(sys.argv[2])
    ConsolidateFileData()
    WriteCommandFile()

if __name__ == '__main__':
    main()

