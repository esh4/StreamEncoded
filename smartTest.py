from StartStopBitCodec import encode_image, decode_image
from PIL import Image
from SendReceiveImage import *

msg = open('testMsg.txt', 'r').read()
filename = 'testImg.png'
img = Image.open(filename)


def compare(s1, s2):
    disc = {}
    for l in range(max(len(s1), len(s2))):
        if s1[l] != s2[l]:
            disc[l] = [s1[l], s2[l]]
    return disc


encoded_img = encode_image(img, msg, (700, 1500), 200)
encoded_img.save('encoded.png')


print('\n\nstarting decode')

encoded_img = Image.open('encoded.png')
decoded_msg = decode_image(encoded_img)
print(decoded_msg)

# send_image('testImg__encoded.png')

# print(compare(msg, decoded_msg))


