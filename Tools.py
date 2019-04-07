import sys, os, subprocess


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


