import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageEnhance, ImageFilter, ImageTk
import traceback
import os
os.environ['TCL_LIBRARY'] = r'C:\Users\Micheal\AppData\Local\Programs\Python\Python312\tcl\tk8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Micheal\AppData\Local\Programs\Python\Python312\tcl\tkdnd2.8'

# Global variables to store the images
original_image = None
edited_image = None


# Function to open file dialog and let the user select an image file
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")]
    )
    if file_path:
        process_image(file_path)
    else:
        messagebox.showwarning("Warning", "No file selected. Please select an image file.")

# Function to handle drag and drop (only works for files dragged from the system)
def drop(event):
    try:
        file_path = event.data.strip('{}')  # Remove any curly braces around the path
        process_image(file_path)
    except Exception as e:
        messagebox.showerror('Error', f"Failed to process dropped file: {e}")

# Function to process the selected image
def process_image(file_path):
    global original_image, edited_image, edited_file_path

    try:
        img = Image.open(file_path)
        
        # Display original image
        display_image(img, original_image_label)

        # Apply a SHARPEN filter and convert to grayscale for edited image
        edited_img = img.filter(ImageFilter.SHARPEN).convert("L")
        display_image(edited_img, edited_image_label)

        # Store the edited image for saving later
        edited_image = edited_img

        # Get the clean filename without extension
        clean_name = os.path.splitext(os.path.basename(file_path))[0]

        # Define the path for the Downloads folder
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Save the edited image to the Downloads directory
        edited_file_path = os.path.join(downloads_dir, f"{clean_name}_edited.jpg")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the image: {e}")

# Function to display the image on the GUI
def display_image(image, label):
    # Resize image for display purposes
    resized_image = image.resize((200, 200))
    tk_image = ImageTk.PhotoImage(resized_image)
    label.config(image=tk_image)
    label.image = tk_image  # Keep a reference to prevent garbage collection

# Function to save the edited image
def save_image():
    if edited_image:
        try:
            # Save the image to the downloads directory
            edited_image.save(edited_file_path)
            messagebox.showinfo("Success", f"Image saved to {edited_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the image: {e}")
    else:
        messagebox.showwarning("Warning", "No edited image to save.")

# Create the main window
root = TkinterDnD.Tk()  # Use TkinterDnD for drag and drop
root.title("Photo Editor")
root.geometry("600x400")
root.configure(bg='#345')

# Instruction label
instruction_label = tk.Label(root, text="Select or drag and drop an image file to edit", bg='#345', fg='#fff')
instruction_label.pack(pady=10)

# Frame to display images
image_frame = tk.Frame(root, bg='#345')
image_frame.pack(pady=10)

# Label to display original image
original_image_label = tk.Label(image_frame, text="Original Image", bg='#eee', width=200, height=200)
original_image_label.grid(row=0, column=0, padx=20)

# Label to display edited image
edited_image_label = tk.Label(image_frame, text="Edited Image", bg='#eee', width=200, height=200)
edited_image_label.grid(row=0, column=1, padx=20)

# Select File button
select_button = tk.Button(root, text="Select File", command = select_file, bg='#FA8072')
select_button.pack(pady=10)

# Save Button
save_button = tk.Button(root, text="Save Image", command=save_image, bg='#FFD700')
save_button.pack(pady=10)

# Enable drag-and-drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# Start the main loop
root.mainloop()

