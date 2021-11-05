from tkinter import *
import pandas as pd
import numpy as np
from PIL import ImageTk, Image


class AnnotationInterface:
    r"""
    EXPERIMENTAL
    """
    def __init__(self, 
                 master, 
                 classes, 
                 image_dir,
                 data_df,
                 bindings,
                 save_csv="annotation.csv",
                 resize_w: int=382,
                 resize_h: int=470,
                 window_w: int=764,
                 window_h: int=1200,
                 start_i: int=0):
        self.master = master
        self.CURR_I = start_i
        self.master.title("Embryo " + str(self.CURR_I))
        self.master.geometry(str(window_w)+"x"+str(window_h))

        self.save_csv = save_csv
        
        self.bindings = bindings

        self.classes = np.array(classes)

        self.data_df = data_df

        self.image_dir = image_dir
        self.image_path = image_dir + "/" + self.data_df["image"][self.CURR_I]

        self.IMG = ImageTk.PhotoImage(Image.open(self.image_path).resize((382, 470)))
        self.IMG_PANEL = Label(self.master, image=self.IMG)
        self.IMG_PANEL.pack(side="bottom", fill="both", expand="yes")

        self.curr_values = np.array(self.data_df.iloc[self.CURR_I,1:])
        self.value_table = [x for x in zip(np.array(self.classes)[self.curr_values > 0], self.curr_values[self.curr_values > 0])]
        self.total_rows = sum(self.curr_values > 0)
        self.TEXT = [str(x[1])+"\t"+str(x[0]) for x in self.value_table]
        self.TEXT = "\n".join(self.TEXT)

        self.TEXT_PANEL = Label(self.master, text=self.TEXT, anchor="e", justify=LEFT, font=("Courier", 20))
        self.TEXT_PANEL.pack(side="bottom", expand="yes")

    def update_labels(self):
        print(self.CURR_I)
        self.curr_values = np.array(self.data_df.iloc[self.CURR_I,1:])
        self.value_table = [x for x in zip(np.array(self.classes)[self.curr_values > 0], self.curr_values[self.curr_values > 0])]
        self.total_rows = sum(self.curr_values > 0)
        self.TEXT = [str(x[1])+"\t"+str(x[0]) for x in self.value_table]
        self.TEXT = "\n".join(self.TEXT)

        self.TEXT_PANEL.configure(text=self.TEXT)
        self.TEXT_PANEL.text = self.TEXT

        self.master.title("Picture " + str(self.CURR_I))
        
    def update_image(self):
        self.image_path = f"{self.image_dir}/{self.data_df['image'][self.CURR_I]}"
        self.IMG = ImageTk.PhotoImage(Image.open(self.image_path).resize((382, 470)))
        self.IMG_PANEL.configure(image=self.IMG)
        self.IMG_PANEL.image = self.IMG

    def next_picture(self, event):
        self.data_df.to_csv(self.save_csv, index=False)
        print("Saved data")

        print("Showing next picture")	
        self.CURR_I = self.CURR_I + 1

        self.update_image()
        self.update_labels()

    def prev_picture(self, event):
        print("Showing previous picture")	
        if(self.CURR_I > 0):
            self.CURR_I = self.CURR_I - 1
        self.update_image()
        self.update_labels()

    def pressEvent(self, event):
        self.set_to(self.CURR_I, self.bindings[event.char])

    def set_to(self, i, curr_class):
        assert curr_class in list(self.classes), "invalid class"
        if self.data_df.iloc[i,1+np.argwhere(self.classes == curr_class)[0][0]] == 1:       
            self.data_df.iloc[i,1+np.argwhere(self.classes == curr_class)[0][0]] = 0
            print("Set to 0")
        else:
            self.data_df.iloc[i,1+np.argwhere(self.classes == curr_class)[0][0]] = 1
            print("Set to 1")
        self.update_labels()
