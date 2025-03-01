import tkinter as tk
import webbrowser
from PIL import Image, ImageTk

# Reviewers and their YouTube links with images
reviewers = {
    "Badal Yadav": {"link": "https://www.youtube.com/@BnfTV", "image": "badal_yadav.jpg"},
    "Mohit Yodha": {"link": "https://www.youtube.com/@comicverseog", "image": "mohit_yodha.jpg"},
    "Priyanshu Aggrwal": {"link": "https://www.youtube.com/@PJExplained", "image": "priyanshu_aggrawal.jpg"},
    "Suraj Kumar": {"link": "https://www.youtube.com/@SurajKumarReview", "image": "suraj_kumar.jpg"},
    "Deeksha Sharma": {"link": "https://www.youtube.com/@FilmiIndian", "image": "deeksha_sharma.jpg"}
}


def open_channel(reviewer):
    webbrowser.open(reviewers[reviewer]["link"])

def home():
    window.destroy()
    import main

# GUI Setup
window = tk.Tk()
window.title("Top movie reviewers")
window.geometry("1660x800")

frame = tk.Frame(window)
frame.pack(pady=10)

# Arrange reviewers in an upside-down pyramid layout
layout = [
    ["Badal Yadav", "Mohit Yodha", "Priyanshu Aggrwal"],
    ["Suraj Kumar", "Deeksha Sharma"]
]

for row_index, row in enumerate(layout):
    row_frame = tk.Frame(frame)
    row_frame.pack()
    for reviewer in row:
        data = reviewers[reviewer]
        img = Image.open(data["image"])  # Ensure the image file is in the same directory
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        btn_frame = tk.Frame(row_frame)
        btn_frame.pack(side=tk.LEFT, padx=10, pady=5)

        btn = tk.Button(btn_frame, image=img_tk, command=lambda r=reviewer: open_channel(r))
        btn.image = img_tk  # Keep a reference to avoid garbage collection
        btn.pack()

        tk.Label(btn_frame, text=reviewer, font=("Arial", 12, "bold")).pack()

home_button = tk.Button(window,width=30, text="HOME", command=home, font=("Helvetica", 30))
home_button.place(x=440,y=300)


window.mainloop()
