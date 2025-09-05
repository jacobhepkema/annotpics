import sys
import os
import click
import json
import logging

from tkinter import Tk

from .modules.interface import AnnotationUI
from .modules.data import AnnotationData
from .modules.image_manager import ImageManager

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
@click.option('--resize_w', default=382, required=False)
@click.option('--resize_h', default=470, required=False)
@click.option('--filetype', default='any', required=False)
def main(image_dir, bindings_json, csv,
         o, start_i,
         window_w, window_h,
         resize_w, resize_h,
         filetype):
    r"""
    EXPERIMENTAL
    Picture annotation tool.
    CSV should contain 'image' column as first column specifying image names 
      without the directory.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    with open(bindings_json) as json_file:
        json_dict = json.load(json_file)
    bindings = json_dict['bindings']
    classes = list(bindings.values())

    data_manager = AnnotationData(image_dir=image_dir, classes=classes, o=o, csv=csv, filetype=filetype)

    # Add image_dir to image_manager
    image_manager = ImageManager(resize_w=resize_w, resize_h=resize_h)
    image_manager.image_dir = image_dir

    root = Tk()

    app = AnnotationUI(master=root,
                       data_manager=data_manager,
                       image_manager=image_manager,
                       bindings=bindings,
                       start_i=start_i,
                       window_w=window_w,
                       window_h=window_h)

    root.mainloop()


if __name__ == '__main__':
    main()
