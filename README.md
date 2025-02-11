# annotpics

Annotate pictures with binary labels for given classes and keybindings. Experimental, in development.

Press space to go to the next picture, press return to go to the previous picture.

Given [a file that specifies keybindings (argument BINDINGS\_JSON)](#Key-bindings), the program will go through the images in `IMAGE_DIR` and you can switch the annotation of a class using the specified keybindings. It will save to output file `--o` (default: `output.csv`). With every new annotation, the annotations are saved to the output file.

It is also possible to start from an existing annotation by using the `--csv` argument. Currently, the keybinding categories have to exactly match the column names of the annotation csv (it cannot be a subset at the time). The output file is different to the input `--csv` argument so that it does not overwrite.

## Install

```
pip install git+https://github.com/jacobhepkema/annotpics.git
```

## Usage

```
Usage: annotpics [OPTIONS] IMAGE_DIR BINDINGS_JSON

  EXPERIMENTAL Picture annotation tool. CSV should contain 'image' column as
  first column specifying image names without the directory.

Options:
  --csv TEXT          Location of annotation CSV file [None]
  --o TEXT            File to save annotations to [output.csv]
  --start_i INTEGER   Index of image to start with [0]
  --window_w INTEGER  Window width in pixels
  --window_h INTEGER  Window height in pixels
  --resize_w INTEGER  
  --resize_h INTEGER  
  --filetype TEXT     Filetype of images in IMAGE_DIR [any]
  --version           Show the version and exit.
  --help              Show this message and exit.
```

## Key bindings

Example key binding config JSON file:

```json
{
    "bindings": {
        "a": "a_category",
        "b": "b_category",
        "c": "c_category",
        "d": "d_category",
        "e": "e_category",
        "f": "f_category"
    }
}
```
