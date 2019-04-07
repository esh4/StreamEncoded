from StartStopBitCodec import encode_image, decode_image
from PIL import Image

msg = open('testMsg.txt', 'r').read()
filename = 'testImg.png'
img = Image.open(filename)


def compare(s1, s2):
    disc = {}
    for l in range(max(len(s1), len(s2))):
        if s1[l] != s2[l]:
            disc[l] = [s1[l], s2[l]]
    return disc

try:
    encoded_img = encode_image(img, msg, (600, 0))
    encoded_img.save('encoded.png')

    encoded_img = Image.open('encoded.png')
    decoded_msg = decode_image(encoded_img)
    print(decoded_msg)
    print(compare(msg, decoded_msg))

except Exception as e:
    print(e.with_traceback())


