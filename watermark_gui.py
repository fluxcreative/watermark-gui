import os
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, OptionMenu
from PIL import Image, ImageShow

def overlay_logo(image_path, logo_path, position):
    print(f"Overlaying logo: {logo_path} on image: {image_path} at position: {position}")
    image = Image.open(image_path)
    logo = Image.open(logo_path)
    if logo.mode != 'RGBA':
        logo = logo.convert("RGBA")
        alpha = Image.new('L', logo.size, 255)
        logo.putalpha(alpha)

    image_width, image_height = image.size
    max_logo_size = int(min(image_width, image_height) * 0.08)
    logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)
    print(f"Resized logo to: {logo.size}")

    logo_width, logo_height = logo.size
    padding = 10  # Add padding
    if position == 'top-left':
        x, y = padding, padding
    elif position == 'top-right':
        x, y = image_width - logo_width - padding, padding
    elif position == 'bottom-left':
        x, y = padding, image_height - logo_height - padding
    elif position == 'bottom-right':
        x, y = image_width - logo_width - padding, image_height - logo_height - padding
    else:
        raise ValueError("Invalid position. Choose from 'top-left', 'top-right', 'bottom-left', 'bottom-right'.")

    print(f"Pasting logo at: ({x}, {y})")

    # Adjust opacity
    logo = logo.convert("RGBA")
    alpha = logo.split()[3]
    alpha = alpha.point(lambda p: p * 0.5)  # Set opacity to 50%
    logo.putalpha(alpha)

    image.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)
    output_path = os.path.join('output', os.path.basename(image_path))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    print(f"Image saved as {output_path}")

    # Display the image for verification
    image.show()

def process_images(input_path, logo_path, position):
    print(f"Processing images in: {input_path} with logo: {logo_path} at position: {position}")
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(input_path, filename)
                overlay_logo(image_path, logo_path, position)
    elif os.path.isfile(input_path):
        overlay_logo(input_path, logo_path, position)
    else:
        raise ValueError("Invalid input path. Provide a valid file or directory.")

def select_image():
    path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if path:
        image_or_directory_path.set(path)
        print(f"Selected image: {path}")
    else:
        print("No image selected.")

def select_directory():
    path = filedialog.askdirectory(title="Select a directory")
    if path:
        image_or_directory_path.set(path)
        print(f"Selected directory: {path}")
    else:
        print("No directory selected.")

def select_logo():
    path = filedialog.askopenfilename()
    logo_path.set(path)
    print(f"Selected logo: {path}")

def run():
    try:
        process_images(image_or_directory_path.get(), logo_path.get(), position.get())
        print("Processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

root = Tk()
root.title("Image Watermarking")

image_or_directory_path = StringVar()
logo_path = StringVar()
position = StringVar(value='top-left')

Label(root, text="Image or Directory:").grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=image_or_directory_path, width=50).grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Image", command=select_image).grid(row=0, column=2, padx=10, pady=10)
Button(root, text="Directory", command=select_directory).grid(row=0, column=3, padx=10, pady=10)

Label(root, text="Logo:").grid(row=1, column=0, padx=10, pady=10)
Entry(root, textvariable=logo_path, width=50).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_logo).grid(row=1, column=2, padx=10, pady=10)

Label(root, text="Position:").grid(row=2, column=0, padx=10, pady=10)
OptionMenu(root, position, 'top-left', 'top-right', 'bottom-left', 'bottom-right').grid(row=2, column=1, padx=10, pady=10)

Button(root, text="Run", command=run).grid(row=3, column=1, padx=10, pady=10)

root.mainloop()