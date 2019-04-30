import sys, os, subprocess


def verify_image_format(encoder_decoder_func):
    # make this a cool decorator for the functions
    pass

def open_file(filename):
    """
    Open a file with the os's default application on any platform.
    os.startfile is only supported on Windows...
    :param filename: String; file to open
    :return:
    """
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


class MessageOverflowError(Exception):
    pass
