from Tools import MessageOverflowError
from math import ceil
import re

# TODO: verivy that the size can actually hold the entire message
# todo: make sure the size + location actually fit in the image

def scale(num, scalefrom, scaleto):
    """
    scales a number from (0 - scalefrom) to (0 - scaleto)
    :param num:
    :param scalefrom:
    :param scaleto:
    :return:
    """
    return ceil((scaleto * num) / scalefrom)


def verify_message_len(func):
    def wrapper(img, msg, start_location, message_width):
        """
        this function checks that the message will fit into the picture.
        :param xy: coordinates beginning of the message
        :param wh: width and height of the image
        :param message_width:
        :return:
        """
        wh = img.size
        if start_location[0]*100 != 0 or start_location[1] % 100 != 0:
            # raise ValueError('please insert a whole number')
            print('WARNING', 'your starting location might be shit')

        if start_location[0] + message_width > wh[0]:
            print('WARNING: ', 'Your message width will be trimmed at the edge of the image. \n'
                               'updating message length to fit image.')
            message_width = wh[0] - start_location[0]
            print('message width now {0}'.format(message_width))

        message_height = ceil(len(msg)/message_width)      # how many rows the massage will take up

        if start_location[1] + message_height > wh[1]:
            raise MessageOverflowError('message takes up {} rows!'.format(message_height))

        return func(img, msg, start_location, message_width=message_width)

    return wrapper


@verify_message_len
def encode_image(img, msg, start_location=(50, 700), **kwargs):
    """
    :param img: image to encode message into
    :param msg:
    :param start_location: location of start bit. IMPORTANT - the format is desired location / 100.
                            ****for example: if i want to start the pixel 700 i will write 7 as the parameter****
    :param kwarg: size: tuple with dimentions of submatrix
    :return:
    """
    encoded = img.copy()
    width, height = img.size
    print('image size: {} x {}'.format(width, height))

    col_offset, row_offset = start_location
    msg_index = 0

    if 'message_width' in kwargs:
        message_width = kwargs['message_width']
    else:
        message_width = width - col_offset

    # scale message location
    start_location = scale(start_location[0], width, 255), scale(start_location[1], height, 255)

    encoded.putpixel((0, 0), (message_width, start_location[0], start_location[1]))     # add the message's location to the top of the image

    for row in range(row_offset, height):
        for col in range(col_offset, min(col_offset + message_width, width)):
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
    print('starting location pre scale', start_location)
    # scale back to normal
    start_location = round(scale(start_location[0], 255, width), - 2), round(scale(start_location[1], 255, height), - 2)

    message_width = r
    print('starting location post re-scale', start_location)
    print('message width ', message_width)

    def loop():     # function used to 'break' out of two loops
        msg = ''
        index = 0
        for row in range(start_location[1], height):
            for col in range(start_location[0], min(start_location[0] + message_width, width)):
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

    # strip off null bits
    stripped = ''
    for x in range(len(msg)):
        if ord(msg[x]) != 0:
            stripped += msg[x]

    return stripped

