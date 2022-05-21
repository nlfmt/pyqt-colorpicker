"""
vcolorpicker

Simply let a user pick a color using a visual selector.
"""

__version__ = "1.4.0"
__author__ = 'nlfmt'

from .vcolorpicker import ColorPicker
from .vcolorpicker import hsv2rgb, hsv2hex, rgb2hsv, rgb2hex, hex2rgb, hex2hsv
from .vcolorpicker import getColor, useAlpha, useLightTheme

