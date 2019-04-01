class ImageCodec:
    @staticmethod
    def encode_image(img, msg):
        raise NotImplemented()

    @staticmethod
    def decode_image(img):
        raise NotImplemented()


class BasicCodec(ImageCodec):
    @staticmethod
    def encode_image(img, msg):
        """
        use the red portion of an image (r, g, b) tuple to
        hide the msg string characters as ASCII values
        red value of the first pixel is used for length of string
        """
        length = len(msg)
        # limit length of message to 255
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return False
        # use a copy of image to hide the text in
        encoded = img.copy()
        width, height = img.size
        index = 0
        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index - 1]
                    asc = ord(c)
                else:
                    asc = r
                encoded.putpixel((col, row), (asc, g, b))
                index += 1
        return encoded

    @staticmethod
    def decode_image(img):
        def decode_image(img):
            """
            check the red portion of an image (r, g, b) tuple for
            hidden message characters (ASCII values)
            """
            width, height = img.size
            msg = ""
            index = 0
            for row in range(height):
                for col in range(width):
                    try:
                        r, g, b = img.getpixel((col, row))
                    except ValueError:
                        # need to add transparency a for some .png files
                        r, g, b, a = img.getpixel((col, row))
                    # first pixel r value is length of message
                    if row == 0 and col == 0:
                        length = r
                    elif index <= length:
                        msg += chr(r)
                    index += 1
            return msg


class StopBitCodec(ImageCodec):
    @staticmethod
    def encode_image(img, msg):
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

    @staticmethod
    def decode_image(img):
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


class StartStopCodec(ImageCodec):
    pass
