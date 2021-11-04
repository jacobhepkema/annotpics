import sys
import os
import click
import json
import re
import pandas as pd
import numpy as np

from PIL import ImageTk, Image
from tkinter import Tk

from annotpics.modules.interface import AnnotationInterface

@click.version_option("0.0.1")
@click.command()
@click.argument('image_dir', required=True)
@click.argument('bindings_json', required=True)
@click.option('--csv', required=False, default=None, 
              help='Location of annotation CSV file')
@click.option('--o', default="output.csv", required=False, 
              help='File to save annotations to')
@click.option('--start_i', default=0, required=False)
@click.option('--window_w', default=764, required=False)
@click.option('--window_h', default=1200, required=False)
@click.option('--filetype', default='jpg', required=False)
def main(image_dir, bindings_json, csv,
         o, start_i, window_w, window_h,
         filetype):
    r"""
    EXPERIMENTAL
    Picture annotation tool.
    CSV should contain 'image' column as first column specifying image names 
      without the directory.
    """
    print("csv =", csv)
    print("image_dir=", image_dir)
    print("bindings_json =", bindings_json)
    print("start_i =", start_i)
    print("window_w =", window_w)
    print("window_h =", window_h)
    print("filetype =", filetype)

    with open(bindings_json) as json_file:
        json_dict = json.load(json_file)
    bindings = json_dict['bindings']

    print("bindings =", bindings)
    classes = list(bindings.values())
    print("classes = ", classes)
    filetype_regex = re.compile(f".+\\.{filetype}$")

    # Default behaviour: if CSV is not provided, create empty dataframe with the
    #   categories set to the classes from the keybindings and the number of 
    #   rows corresponding to the pictures .
    # If CSV is provided, use that as the annotation df (make sure the 
    # keybinding classes are a subset of the annotation classes)
    if csv is None:
        files_in_image_dir = os.listdir(image_dir)
        image_names = list(filter(filetype_regex.match, files_in_image_dir))
        num_pictures = len(image_names)
        annotation_classes = classes
        annotation_values = np.zeros((num_pictures, len(annotation_classes)))
        annotations = pd.concat((pd.DataFrame(image_names), pd.DataFrame(annotation_values)), axis=1)
        annotations.columns = ['image'] + annotation_classes
    else:
        with open(csv) as csv_file:
            annotations = pd.read_csv(csv, index_col=0)
        annotation_classes = [x for i,x in 
                              enumerate(self.annotations.columns) if i>0]
    print("annotations =", annotations)
    print(annotations['image'])
    
    root = Tk()

    ai = AnnotationInterface(root, classes, image_dir, annotations,
                             save_csv="annotation.csv", 
                             window_w = window_w, window_h = window_h,
                             start_i = start_i)

    root.mainloop()


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Picture annotation tool")
    main()
