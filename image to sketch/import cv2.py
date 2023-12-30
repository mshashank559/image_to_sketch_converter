import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import numpy as np

def convert_to_pencil_sketch(image_path, output_path):
    # Load the image using Pillow
    image = Image.open(image_path)

    # Convert the image to grayscale
    gray_image = image.convert("L")

    # Convert the grayscale image to a NumPy array
    gray_array = cv2.cvtColor(src=np.array(gray_image), code=cv2.COLOR_GRAY2BGR)

    # Invert the image
    inverted_image = cv2.bitwise_not(gray_array)

    # Blur the inverted image
    blurred_image = cv2.GaussianBlur(inverted_image, (111, 111), sigmaX=0, sigmaY=0)

    # Invert the blurred image
    inverted_blurred_image = cv2.bitwise_not(blurred_image)

    # Create the pencil sketch image by blending the original and inverted blurred images
    pencil_sketch = cv2.divide(gray_array, inverted_blurred_image, scale=256.0)

    # Save the result
    cv2.imwrite(output_path, pencil_sketch)

class ImageToSketchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sketch Pencil App")

        # Create UI elements
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.convert_button = tk.Button(root, text="Convert to Sketch", command=self.convert_to_sketch, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        # Canvas to display images
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        # File path variables
        self.image_path = None
        self.sketch_path = "output_sketch.jpg"

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.load_and_display_image()
            self.convert_button["state"] = tk.NORMAL

    def load_and_display_image(self):
        # Load the image using Pillow and resize for display
        image = Image.open(self.image_path)
        image = image.resize((400, 400))
        photo = ImageTk.PhotoImage(image)

        # Update the canvas with the new image
        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def convert_to_sketch(self):
        convert_to_pencil_sketch(self.image_path, self.sketch_path)
        
        # Open the saved image using Pillow
        sketch_image = Image.open(self.sketch_path)
        sketch_image.show()

        # Ask the user to save the image
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if save_path:
            sketch_image.save(save_path)
            print("Pencil sketch saved to", save_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToSketchApp(root)
    root.mainloop()
