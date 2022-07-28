import cv2
from pyzbar import pyzbar

# QR scanning
def read_barcode(frame):
    barcodes = pyzbar.decode(frame)
    barcode_info = ''
    for barcode in barcodes:
        x, y, w, h = barcode.rect

        # 1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

    return frame, barcode_info

# camera access
def start_scan():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    #2
    while ret:
        ret, frame = camera.read()
        frame, code = read_barcode(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27 or code != '':
            break
    #3
    camera.release()
    cv2.destroyAllWindows()

    return code
