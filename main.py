import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class AnnotationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Image Annotation Tool")

        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the image frame
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Create the canvas to display the image
        self.image_canvas = tk.Canvas(self.image_frame, bg="white")
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        # Create the button frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X)

        # Create the "Open Image" button
        self.open_image_button = tk.Button(self.button_frame, text="Open Image", command=self.open_image)
        self.open_image_button.pack(side=tk.LEFT)

        # Create the "Add Annotation" button
        self.add_annotation_button = tk.Button(self.button_frame, text="Add Annotation", command=self.add_annotation)
        self.add_annotation_button.pack(side=tk.LEFT)

        # Create the "Save Annotations" button
        self.save_annotations_button = tk.Button(self.button_frame, text="Save Annotations", command=self.save_annotations)
        self.save_annotations_button.pack(side=tk.LEFT)

        # Create the "Clear Annotations" button
        self.clear_annotations_button = tk.Button(self.button_frame, text="Clear Annotations", command=self.clear_annotations)
        self.clear_annotations_button.pack(side=tk.LEFT)

        # Create the list to store the annotations
        self.annotations = []

    def open_image(self):
        # Open the file dialog to select the image
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        # Load the image and display it on the canvas
        image = Image.open(file_path)
        image = image.resize((self.image_canvas.winfo_width(), self.image_canvas.winfo_height()), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.image_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def add_annotation(self):
        # Add the annotation to the list of annotations
        x1, y1, x2, y2 = self.image_