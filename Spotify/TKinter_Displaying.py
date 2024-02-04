from API_Access import CurrentlyPlaying, GetCover

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

def main():
    global image, canvas, text1, text2

    height = 1080
    width = 1920
    background_color = "#222222"

    root = tk.Tk()
    root.title("TheFrame")  # Set the title to "TheFrame"

    # Set the background color to dark grey
    root.configure(bg=background_color)

    # Set the window to full screen
    #root.attributes('-fullscreen', True)

    # Load and resize the image
    image_path = "../cover.jpg"  # Replace with the actual path to your image
    original_image = Image.open(image_path)
    resized_image = original_image.resize((300, 300))  # Adjust the size as needed
    image = ImageTk.PhotoImage(original_image)

    # Create and display the canvas with a dark grey background
    canvas = tk.Canvas(root, width=width, height=height, bg=background_color, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=2, pady=10)

    # Display the image on the canvas
    global image_id
    image_id = canvas.create_image(width/2, height/2, anchor= "center", image=image)

    # Create and display the first line of text using themed label with white text
    text1 = tk.Label(root, text=CurrentlyPlaying()["titel"], font=("Helvetica", 14), fg="white", bg=background_color)
    text1.grid(row=1, column=0, columnspan=2, pady=(0, 5))

    # Create and display the second line of text using themed label with white text
    text2 = tk.Label(root, text=CurrentlyPlaying()["artist"], font=("Helvetica", 14), fg="#999999", bg=background_color)
    text2.grid(row=2, column=0, columnspan=2, pady=(0, 5))



    root.mainloop()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    main()
