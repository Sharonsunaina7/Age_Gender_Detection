# Necessary Libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np

# Loading the Model
from keras.models import load_model
model = load_model("Age_Sex_Detection3.keras")

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age & Gender Detector')
top.configure(background='#CDCDCD')

# Initializing the Labels (1 for age and 1 for sex)
label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
sign_image = Label(top)

def Detect(file_path):
    global label1, label2
    image = Image.open(file_path)
    image = np.array(image)  # Convert PIL image to NumPy array
    
    # Check if image has 3 channels
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif len(image.shape) == 2:  # Grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    image = cv2.resize(image, (48, 48))  # Resize the image to 48x48
    image = np.expand_dims(image, axis=0)  # Expand dimensions to match model input
    image = image / 255.0  # Normalize the image
    
    # Predict using the model
    pred = model.predict(image)
    age = int(np.round(pred[1][0]))
    sex = int(np.round(pred[0][0]))
    
    sex_f = ["Male", "Female"]
    print(f"Predicted Age: {age}")
    print(f"Predicted Gender: {sex_f[sex]}")
    
    label1.configure(foreground="#011638", text=f"Predicted Age: {age}")
    label2.configure(foreground="#011638", text=f"Predicted Gender: {sex_f[sex]}")

# Defining Show_detect button function
def show_Detect_button(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Defining Upload Image Function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)
        
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        
        show_Detect_button(file_path)
    except Exception as e:
        print(f"Error: {e}")

upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text="Age and Gender Detector", pady=20, font=('arial', 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()
top.mainloop()