__author__ = 'Ramya Shimoga Prakash'
import sys
import time
import threading

from rdpy.protocol.rdp import rdp
import rdpy.core.log as log
log._LOG_LEVEL = log.Level.INFO
from twisted.internet import reactor

import translator
import interpretCommandFiles


class MouseMover(threading.Thread):
    _controller = None
    _currX = 0
    _currY = 0
    _destX = 0
    _destY = 0
    _sleep = 0.0040
    _stepSize = 5

    def __init__(self, controller, currX, currY, destX, destY):
        self._controller = controller
        self._currX = currX
        self._currY = currY
        self._destX = destX
        self._destY = destY
        threading.Thread.__init__(self)

    def run(self):
        if self._currX > self._destX:
            while self._currX > self._destX:
                self._currX -= self._stepSize
                if self._currY > self._destY:
                    self._currY -= self._stepSize
                elif self._currY < self._destY:
                    self._currY += self._stepSize
                time.sleep(self._sleep)
                self._controller.sendPointerEvent(self._currX, self._currY, 1, False)
                if self._currX < self._destX:
                    break
        if self._currX < self._destX:
            while self._currX < self._destX:
                self._currX += self._stepSize
                if self._currY > self._destY:
                    self._currY -= self._stepSize
                elif self._currY < self._destY:
                    self._currY += self._stepSize
                time.sleep(self._sleep)
                self._controller.sendPointerEvent(self._currX, self._currY, 1, False)
                if self._currX > self._destX:
                    break
        if self._currY > self._destY:
            while self._currY > self._destY:
                self._currY -= self._stepSize
                time.sleep(self._sleep)
                self._controller.sendPointerEvent(self._currX, self._currY, 1, False)
                if self._currY < self._destY:
                    break
        if self._currY < self._destY:
            while self._currY < self._destY:
                self._currY += self._stepSize
                time.sleep(self._sleep)
                self._controller.sendPointerEvent(self._currX, self._currY, 1, False)
                if self._currY > self._destY:
                    break


class Worker(threading.Thread):
    _controller = None
    posX = 0
    posY = 0
    last_x = 0
    last_y = 0

    def __init__(self, controller):
        self.offset_x = int(sys.argv[3]) + 10
        self.offset_y = int(sys.argv[4]) + 10
        self._controller = controller
        threading.Thread.__init__(self)

    def run(self):
        self.executeCommands()

    def executeCommands(self):
        for command in commandsToSend:
            if type(command) == tuple:
                if command[0] >= 0 and command[1] >= 0:
                    self.sendPointerEventToServer(command[0] + self.offset_x, command[1] + self.offset_y)
                else:
                    log.info("Invalid co-ordinates provided")
            elif type(command) == str:
                self.sendCharacterCode(command)
        connection.disconnect()


    def sendPointerEventToServer(self, x, y):
        self.posX = x
        self.posY = y
        self.new_x = self.posX
        self.new_y = self.posY
        log.info("Moving towards: " + str(self.new_x) + ", " + str(self.new_y))
        mover = MouseMover(self._controller, self.last_x, self.last_y, self.new_x, self.new_y)
        self.last_x = self.posX
        self.last_y = self.posY
        mover.start()
        mover.join()
        log.info("Clicking at: " + str(self.last_x) + ", " + str(self.last_y))
        self._controller.sendPointerEvent(self.last_x, self.last_y, 1, True)

    def sendCharacterCode(self, char):
        self._controller.sendKeyEventUnicode(ord(char.encode(encoding='UTF-8', errors='ignore')), False)
        time.sleep(0.25)


class RDPClient(rdp.ClientFactory):

    def clientConnectionLost(self, connector, reason):
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def buildObserver(self, controller, addr):

        class MyObserver(rdp.RDPClientObserver):

            def onReady(self):
                """
                @summary: Call when stack is ready
                """
                worker = Worker(self._controller)
                worker.start()


            def onUpdate(self, destLeft, destTop, destRight, destBottom, width, height, bitsPerPixel, isCompress, data):
                """
                @summary: Notify bitmap update
                @param destLeft: xmin position
                @param destTop: ymin position
                @param destRight: xmax position because RDP can send bitmap with padding
                @param destBottom: ymax position because RDP can send bitmap with padding
                @param width: width of bitmap
                @param height: height of bitmap
                @param bitsPerPixel: number of bit per pixel
                @param isCompress: use RLE compression
                @param data: bitmap data
                """

            def onClose(self):
                """
                @summary: Call when stack is close
                """

        return MyObserver(controller)


if __name__ == '__main__':
    if len(sys.argv) == 5:
        translator.execute("UserInterface.txt", "UserInput.txt")
        commandsToSend = []
        commandsToSend = interpretCommandFiles.readCommandFile()
        if len(commandsToSend) > 0:
            connection = reactor.connectTCP(str(sys.argv[1]), int(sys.argv[2]), RDPClient())
            reactor.run()
    else:
        log.info("Please provide the ip address, port and the offsets for the GUI")
        log.info("Usage: python RDPYClient.py <ip address> <port> <x-offset> <y-offset>")