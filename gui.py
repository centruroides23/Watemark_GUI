# ------------------------------------------------ DEPENDENCIES ------------------------------------------------------ #
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os
from tkinter import filedialog, simpledialog

# ------------------------------------------------- GUI COLORS ------------------------------------------------------- #
sidebar_color = "#16e053"
background_color = "#000000"
header_color = "#29ab63"


# ----------------------------------------------- STATIC FUNCTIONS --------------------------------------------------- #
def resize_to_canvas(image):
    if image.size[0] > 2000 or image.size[1] > 2000:
        image = image.resize((int(image.size[0] / 8), int(image.size[1] / 8)))
    elif image.size[0] > 1000 or image.size[1] > 1000:
        image = image.resize((int(image.size[0] / 4), int(image.size[1] / 4)))
    elif image.size[0] > 500 or image.size[1] > 500:
        image = image.resize((int(image.size[0] / 2), int(image.size[1] / 2)))
    return image


def set_position(position,
                 watermark_width,
                 watermark_height,
                 image_width,
                 image_height):
    if position == 101:
        x = image_width - watermark_width
        y = 0
        result = (x, y)
        return result
    elif position == 102:
        result = (0, 0)
        return result
    elif position == 103:
        x = image_width - watermark_width
        y = image_height - watermark_height
        result = (x, y)
        return result
    elif position == 104:
        x = 0
        y = image_height - watermark_height
        result = (x, y)
        return result
    elif position == 105:
        x = (image_width - watermark_width) // 2
        y = (image_height - watermark_height) // 2
        result = (x, y)
        return result


def apply_transparency(watermark, alpha):
    # Create an alpha layer
    alpha_layer = watermark.split()[3]
    alpha_layer = ImageEnhance.Brightness(alpha_layer).enhance(alpha / 255.0)
    watermark.putalpha(alpha_layer)
    return watermark


