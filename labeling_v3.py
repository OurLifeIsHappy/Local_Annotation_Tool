import cv2
import numpy as np
import pytesseract
import json
import tkinter as tk
from tkinter import filedialog


def main(img_path):
# Load the image
    img = cv2.imread(img_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform thresholding to obtain a binary image
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a list to store the labels
    labels = []

    # Function to label the text in a contour
    def label_text(cnt):
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = gray[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi)
            labels.append({"bl": (x,y), "tl": (x,y+h), "br": (x+w,y), "tr": (x+w,y+h), "text": text})

    # Function to save the labels to a JSON file
    def save_labels():
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        with open(file_path, "w") as f:
            json.dump(labels, f)

    # Create the GUI
    root = tk.Tk()
    root.title("Label Text in Images")

    # Create the label button
    label_button = tk.Button(root, text="Label Text", command=lambda: label_text(contours))
    label_button.pack()

    # Create the save button
    save_button = tk.Button(root, text="Save Labels", command=save_labels)
    save_button.pack()

    # Show the GUI
    root.mainloop()


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = R'C:/Program Files/Tesseract-OCR/tesseract' 
    img_path = "C:/Data/annotation/data/input/image001.png"
    main(img_path)