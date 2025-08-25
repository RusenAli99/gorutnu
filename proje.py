import cv2
import pytesseract
from fuzzywuzzy import fuzz

# Tesseract yolu (Windows için)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Görseli oku
img = cv2.imread("C:\\Users\\rusen\\Desktop\\7c36522c-5cd9-46cd-bc2f-4322b82cd22c.jpg")

# Griye çevir ve threshold uygula
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

# OCR işlemi
metin = pytesseract.image_to_string(thresh, lang="tur+eng").upper()

# Tüm kelimeleri ayır
kelimeler = metin.split()

# Tür filtreleri
kucukbas_turleri = ["KOYUN", "KEÇİ"]
buyukbas_turleri = ["SIĞIR", "İNEK", "MANDA", "DANA"]

# Sayaçlar
kucukbas_sayisi = 0
buyukbas_sayisi = 0

# Kelime bazlı fuzzy eşleşme
for kelime in kelimeler:
    for tur in kucukbas_turleri:
        if fuzz.ratio(kelime, tur) > 70:  # %70 benzerlik
            kucukbas_sayisi += 1
            break
    for tur in buyukbas_turleri:
        if fuzz.ratio(kelime, tur) > 70:
            buyukbas_sayisi += 1
            break

# Sonuçları yaz
print("📜 OCR Çıktısı (ilk 500 karakter):")
print(metin[:500])  # debug için ilk kısmını göster

print(f"✅ Küçükbaş hayvan sayısı: {kucukbas_sayisi}")
print(f"✅ Büyükbaş hayvan sayısı: {buyukbas_sayisi}")