# ----------------------------------------------- GUI CONFIGURATION -------------------------------------------------- #
class UserInterphase(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.position = (0, 0)
        self.result_image = None

        # ------------------- BASIC APP LAYOUT ---------------------- #
        self.title("Add Water Mark")
        self.geometry("1450x650")
        self.config(background=background_color)
        self.file_path = None
        self.uploaded_images = []
        self.uploaded_watermarks = []

        # --------------------- HEADER LAYOUT ------------------------ #
        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.title = Label(self.header, text="ADD A WATERMARK", bg=header_color, font=("Arial", 23, "bold"))
        self.title.place(x=600, y=10)

        # --------------------- SIDEBAR LAYOUT ----------------------- #
        # Sidebar Frame Placement
        self.sidebar = Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.14, relheight=1)

        # Brand Frame Placement
        self.brand_frame = Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.40)

        # Logo Canvas Placement
        self.icon_canvas = Canvas(self.brand_frame, width=150, height=150, bg=sidebar_color, highlightthickness=0)
        original_icon = Image.open("images/watermark.png")
        resized_icon = original_icon.resize((150, 150))
        self.icon = ImageTk.PhotoImage(image=resized_icon)
        self.icon_canvas.create_image(75, 75, image=self.icon)
        self.icon_canvas.place(x=25, y=20)

        # Sidebar Button Placement
        self.b1 = Button(text="Upload an Image",
                         background="black",
                         foreground="white",
                         activebackground="green",
                         activeforeground="white",
                         highlightthickness=2,
                         highlightcolor="WHITE",
                         width=17,
                         height=2,
                         border=4,
                         borderwidth=2,
                         cursor="hand1",
                         command=self.upload_image)
        self.b1.place(x=35, y=250, anchor="w")

        self.b2 = Button(text="Upload a Watermark",
                         background="black",
                         foreground="white",
                         activebackground="green",
                         activeforeground="white",
                         highlightthickness=2,
                         highlightcolor="WHITE",
                         width=17,
                         height=2,
                         border=4,
                         borderwidth=2,
                         cursor="hand1",
                         command=self.upload_watermark)
        self.b2.place(x=35, y=320, anchor="w")

        self.b3 = Button(text="Place Watermark",
                         background="black",
                         foreground="white",
                         activebackground="green",
                         activeforeground="white",
                         highlightthickness=2,
                         highlightcolor="WHITE",
                         width=17,
                         height=2,
                         border=4,
                         borderwidth=2,
                         cursor="hand1",
                         command=self.place_watermark)
        self.b3.place(x=35, y=390, anchor="w")

        download_icon = PhotoImage(file="images/download.png")
        download_rz1 = download_icon.subsample(2, 2)
        download_rz2 = download_rz1.subsample(2, 2)
        self.download_label = Label(self.sidebar, bg=sidebar_color, text="Download Image", font=("Arial", 14))
        self.b4 = Button(image=download_rz2,
                         background="green",
                         foreground="white",
                         activebackground="green",
                         activeforeground="white",
                         highlightthickness=2,
                         highlightcolor="WHITE",
                         border=4,
                         borderwidth=2,
                         cursor="hand1",
                         command=self.save_image)
        self.b4.place(x=33, y=550, anchor="w")
        self.download_label.place(x=29, y=443)

        # --------------------- MAIN LAYOUT ----------------------- #
        self.main_frame = Frame(self, bg=background_color)
        self.main_frame.place(relx=0.14, rely=0.1, relwidth=1, relheight=0.9)

        # --------------------- MAIN LAYOUT: IMAGE FRAME ----------------------- #
        self.image_frame = Frame(self.main_frame, bg="black")
        self.image_frame.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        # Original Upload Canvas Placement
        self.image_canvas = Canvas(self.image_frame, width=540, height=540, bg="white", highlightthickness=0)
        self.image = Image.open("images/upload_image.jpg")
        self.resized_original = self.image.resize((540, 540))
        self.image = ImageTk.PhotoImage(image=self.resized_original)
        self.image_canvas.create_image(270, 270, image=self.image)
        self.image_canvas.place(x=10, y=10)

        # --------------------- MAIN LAYOUT: IMAGE INFORMATION ----------------------- #
        # Set Image Information Area
        self.image_info = Frame(self.main_frame, bg="gray")
        self.image_info.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

        # Listbox of uploaded Image List
        self.image_list_label = Label(self.image_info, bg="grey", text="Uploaded Images", font=("Arial", 14))
        self.image_list_label.place(x=10, y=10)

        self.image_list = Listbox(self.image_info, width=103, height=5, exportselection=False)
        self.image_list.place(x=10, y=45)

        # Listbox of uploaded Watermarks
        self.watermark_list_label = Label(self.image_info, bg="grey", text="Uploaded Watermarks", font=("Arial", 14))
        self.watermark_list_label.place(x=10, y=150)

        self.watermark_list = Listbox(self.image_info, width=103, height=5, exportselection=False)
        self.watermark_list.place(x=10, y=185)

        # Slider for watermark transparency
        self.transparency_label = Label(self.image_info, bg="grey", text="Adjust Transparency", font=("Arial", 14))
        self.transparency_label.place(x=10, y=290)

        self.transparency = Scale(self.image_info,
                                  from_=100,
                                  to=0,
                                  orient=HORIZONTAL,
                                  width=30,
                                  length=615,
                                  command=self.transparency_watermark)
        self.transparency.set(100)
        self.transparency.place(x=10, y=330)

        # Radio Buttons for watermark position
        self.v = IntVar()
        self.v.set(101)
        self.choices = {
            "Top-right": 101,
            "Top-left": 102,
            "Bottom-right": 103,
            "Bottom-left": 104,
            "Center": 105
        }
        self.radiobutton_label = Label(self.image_info, bg="grey", text="Adjust Watermark Position", font=("Arial", 14))
        self.y_coord = 420
        for position, value in self.choices.items():
            self.y_coord += 25
            Radiobutton(self.image_info,
                        text=position,
                        bg="grey",
                        variable=self.v,
                        value=value,
                        command=self.reposition_watermark).place(x=10, y=self.y_coord)
        self.radiobutton_label.place(x=10, y=410)

        # Instructions Area
        self.instructions_title = Label(self.image_info, bg="grey", text="Instructions", font=("Arial", 14))
        self.first_instruction = Label(self.image_info,
                                       text="1.- Upload base image and a watermark",
                                       bg="grey", font=("Arial", 11))
        self.second_instruction = Label(self.image_info,
                                        text="2.- Select base image and watermark from list boxes",
                                        bg="grey", font=("Arial", 11))
        self.third_instruction = Label(self.image_info,
                                       text="3.- Click 'Place Watermark' to display the result",
                                       bg="grey", font=("Arial", 11))
        self.fourth_instruction = Label(self.image_info,
                                        text="4.- Adjust transparency and position",
                                        bg="grey", font=("Arial", 11))
        self.instructions_title.place(x=300, y=410)
        self.first_instruction.place(x=300, y=440)
        self.second_instruction.place(x=300, y=470)
        self.third_instruction.place(x=300, y=500)
        self.fourth_instruction.place(x=300, y=530)

        self.mainloop()

    # --------------------- UPLOAD IMAGE FUNCTIONS ----------------------- #

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select a File",
                                               filetypes=[("Jpg Files", "*.jpg"), ("Png Files", "*.png")])

        self.uploaded_images.append(file_path)
        self.image_list.insert("end", self.uploaded_images[-1])
        image = Image.open(file_path)

        image = resize_to_canvas(image)

        x_size, y_size = image.size

        self.image = ImageTk.PhotoImage(image)
        self.image_canvas.config(width=x_size, height=y_size)
        new_image = self.image_canvas.create_image(x_size / 2, y_size / 2, anchor=CENTER, image=self.image)
        self.image_canvas.itemconfig(new_image)

        return image

    def upload_watermark(self):
        # Fetch the path for the selected image
        file_path = filedialog.askopenfilename(title="Select a File",
                                               filetypes=[("Jpg Files", "*.jpg"), ("Png Files", "*.png")])

        # Place the newly uploaded file in the watermark listbox
        self.uploaded_watermarks.append(file_path)
        self.watermark_list.insert("end", self.uploaded_watermarks[-1])
        image = Image.open(file_path)

        # Resize the image to fit canvas
        image = resize_to_canvas(image)

        # Get new dimensions for canvas
        x_size, y_size = image.size

        # Update canvas with uploaded image
        self.image = ImageTk.PhotoImage(image)
        self.image_canvas.config(width=x_size, height=y_size)
        new_image = self.image_canvas.create_image(x_size / 2, y_size / 2, anchor=CENTER, image=self.image)
        self.image_canvas.itemconfig(new_image)

        return image

    def place_watermark(self):
        # Grab the image and watermark
        image_path = self.image_list.get(self.image_list.curselection())
        watermark_path = self.watermark_list.get(self.watermark_list.curselection())

        # Read the images
        main_image = Image.open(image_path)
        watermark = Image.open(watermark_path)

        # Obtain the size of main images
        img_width, img_height = main_image.size

        # Overlay the watermark over the image
        self.result_image = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        self.result_image.paste(main_image, (0, 0))
        self.result_image.paste(watermark, self.position, mask=watermark)

        # Resize image to display to canvas
        self.result_image = resize_to_canvas(self.result_image)

        # Get new coordinates for canvas dimensions
        x_size, y_size = self.result_image.size

        # Update the canvas with processed image
        self.image = ImageTk.PhotoImage(self.result_image)
        self.image_canvas.config(width=x_size, height=y_size)
        new_image = self.image_canvas.create_image(x_size / 2, y_size / 2, anchor=CENTER, image=self.image)
        self.image_canvas.itemconfig(new_image)

        return self.result_image

    def reposition_watermark(self):
        # Grab the image and watermark
        image_path = self.image_list.get(self.image_list.curselection())
        watermark_path = self.watermark_list.get(self.watermark_list.curselection())

        # Read the images
        main_image = Image.open(image_path)
        watermark = Image.open(watermark_path)

        # Obtain the size of main images
        img_width, img_height = main_image.size
        mark_width, mark_height = watermark.size

        self.position = set_position(self.v.get(),
                                     mark_width,
                                     mark_height,
                                     img_width,
                                     img_height)

        # Overlay the watermark over the image
        self.result_image = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        self.result_image.paste(main_image, (0, 0))
        self.result_image.paste(watermark, self.position, mask=watermark)

        # Resize image to display to canvas
        self.result_image = resize_to_canvas(self.result_image)

        # Get new coordinates for canvas dimensions
        x_size, y_size = self.result_image.size

        # Update the canvas with processed image
        self.image = ImageTk.PhotoImage(self.result_image)
        self.image_canvas.config(width=x_size, height=y_size)
        new_image = self.image_canvas.create_image(x_size / 2, y_size / 2, anchor=CENTER, image=self.image)
        self.image_canvas.itemconfig(new_image)

        return self.result_image

    def transparency_watermark(self, value):
        # Grab the image and watermark
        image_path = self.image_list.get(self.image_list.curselection())
        watermark_path = self.watermark_list.get(self.watermark_list.curselection())

        # Read the images
        main_image = Image.open(image_path)
        watermark = Image.open(watermark_path)

        # Obtain the size of main images
        img_width, img_height = main_image.size

        transparency = int(value)
        alpha = int(transparency * 255 / 100)

        watermark = apply_transparency(watermark, alpha)

        # Overlay the watermark over the image
        self.result_image = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        self.result_image.paste(main_image, (0, 0))
        self.result_image.paste(watermark, self.position, mask=watermark)

        # Resize image to display to canvas
        self.result_image = resize_to_canvas(self.result_image)

        # Get new coordinates for canvas dimensions
        x_size, y_size = self.result_image.size

        # Update the canvas with processed image
        self.image = ImageTk.PhotoImage(self.result_image)
        self.image_canvas.config(width=x_size, height=y_size)
        new_image = self.image_canvas.create_image(x_size / 2, y_size / 2, anchor=CENTER, image=self.image)
        self.image_canvas.itemconfig(new_image)

        return self.result_image

    def save_image(self):
        image_to_save = self.result_image.convert("RGB")
        output_directory = filedialog.askdirectory()
        filename = "watermark_image" + ".jpeg"
        image_to_save.save(os.path.join(output_directory, filename), "JPEG")

