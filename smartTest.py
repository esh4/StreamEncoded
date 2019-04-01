from .test import encode_image
from PIL import Image

msg = input('enter message: ')
filename = input('enter filename')

img = Image.open(filename)
try:
    encode_image(img, msg)

except Exception as e:
    print(e)
