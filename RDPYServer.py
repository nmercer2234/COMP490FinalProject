__author__ = 'Ramya Shimoga Prakash'
import sys
from datetime import datetime
import time
from rdpy.protocol.rdp import rdp
from rdpy.core.error import CallPureVirtualFuntion, InvalidValue
import rdpy.core.log as log
log._LOG_LEVEL = log.Level.INFO
from pymouse import PyMouse
from pykeyboard import PyKeyboard


class RDPServer(rdp.ServerFactory):

    """
    @summary: Factory of Server RDP protocol
    """
    def __init__(self, colorDepth = 24, privateKeyFileName = None, certificateFileName = None):
        """
        @param colorDepth: color depth of session
        @param privateKeyFileName: file contain server private key (if none -> back to standard RDP security)
        @param certficiateFileName: file that contain public key (if none -> back to standard RDP security)
        """
        self._colorDepth = colorDepth
        self._privateKeyFileName = privateKeyFileName
        self._certificateFileName = certificateFileName

    def buildObserver(self, controller, addr):

        class MyObserver(rdp.RDPServerObserver):

            def onReady(self):
                """
                @summary: Call when server is ready
                to send and receive messages
                """
                log.info("onReady")

            def onKeyEventScancode(self, code, isPressed):
                """
                @summary: Event call when a keyboard event is catch in scan code format
                @param code: scan code of key
                @param isPressed: True if key is down
                @see: rdp.RDPServerObserver.onKeyEventScancode
                """
                if not isPressed:
                    k.type_string(chr(code))
                    log.info("KeyEventScancode: " + chr(code))

            def onKeyEventUnicode(self, code, isPressed):
                """
                @summary: Event call when a keyboard event is catch in unicode format
                @param code: unicode of key
                @param isPressed: True if key is down
                @see: rdp.RDPServerObserver.onKeyEventUnicode
                """
                if not isPressed:
                    k.type_string(chr(code))
                    log.info("KeyEventUnicode: " + chr(code))

            def onPointerEvent(self, x, y, button, isPressed):
                """
                @summary: Event call on mouse event
                @param x: x position
                @param y: y position
                @param button: 1, 2 or 3 button
                @param isPressed: True if mouse button is pressed
                @see: rdp.RDPServerObserver.onPointerEvent
                """
                if isPressed:
                    m.press(x, y, button)
                    time.sleep(0.05)
                    m.release(x, y)
                else:
                    m.move(x, y)
                log.info("PointerEvent: " + str(x) + " " + str(y) + " @" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            def onClose(self):
                """
                @summary: Call when human client close connection
                @see: rdp.RDPServerObserver.onClose
                """

        return MyObserver(controller)

from twisted.internet import reactor


if __name__ == '__main__':
    if len(sys.argv) == 2:
        m = PyMouse()
        k = PyKeyboard()
        x_dim, y_dim = m.screen_size()
        reactor.listenTCP(int(sys.argv[1]), RDPServer())
        reactor.run()
    else:
        log.info("Please provide the port")