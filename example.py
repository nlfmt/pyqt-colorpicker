from colorpicker import ColorPicker
from PyQt5.QtWidgets import QApplication

app = QApplication([])

my_color_picker = ColorPicker(useAlpha=True)
my_color_picker_light = ColorPicker(lightTheme=False)

old_color = (255,255,255)

picked_color = my_color_picker.getRGB(old_color)
print(picked_color)

picked_color = my_color_picker_light.getColor()
print(picked_color)
