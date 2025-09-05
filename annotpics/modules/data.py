import pandas as pd
import numpy as np
import os

class AnnotationData:
    def __init__(self, image_dir, classes, o, csv=None, filetype='any'):
        self.save_csv = o
        self.classes = classes
        if csv is None:
            assert not os.path.isfile(o), f"csv not specified but output file '{o}' exists"
            image_names = self._get_image_names(image_dir, filetype)
            self.data_df = self._create_empty_dataframe(image_names, classes)
        else:
            self.data_df = pd.read_csv(csv)

        # Ensure columns after 'image' match the classes
        self.data_df.columns = ['image'] + self.classes

    def _get_image_names(self, image_dir, filetype):
        import re
        if filetype.lower() == 'any':
            filetype_regex = re.compile(".*\\.(jpg|jpeg|png|gif)$", re.IGNORECASE)
        elif filetype.lower() in ['jpg', 'jpeg']:
            filetype_regex = re.compile(".*\\.(jpg|jpeg)$", re.IGNORECASE)
        else:
            filetype_regex = re.compile(f".+\\.{filetype}$", re.IGNORECASE)

        files_in_image_dir = os.listdir(image_dir)
        return list(filter(filetype_regex.match, files_in_image_dir))

    def _create_empty_dataframe(self, image_names, classes):
        num_pictures = len(image_names)
        annotation_values = np.zeros((num_pictures, len(classes)))
        annotations = pd.concat((pd.DataFrame(image_names), pd.DataFrame(annotation_values)), axis=1)
        annotations.columns = ['image'] + classes
        return annotations

    def get_image_path(self, i, image_dir):
        return f"{image_dir}/{self.data_df['image'][i]}"

    def get_annotations(self, i):
        return self.data_df.iloc[i, 1:].to_dict()

    def toggle_annotation(self, i, curr_class):
        assert curr_class in self.classes, "invalid class"
        current_value = self.data_df.loc[i, curr_class]
        self.data_df.loc[i, curr_class] = 1 - current_value
        return 1 - current_value

    def save(self):
        self.data_df.to_csv(self.save_csv, index=False)

    @property
    def num_images(self):
        return len(self.data_df)
