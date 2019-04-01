class ImageCodec:
    @staticmethod
    def encode_image(img, msg):
        raise NotImplemented()

    @staticmethod
    def decode_image(img):
        raise NotImplemented()


class BasicCodec(ImageCodec):
    pass


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
