# import paddleocr
import cv2
from paddleocr import PaddleOCR
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Paddle OCR 초기화
ocr = PaddleOCR(lang='korean')

# 이미지 불러오기
img = cv2.imread("C:/Data/annotation/data/input/image001.png")

# OCR 수행
result = ocr.ocr(img,det=True, rec=True, cls=True)

# 결과 출력
for line in result:
    print(line)