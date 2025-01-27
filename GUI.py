import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Image Grid")
root.geometry("1000x950")  # Adjust size as needed

# Create a frame to hold the grid
frame = tk.Frame(root)
frame.pack(pady=30, padx=20)

# Function to load and resize image
def load_image(image_path, size=(275, 220)):  # Adjust size as needed
    img = Image.open(image_path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

# Create 4x3 grid of images
# Replace 'image1.png', 'image2.png', etc. with your actual image paths
image_paths = [
    'aapl_event_analysis.png', 'AUDUSD=X_event_analysis.png', 'bno_event_analysis.png', 'BTC_event_analysis.png',
    'f_event_analysis.png', 'fxb_event_analysis.png', 'msft_event_analysis.png', 'nflx_event_analysis.png',
    'spy_event_analysis.png', 'tsla_event_analysis.png', 'X_event_analysis.png', 'xom_event_analysis.png'
]

# Store PhotoImage objects in a list to prevent garbage collection
photo_images = []


# Create grid
for i in range(4):  # rows
    for j in range(3):  # columns
        index = i * 3 + j
        if index < len(image_paths):
            try:
                # Load and store the PhotoImage
                photo = load_image(image_paths[index])
                photo_images.append(photo)
                
                # Create label with image
                label = tk.Label(frame, image=photo)
                label.grid(row=i, column=j, padx=0, pady=0)
            except Exception as e:
                # If image fails to load, show error placeholder
                error_label = tk.Label(frame, text=f"Image {index+1}\nNot Found", 
                                     width=20, height=10, relief="solid")
                error_label.grid(row=i, column=j, padx=5, pady=5)


root.mainloop()