# ------------------------------------- #
#                                       #
# Modern Color Picker by Tom F.         #
# Version 1.0.0                         #
# made with Qt Creator & PyQt5          #
#                                       #
# ------------------------------------- #

import sys
import colorsys

from PyQt5.QtCore import (QPoint, Qt)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QDialog, QGraphicsDropShadowEffect)


from .ui_dark import Ui_ColorPicker as Ui_Dark
from .ui_light import Ui_ColorPicker as Ui_Light


class ColorPicker(QDialog):

    def __init__(self, lightTheme=False):
        super(ColorPicker, self).__init__()

        # Call UI Builder function
        if lightTheme: self.ui = Ui_Light()
        else: self.ui = Ui_Dark()
        self.ui.setupUi(self)

        # Make Frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Color Picker")

        # Add DropShadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)

        # Connect update functions
        self.ui.hue.sliderMoved.connect(self.hsvChanged)
        self.ui.red.textEdited.connect(self.rgbChanged)
        self.ui.green.textEdited.connect(self.rgbChanged)
        self.ui.blue.textEdited.connect(self.rgbChanged)
        self.ui.hex.textEdited.connect(self.hexChanged)

        # Connect window dragging functions
        self.ui.title_bar.mouseMoveEvent = self.moveWindow
        self.ui.title_bar.mousePressEvent = self.setDragPos
        self.ui.window_title.mouseMoveEvent = self.moveWindow
        self.ui.window_title.mousePressEvent = self.setDragPos

        # Connect selector moving function
        self.ui.black_overlay.mouseMoveEvent = self.moveSelector
        self.ui.black_overlay.mousePressEvent = self.moveSelector

        # Connect Ok|Cancel Button Box and X Button
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.exit_btn.clicked.connect(self.reject)

        self.lastcolor = (0,0,0)
        self.color = (0,0,0)


    ## Main Function ##
    def getColor(self, lc=None):
            if lc == None: lc = self.lastcolor
            else: self.lastcolor = lc

            self.setRGB(self.rgb2hsv(lc))
            self.rgbChanged()
            r,g,b = self.hsv2rgb(lc)
            self.ui.lastcolor_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")

            if self.exec_():
                r, g, b = self.hsv2rgb(self.color)
                return (r,g,b)

            else:
                return self.lastcolor


    ## Update Functions ##
    def hsvChanged(self):
        h,s,v = (self.ui.hue.value(), (self.ui.selector.x() + 6) / 2.0, (194 - self.ui.selector.y()) / 2.0)
        r,g,b = self.hsv2rgb(h,s,v)
        self.color = (h,s,v)
        self.setRGB(self.color)
        self.setHex(self.color)
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")
        self.ui.color_view.setStyleSheet(f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({h}%,100%,50%), stop:1 #fff);")

    def rgbChanged(self):
        r,g,b = int(self.ui.red.text()), int(self.ui.green.text()), int(self.ui.blue.text())
        self.color = self.rgb2hsv(r,g,b)
        self.setHSV(self.color)
        self.setHex(self.color)
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")

    def hexChanged(self):
        hex = self.ui.hex.text()
        r,g,b = self.hex2rgb(hex)
        self.color = self.hex2hsv(hex)
        self.setHSV(self.color)
        self.setRGB(self.color)
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")


    def setRGB(self, c):
        r,g,b = self.hsv2rgb(c)
        self.ui.red.setText(str(int(r)))
        self.ui.green.setText(str(int(g)))
        self.ui.blue.setText(str(int(b)))

    def setHSV(self, c):
        self.ui.hue.setValue(c[0])
        self.ui.color_view.setStyleSheet(f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({c[0]}%,100%,50%), stop:1 #fff);")
        self.ui.selector.move(c[1] * 2 - 6, (200 - c[2] * 2) - 6)

    def setHex(self, c):
        self.ui.hex.setText(self.hsv2hex(c))


    ## Color Utility ##
    def hsv2rgb(self, h_or_color, s = 0, v = 0):
        if type(h_or_color).__name__ == "tuple": h,s,v = h_or_color
        else: h = h_or_color
        r,g,b = colorsys.hsv_to_rgb(h / 100.0, s / 100.0, v / 100.0)
        return (r * 255, g * 255, b * 255)

    def rgb2hsv(self, r_or_color, g = 0, b = 0):
        if type(r_or_color).__name__ == "tuple": r,g,b = r_or_color
        else: r = r_or_color
        h,s,v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        return (h * 100, s * 100, v * 100)

    def hex2rgb(self, hex):
        if len(hex) < 6: hex += "0"*(6-len(hex))
        elif len(hex) > 6: hex = hex[0:6]
        rgb = tuple(int(hex[i:i+2], 16) for i in (0,2,4))
        return rgb

    def rgb2hex(self, r_or_color, g = 0, b = 0):
        if type(r_or_color).__name__ == "tuple": r,g,b = r_or_color
        else: r = r_or_color
        hex = '%02x%02x%02x' % (int(r),int(g),int(b))
        return hex

    def hex2hsv(self, hex):
        return self.rgb2hsv(self.hex2rgb(hex))

    def hsv2hex(self, h_or_color, s = 0, v = 0):
        if type(h_or_color).__name__ == "tuple": h,s,v = h_or_color
        else: h = h_or_color
        return self.rgb2hex(self.hsv2rgb(h,s,v))


    ## Dragging Functions ##
    def setDragPos(self, event):
        self.dragPos = event.globalPos()

    def moveWindow(self, event):
        # MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def moveSelector(self, event):
        if event.buttons() == Qt.LeftButton:
            pos = event.pos()
            if pos.x() < 0: pos.setX(0)
            if pos.y() < 0: pos.setY(0)
            if pos.x() > 200: pos.setX(200)
            if pos.y() > 200: pos.setY(200)
            self.ui.selector.move(pos - QPoint(6,6))
            self.hsvChanged()


if __name__ == "__main__":
    app = QApplication([])
    cp = ColorPicker()
    cp.getColor()
