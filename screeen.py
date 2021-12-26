
from PIL import ImageGrab
import mkascii

while True:
    screenshot = ImageGrab.grab()
    mkascii.frame(screenshot)