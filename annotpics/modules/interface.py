from tkinter import ttk, font
import logging

class AnnotationUI:
    def __init__(self, master, data_manager, image_manager, bindings, start_i=0, window_w=764, window_h=1200):
        self.master = master
        self.data_manager = data_manager
        self.image_manager = image_manager
        self.bindings = bindings
        self.curr_i = start_i

        # --- Basic Setup ---
        self.master.geometry(f"{window_w}x{window_h}")
        self.master.title(f"Image {self.curr_i}")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Key Bindings ---
        self.master.bind("<Return>", self.prev_picture)
        self.master.bind("<space>", self.next_picture)
        for key in self.bindings.keys():
            self.master.bind(key, self.press_event)

        # --- Styling ---
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' is a good-looking theme
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 14))
        self.style.configure("Green.TLabel", foreground="green", font=("Helvetica", 14, "bold"))
        self.style.configure("Red.TLabel", foreground="red", font=("Helvetica", 14))
        self.style.configure("Key.TLabel", font=("Courier", 14, "bold"))

        # --- Main Layout ---
        self.content_frame = ttk.Frame(self.master, padding=(10, 10, 10, 10))
        self.content_frame.pack(fill="both", expand=True)

        # --- Image Panel ---
        self.img_panel = ttk.Label(self.content_frame, anchor="center")
        self.img_panel.pack(side="top", fill="both", expand=True, pady=(0, 10))

        # --- Separator ---
        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(side="top", fill='x', pady=5)

        # --- Annotation Panel ---
        self.annotation_frame = ttk.Frame(self.content_frame)
        self.annotation_frame.pack(side="bottom", fill="x", expand=False)
        self.annotation_labels = {}
        self._create_annotation_labels()

        # --- Initial UI Update ---
        self.update_ui()

    def _create_annotation_labels(self):
        self.annotation_frame.columnconfigure(1, weight=1)
        row = 0
        for key, class_name in self.bindings.items():
            key_label = ttk.Label(self.annotation_frame, text=f"[{key}]", style="Key.TLabel")
            key_label.grid(row=row, column=0, sticky='w', padx=(5, 10))

            label = ttk.Label(self.annotation_frame, text=class_name, anchor="w")
            label.grid(row=row, column=1, sticky='we', padx=5, pady=2)
            self.annotation_labels[class_name] = label
            row += 1

    def update_ui(self):
        self.master.title(f"Picture {self.curr_i}")
        self.update_image()
        self.update_labels()

    def update_image(self):
        image_path = self.data_manager.get_image_path(self.curr_i, self.image_manager.image_dir)
        try:
            photo_img = self.image_manager.get_image(image_path)
            self.img_panel.configure(image=photo_img)
            self.img_panel.image = photo_img
        except Exception as e:
            logging.error(f"Failed to load image: {image_path}. Error: {e}")
            # Optionally display a placeholder or error message in the UI
            self.img_panel.configure(text=f"Error loading image:\n{image_path}", image=None)
            self.img_panel.image = None

    def update_labels(self):
        annotations = self.data_manager.get_annotations(self.curr_i)
        for class_name, value in annotations.items():
            if class_name in self.annotation_labels:
                label = self.annotation_labels[class_name]
                text = f"{class_name}"
                if value == 1:
                    label.config(style="Green.TLabel", text=f"{text} (ON)")
                else:
                    label.config(style="Red.TLabel", text=f"{text} (OFF)")

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
