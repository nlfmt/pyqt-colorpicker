# ------------------------------------- #
#                                       #
# Modern Color Picker by Tom F.         #
# Version 1.4.2                         #
# made with Qt Creator & PyQt5          #
#                                       #
# ------------------------------------- #

import colorsys
from typing import Union

from PyQt5.QtCore import (QPoint, Qt)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QDialog, QGraphicsDropShadowEffect)

from .ui_dark import Ui_ColorPicker as Ui_Dark
from .ui_dark_alpha import Ui_ColorPicker as Ui_Dark_Alpha
from .ui_light import Ui_ColorPicker as Ui_Light
from .ui_light_alpha import Ui_ColorPicker as Ui_Light_Alpha

from .img import *


class ColorPicker(QDialog):

    def __init__(self, lightTheme: bool = False, useAlpha: bool = False):
        """Create a new ColorPicker instance.

        :param lightTheme: If the UI should be light themed.
        :param useAlpha: If the ColorPicker should work with alpha values.
        """

        # auto-create QApplication if it doesn't exist yet
        self.app = QApplication.instance()
        if self.app is None: self.app = QApplication([])

        super(ColorPicker, self).__init__()

        self.usingAlpha = useAlpha
        self.usingLightTheme = lightTheme

        # Call UI Builder function
        if useAlpha:
            if lightTheme: self.ui = Ui_Light_Alpha()
            else: self.ui = Ui_Dark_Alpha()
            self.ui.setupUi(self)
        else:
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
        self.ui.hue.mousePressEvent = self.moveHueSelector
        self.ui.hue.mouseMoveEvent = self.moveHueSelector
        self.ui.red.textEdited.connect(self.rgbChanged)
        self.ui.green.textEdited.connect(self.rgbChanged)
        self.ui.blue.textEdited.connect(self.rgbChanged)
        self.ui.hex.textEdited.connect(self.hexChanged)
        if self.usingAlpha: self.ui.alpha.textEdited.connect(self.alphaChanged)

        # Connect window dragging functions
        self.ui.title_bar.mouseMoveEvent = self.moveWindow
        self.ui.title_bar.mousePressEvent = self.setDragPos
        self.ui.window_title.mouseMoveEvent = self.moveWindow
        self.ui.window_title.mousePressEvent = self.setDragPos

        # Connect selector moving function
        self.ui.black_overlay.mouseMoveEvent = self.moveSVSelector
        self.ui.black_overlay.mousePressEvent = self.moveSVSelector

        # Connect Ok|Cancel Button Box and X Button
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.exit_btn.clicked.connect(self.reject)

        self.lastcolor = (0, 0, 0)
        self.color = (0, 0, 0)
        self.alpha = 100

    def getColor(self, lc: tuple = None):
        """Open the UI and get a color from the user.

        :param lc: The color to show as previous color.
        :return: The selected color.
        """

        if lc != None and self.usingAlpha:
            alpha = lc[3]
            lc = lc[:3]
            self.setAlpha(alpha)
            self.alpha = alpha
        if lc == None: lc = self.lastcolor
        else: self.lastcolor = lc

        self.setRGB(lc)
        self.rgbChanged()
        r,g,b = lc
        self.ui.lastcolor_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")

        if self.exec_():
            r, g, b = hsv2rgb(self.color)
            self.lastcolor = (r,g,b)
            if self.usingAlpha: return (r,g,b,self.alpha)
            return (r,g,b)

        else:
            return self.lastcolor

    # Update Functions
    def hsvChanged(self):
        h,s,v = (100 - self.ui.hue_selector.y() / 1.85, (self.ui.selector.x() + 6) / 2.0, (194 - self.ui.selector.y()) / 2.0)
        r,g,b = hsv2rgb(h,s,v)
        self.color = (h,s,v)
        self.setRGB((r,g,b))
        self.setHex(hsv2hex(self.color))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")
        self.ui.color_view.setStyleSheet(f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({h}%,100%,50%), stop:1 #fff);")

    def rgbChanged(self):
        r,g,b = self.i(self.ui.red.text()), self.i(self.ui.green.text()), self.i(self.ui.blue.text())
        cr,cg,cb = self.clampRGB((r,g,b))

        if r!=cr or (r==0 and self.ui.red.hasFocus()):
            self.setRGB((cr,cg,cb))
            self.ui.red.selectAll()
        if g!=cg or (g==0 and self.ui.green.hasFocus()):
            self.setRGB((cr,cg,cb))
            self.ui.green.selectAll()
        if b!=cb or (b==0 and self.ui.blue.hasFocus()):
            self.setRGB((cr,cg,cb))
            self.ui.blue.selectAll()

        self.color = rgb2hsv(r,g,b)
        self.setHSV(self.color)
        self.setHex(rgb2hex((r,g,b)))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")

    def hexChanged(self):
        hex = self.ui.hex.text()
        try:
            int(hex, 16)
        except ValueError:
            hex = "000000"
            self.ui.hex.setText("")
        r, g, b = hex2rgb(hex)
        self.color = hex2hsv(hex)
        self.setHSV(self.color)
        self.setRGB((r, g, b))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")

    def alphaChanged(self):
        alpha = self.i(self.ui.alpha.text())
        oldalpha = alpha
        if alpha < 0: alpha = 0
        if alpha > 100: alpha = 100
        if alpha != oldalpha or alpha == 0:
            self.ui.alpha.setText(str(alpha))
            self.ui.alpha.selectAll()
        self.alpha = alpha

    # Internal setting functions
    def setRGB(self, c):
        r,g,b = c
        self.ui.red.setText(str(self.i(r)))
        self.ui.green.setText(str(self.i(g)))
        self.ui.blue.setText(str(self.i(b)))

    def setHSV(self, c):
        self.ui.hue_selector.move(7, int((100 - c[0]) * 1.85))
        self.ui.color_view.setStyleSheet(f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({c[0]}%,100%,50%), stop:1 #fff);")
        self.ui.selector.move(int(c[1] * 2 - 6), int((200 - c[2] * 2) - 6))

    def setHex(self, c):
        self.ui.hex.setText(c)

    def setAlpha(self, a):
        self.ui.alpha.setText(str(a))

    # Dragging Functions
    def setDragPos(self, event):
        self.dragPos = event.globalPos()

    def moveWindow(self, event):
        # MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def moveSVSelector(self, event):
        if event.buttons() == Qt.LeftButton:
            pos = event.pos()
            if pos.x() < 0: pos.setX(0)
            if pos.y() < 0: pos.setY(0)
            if pos.x() > 200: pos.setX(200)
            if pos.y() > 200: pos.setY(200)
            self.ui.selector.move(pos - QPoint(6,6))
            self.hsvChanged()

    def moveHueSelector(self, event):
        if event.buttons() == Qt.LeftButton:
            pos = event.pos().y() - 7
            if pos < 0: pos = 0
            if pos > 185: pos = 185
            self.ui.hue_selector.move(QPoint(7, pos))
            self.hsvChanged()

    # Utility

    # Custom int() function, that converts invalid strings to 0
    def i(self, text):
        try: return int(text)
        except ValueError: return 0

    # clamp function to remove near-zero values
    def clampRGB(self, rgb):
        r, g, b = rgb
        if r<0.0001: r=0
        if g<0.0001: g=0
        if b<0.0001: b=0
        if r>255: r=255
        if g>255: g=255
        if b>255: b=255
        return r, g, b


# Color Utility
def hsv2rgb(h_or_color: Union[tuple, int], s: int = 0, v: int = 0, a: int = None) -> tuple:
    """Convert hsv color to rgb color.

    :param h_or_color: The 'hue' value or a color tuple.
    :param s: The 'saturation' value.
    :param v: The 'value' value.
    :param a: The 'alpha' value.
    :return: The converted rgb tuple color.
    """

    if type(h_or_color).__name__ == "tuple":
        if len(h_or_color) == 4:
            h, s, v, a = h_or_color
        else:
            h, s, v = h_or_color
    else: h = h_or_color
    r, g, b = colorsys.hsv_to_rgb(h / 100.0, s / 100.0, v / 100.0)
    if a is not None: return r * 255, g * 255, b * 255, a
    return r * 255, g * 255, b * 255


def rgb2hsv(r_or_color: Union[tuple, int], g: int = 0, b: int = 0, a: int = None) -> tuple:
    """Convert rgb color to hsv color.

    :param r_or_color: The 'red' value or a color tuple.
    :param g: The 'green' value.
    :param b: The 'blue' value.
    :param a: The 'alpha' value.
    :return: The converted hsv tuple color.
    """

    if type(r_or_color).__name__ == "tuple":
        if len(r_or_color) == 4:
            r, g, b, a = r_or_color
        else:
            r, g, b = r_or_color
    else: r = r_or_color
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    if a is not None: return h * 100, s * 100, v * 100, a
    return h * 100, s * 100, v * 100


def hex2rgb(hex: str) -> tuple:
    """Convert hex color to rgb color.

    :param hex: The hexadecimal string ("xxxxxx").
    :return: The converted rgb tuple color.
    """

    if len(hex) < 6: hex += "0"*(6-len(hex))
    elif len(hex) > 6: hex = hex[0:6]
    rgb = tuple(int(hex[i:i+2], 16) for i in (0,2,4))
    return rgb


def rgb2hex(r_or_color: Union[tuple, int], g: int = 0, b: int = 0, a: int = 0) -> str:
    """Convert rgb color to hex color.

    :param r_or_color: The 'red' value or a color tuple.
    :param g: The 'green' value.
    :param b: The 'blue' value.
    :param a: The 'alpha' value.
    :return: The converted hexadecimal color.
    """

    if type(r_or_color).__name__ == "tuple": r, g, b = r_or_color[:3]
    else: r = r_or_color
    hex = '%02x%02x%02x' % (int(r), int(g), int(b))
    return hex


def hex2hsv(hex: str) -> tuple:
    """Convert hex color to hsv color.

    :param hex: The hexadecimal string ("xxxxxx").
    :return: The converted hsv tuple color.
    """

    return rgb2hsv(hex2rgb(hex))


def hsv2hex(h_or_color: Union[tuple, int], s: int = 0, v: int = 0, a: int = 0) -> str:
    """Convert hsv color to hex color.

    :param h_or_color: The 'hue' value or a color tuple.
    :param s: The 'saturation' value.
    :param v: The 'value' value.
    :param a: The 'alpha' value.
    :return: The converted hexadecimal color.
    """

    if type(h_or_color).__name__ == "tuple": h, s, v = h_or_color[:3]
    else: h = h_or_color
    return rgb2hex(hsv2rgb(h, s, v))


# toplevel functions

__instance = None
__lightTheme = False
__useAlpha = False


def useAlpha(value=True) -> None:
    """Set if the ColorPicker should display an alpha field.

    :param value: True for alpha field, False for no alpha field. Defaults to True
    :return:
    """
    global __useAlpha
    __useAlpha = value


def useLightTheme(value=True) -> None:
    """Set if the ColorPicker should use the light theme.

    :param value: True for light theme, False for dark theme. Defaults to True
    :return: None
    """

    global __lightTheme
    __lightTheme = value


def getColor(lc: tuple = None) -> tuple:
    """Shows the ColorPicker and returns the picked color.

    :param lc: The color to display as previous color.
    :return: The picked color.
    """

    global __instance

    if __instance is None:
        __instance = ColorPicker(useAlpha=__useAlpha, lightTheme=__lightTheme)

    if __useAlpha != __instance.usingAlpha or __lightTheme != __instance.usingLightTheme:
        del __instance
        __instance = ColorPicker(useAlpha=__useAlpha, lightTheme=__lightTheme)

    return __instance.getColor(lc)

