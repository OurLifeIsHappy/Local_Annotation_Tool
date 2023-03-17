import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import cv2
import numpy as np
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from os.path import join
from glob import glob
from pororo import Pororo

cr = Pororo(task="ocr", lang="ko")
def labeling(num,img_path):
    # Load the image
    img = cv2.imread(img_path)
    weight,height,channel = img.shape
    image_size = (weight,height)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5,5), 0) # (gray, ksize, 0)
    # edged = cv2.Canny(blurred, 75, 200) # (blurred, min_threshold, max_threshold)
    # gray = cv2.cvtColor(edged, cv2.COLOR_BGR2GRAY)

    # Initialize a list to store the labels
    labels = []
    bounding_boxes = []
    
    # Function to draw a bounding box on the image
    def draw_box(event, x, y, flags, param):
        nonlocal bounding_boxes
        global start_point, end_point, drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                end_point = (x, y)
                img[:] = original_img.copy()
                cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            end_point = (x, y)
            cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)
            label_text(num,img_path)

    # Function to label the text in a bounding box
    def label_text(num,img_path):
        nonlocal labels, bounding_boxes
        x1, y1 = start_point
        x2, y2 = end_point
        # roi = edged[y1:y2, x1:x2]
        roi = img.copy()[y1:y2, x1:x2]
        # text = simpledialog.askstring("text", "Enter the text for this box:")
        text = reader.recognize(roi)
        print(f"################\n#################\ntext : {text}") 
        label = simpledialog.askstring("Label", "Enter the label for this box:")
        labels.append({f"{img_path}_{num}" : [{"image_path" : img_path, "label": label, "text": text, "pageSize": image_size, "normalizedVerticles": [{"x1": x1, "y1": y1}, {"x2": x2, "y1": y1}, {"x2": x2, "y2": y2}, {"x1": x1, "y2": y2}]}]})
        bounding_boxes = []

    # Function to save the labels to a JSON file
    def save_labels():
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        with open(file_path, "w") as f:
            json.dump(labels, f)

    # Set up the mouse event callback
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", draw_box)

    # Keep a copy of the original image
    original_img = img.copy()

    # Show the image
    while True:
        cv2.imshow("image", img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord("s"):
            save_labels()
            break
        elif k == 27:
            break

    cv2.destroyAllWindows()

def load_img_path(path):
    files = []
    for ext in ('*.png', '*.jpg'):
        files.extend(glob(join(path, ext)))
    print(files)
    return files


if __name__ == '__main__':
    path = "C:/Data/annotation/data/input"
    img_path_list = load_img_path(path)
    img_stopped = ""
    num_stopped = -1 # write down the index(stopped + 1) you want to restart.  default -1
    # try:
    for num,img_path in enumerate(img_path_list):
        if num <= num_stopped:
            continue
        labeling(num,img_path)
        img_stopped = img_path
        num_stopped = num
        print(f"The Labeling is complete labeling image : {img_stopped}. \nit's {num_stopped+1}th image in the folder now")
    # except:
    #     print(f"The Labeling is stopped at {img_stopped}. \nit's {num_stopped}th image in the folder now")


