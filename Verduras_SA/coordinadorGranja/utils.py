import cv2
import pytesseract
import numpy as np
import re
import platform
import shutil

so = platform.system()

if so == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"D:\Programas\Tesseract-OCR\tesseract.exe"
else:
    t_path = shutil.which("tesseract")
    if t_path:
        pytesseract.pytesseract.tesseract_cmd = t_path
    else:
        print("⚠ Tesseract no encontrado. Instálalo con: sudo apt install tesseract-ocr")


def process_image_and_read_plate(image_cv):
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    plate_contour = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            plate_contour = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    if plate_contour is not None:
        cv2.drawContours(mask, [plate_contour], 0, 255, -1)
        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped = gray[x1:x2 + 1, y1:y2 + 1]
    else:
        cropped = gray  # fallback

    thresh = cv2.adaptiveThreshold(
        cropped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 35, 11
    )

    config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    raw_text = pytesseract.image_to_string(thresh, config=config).strip()

    cleaned = re.sub(r'[^A-Z0-9]', '', raw_text)
    match = re.search(r'[A-Z]{3}\d{2,3}[A-Z0-9]?', cleaned)

    plate = match.group(0) if match else cleaned

    return plate, raw_text
