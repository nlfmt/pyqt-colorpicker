from colorpicker import ColorPicker
from PyQt5.QtWidgets import QApplication

app = QApplication([])

my_color_picker = ColorPicker()
my_color_picker_light = ColorPicker(lightTheme=True)

old_color = (255,255,255)

picked_color = my_color_picker.getColor(old_color)
print(picked_color)

picked_color = my_color_picker_light.getColor()
print(picked_color)
