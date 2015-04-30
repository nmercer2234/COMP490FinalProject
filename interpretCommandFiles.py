__author__ = 'Thomas Larsen'
import os

def verifyCommandFile():
    if os.access("commands", os.F_OK):
        return True
    else:
        print("Not a valid File")
        return False

def verifyFileSyntax(file):
    valid = True
    for line in file:
        if line != "\n":
            args = line.split()
            if args[0] == 'C' and len(args) == 3:
                valid = args[1].isdigit() and args[2].isdigit()
            elif args[0] == 'T':
                valid = True
            else:
                valid = False

            if valid == False:
                print("Invalid Syntax on line: " + line)
                break

    return valid

def sendCoordinates(command):
    global commandList
    command = command.split()
    x = int(command[1])
    y = int(command[2])
    commandList.append((x,y))


def sendTextData(command):
    global commandList
    word = command[2:-1]
    for letter in word:
        commandList.append(letter)


def readCommandFile():
    global commandList
    commandList = []
    if(verifyCommandFile()):
        commandFile = open("commands", 'r')
        if(verifyFileSyntax(commandFile)):
            commandFile.seek(0)

            for line in commandFile:
                arg = line[0]
                if arg == 'C':
                    sendCoordinates(line)
                else:
                    sendTextData(line)
    print(commandList)
    return commandList

readCommandFile()






