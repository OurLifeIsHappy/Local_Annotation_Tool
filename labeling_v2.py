import cv2
import numpy as np
import pytesseract
import json


def main(img_path):
    # Load the image
    img = cv2.imread(img_path)
    weight,height,channel = img.shape
    image_size = (weight,height)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform thresholding to obtain a binary image
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a list to store the labels
    Category = {"1":"Total", "2" :"Date", "3" : "Company_Name", "4" : "Total_Price", "5" : "Item", "6" : "Item_Price"}
    labels = []
    labels.append({"src_img_size" : image_size})
    # Iterate through the contours and label the text in each one
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        roi = gray[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi)
        labels.append({"bl": (x,y), "tl": (x,y+h), "br": (x+w,y), "tr": (x+w,y+h), "text": text})

    # Save the labels to a JSON file
    with open("labels.json", "w") as f:
        json.dump(labels, f)

    # Show the image with the labeled text
    cv2.imshow("Labeled Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = R'C:/Program Files/Tesseract-OCR/tesseract' 
    img_path = "C:/Data/annotation/data/input/image001.png"
    main(img_path)