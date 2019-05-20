import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

import CNN

# global SOURCE_DIR # 图片存放地址
SOURCE_DIR = './thumbnails/'

root = Tk()
root.title('Image Retrieval')
# root.geometry('800x400')
frame = Frame(root)
v = StringVar()

cnn = Radiobutton(root, text="CNN", variable=v, value=3)

cnn.pack(anchor=W)

SELECTED_FILE = None
RES_LIST = []
img = None
imgs = None

# components
selected_label = None
selected_img = None
info_label = None
retrieved_imgs = None


def retrieve():
    global frame
    global SOURCE_DIR
    global SELECTED_FILE
    global selected_label
    global selected_img
    global info_label
    global retrieved_imgs
    global img
    global imgs

    SOURCE_DIR = './thumbnails/'
    if SELECTED_FILE != '':
        mode = v.get()

        RES_LIST = CNN.cnn_query(SELECTED_FILE)
        img_open = Image.open(SELECTED_FILE)
        img = ImageTk.PhotoImage(img_open)
        selected_label = Label(root, text='[Selected Pictures]')
        selected_label.pack()

        selected_img = Label(root, image=img)
        selected_img.pack()

        imgs = [ImageTk.PhotoImage(Image.open(SOURCE_DIR + one)) for one in RES_LIST]
        counter = 0

        info_label = Label(root, text='[Retrieved Pictures]')
        info_label.pack()

        retrieved_imgs = {}
        for per_img in imgs:
            retrieved_imgs[counter] = Label(root, image=imgs[counter])
            retrieved_imgs[counter].pack(side='left')
            counter += 1


def openfiles2():
    global SELECTED_FILE
    global selected_label
    global selected_img
    global info_label
    global retrieved_imgs

    SELECTED_FILE = filedialog.askopenfilename(title='选择图片', filetypes=[('~', '*.jpg'), ('All Files', '*')])
    print(SELECTED_FILE)

    # Depack components
    if selected_label != None:
        selected_label.pack_forget()
    if selected_img != None:
        selected_img.pack_forget()
    if info_label != None:
        info_label.pack_forget()
    if retrieved_imgs != None:
        for one in retrieved_imgs:
            retrieved_imgs[one].pack_forget()


select = Button(frame, text="select", command=openfiles2)
select.pack()

textLabel = Label(frame, textvariable='search', justify=LEFT)
textLabel.pack(side=LEFT)

theButton = Button(frame, text="search", command=retrieve)
theButton.pack()

frame.pack(padx=10, pady=10)

root.mainloop()
