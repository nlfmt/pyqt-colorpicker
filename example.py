from colorpicker import ColorPicker
from PyQt5.QtWidgets import QApplication

app = QApplication([])

my_color_picker = ColorPicker(lightTheme=False)

old_color = (255,255,255)

picked_color = my_color_picker.getColor(old_color)

print(picked_color)
