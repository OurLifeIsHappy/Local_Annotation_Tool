import cv2
import numpy as np
import json

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

    # Iterate through the contours and draw rectangles around each one
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #labels include label of text

        labels.append({"x": x, "y": y, "w": w, "h": h})

    # Save the labels to a JSON file
    with open("labels.json", "w") as f:
        json.dump(labels, f)

    # Show the image with the labeled rectangles
    cv2.imshow("Labeled Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    img_path = "C:/Data/annotation/data/sample.png"
    main(img_path)