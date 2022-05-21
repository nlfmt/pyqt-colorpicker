from vcolorpicker import getColor, useLightTheme, useAlpha

old_color = (255, 255, 255)
picked_color = getColor(old_color)
print(picked_color)

useLightTheme(True)
useAlpha(True)

old_color = (255, 230, 255, 50)
picked_color = getColor(old_color)
print(picked_color)


# Using the old way of creating a ColorPicker:
from vcolorpicker import ColorPicker, hsv2rgb, rgb2hsv


my_color_picker = ColorPicker(useAlpha=True)
my_color_picker_light = ColorPicker(lightTheme=True)


old_color = (255, 255, 255, 50)
picked_color = my_color_picker.getColor(old_color)
print(picked_color)


old_color = (255,0,255)
picked_color = my_color_picker_light.getColor(old_color)
print(picked_color)


# Don't have your color in RGB format?
my_color = (50, 50, 100, 60)  # HSV Color in percent
old_color = hsv2rgb(my_color)
picked_color = rgb2hsv(my_color_picker.getColor(old_color))
print(picked_color)
