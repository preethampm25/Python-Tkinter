from tkinter import *
from tkinter import colorchooser, ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab, ImageDraw

root = Tk()
root.geometry('700x700')
root.title('Paint Application')
root.iconbitmap('icons/paint.ico')
root.resizable(height=False, width=False)

# Initial Constants
brush_color = 'black'


# Define Change brush size
def change_brush_change(thing):
    slider_label.config(text=int(my_slider.get()))


# Change Brush Color
def change_brush_color():
    global brush_color
    brush_color = colorchooser.askcolor()[1]


# Change Canvas Color
def change_canvas_color():
    global canvas_color
    canvas_color = colorchooser.askcolor()[1]
    my_canvas.config(bg=canvas_color)


# Clear Screen
def clear_screen():
    my_canvas.delete(ALL)
    my_canvas.config(bg='white')


# Save as PNG
def save_as_png():
    result = filedialog.asksaveasfilename(initialdir='F:/', filetypes=(('PNG Files', '*.png'), ('All Files', '*.*')))
    if result.endswith('.png'):
        pass
    else:
        result = result + '.png'
    if result:
        x = root.winfo_rootx() + my_canvas.winfo_rootx()
        y = root.winfo_rooty() + my_canvas.winfo_rooty()
        x1 = x + my_canvas.winfo_width()
        y1 = y + my_canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(result)

        # Pop up success massage
        messagebox.showinfo('Image Saved', 'Your image has been saved')


# Paint function
def paint(e):
    # Brush Parameters
    brush_width = int(my_slider.get())
    brush_color_final = brush_color

    # Brush Type :  BUTT, ROUND, PROJECTING
    brush_type_final = brush_type.get()

    # Start position
    x1 = e.x - 1
    y1 = e.y - 1

    # End position
    x2 = e.x + 1
    y2 = e.y + 1

    # Draw on canvas
    my_canvas.create_line(x1, y1, x2, y2, width=brush_width, capstyle=brush_type_final, fill=brush_color_final,
                          smooth=True)


# Blank white widget
w = 550
h = 350
my_canvas = Canvas(root, width=w, height=h, bg='white')
my_canvas.pack(pady=20)

# Mouse movement
my_canvas.bind('<B1-Motion>', paint)

# Creating Brush Option Frame
brush_option_frame = Frame(root)
brush_option_frame.pack(pady=10)

# Brush Size
brush_size_frame = LabelFrame(brush_option_frame, text="Brush Size")
brush_size_frame.grid(row=0, column=0)
# Brush Slider
my_slider = ttk.Scale(brush_size_frame, from_=1, to=50, command=change_brush_change, orient=VERTICAL, value=10)
my_slider.pack()
# Brush Slider size Label
slider_label = Label(brush_size_frame, text=my_slider.get())
slider_label.pack()

# Brush Type
brush_type_frame = LabelFrame(brush_option_frame, text='Brush Type', height=400)
brush_type_frame.grid(row=0, column=1, padx=50, )

brush_type = StringVar()
brush_type.set('round')

brush_type_radio1 = Radiobutton(brush_type_frame, text='Round', variable=brush_type, value='round')
brush_type_radio2 = Radiobutton(brush_type_frame, text='Diamond', variable=brush_type, value='projecting')
brush_type_radio3 = Radiobutton(brush_type_frame, text='Slash', variable=brush_type, value='butt')

brush_type_radio1.pack(anchor=W)
brush_type_radio2.pack(anchor=W)
brush_type_radio3.pack(anchor=W)

# Change Colors
change_color_frame = LabelFrame(brush_option_frame, text='Change Colour')
change_color_frame.grid(column=2, row=0)

# Change Brush Color
brush_color_button = Button(change_color_frame, text='Brush Colour', command=change_brush_color)
brush_color_button.pack(pady=10, padx=10)

# Change Canvas Color
canvas_color_button = Button(change_color_frame, text='Canvas Colour', command=change_canvas_color)
canvas_color_button.pack(pady=10, padx=10)

# Program Options
option_frame = LabelFrame(brush_option_frame, text='Program Optioms')
option_frame.grid(row=0, column=3, padx=50)

# Clear and Save
clear_button = Button(option_frame, text='Clear Screen', command=clear_screen)
clear_button.pack(padx=5, pady=5)
save_button = Button(option_frame, text='Save to PNG', command=save_as_png)
save_button.pack(padx=5, pady=5)

root.mainloop()
