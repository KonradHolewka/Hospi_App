import pyqrcode
import platform

# new qc code generation
def new_qr(code):
    qr = pyqrcode.create(code)
    # path for Windows!

    if platform.system() == "Windows":
        filename = "./patients_qrcodes/" + code + "_qrcode.png"
    # path for Android!
    else:
        filename = "/storage/emulated/0/Documents/" + code + "_qrcode.png"
    qr.png(filename, scale=16)