# TODO: verivy that the size can actually hold the entire message
# todo: make sure the size + location actually fit in the image

### NEW IDEA - instead of size, just have a message_width

def encode_image(img, msg, start_location=(50, 700), **kwargs):
    """
    :param img: image to encode message into
    :param msg:
    :param start_location: location of start bit
    :param kwarg: size: tuple with dimentions of submatrix
    :return:
    """

    encoded = img.copy()
    width, height = img.size
    print('image size: {} x {}'.format(width, height))
    row_offset, col_offset = start_location
    msg_index = 0

    if 'size' in kwargs:
        size = kwargs['size']
    else:
        size = width - col_offset

    encoded.putpixel((0, 0), (size, start_location[0], start_location[1]))     # add the message's location to the top of the image

    # print('size', size)
    for row in range(row_offset, height):
        for col in range(col_offset, min(col_offset + size, width)):
            r, g, b = img.getpixel((col, row))
            if msg_index < len(msg):
                asc = ord(msg[msg_index])
            elif msg_index == len(msg):     # end of the massage
                asc = r
            elif msg_index == len(msg) + 1:
                asc = ord('#')    # stop bit
                print('stop bit added')
            else:
                asc = r
            msg_index += 1
            encoded.putpixel((col, row), (asc, g, b))
            # print(col, row)
    return encoded


def decode_image(img):
    width, height = img.size

    # find message location and width
    try:
        r, g, b = img.getpixel((0, 0))
    except ValueError:
        # need to add transparency a for some
        r, g, b, a = img.getpixel((0, 0))

    start_location = (g, b)     # (row, col)
    message_width = r
    print('starting location', start_location)
    print('message width ', message_width)

    def loop():
        msg = ''
        index = 0
        for row in range(start_location[0], height):
            for col in range(start_location[1], min(start_location[1] + message_width, width)):
                try:
                    r, g, b = img.getpixel((col, row))
                except ValueError:
                    # need to add transparency a for some
                    r, g, b, a = img.getpixel((col, row))
                if chr(r) != '#':
                    msg += chr(r)
                else:
                    print('found stop bit: ', chr(g))
                    return msg
                index += 1

    msg = loop()
    return msg

