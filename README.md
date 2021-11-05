# annotpics
Annotate pictures given classes and keybindings. Experimental, in development.

```
pip install git+https://github.com/jacobhepkema/annotpics.git
```

```
Usage: annotpics [OPTIONS] IMAGE_DIR BINDINGS_JSON

  EXPERIMENTAL Picture annotation tool. CSV should contain 'image' column as
  first column specifying image names    without the directory.

Options:
  --csv TEXT          Location of annotation CSV file
  --o TEXT            File to save annotations to
  --start_i INTEGER
  --window_w INTEGER
  --window_h INTEGER
  --resize_w INTEGER
  --resize_h INTEGER
  --filetype TEXT
  --version           Show the version and exit.
  --help              Show this message and exit.
```
