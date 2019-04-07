
''' PIL_HideText1.py
hide a short message (255 char max) in an image
the image has to be .bmp or .png format
and the image mode has to be 'RGB'
'''
from PIL import Image
import os, sys, subprocess


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def encode_image_stop_bit(img, msg):
    if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if index < len(msg):
                asc = ord(msg[index])
            elif index == len(msg):
                asc = r
                g = ord('#')
                print('stop bit added')
            else:
                asc = r
            index += 1
            encoded.putpixel((col, row), (asc, g, b))
    return encoded


def decode_image_stop_bit(img):
    width, height = img.size
    def loop():
        msg = ''
        index = 0
        for row in range(height):
            for col in range(width):
                try:
                    r, g, b = img.getpixel((col, row))
                except ValueError:
                    # need to add transparency a for some .png files
                    r, g, b, a = img.getpixel((col, row))
                if chr(g) != '#':
                    msg += chr(r)
                    # print(str(r) + ' -> ' + chr(r))
                else:
                    return msg
                index += 1
    msg = loop()
    return msg


# pick a .png or .bmp file you have in the working directory
# or give full path name
original_image_file = "testImg.png"
# original_image_file = "Beach7.bmp"
img = Image.open(original_image_file)
# image mode needs to be 'RGB'
print(img, img.mode)  # test
# create a new filename for the modified/encoded image
encoded_image_file = "enc_" + original_image_file
# don't exceed 255 characters in the message
secret_msg = open('testMsg.txt').read()
print(len(secret_msg))  # test
img_encoded = encode_image_stop_bit(img, secret_msg)
if img_encoded:
    # save the image with the hidden text
    img_encoded.save(encoded_image_file)
    print("{} saved!".format(encoded_image_file))
    # view the saved file, works with Windows only
    # behaves like double-clicking on the saved file

    open_file(encoded_image_file)
    '''
    # or activate the default viewer associated with the image
    # works on more platforms like Windows and Linux
    import webbrowser
    webbrowser.open(encoded_image_file)
    '''
    # get the hidden text back ...
    img2 = Image.open(encoded_image_file)
    hidden_text = decode_image_stop_bit(img2)
    # print("Hidden text:\n{}".format(hidden_text))

