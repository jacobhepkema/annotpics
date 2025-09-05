from tkinter import Label, LEFT, Frame, BOTH
import logging

class AnnotationUI:
    def __init__(self, master, data_manager, image_manager, bindings, start_i=0, window_w=764, window_h=1200):
        self.master = master
        self.data_manager = data_manager
        self.image_manager = image_manager
        self.bindings = bindings
        self.curr_i = start_i

        self.master.geometry(f"{window_w}x{window_h}")
        self.master.title(f"Image {self.curr_i}")
        self.master.bind("<Return>", self.prev_picture)
        self.master.bind("<space>", self.next_picture)
        for key in self.bindings.keys():
            self.master.bind(key, self.press_event)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Image Panel
        self.img_panel = Label(self.master)
        self.img_panel.pack(side="bottom", fill="both", expand="yes")

        # Annotation Panel
        self.annotation_frame = Frame(self.master)
        self.annotation_frame.pack(side="bottom", fill="both", expand="yes")
        self.annotation_labels = {}

        self._create_annotation_labels()
        self.update_ui()

    def _create_annotation_labels(self):
        # Using a more structured grid layout
        self.annotation_frame.columnconfigure(1, weight=1)
        row = 0
        for key, class_name in self.bindings.items():
            key_label = Label(self.annotation_frame, text=f"[{key}]", font=("Courier", 14))
            key_label.grid(row=row, column=0, sticky='w', padx=5, pady=2)

            label = Label(self.annotation_frame, text=class_name, font=("Courier", 14), anchor="w")
            label.grid(row=row, column=1, sticky='we', padx=5, pady=2)
            self.annotation_labels[class_name] = label
            row += 1

    def update_ui(self):
        self.master.title(f"Picture {self.curr_i}")
        self.update_image()
        self.update_labels()

    def update_image(self):
        image_path = self.data_manager.get_image_path(self.curr_i, self.image_manager.image_dir)
        photo_img = self.image_manager.get_image(image_path)
        self.img_panel.configure(image=photo_img)
        self.img_panel.image = photo_img

    def update_labels(self):
        annotations = self.data_manager.get_annotations(self.curr_i)
        for class_name, value in annotations.items():
            if class_name in self.annotation_labels:
                label = self.annotation_labels[class_name]
                if value == 1:
                    label.config(fg="green", text=f"{class_name} (ON)")
                else:
                    label.config(fg="red", text=f"{class_name} (OFF)")

    def next_picture(self, event):
        if self.curr_i < self.data_manager.num_images - 1:
            self.curr_i += 1
            self.update_ui()
            logging.info(f"Showing next picture: {self.curr_i}")
        else:
            logging.info("Already at the last picture.")

    def prev_picture(self, event):
        if self.curr_i > 0:
            self.curr_i -= 1
            self.update_ui()
            logging.info(f"Showing previous picture: {self.curr_i}")
        else:
            logging.info("Already at the first picture.")

    def press_event(self, event):
        class_name = self.bindings.get(event.char)
        if class_name:
            new_value = self.data_manager.toggle_annotation(self.curr_i, class_name)
            logging.info(f"Set annotation for '{class_name}' to {new_value}")
            self.update_labels()
        else:
            logging.warning(f"No binding found for key: {event.char}")

    def on_closing(self):
        logging.info("Window closed, saving annotations...")
        self.data_manager.save()
        self.master.destroy()
