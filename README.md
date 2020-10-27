# PyQt5 Color Picker
Simple Color Picker with a modern UI created with PyQt5 to easily get color input from the user.

![colorpicker](https://user-images.githubusercontent.com/71983360/95017068-408f8100-0657-11eb-8001-a6788e94abba.png)


## Usage

1. To use the Color Picker in a python project make sure you have the `PyQt5` library:

   ```
   pip install PyQt5
   ```

   then add the `colorpicker` folder into your project folder and import `ColorPicker`, and `QApplication`

   ```python
   from colorpicker import ColorPicker
   from PyQt5.QtWidgets import QApplication
   ```

2. To ask for a color first create a `QApplication`:

   ```python
   app = QApplication([])
   ```

   then simply create an instance of the class:

   ```python
   my_color_picker = ColorPicker()
   ```

   and run the `getColor` method:

   ```python
   picked_color = my_color_picker.getColor()
   ```

## Customization

* **Showing custom last color:**

   ```python
   old_color = (255,255,255)
   picked_color = my_color_picker.getColor(old_color)
   ```

* **Changing the UI Theme**

  ```python
  my_color_picker = ColorPicker(lightTheme=True)
  ```

* **Adding Alpha selection**

  ```python
  my_color_picker = ColorPicker(useAlpha=True)
  ```

  When the ColorPicker uses Alpha, you have to pass a RGBA tuple\
  as the last color, otherwise there wil be an error.

  ```python
  my_color_picker = ColorPicker(useAlpha=True)

  old_color = (255,255,255,100)
  picked_color = my_color_picker.getColor(old_color) # => (r,g,b,a)
  ```

## Color Formats and Conversion

* The default format `getColor` will give you is RGB(A),\
  but you can use Colorpickers color conversion functions\
  if you have a different format like HSV or HEX.

   `hsv2rgb` **HSV(A)** to **RGB(A)**\
   `rgb2hsv` **RGB(A)** to **HSV(A)**\
   `rgb2hex` **RGB(A)** to **HEX**\
   `hex2rgb` **HEX** to **RGB**\
   `hex2hsv` **HEX** to **HSV**\
   `hsv2hex` **HSV(A)** to **HEX**

* Example:
  ```python
  cp = ColorPicker(useAlpha=True)

  old_color = cp.hsv2rgb((50,50,100,100))  # => (127,255,255,100)

  picked_color = cp.rgb2hsv(cp.getColor(old_color))
  ```

* **Color Formats:**

  **RGB** values range from **0** to **255**\
  **HSV** values range from **0** to **100**\
  **HEX** values should be in format: `"XXXXXX"` or `"xxxxxx"`\
  **Alpha** values range from **0** to **100**


## License

  This software is licensed under the **MIT License**.\
  More information is provided in the dedicated LICENSE file.
