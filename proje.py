import cv2
import pytesseract
from pytesseract import Output
from rapidfuzz import fuzz
import re


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
IMAGE_PATH = r"C:\Users\rusen\Desktop\7c36522c-5cd9-46cd-bc2f-4322b82cd22c.jpg"


img = cv2.imread(IMAGE_PATH)
if img is None:
    raise FileNotFoundError(f"Resim bulunamadı: {IMAGE_PATH}")

scale = 1.4
img = cv2.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_LINEAR)

# Ön işlem
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 9, 75, 75)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 15, 8)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

data = pytesseract.image_to_data(thresh, lang="tur+eng", config="--psm 6", output_type=Output.DICT)

lines = {}
for i in range(len(data['text'])):
    t = data['text'][i].strip()
    if t == "":
        continue
    key = (data['block_num'][i], data['line_num'][i])
    lines.setdefault(key, []).append(t)

line_texts = [" ".join(lines[k]) for k in sorted(lines.keys())]


koyun_lines = [lt for lt in line_texts if fuzz.partial_ratio(lt.upper(), "KOYUN") >= 75]


def is_header_line(s):
    u = s.upper()
    keywords = ["İŞLETME", "ISLETME", "HAYVAN", "RAPORU", "KOYUN KEG", "KOYUN KEGI"]
    return any(k in u for k in keywords)


filtered = koyun_lines.copy()
if len(koyun_lines) > 0 and is_header_line(koyun_lines[0]):
    filtered = koyun_lines[1:]


final_count = len(filtered)


print("----- Bulunan 'KOYUN' satırları (başlık çıkarıldı) -----")
for s in filtered[:40]:
    print("-", s)

print("\n***** SONUÇ: Bu görsel için bulunan koyun sayısı (satır bazlı):", final_count, "*****")
