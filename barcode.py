import pyqrcode
import platform

# tworzenie nowego kodu qr
def new_qr(code):
    qr = pyqrcode.create(code)
    # sciezka w Windowsie!

    if platform.system() == "Windows":
        filename = code + "_qrcode.png"
    # sciezka w Androidzie!
    else:
        filename = "/storage/emulated/0/Documents/" + code + "_qrcode.png"
    qr.png(filename, scale=16)