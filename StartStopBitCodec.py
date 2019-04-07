def encode_image(img, msg, start_location=(50, 700)):
    """
    :param img: image to encode message into
    :param msg:
    :param start_location: location of start bit
    :return:
    """
    encoded = img.copy()
    width, height = img.size
    print('image size: {} x {}'.format(width, height))
    row_offset, col_offset = start_location
    msg_index = 0

    r, g, b = img.getpixel(start_location)
    encoded.putpixel((0, 0), (r, start_location[0], start_location[1]))

    for row in range(row_offset, height):
        for col in range(width):
            r, g, b = img.getpixel((min(col + col_offset*(row == row_offset), width - 1), row))
            if msg_index < len(msg):
                asc = ord(msg[msg_index])
            elif msg_index == len(msg):
                asc = r
                g = ord('#')
                print('stop bit added')
            else:
                asc = r
            msg_index += 1
            encoded.putpixel((min(col + col_offset*(row == row_offset), width - 1), row), (asc, g, b))
    return encoded


def decode_image(img):
    width, height = img.size

    # find message location
    try:
        r, g, b = img.getpixel((0, 0))
    except ValueError:
        # need to add transparency a for some
        r, g, b, a = img.getpixel((0, 0))

    start_location = (g, b)     # (row, col)
    print(start_location)

    def loop():
        msg = ''
        index = 0
        for row in range(start_location[0], height):
            for col in range(width):
                try:
                    r, g, b = img.getpixel((min(col + start_location[1]*(row == start_location[0]), width - 1), row))
                except ValueError:
                    # need to add transparency a for some
                    r, g, b, a = img.getpixel((min(col + start_location[1]*(row == start_location[0]), width - 1), row))
                if chr(g) != '#':
                    msg += chr(r)
                else:
                    return msg
                index += 1

    msg = loop()
    return msg

